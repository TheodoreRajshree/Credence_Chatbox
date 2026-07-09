from bson import ObjectId
from datetime import datetime, timedelta, timezone
from rbac import get_rbac_filter
import re
from branch_engine import BranchEngine
from device_engine import DeviceEngine
from vehicle_km_engine import VehicleKmEngine
from report_status_engine import ReportStatusEngine
from datetime import datetime, timedelta
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import requests
import time

# from datetime import datetime, timedelta
class BranchDeviceEngine:

    def __init__(self, db):
    
        self.db = db
        self.branch_engine = BranchEngine(db)
        self.device_engine = DeviceEngine(db)
        self.vehicle_km_engine = VehicleKmEngine(db)
        self.report_status_engine =ReportStatusEngine(db)
      
   


   


    def get_address(self, latitude, longitude):

        print("ADDRESS REQUEST:", latitude, longitude)

        try:

            time.sleep(1)   # avoid Nominatim 429


            location = self.geolocator.reverse(
            f"{latitude},{longitude}",
            language="en"
        )


            print("LOCATION RESPONSE:", location)


            if location:

                return location.address


        except Exception as e:

            print("Reverse Geocoding Error:", e)


        return "Address Not Available"
    # =====================================================
    # OBJECT ID HELPER
    # =====================================================

    def convert_id(self, value):

        try:
            return ObjectId(value)

        except:
            return value
    def normalize_unique_id(self, uid):

        ids = []

        if uid is None:
            return ids

        ids.append(uid)
        ids.append(str(uid))

        try:
            ids.append(int(float(uid)))
        except:
            pass

        try:
            ids.append(float(uid))
        except:
            pass

        return list(set(ids))
    
    def get_allowed_devices(
        self,
        unique_id,
        role,
        user
    ):

        device_filter = get_rbac_filter(
            role,
            user,
            "devices",
            self.db
        )


        return self.db["devices"].find_one({

            "$and":[

                device_filter,

                {
                    "uniqueId":{
                        "$in":[
                            unique_id,
                            str(unique_id)
                        ]
                    }
                }

            ]

        })
# =====================================
# SPECIFIC VEHICLE IDLE REPORT
# =====================================


    def _parse_float(self, value, default=0.0):
        """
        daily_vehicle_distance_cache.totalKm is stored as a STRING
        (e.g. "2019.374"). Summing strings directly either throws
        or silently concatenates — always parse first.
        """
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def _sum_positive_diffs(self, records):
        """
        report_distances.distance is a CUMULATIVE ("current") odometer
        reading, confirmed. To get km travelled in a window we sum only
        the positive steps between consecutive time-sorted readings.

        Why not max-min? If the device resets its counter mid-window
        (reboot / re-registration), the counter can drop then climb
        back up. Diffing consecutive readings and ignoring negative
        steps (resets) is the only version of this that stays correct
        across a reset, and it's immune to a single stray outlier
        skewing the whole window the way max-min is.
        """
        if len(records) < 2:
            return 0.0

        distances = [self._parse_float(r.get("distance", 0)) for r in records]

        total = 0.0
        for i in range(1, len(distances)):
            diff = distances[i] - distances[i - 1]
            if diff > 0:
                total += diff
            # diff <= 0 -> reset or no movement, skip (don't subtract)

        return round(total, 2)

    def _sum_cache_km(self, records):
        """
        daily_vehicle_distance_cache holds one precomputed totalKm
        string per vehicle per completed day. Summing these (after
        parsing to float) gives km for any range of completed days
        without re-deriving anything from raw odometer events.
        """
        return round(sum(self._parse_float(r.get("totalKm", 0)) for r in records), 2)
   
    # =====================================
# SPECIFIC VEHICLE IDLE REPORT
# =====================================

    def get_specific_vehicle_idle_report(
    self,
    branch_name,
    vehicle_input,
    role,
    user,
    limit=100
):

    # Normalize input
        vehicle_input = str(vehicle_input).strip().lower().replace(" ", "")

    # Get devices allowed by RBAC
        device_filter = get_rbac_filter(
        role,
        user,
        "devices",
        self.db
    )

        devices = list(
        self.db["devices"].find(device_filter)
    )

        selected_device = None

    # Search vehicle
        for device in devices:

            vehicle_name = str(device.get("vehicleName", "")).lower().replace(" ", "")
            vehicle_number = str(device.get("vehicleNumber", "")).lower().replace(" ", "")
            name = str(device.get("name", "")).lower().replace(" ", "")
            unique_id = str(device.get("uniqueId", "")).lower().replace(" ", "")

            print("--------------------------------")
            print("Searching :", vehicle_input)
            print("Vehicle Name :", vehicle_name)
            print("Vehicle Number :", vehicle_number)
            print("Name :", name)
            print("Unique ID :", unique_id)

            if (
            vehicle_input == vehicle_name
            or vehicle_input == vehicle_number
            or vehicle_input == name
            or vehicle_input == unique_id
        ):
                selected_device = device
                break

    # IMPORTANT: Check AFTER loop
        if selected_device is None:
            return {
            "success": False,
            "message": "Vehicle not found."
        }

    # Get idle reports
        idle_filter = get_rbac_filter(
        role,
        user,
        "report_idles",
        self.db
    )

        reports = list(
        self.db["report_idles"].find({

            "$and": [

                idle_filter,

                {
                    "uniqueId": {
                        "$in": self.normalize_unique_id(
                            selected_device["uniqueId"]
                        )
                    }
                }

            ]

        })
        .sort("idleStartTime", -1)
        .limit(limit)
    )

        return {

        "success": True,

        "branch": {
            "branchId": str(user.get("branchId")),
            "branchName": branch_name
        },

        "vehicle": {
            "vehicleName": selected_device.get("vehicleName"),
            "vehicleNumber": selected_device.get("vehicleNumber"),
            "name": selected_device.get("name"),
            "uniqueId": selected_device.get("uniqueId")
        },

        "idleReports": [
            self.clean(report)
            for report in reports
        ]

    }
# ====================================
# SPECIFIC BRANCH VEHICLE LAST POSITION
# ====================================

    def get_specific_vehicle_last_position(
    self,
    branch_name,
    vehicle_input,
    role,
    user
):
        vehicle_input = str(vehicle_input).strip().lower().replace(" ", "")

    # RBAC filter for devices
        device_filter = get_rbac_filter(
        role,
        user,
        "devices",
        self.db
    )

        devices = list(
        self.db["devices"].find(device_filter)
    )

        selected_device = None

        for device in devices:

            vehicle_name = str(device.get("vehicleName", "")).lower().replace(" ", "")
            vehicle_number = str(device.get("vehicleNumber", "")).lower().replace(" ", "")
            name = str(device.get("name", "")).lower().replace(" ", "")
            unique_id = str(device.get("uniqueId", "")).lower().replace(" ", "")

            if (
            vehicle_input == vehicle_name
            or vehicle_input == vehicle_number
            or vehicle_input == name
            or vehicle_input == unique_id
        ):
                selected_device = device
                break

    # AFTER loop
        if selected_device is None:
            return {
            "success": False,
            "message": "Vehicle not found."
        }




    # Find last position
        position = self.db["vehiclelastpositions"].find_one({

        "$and": [

            get_rbac_filter(
                role,
                user,
                "vehiclelastpositions",
                self.db
            ),

            {
                "uniqueId": str(selected_device["uniqueId"])
            }

        ]

    })

        if not position:
            return {
            "success": False,
            "message": "No last position found."
        }
       

        address = position.get("address")

        print("OLD ADDRESS:", address)


        if address is None or address == "":


            latitude = position.get("latitude")
            longitude = position.get("longitude")


            print("LAT:", latitude)
            print("LONG:", longitude)


            if latitude is not None and longitude is not None:


                address = self.get_address(
            latitude,
            longitude
        )


                print("NEW ADDRESS:", address)


        
            
        return {
        "success": True,

        "branch": {
            "branchId": str(user.get("branchId")),
            "branchName": branch_name
        },
        "vehicle": {
            "vehicleName": selected_device.get("vehicleName"),
            "vehicleNumber": selected_device.get("vehicleNumber"),
            "name": selected_device.get("name"),
            "uniqueId": selected_device.get("uniqueId")
        },

        "lastPosition": {

            "latitude": position.get("latitude"),
            "longitude": position.get("longitude"),
            "speed": position.get("speed"),
            "course": position.get("course"),
            "accuracy": position.get("accuracy"),
            "altitude": position.get("altitude"),
            "address": address,
            "protocol": position.get("protocol"),
            "deviceTime": position.get("deviceTime"),
            "fixTime": position.get("fixTime"),
            "serverTime": position.get("serverTime"),
            "lastUpdate": position.get("lastUpdate"),
            "valid": position.get("valid"),
            "outdated": position.get("outdated")

        }

    }
# =====================================
# SPECIFIC BRANCH GEOFENCE
# =====================================

    def get_specific_branch_geofence(
    self,
    branch_name,
    vehicle_input,
    role,
    user
):

    # ==========================
    # Find Branch
    # ==========================
        branch = self.find_branch(
        branch_name,
        role,
        user
    )

        if not branch:
            return {
            "success": False,
            "message": "Branch not found."
        }

        branch_id = branch["_id"]

    # ==========================
    # RBAC Device Filter
    # ==========================
        device_filter = get_rbac_filter(
        role,
        user,
        "devices",
        self.db
    )

        vehicle_input = str(vehicle_input).strip().lower()

        device = self.db["devices"].find_one({

        "$and":[

            device_filter,

            {
                "$or":[
                    {"branchId": branch_id},
                    {"branchId": str(branch_id)}
                ]
            },

            {
                "$or":[

                    {
                        "vehicleNumber":{
                            "$regex": f"^{vehicle_input}$",
                            "$options":"i"
                        }
                    },

                    {
                        "vehicle_name":{
                            "$regex": f"^{vehicle_input}$",
                            "$options":"i"
                        }
                    },

                    {
                        "name":{
                            "$regex": f"^{vehicle_input}$",
                            "$options":"i"
                        }
                    },

                    {
                        "uniqueId":{
                            "$in":[
                                vehicle_input,
                                str(vehicle_input)
                            ]
                        }
                    }

                ]
            }

        ]

    })

        if not device:
            return {
            "success": False,
            "message": "Vehicle not found."
        }

    # ==========================
    # Find Vehicle Geofence
    # ==========================
        geofence_id = device.get("geofenceId")

        if not geofence_id:
            return {
            "success": False,
            "message": "No geofence assigned to this vehicle."
        }

        geofence_filter = get_rbac_filter(
        role,
        user,
        "geofences",
        self.db
    )

        geofence = self.db["geofences"].find_one({

        "$and":[

            geofence_filter,

            {
                "$or":[
                    {"_id": geofence_id},
                    {"_id": ObjectId(str(geofence_id))} if ObjectId.is_valid(str(geofence_id)) else {"_id": geofence_id}
                ]
            }

        ]

    })

        if not geofence:
            return {
            "success": False,
            "message": "Geofence not found."
        }

        return {

        "success": True,

        "branch":{

            "branchId": str(branch["_id"]),
            "branchName": branch.get("branchName")

        },

        "vehicle":{

            "vehicleName": (
                device.get("vehicleNumber")
                or device.get("vehicle_name")
                or device.get("name")
            ),

            "uniqueId": device.get("uniqueId")

        },

        "geofence":{

            "geofenceId": str(geofence["_id"]),

            "name": geofence.get("geofenceName"),

            "address": geofence.get("address"),

            "latitude": geofence.get("latitude"),

            "longitude": geofence.get("longitude")

        }

    }
    # =====================================
# SPECIFIC BRANCH VEHICLE DAILY DISTANCE
# =====================================

    # =====================================
# SPECIFIC BRANCH VEHICLE DAILY DISTANCE
# =====================================

    def get_specific_vehicle_daily_distance(
    self,
    branch_name,
    vehicle_input,
    role,
    user,
    limit=100
):

        vehicle_input = str(vehicle_input).strip().lower()

    # RBAC allowed devices
        device_filter = get_rbac_filter(
        role,
        user,
        "devices",
        self.db
    )

        devices = list(
        self.db["devices"].find(device_filter)
    )

        selected_device = None

        for device in devices:

            vehicle_name = str(device.get("vehicleName", "")).lower()
            vehicle_number = str(device.get("vehicleNumber", "")).lower()
            name = str(device.get("name", "")).lower()
            unique_id = str(device.get("uniqueId", "")).lower()

            if (
            vehicle_input == vehicle_name
            or vehicle_input == vehicle_number
            or vehicle_input == name
            or vehicle_input == unique_id
        ):
                selected_device = device
                break

        if not selected_device:
            return {
            "success": False,
            "message": "Vehicle not found."
        }

        reports = list(

        self.db["daily_vehicle_distance_caches"].find({

            "uniqueId": {
                "$in": self.normalize_unique_id(
                    selected_device["uniqueId"]
                )
            }

        })

        .sort("createdAt", -1)
        .limit(limit)

    )

        return {

        "success": True,

        "vehicle": {

            "vehicleName": selected_device.get("vehicleName"),
            "vehicleNumber": selected_device.get("vehicleNumber"),
            "name": selected_device.get("name"),
            "uniqueId": selected_device.get("uniqueId")

        },

        "dailyDistance": [

            self.clean(report)

            for report in reports

        ]

    }
    # =====================================
# SPECIFIC VEHICLE TRAVEL SUMMARY
# =====================================

    def get_specific_vehicle_travel_summary(
    self,
    branch_name,
    vehicle_input,
    role,
    user,
    limit=100
):

        vehicle_input = str(vehicle_input).strip().lower()

        device_filter = get_rbac_filter(
        role,
        user,
        "devices",
        self.db
    )

        devices = list(
            self.db["devices"].find(device_filter)
    )

        selected_device = None

        for device in devices:

            vehicle_name = str(device.get("vehicleName", "")).lower()
            vehicle_number = str(device.get("vehicleNumber", "")).lower()
            name = str(device.get("name", "")).lower()
            unique_id = str(device.get("uniqueId", "")).lower()

            if (
                vehicle_input == vehicle_name
                or vehicle_input == vehicle_number
                or vehicle_input == name
                or vehicle_input == unique_id
        ):
                selected_device = device
                break

        if not selected_device:
            return {
            "success": False,
            "message": "Vehicle not found."
        }

        summary_filter = get_rbac_filter(
        role,
        user,
        "report_travelsummaries",
        self.db
    )

        reports = list(

            self.db["report_travelsummaries"].find({

            "$and": [

                summary_filter,

                {
                    "uniqueId": {
                        "$in": self.normalize_unique_id(
                            selected_device["uniqueId"]
                        )
                    }
                }

            ]

        })
        .sort("startTime", -1)
        .limit(limit)

    )

        return {

        "success": True,

        "vehicle": {

            "vehicleName": selected_device.get("vehicleName"),
            "vehicleNumber": selected_device.get("vehicleNumber"),
            "name": selected_device.get("name"),
            "uniqueId": selected_device.get("uniqueId")

        },

        "travelSummary": [

            self.clean(r)

            for r in reports

        ]

    }
    # =====================================================
    # FIND BRANCH
    # =====================================================
    def get_branch_single_vehicle(
    self,
    branch_name,
    vehicle_input,
    role,
    user
):

    # -----------------------
    # Find Branch
    # -----------------------
        branch = self.find_branch(
        branch_name,
        role,
        user
    )

        if not branch:
            return {
            "success": False,
            "message": f"Branch '{branch_name}' not found"
        }

        branch_id = branch["_id"]

        vehicle_input = str(vehicle_input).strip()

        device_filter = get_rbac_filter(
        role,
        user,
        "devices",
        self.db
    )

    # -----------------------
    # Find Vehicle DIRECTLY
    # -----------------------
        device = self.db["devices"].find_one({

        "$and": [

            device_filter,

            {
                "$or": [
                    {"branchId": branch_id},
                    {"branchId": str(branch_id)}
                ]
            },

            {
                "$or": [

                    {
                        "vehicleNumber": {
                            "$regex": f"^{re.escape(vehicle_input)}$",
                            "$options": "i"
                        }
                    },

                    {
                        "vehicle_name": {
                            "$regex": f"^{re.escape(vehicle_input)}$",
                            "$options": "i"
                        }
                    },

                    {
                        "name": {
                            "$regex": f"^{re.escape(vehicle_input)}$",
                            "$options": "i"
                        }
                    },

                    {
                        "uniqueId": {
                            "$in": [
                                vehicle_input,
                                str(vehicle_input)
                            ]
                        }
                    }

                ]
            }

        ]

    })

        if not device:
            return {
            "success": False,
            "message": "Vehicle not found in this branch."
        }

        return {

        "success": True,

        "branch": {

            "branchId": str(branch["_id"]),
            "branchName": branch.get("branchName")

        },

        "vehicle": {

            "vehicleName": (
                device.get("vehicleNumber")
                or device.get("vehicle_name")
                or device.get("name")
                or device.get("uniqueId")
            ),

            "deviceId": str(device.get("_id")),

            "uniqueId": device.get("uniqueId"),

            "status": device.get("status"),

            "model": device.get("model"),

            "category": device.get("category"),

            "speed": device.get("speed"),

            "totalKm": device.get("TotalKmOfDevice", 0)

        }

    }
    
    def find_branch(self, branch_name, role, user):

        rbac_filter = get_rbac_filter(
        role,
        user,
        "branches",
        self.db
    )
        
    # ✅ FORCE STRING
        # branch_name = str(branch_name) if branch_name is not None else ""
        branch_name = str(branch_name).strip() if branch_name is not None else ""
    # 1st try: ObjectId match
        branch = None
        try:
            branch = self.db["branches"].find_one({
            "$and": [
                rbac_filter,
                {
                    "_id": ObjectId(branch_name)
                }
            ]
        })
        except:
            pass

    # 2nd try: regex fallback
        if not branch:

            branch = self.db["branches"].find_one({
            "$and": [
                rbac_filter,
                {
                    "$or": [
                        {
                            "branchName": {
                                "$regex": branch_name,
                                "$options": "i"
                            }
                        },
                        {
                            "username": {
                                "$regex": branch_name,
                                "$options": "i"
                            }
                        }
                    ]
                }
            ]
        })

        return branch
    
    def get_single_branch_vehicle_status(
    self,
    branch_name,
    vehicle_input,
    role,
    user,
    limit=100
):

        branch = self.find_branch(
        branch_name,
        role,
        user
    )

        if not branch:
            return {
            "success": False,
            "message": "Branch not found."
        }

        result = self.get_branch_single_vehicle(
        branch_name,
        vehicle_input,
        role,
        user
    )

        if not result["success"]:
            return result

        status = self.report_status_engine.get_single_branch_vehicle_status_report(

        branch["_id"],
        result["vehicle"]["uniqueId"],
        role,
        user,
        limit

    )

        return {

        "success": True,

        "branch": result["branch"],

        "vehicle": result["vehicle"],

        "statusReport": status

    }
    # =====================================
# SPECIFIC VEHICLE DISTANCE REPORT
# =====================================

  
    def get_specific_vehicle_distance_report(
    self,
    branch_name,
    vehicle_input,
    role,
    user,
    limit=100
):

    # Reuse existing vehicle search
        result = self.get_branch_single_vehicle(
        branch_name,
        vehicle_input,
        role,
        user
    )

        if not result["success"]:
            return result

        vehicle = result["vehicle"]

        reports = list(
        self.db["report_distances"].find({

            "$and": [

                get_rbac_filter(
                    role,
                    user,
                    "report_distances",
                    self.db
                ),

                {
                    "uniqueId": {
                        "$in": self.normalize_unique_id(
                            vehicle["uniqueId"]
                        )
                    }
                }

            ]

        })
        .sort("createdAt", -1)
        .limit(limit)
    )

        return {

        "success": True,

        "branch": result["branch"],

        "vehicle": vehicle,

        "reports": [

            self.clean(r)

            for r in reports

        ]

    }
    # =====================================================
    # GET BRANCH + VEHICLES
    # =====================================================

    def get_branch_with_vehicles(
        self,
        branch_name,
        role,
        user
    ):


        branch = self.find_branch(
            branch_name,
            role,
            user
        )


        if not branch:

            return {

                "success":False,

                "message":
                f"Branch '{branch_name}' not found"

            }


        branch_id = branch["_id"]


        device_filter = get_rbac_filter(
            role,
            user,
            "devices",
            self.db
        )


        devices = list(

            self.db["devices"].find({

                "$and":[

                    device_filter,

                    {

                        "$or":[

                            {
                                "branchId":branch_id
                            },

                            {
                                "branchId":
                                str(branch_id)
                            }

                        ]

                    }

                ]

            })

        )



        vehicle_list=[]


        for device in devices:


            vehicle_name = (

                device.get("vehicleNumber")

                or device.get("vehicle_name")

                or device.get("name")

                or device.get("uniqueId")

                or ""

            )


            vehicle_list.append({

                "vehicleName":
                vehicle_name,


                "deviceId":
                str(device.get("_id")),


                "uniqueId":
                device.get("uniqueId"),


                "status":
                device.get("status"),


                "model":
                device.get("model"),


                "category":
                device.get("category"),


                "speed":
                device.get("speed"),


                "totalKm":
                device.get(
                    "TotalKmOfDevice",
                    0
                )

            })



        return {


            "success":True,


            "branch":{

                "branchId":
                str(branch["_id"]),


                "branchName":
                branch.get(
                    "branchName"
                ),


                "username":
                branch.get(
                    "username"
                ),


                "mobileNo":
                branch.get(
                    "mobileNo"
                )

            },


            "totalVehicles":
            len(vehicle_list),


            "vehicles":
            vehicle_list

        }



    # =====================================================
    # BRANCH DASHBOARD
    # =====================================================

    def get_branch_dashboard(
        self,
        branch_name,
        role,
        user
    ):


        branch = self.find_branch(
            branch_name,
            role,
            user
        )


        if not branch:
            return None


        branch_id = branch["_id"]



        return {


            "branchName":
            branch.get(
                "branchName"
            ),


            "vehicleCount":
            self.branch_engine
            .get_branch_vehicle_count(
                branch_id,
                role,
                user
            ),


            "driverCount":
            self.branch_engine
            .get_branch_driver_count(
                branch_id,
                role,
                user
            )


        }



    # =====================================================
    # GET BRANCH DEVICES
    # =====================================================

    def get_branch_devices(
        self,
        branch_id,
        role,
        user
    ):


        branch_id_obj = self.convert_id(
            branch_id
        )


        device_filter = get_rbac_filter(
            role,
            user,
            "devices",
            self.db
        )



        devices=list(

            self.db["devices"].find({

                "$and":[

                    device_filter,

                    {

                        "$or":[

                            {
                                "branchId":
                                branch_id_obj
                            },

                            {
                                "branchId":
                                str(branch_id_obj)
                            }

                        ]

                    }

                ]

            })

        )



        return {


            "branchId":
            str(branch_id),


            "totalDevices":
            len(devices),


            "devices":[

                self.clean(d)

                for d in devices

            ]

        }



    # =====================================================
    # CLEAN
    # =====================================================

    def clean(self,doc):

        if not doc:
            return doc


        cleaned={}


        for key,value in doc.items():

            if isinstance(value,ObjectId):

                cleaned[key]=str(value)

            else:

                cleaned[key]=value


        return cleaned
    def get_branch_status_report(
    self,
    branch_id,
    role,
    user,
    limit=100
):

        return self.report_status_engine.get_branch_status_report(
        branch_id,
        role,
        user,
        limit
    )
    # =====================================================
# BRANCH VEHICLE KM REPORT
# =====================================================

    def get_branch_vehicle_km_report(
    self,
    role,
    user,
    limit=20
):

    # ==========================================
    # BRANCH ID
    # ==========================================

        branch_id = user.get("branchId")

        if not branch_id:
            return {
            "success": False,
            "message": "Branch not found."
        }

    # ==========================================
    # RBAC FILTER
    # ==========================================

        device_filter = get_rbac_filter(
        role,
        user,
        "devices",
        self.db
    )

    # ==========================================
    # BRANCH FILTER
    # ==========================================

        branch_filters = [
        {
            "branchId": branch_id
        }
    ]

        if ObjectId.is_valid(str(branch_id)):
            branch_filters.append({
            "branchId": ObjectId(str(branch_id))
        })

    # ==========================================
    # GET DEVICES
    # ==========================================

        cursor = self.db["devices"].find({

        "$and": [

            device_filter,

            {
                "$or": branch_filters
            }

        ]

    })

        if limit > 0:
            cursor = cursor.limit(limit)

        devices = list(cursor)

        if not devices:
            return {
            "success": False,
            "message": "No vehicles found for this branch."
        }

    # ==========================================
    # REPORTS
    # ==========================================

        reports = []

        for device in devices:

            unique_id = device.get("uniqueId")

            if not unique_id:
                continue

            km_report = self.get_km_report(
            unique_id,
            "",
            role,
            user
        )

            if not km_report:
                continue

            reports.append({

            "deviceId": str(device.get("_id")),

            "vehicleName": (
                device.get("vehicleNumber")
                or device.get("vehicle_name")
                or device.get("name")
                or str(unique_id)
            ),

            "uniqueId": unique_id,

            "todayKm": km_report.get(
                "today_km",
                0
            ),

            "yesterdayKm": km_report.get(
                "yesterday_km",
                0
            ),

            "oneWeekKm": km_report.get(
                "one_week_km",
                0
            ),

            "oneMonthKm": km_report.get(
                "one_month_km",
                0
            ),

            "totalKm": km_report.get(
                "total_km_report",
                {}
            ).get(
                "totalKm",
                0
            ),

            "lastPosition": km_report.get(
                "last_position",
                {}
            )

        })

        return {

        "success": True,

        "branchId": str(branch_id),

        "totalVehicles": len(reports),

        "vehicles": reports

    }
    
    def get_km_report(self, unique_id, message, role, user):

        device = self.get_allowed_device(unique_id, role, user)

        if not device:
            return None

        uid_filter = self.build_uid_filter(device)

        distance_access = get_rbac_filter(role, user, "report_distances", self.db)
        cache_access = get_rbac_filter(role, user, "daily_vehicle_distance_caches", self.db)

        result = {}
        now = datetime.now(timezone.utc)

        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - timedelta(days=1)
        week_start = today_start - timedelta(days=7)
        month_start = today_start - timedelta(days=30)

        # ==================================================
        # TODAY: no cache entry exists yet for an in-progress day,
        # so this is computed LIVE from raw report_distances readings.
        # ==================================================
        today_records = list(self.db["report_distances"].find({
            "$and": [
                distance_access,
                uid_filter,
                {"createdAt": {"$gte": today_start, "$lte": now}}
            ]
        }).sort("createdAt", 1))

        today_km = self._sum_positive_diffs(today_records)
        result["today_km"] = today_km

        # ==================================================
        # YESTERDAY: fully completed day -> cache only.
        # ==================================================
        yesterday_cache = list(self.db["daily_vehicle_distance_caches"].find({
            "$and": [
                cache_access,
                uid_filter,
                {"createdAt": {"$gte": yesterday_start, "$lt": today_start}}
            ]
        }))

        result["yesterday_km"] = self._sum_cache_km(yesterday_cache)

        # ==================================================
        # ONE WEEK / ONE MONTH: cache covers the completed days in
        # the window, today's partial day is added live so the
        # window is "up to right now", not "up to yesterday".
        # ==================================================
        week_cache = list(self.db["daily_vehicle_distance_caches"].find({
            "$and": [
                cache_access,
                uid_filter,
                {"createdAt": {"$gte": week_start, "$lt": today_start}}
            ]
        }))

        result["one_week_km"] = round(self._sum_cache_km(week_cache) + today_km, 2)

        month_cache = list(self.db["daily_vehicle_distance_caches"].find({
            "$and": [
                cache_access,
                uid_filter,
                {"createdAt": {"$gte": month_start, "$lt": today_start}}
            ]
        }))

        result["one_month_km"] = round(self._sum_cache_km(month_cache) + today_km, 2)

        # ==================================================
        # TOTAL: every completed day in the cache, plus today live.
        # ==================================================
        all_cache = list(self.db["daily_vehicle_distance_caches"].find({
            "$and": [cache_access, uid_filter]
        }))

        result["total_km_report"] = {
            "vehicle": str(unique_id),
            "totalKm": round(self._sum_cache_km(all_cache) + today_km, 2)
        }

        # ==================================================
        # LAST POSITION
        # ==================================================
        position_filter = get_rbac_filter(role, user, "vehiclelastpositions", self.db)

        last = self.db["vehiclelastpositions"].find_one({
            "$and": [
                position_filter,
                {"uniqueId": {"$in": self.normalize_unique_id(unique_id)}}
            ]
        })

        if last:
            result["last_position"] = {
                "lat": last.get("latitude"),
                "lng": last.get("longitude"),
                "speed": last.get("speed")
            }

        return result

    def get_allowed_device(self, unique_id, role, user):

        device_filter = get_rbac_filter(role, user, "devices", self.db)

        return self.db["devices"].find_one({
            "$and": [
                device_filter,
                {"uniqueId": {"$in": self.normalize_unique_id(unique_id)}}
            ]
        })
    
    def build_uid_filter(self, device):
        return {
            "uniqueId": {
                "$in": self.normalize_unique_id(device.get("uniqueId"))
            }
        }
    def get_branch_single_vehicle_km_report(
    self,
    branch_name,
    vehicle_input,
    role,
    user
):

    # =====================================
    # 1. Get Vehicle
    # =====================================
        result = self.get_branch_single_vehicle(
        branch_name,
        vehicle_input,
        role,
        user
    )

        if not result["success"]:
            return result

        vehicle = result["vehicle"]
        unique_ids = self.normalize_unique_id(vehicle["uniqueId"])

    # =====================================
    # 2. Fetch report_distances
    # =====================================
        report_distances = list(
        self.db["report_distances"]
        .find({
            "$and": [
                get_rbac_filter(role, user, "report_distances", self.db),
                {"uniqueId": {"$in": unique_ids}}
            ]
        })
        .sort("createdAt", -1)
    )

        if not report_distances:
            return {
            "success": False,
            "message": "No distance reports found as the devices."
        }

    # =====================================
    # 3. Build map
    # =====================================
        report_map = {
            r["createdAt"].date(): float(r.get("distance", 0))
            for r in report_distances
    }

        today = datetime.utcnow().date()
        available_dates = sorted(report_map.keys())

    # =====================================
    # 4. Active / Inactive
    # =====================================
        if today in report_map:
            status = "active"
            analysis_base_date = today
            message = "Vehicle is active today."
        else:
            status = "inactive"
            analysis_base_date = available_dates[-1]
            message = f"Vehicle is not active today. Last active was on {analysis_base_date}"

        current_km = round(report_map.get(analysis_base_date, 0), 2)

    # previous active day (correct)
        previous_active_date = None
        for d in reversed(available_dates):
            if d < analysis_base_date:
                previous_active_date = d
                break

        yesterday_km = round(report_map.get(previous_active_date, 0), 2) if previous_active_date else 0

    # =====================================
    # 5. WEEK CALCULATION (CORRECT)
    # =====================================
        week_start = analysis_base_date - timedelta(days=analysis_base_date.weekday())
        week_end = week_start + timedelta(days=6)

        week_total = 0
        for r in report_distances:
            d = r["createdAt"].date()
            if week_start <= d <= week_end:
                week_total += float(r.get("distance", 0))

        week_total = round(week_total, 2)

    # =====================================
    # 6. MONTH CALCULATION (FIXED BUG)
    # =====================================
        month_start = analysis_base_date - timedelta(days=29)
        month_end = analysis_base_date

        month_total = 0
        for r in report_distances:
            d = r["createdAt"].date()
            if month_start <= d <= month_end:
                month_total += float(r.get("distance", 0))

        month_total = round(month_total, 2)

    # =====================================
    # 7. RESPONSE
    # =====================================
        return {
        "success": True,
        "status": status,
        "message": message,

        "branch": result["branch"],

        "vehicle": {
            "vehicleName": vehicle.get("vehicleName"),
            "deviceId": vehicle.get("deviceId"),
            "uniqueId": vehicle.get("uniqueId"),
            "status": vehicle.get("status"),
            "category": vehicle.get("category"),
            "model": vehicle.get("model")
        },

        "reference": {
            "date": analysis_base_date.strftime("%Y-%m-%d"),
            "isTodayActive": status == "active",
            "lastActiveDate": analysis_base_date.strftime("%Y-%m-%d")
        },

        "distanceReport": {

            "current": {
                "label": "Today" if status == "active" else "Last Active",
                "km": current_km
            },

            "yesterday": {
                "date": previous_active_date.strftime("%Y-%m-%d") if previous_active_date else None,
                "km": yesterday_km
            },

            "week": {
                "from": week_start.strftime("%Y-%m-%d"),
                "to": week_end.strftime("%Y-%m-%d"),
                "totalKm": week_total
            },

            "month": {
                "type": "rolling_30_days",
                "from": month_start.strftime("%Y-%m-%d"),
                "to": month_end.strftime("%Y-%m-%d"),
                "totalKm": month_total
            }
        }
    }
    def get_route_branch(self, role, user):

        branch_filter = get_rbac_filter(
        role,
        user,
        "routes",
        self.db
    )

        branch_id = user.get("branchId")

        routes = list(
        self.db["routes"].find({
            "$and": [
                branch_filter,
                {
                    "$or": [
                        {
                            "branchId": branch_id
                        },
                        {
                            "branchId": ObjectId(branch_id)
                        } if ObjectId.is_valid(branch_id) else {
                            "branchId": branch_id
                        }
                    ]
                }
            ]
        })
    )

        if not routes:
            return {
            "success": False,
            "message": "No routes found."
        }

        data = []

        for route in routes:

            data.append({

            "routeId": str(route["_id"]),

            "routeNumber": route.get("routeNumber"),

            "deviceObjId": str(route.get("deviceObjId")) if route.get("deviceObjId") else "",

            "schoolId": str(route.get("schoolId")) if route.get("schoolId") else "",

            "branchId": str(route.get("branchId")) if route.get("branchId") else "",

            "routeCompletionTime": route.get("routeCompletionTime"),

            "createdAt": route.get("createdAt")

        })

        return {

        "success": True,

        "totalRoutes": len(data),

        "routes": data

    }
    

   



    
    def get_route_branch_specific_vehicle(
    self,
    branch_name,
    vehicle_input,
    role,
    user
):

    # ===============================
    # Find Branch
    # ===============================

        branch = self.find_branch(
        branch_name,
        role,
        user
    )

        if not branch:
            return {
            "success": False,
            "message": f"Branch '{branch_name}' not found."
        }

        branch_id = branch["_id"]

    # ===============================
    # RBAC Filters
    # ===============================

        device_filter = get_rbac_filter(
        role,
        user,
        "devices",
        self.db
    )

        route_filter = get_rbac_filter(
        role,
        user,
        "routes",
        self.db
    )

    # ===============================
    # Find Vehicle
    # ===============================

        device = self.db["devices"].find_one({

        "$and":[

            device_filter,

            {
                "$or":[
                    {
                        "branchId": branch_id
                    },
                    {
                        "branchId": str(branch_id)
                    }
                ]
            },

            {
                "$or":[

                    {
                        "vehicleNumber":{
                            "$regex": vehicle_input,
                            "$options":"i"
                        }
                    },

                    {
                        "vehicle_name":{
                            "$regex": vehicle_input,
                            "$options":"i"
                        }
                    },

                    {
                        "name":{
                            "$regex": vehicle_input,
                            "$options":"i"
                        }
                    },

                    {
                        "uniqueId":{
                            "$in":[
                                vehicle_input,
                                str(vehicle_input)
                            ]
                        }
                    }

                ]
            }

        ]

    })

        if not device:
            return {
            "success": False,
            "message": "Vehicle not found."
        }

        device_id = device["_id"]

    # ===============================
    # Find Route
    # ===============================

        route = self.db["routes"].find_one({

        "$and":[

            route_filter,

            {
                "$or":[
                    {
                        "branchId": branch_id
                    },
                    {
                        "branchId": str(branch_id)
                    }
                ]
            },

            {
                "$or":[
                    {
                        "deviceObjId": device_id
                    },
                    {
                        "deviceObjId": str(device_id)
                    }
                ]
            }

        ]

    })

        if not route:
            return {
            "success": False,
            "message": "No route assigned to this vehicle."
        }

        return {

        "success": True,

        "route": {

            "routeId": str(route["_id"]),

            "routeNumber": route.get("routeNumber"),

            "routeCompletionTime": route.get("routeCompletionTime"),

            "vehicle": {

                "deviceId": str(device["_id"]),

                # "vehicleName": (
                #     device.get("vehicleNumber")
                #     or device.get("vehicle_name")
                #     or device.get("name")
                #     or device.get("uniqueId")
                # ),
                "deviceName": (
            device.get("vehicleNumber")
            or device.get("vehicle_name")
            or device.get("name")
            or "N/A"
        ),

                "uniqueId": device.get("uniqueId"),

                "status": device.get("status"),

                "model": device.get("model"),

                "category": device.get("category"),

                "speed": device.get("speed"),

                "totalKm": device.get("TotalKmOfDevice", 0)

            }

        }

    }
    


   

    def get_vehicle_km_custom_report(
    self,
    branch_name,
    vehicle_input,
    role,
    user,
    from_date
):
    # 1. Get vehicle
        result = self.get_branch_single_vehicle(
        branch_name,
        vehicle_input,
        role,
        user
    )

        if not result["success"]:
            return result

        vehicle = result["vehicle"]

    # 2. Fetch reports
        reports = list(
        self.db["report_distances"]
        .find({
            "$and": [
                get_rbac_filter(role, user, "report_distances", self.db),
                {
                    "uniqueId": {
                        "$in": self.normalize_unique_id(vehicle["uniqueId"])
                    }
                }
            ]
        })
        .sort("createdAt", -1)
    )

        if not reports:
            return {
            "success": False,
            "message": "No distance reports found."
        }

    # 3. Build date map
        report_map = {}
        for r in reports:
            report_map[r["createdAt"].date()] = r

    # 4. Parse requested date
        try:
            target_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        except:
            return {
            "success": False,
            "message": "Invalid date format. Use YYYY-MM-DD"
        }

    # 5. Get exact report
        report = report_map.get(target_date)

        if not report:
            return {
            "success": True,
            "vehicle": {
                "vehicleName": vehicle.get("vehicleName"),
                "uniqueId": vehicle.get("uniqueId")
            },
            "report": {
                "date": from_date,
                "km": 0,
                "message": "No movement recorded on this date"
            }
        }

        return {
        "success": True,
        "vehicle": {
            "vehicleName": vehicle.get("vehicleName"),
            "uniqueId": vehicle.get("uniqueId")
        },
        "report": {
            "date": from_date,
            "km": round(report.get("distance", 0), 2)
        }
    }

    def get_branch_vehicle_km_report(
    self,
    branch_name,
    message,
    role,
    user
):


    # FIND BRANCH
        branch = self.find_branch(
        branch_name,
        role,
        user
    )


        if not branch:

            return {

            "success": False,

            "message":
            f"Branch '{branch_name}' not found"

        }


        branch_id = branch["_id"]



    # DEVICE RBAC FILTER

        device_filter = get_rbac_filter(
        role,
        user,
        "devices",
        self.db
    )



    # GET BRANCH DEVICES

        devices = list(

            self.db["devices"].find({

            "$and":[

                device_filter,

                {

                    "$or":[

                        {
                            "branchId": branch_id
                        },

                        {
                            "branchId":
                            str(branch_id)
                        }

                    ]

                }

            ]

        })

    )



        km_reports = []



        for device in devices:


            unique_id = device.get(
            "uniqueId"
        )


            if not unique_id:
                continue



            report = self.vehicle_km_engine.get_km_report(

            unique_id,

            message or "",

            role,

            user

        )


            if report:


                km_reports.append({

                "vehicleName":

                (

                    device.get("vehicleNumber")

                    or device.get("vehicle_name")

                    or device.get("name")

                    or unique_id

                ),


                "uniqueId":
                unique_id,


                "kmReport":
                report

            })



        return {


        "success": True,


        "branch":{


            "branchId":
            str(branch["_id"]),


            "branchName":
            branch.get(
                "branchName"
            ),


            "username":
            branch.get(
                "username"
            )

        },


        "totalVehicles":

        len(km_reports),


        "vehicles":

        km_reports

    } 
  

    def calculate_week_month_distance(self, unique_ids, role, user, reference_date):
        """
        Calculate week and rolling 30-day distance from report_distances.

    Args:
        unique_ids (list): Vehicle unique IDs.
        role: User role.
        user: Current user.
        reference_date (date): Today or Last Active date.

    Returns:
        dict
        """

        reports = list(
        self.db["report_distances"].find({
            "$and": [
                get_rbac_filter(role, user, "report_distances", self.db),
                {
                    "uniqueId": {
                        "$in": unique_ids
                    }
                }
            ]
        })
    )

        report_map = {}

        for report in reports:
            report_date = report["createdAt"].date()
            report_map[report_date] = float(report.get("distance", 0))

    # ----------------------------
    # Week
    # ----------------------------
        week_start = reference_date - timedelta(days=reference_date.weekday())
        week_end = week_start + timedelta(days=6)

        week_total = 0

        current = week_start
        while current <= week_end:
            week_total += report_map.get(current, 0)
            current += timedelta(days=1)

    # ----------------------------
    # Rolling 30 Days
    # ----------------------------
        month_start = reference_date - timedelta(days=29)

        month_total = 0

        current = month_start
        while current <= reference_date:
            month_total += report_map.get(current, 0)
            current += timedelta(days=1)

        return {
        "week": {
            "from": week_start.strftime("%Y-%m-%d"),
            "to": week_end.strftime("%Y-%m-%d"),
            "totalKm": round(week_total, 2)
        },
        "month": {
            "type": "rolling_30_days",
            "from": month_start.strftime("%Y-%m-%d"),
            "to": reference_date.strftime("%Y-%m-%d"),
            "totalKm": round(month_total, 2)
        }
    } 
  
    def get_branch_today_accurate_distance(
    self,
    branch_name,
    vehicle_input,
    role,
    user
):

    # =====================================
    # 1. Find Vehicle using RBAC
    # =====================================

        result = self.get_branch_single_vehicle(
        branch_name,
        vehicle_input,
        role,
        user
    )

        if not result["success"]:
            return result

        vehicle = result["vehicle"]

        unique_ids = self.normalize_unique_id(
        vehicle["uniqueId"]
    )

    # =====================================
    # 2. Today's IST Time
    # =====================================

        IST = timezone(timedelta(hours=5, minutes=30))

        now = datetime.now(IST)

        today_start = now.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

        today_end = now.replace(
        hour=23,
        minute=59,
        second=59,
        microsecond=999999
    )

    # =====================================
    # 3. Aggregate History (RBAC Applied)
    # =====================================

        pipeline = [

        {
            "$match": {

                "$and": [

                    get_rbac_filter(
                        role,
                        user,
                        "histories",
                        self.db
                    ),

                    {
                        "uniqueId": {
                            "$in": unique_ids
                        }
                    },

                    {
                        "attributes.totalDistance": {
                            "$ne": None
                        }
                    },

                    {
                        "createdAt": {
                            "$gte": today_start,
                            "$lte": today_end
                        }
                    }

                ]

            }
        },

        {
            "$sort": {
                "createdAt": 1
            }
        },

        {
            "$project": {

                "_id": 0,

                "name": 1,

                "createdAt": 1,

                "totalDistanceKm": {
                    "$divide": [
                        "$attributes.totalDistance",
                        1000
                    ]
                }

            }
        },

        {
            "$group": {

                "_id": None,

                "vehicleName": {
                    "$first": "$name"
                },

                "startDistance": {
                    "$first": "$totalDistanceKm"
                },

                "endDistance": {
                    "$last": "$totalDistanceKm"
                },

                "firstRecord": {
                    "$first": "$createdAt"
                },

                "lastRecord": {
                    "$last": "$createdAt"
                }

            }
        },

        {
            "$project": {

                "_id": 0,

                "vehicleName": 1,

                "firstRecord": 1,

                "lastRecord": 1,

                "todayDistance": {

                    "$round": [

                        {
                            "$subtract": [
                                "$endDistance",
                                "$startDistance"
                            ]
                        },

                        2

                    ]

                }

            }
        }

    ]

        report = list(
        self.db["histories"].aggregate(pipeline)
    )

        if not report:

            return {
            "success": False,
            "message": "No history found for today."
        }

        report = report[0]

        return {

        "success": True,

        "branch": result["branch"],

        "vehicle": {

            "vehicleName": vehicle.get("vehicleName"),
            "deviceId": vehicle.get("deviceId"),
            "uniqueId": vehicle.get("uniqueId"),
            "status": vehicle.get("status"),
            "category": vehicle.get("category"),
            "model": vehicle.get("model")

        },

        "todayAccurateDistance": {

            "date": now.strftime("%Y-%m-%d"),

            "distanceKm": report["todayDistance"],

            "firstRecord": report["firstRecord"],

            "lastRecord": report["lastRecord"]

        }

    }
    
    def get_superadmin_single_vehicle_km_report(
    self,
    vehicle_input
):
        def extract_vehicle_input(payload):
            if isinstance(payload, dict):
                return payload.get("vehicle_input")

            if isinstance(payload, list) and len(payload) > 0:
                if isinstance(payload[0], dict):
                    return payload[0].get("vehicle_input")

            return payload
    # =====================================
    # 1. FIND VEHICLE (GLOBAL - ALL DEVICES)
    # =====================================
        vehicle_input = extract_vehicle_input(vehicle_input)
        vehicle_input = str(vehicle_input or "").strip()

        vehicle = self.db["devices"].find_one({
    "$or": [
        {"vehicleName": {"$regex": vehicle_input, "$options": "i"}},
        {"name": {"$regex": vehicle_input, "$options": "i"}},
        {"uniqueId": vehicle_input},
        {"uniqueId": str(vehicle_input)}
    ]
})

        if not vehicle:
            return {
            "success": False,
            "message": "Vehicle not found in any device"
        }

        unique_ids = self.normalize_unique_id(vehicle["uniqueId"])

    # =====================================
    # 2. FETCH DISTANCE REPORTS (NO RBAC)
    # =====================================
        report_distances = list(
        self.db["report_distances"]
        .find({
            "uniqueId": {"$in": unique_ids}
        })
        .sort("createdAt", -1)
    )

        if not report_distances:
            return {
            "success": False,
            "message": "No distance reports found for this vehicle"
        }

    # =====================================
    # 3. BUILD DAILY MAP
    # =====================================
        report_map = {
            r["createdAt"].date(): float(r.get("distance", 0))
            for r in report_distances
    }

        today = datetime.utcnow().date()
        available_dates = sorted(report_map.keys())

    # =====================================
    # 4. ACTIVE / INACTIVE LOGIC
    # =====================================
        if today in report_map:
            status = "active"
            analysis_base_date = today
            message = "Vehicle is active today."
        else:
            status = "inactive"
            analysis_base_date = available_dates[-1]
            message = f"Vehicle inactive today. Last active: {analysis_base_date}"

        current_km = round(report_map.get(analysis_base_date, 0), 2)

        previous_date = None
        for d in reversed(available_dates):
            if d < analysis_base_date:
                previous_date = d
                break

        yesterday_km = round(report_map.get(previous_date, 0), 2) if previous_date else 0

    # =====================================
    # 5. WEEK CALCULATION
    # =====================================
        week_start = analysis_base_date - timedelta(days=analysis_base_date.weekday())
        week_end = week_start + timedelta(days=6)

        week_total = sum(
        float(r.get("distance", 0))
            for r in report_distances
            if week_start <= r["createdAt"].date() <= week_end
    )

    # =====================================
    # 6. MONTH CALCULATION (30 DAYS)
    # =====================================
        month_start = analysis_base_date - timedelta(days=29)

        month_total = sum(
        float(r.get("distance", 0))
        for r in report_distances
        if month_start <= r["createdAt"].date() <= analysis_base_date
    )

        return {
        "success": True,
        "status": status,
        "message": message,

        "vehicle": {
            "vehicleName": vehicle.get("name"),
            "deviceId": str(vehicle.get("_id")),
            "uniqueId": vehicle.get("uniqueId"),
            "status": vehicle.get("status"),
            "category": vehicle.get("category"),
            "model": vehicle.get("model")
        },

        "reference": {
            "date": analysis_base_date.strftime("%Y-%m-%d"),
            "isTodayActive": status == "active"
        },

        "distanceReport": {
            "current": {
                "km": current_km
            },
            "yesterday": {
                "date": previous_date.strftime("%Y-%m-%d") if previous_date else None,
                "km": yesterday_km
            },
            "week": {
                "from": week_start.strftime("%Y-%m-%d"),
                "to": week_end.strftime("%Y-%m-%d"),
                "totalKm": round(week_total, 2)
            },
            "month": {
                "from": month_start.strftime("%Y-%m-%d"),
                "to": analysis_base_date.strftime("%Y-%m-%d"),
                "totalKm": round(month_total, 2)
            }
        }
    }