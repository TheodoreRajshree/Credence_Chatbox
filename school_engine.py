from bson import ObjectId
from rbac import get_rbac_filter
from geofences_engine import GeofencesEngine
from geofence_report_engine import GeofenceReportEngine 
from route_engine import RouteEngine
from vehicle_km_engine import VehicleKmEngine
from bson import ObjectId
from datetime import datetime, timedelta, timezone
import re
import os

from dotenv import load_dotenv

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
load_dotenv()
class SchoolEngine:


    def __init__(self, db):
        self.db = db
        self.geofences_engine = GeofencesEngine(db)
        self.route_engine =RouteEngine(db)
        self.geofence_report_engine =GeofenceReportEngine (db)
        self.vehicle_km_engine = VehicleKmEngine(db)
        self.encryption_key = os.getenv("ENCRYPTION_KEY").encode("utf-8")
        self.iv = os.getenv("IV").encode("utf-8")
        
       
    def decrypt_password(
    self,
    encrypted_text
):

        try:

            if not encrypted_text:
                return None

            cipher = AES.new(

            self.encryption_key,

            AES.MODE_CBC,

            self.iv

        )

            decrypted = unpad(

            cipher.decrypt(
                bytes.fromhex(encrypted_text)
            ),

            AES.block_size

        )

            return decrypted.decode("utf-8")

        except Exception as e:

            print("PASSWORD DECRYPT ERROR :", e)

            return encrypted_text
    def _convert_school_id(self, school_id):

        if not school_id:
            return None

        if isinstance(school_id, ObjectId):
            return school_id

        try:
            return ObjectId(str(school_id))

        except Exception:
            return school_id
    
   

    
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
   

    def clean(self, doc):

        if not doc:
            return doc

        result = {}

        for k, v in doc.items():

            if isinstance(v, ObjectId):
                result[k] = str(v)

            elif isinstance(v, dict):
                result[k] = self.clean(v)

            elif isinstance(v, list):
                result[k] = [
                    self.clean(item) if isinstance(item, dict) else item
                    for item in v
            ]

            else:
                result[k] = v

    # ==========================================
    # Populate School
    # ==========================================

        school_id = doc.get("schoolId")

        if school_id:

            try:

                if isinstance(school_id, str):
                    school_id = ObjectId(school_id)

                school = self.db["schools"].find_one(
                {"_id": school_id},
                {"name": 1}
            )

                if school:
                    result["schoolName"] = school.get("name")

            except:
                pass

    # ==========================================
    # Populate Branch
    # ==========================================

        branch_id = doc.get("branchId")

        if branch_id:

            try:

                if isinstance(branch_id, str):
                    branch_id = ObjectId(branch_id)

                branch = self.db["branches"].find_one(
                {"_id": branch_id},
                {"name": 1}
            )

                if branch:
                    result["branchName"] = branch.get("name")

            except:
                pass

        return result
    def get_specific_vehicle_idle_report(
    self,
    school_name,
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

        "school": {
            "schoolId": str(user.get("branchId")),
            "schoolName": school_name
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
    
    def get_specific_vehicle_last_position(
    self,
    school_name,
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

        return {

        "success": True,

        "school": {
            "schoolId": str(user.get("schoolId")),
            "schoolName": school_name
        },

        "vehicle": {
            # "vehicleName": selected_device.get("vehicleName"),
            # "vehicleNumber": selected_device.get("vehicleNumber"),
            "name": selected_device.get("name"),
            "uniqueId": selected_device.get("uniqueId")
        },

        "lastPosition": {

            "latitude": position.get("latitude"),
            "longitude": position.get("longitude"),
            # "speed": position.get("speed"),
            # "course": position.get("course"),
            # "accuracy": position.get("accuracy"),
            # "altitude": position.get("altitude"),
            # "address": position.get("address"),
            # "protocol": position.get("protocol"),
            # "deviceTime": position.get("deviceTime"),
            # "fixTime": position.get("fixTime"),
            # "serverTime": position.get("serverTime"),
            # "lastUpdate": position.get("lastUpdate"),
            # "valid": position.get("valid"),
            # "outdated": position.get("outdated")

        }

    }
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
    def get_school_specific_geofence(
    self,
    school_name,
    vehicle_input,
    role,
    user
):

    # ==========================
    # Find School
    # ==========================
        school = self.find_school(
        school_name,
        role,
        user
    )

        if not school:
            return {
            "success": False,
            "message": "School not found."
        }

        school_id = school["_id"]

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

        "$and": [

            device_filter,

            {
                "$or": [
                    {"schoolId": school_id},
                    {"schoolId": str(school_id)}
                ]
            },

            {
                "$or": [

                    {
                        "vehicleNumber": {
                            "$regex": f"^{vehicle_input}$",
                            "$options": "i"
                        }
                    },

                    {
                        "vehicle_name": {
                            "$regex": f"^{vehicle_input}$",
                            "$options": "i"
                        }
                    },

                    {
                        "name": {
                            "$regex": f"^{vehicle_input}$",
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

        query = {
        "$and": [
            geofence_filter,
            {
                "$or": [
                    {"_id": geofence_id}
                ]
            }
        ]
    }

        if ObjectId.is_valid(str(geofence_id)):
            query["$and"][1]["$or"].append(
            {"_id": ObjectId(str(geofence_id))}
        )

        geofence = self.db["geofences"].find_one(query)

        if not geofence:
            return {
            "success": False,
            "message": "Geofence not found."
        }

        return {

        "success": True,

        "school": {

            "schoolId": str(school["_id"]),
            "schoolName": school.get("schoolName")

        },

        "vehicle": {

            "vehicleName": (
                device.get("vehicleNumber")
                or device.get("vehicle_name")
                or device.get("name")
            ),

            "uniqueId": device.get("uniqueId")

        },

        "geofence": {

            "geofenceId": str(geofence["_id"]),

            "name": geofence.get("geofenceName"),

            "address": geofence.get("address"),

            "latitude": geofence.get("latitude"),

            "longitude": geofence.get("longitude"),

            "radius": geofence.get("radius"),

            "description": geofence.get("description")

        }

    }
    def get_school_km_report(
    self,
    school_id,
    message,
    role,
    user
):
        return self.vehicle_km_engine.get_group_km_report(
        "school",
        school_id,
        message,
        role,
        user
    )
    def school_id_filter(self, school_id):

        values = [
        str(school_id)
    ]

        try:
            values.append(
            ObjectId(str(school_id))
        )
        except:
            pass


        return {
        "$or":[
            {
                "schoolId":v
            }
            for v in values
        ]
    }
    def get_school_profile(
    self,
    school_id=None,
    role=None,
    user=None
):

    # take school id from logged in user
        if not school_id:

            if user:

                school_id = (
                user.get("schoolId")
                or user.get("_id")
                or user.get("school_id")
            )


        if not school_id:
            return {
            "error":"school id missing",
            "user":user
        }


        school_filter = get_rbac_filter(
        role,
        user,
        "schools",
        self.db
    )


        query = {

        "$and":[

            school_filter,

            {
                "_id":
                self._convert_school_id(
                    school_id
                )
            }

        ]

    }


        print("SCHOOL PROFILE QUERY:", query)


        school = self.db["schools"].find_one(query)


        print("SCHOOL FOUND:", school)


        if not school:
            return None


        return {

        "schoolId":str(school["_id"]),

        "schoolName":
        school.get("schoolName"),

        "username":
        school.get("username"),

        "email":
        school.get("email"),

        "mobileNo":
        school.get("mobileNo"),

        "assignedCompany":
        school.get("assignedCompany"),

        "active":
        school.get("Active")

    }
    # ====================================
    # SCHOOL PROFILE
    # ====================================
     
    

    # ====================================
    # VEHICLES
    # ====================================

    def get_school_vehicles(
        self,
        school_id,
        role,
        user
    ):


        device_filter = get_rbac_filter(
            role,
            user,
            "devices",
            self.db
        )


        vehicles = list(

            self.db["devices"].find({

                "$and":[

                    device_filter,

                    {
                        "schoolId":
                        self._convert_school_id(
                            school_id
                        )
                    }

                ]

            })
        )
        return [

            {

                "name":
                v.get("name"),

                "uniqueId":
                v.get("uniqueId"),

                "status":
                v.get("status"),

                "model":
                v.get("model"),

                "category":
                v.get("category")

            }

            for v in vehicles

        ]

    def get_school_vehicle_count(
        self,
        school_id,
        role,
        user
    ):

        return len(

            self.get_school_vehicles(

                school_id,

                role,

                user

            )

        )

    # ====================================
    # DRIVERS
    # ====================================

    def get_school_drivers(
        self,
        school_id,
        role,
        user
    ):


        driver_filter = get_rbac_filter(
            role,
            user,
            "drivers",
            self.db
        )
        drivers = list(

            self.db["drivers"].find({

                "$and":[

                    driver_filter,

                    {
                        "schoolId":
                        self._convert_school_id(
                            school_id
                        )
                    }

                ]

            })

        )
        return [

            {

                "driverName":
                d.get("driverName"),

                "mobileNo":
                d.get("mobileNo"),

                "status":
                d.get("isApproved")

            }

            for d in drivers

        ]
    def get_school_devices(
    self,
    school_id,
    role,
    user
):

    # RBAC filter
        device_filter = get_rbac_filter(
        role,
        user,
        "devices",
        self.db
    )

    # Get all devices of school
        devices = self.db["devices"].find({

        "$and": [

            device_filter,

            {
                "$or": [
                    {"schoolId": ObjectId(str(school_id))},
                    {"schoolId": str(school_id)}
                ]
            }

        ]

    })


        vehicles = []

        for device in devices:

            vehicle = {

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

            "average": device.get("average")

        }

            vehicles.append(vehicle)


        return {

        "success": True,

        "schoolId": str(school_id),

        "totalDevices": len(vehicles),

        "vehicles": vehicles

    }
    import re

    def get_school_single_vehicle(
    self,
    school_name,
    vehicle_input,
    role,
    user
):
    # =====================================
    # FIND SCHOOL
    # =====================================

        school = self.find_school(
        school_name,
        role,
        user
    )

        if not school:
            return {
            "success": False,
            "message": f"School '{school_name}' not found"
        }

        school_id = school["_id"]

    # =====================================
    # RBAC FILTER
    # =====================================

        device_filter = get_rbac_filter(
        role,
        user,
        "devices",
        self.db
    )

    # =====================================
    # NORMALIZE INPUT
    # =====================================

        def normalize(text):
            return re.sub(r"\s+", "", str(text or "")).lower()

        normalized_input = normalize(vehicle_input)

    # =====================================
    # GET ALL VEHICLES OF THIS SCHOOL
    # =====================================

        devices = self.db["devices"].find({
        "$and": [
            device_filter,
            {
                "$or": [
                    {"schoolId": school_id},
                    {"schoolId": str(school_id)}
                ]
            }
        ]
    })

        device = None

        for d in devices:

            vehicle_number = normalize(d.get("vehicleNumber"))
            vehicle_name = normalize(d.get("vehicle_name"))
            name = normalize(d.get("name"))
            unique_id = normalize(d.get("uniqueId"))

            if (
                normalized_input == vehicle_number or
                normalized_input == vehicle_name or
                normalized_input == name or
                normalized_input == unique_id
        ):
                device = d
                break

        if not device:
            return {
            "success": False,
            "message": "Vehicle not found."
        }

        vehicle = {
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
    }

        return {
        "success": True,
        "school": {
            "schoolId": str(school["_id"]),
            "schoolName": school.get("schoolName")
        },
        "vehicle": vehicle
    }
    def find_school(self, school_name, role, user):

        rbac_filter = get_rbac_filter(
        role,
        user,
        "schools",
        self.db
    )

        school_name = str(school_name).strip() if school_name is not None else ""

        school = None

    # 1st try: ObjectId match
        try:
            school = self.db["schools"].find_one({

            "$and":[

                rbac_filter,

                {
                    "_id": ObjectId(school_name)
                }

            ]

        })

        except:
            pass

    # 2nd try: Name / Username match
        if not school:

            school = self.db["schools"].find_one({

            "$and":[

                rbac_filter,

                {

                    "$or":[

                        {
                            "schoolName": {
                                "$regex": school_name,
                                "$options": "i"
                            }
                        },

                        {
                            "username": {
                                "$regex": school_name,
                                "$options": "i"
                            }
                        }

                    ]

                }

            ]

        })

        return school
    def get_single_school_vehicle_status(
    self,
    school_name,
    vehicle_input,
    role,
    user,
    limit=100
):

    # =====================================
    # Logged-in School
    # =====================================

        school_id = user.get("schoolId")

        if not school_id:
            return {
            "success": False,
            "message": "School not found."
        }

        school = self.db["schools"].find_one({
        "_id": self._convert_school_id(school_id)
    })

        if not school:
            return {
            "success": False,
            "message": "School not found."
        }

    # =====================================
    # Find Vehicle
    # =====================================

        result = self.get_school_single_vehicle(
        school.get("schoolName"),
        vehicle_input,
        role,
        user
    )

        if not result["success"]:
            return result

    # =====================================
    # Status Reports
    # =====================================

        status_filter = get_rbac_filter(
        role,
        user,
        "report_statuses",
        self.db
    )

        reports = list(

        self.db["report_statuses"].find({

            "$and": [

                status_filter,

                {
                    "uniqueId": {
                        "$in": self.vehicle_km_engine.normalize_unique_id(
                            result["vehicle"]["uniqueId"]
                        )
                    }
                }

            ]

        })

        .sort("startDateTime", -1)

        .limit(limit)

    )

    # =====================================
    # Response
    # =====================================

        return {

        "success": True,

        "school": {

            "schoolId": str(school["_id"]),
            "schoolName": school.get("schoolName"),
            "username": school.get("username")

        },

        "vehicle": result["vehicle"],

        "statusReport": [

            self.clean(report)

            for report in reports

        ]

    }
    def get_specific_vehicle_travel_summary(
    self,
    school_name,
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
    def get_specific_school_vehicle_distance_report(
    self,
    school_name,
    vehicle_input,
    role,
    user,
    limit=100
):

        school_id = user.get("schoolId")

        if not school_id:
            return {
            "success": False,
            "message": "School not found."
        }

        school = self.db["schools"].find_one({
        "_id": self._convert_school_id(school_id)
    })

        if not school:
            return {
            "success": False,
            "message": "School not found."
        }

        result = self.get_school_single_vehicle(
        school.get("schoolName"),
        vehicle_input,
        role,
        user
    )

        if not result["success"]:
            return result

        vehicle = result["vehicle"]

        reports = list(

        self.db["report_distances"].find({

            "$and":[

                get_rbac_filter(
                    role,
                    user,
                    "report_distances",
                    self.db
                ),

                {
                    "uniqueId":{
                        "$in": self.vehicle_km_engine.normalize_unique_id(
                            vehicle["uniqueId"]
                        )
                    }
                }

            ]

        })

        .sort("createdAt",-1)

        .limit(limit)

    )

        return {

        "success": True,

        "school": {
            "schoolId": str(school["_id"]),
            "schoolName": school.get("schoolName")
        },

        "vehicle": vehicle,

        "reports": [
            self.clean(r)
            for r in reports
        ]

    }
    def get_school_driver_count(
        self,
        school_id,
        role,
        user
    ):
        return len(

            self.get_school_drivers(

                school_id,

                role,

                user

            )

        )

    # ====================================
    # ROUTES
    # ====================================

    def get_route_school(
        self,
        route_id,
        role,
        user
    ):


        route = self.route_engine.get_route(
    route_id,
    role,
    user
)


        if not route:
            return None


        school_filter = get_rbac_filter(

            role,

            user,

            "schools",

            self.db

        )


        school = self.db["routes"].find_one({

            "$and":[

                school_filter,

                {
                    "_id":
                    self._convert_id(
                        route.get("schoolId")
                    )
                }

            ]

        })


        if not school:
            return None


        return {

            "schoolName":
            school.get("schoolName"),

            "username":
            school.get("username"),

            "mobileNo":
            school.get("mobileNo")

        }

    # ====================================
    # GEOFENCES
    # ====================================

    def get_school_geofences(
    self,
    school_id,
    role,
    user
):

        geofence_filter = get_rbac_filter(
        role,
        user,
        "geofences",
        self.db
    )


        geofences = list(

        self.db["geofences"].find({

            "$and":[

                geofence_filter,

                {
                    "schoolId":
                    self._convert_school_id(
                        school_id
                    )
                }

            ]

        })

    )


        return [

        self.clean(g)

        for g in geofences

    ]
    def get_school_geofence_report(
        self,
        school_id,
        role,
        user,
        limit=100
    ):


        geofences = self.geofence_report_engine.get_school_geofence_report(

            school_id,

            role,

            user,

            limit=500

        )



        if not geofences:

            return []

        geofence_ids = [
        ObjectId(g["_id"])
        for g in geofences
    ]

        



        return self.get_reports_by_geofence_ids(

            geofence_ids,

            role,

            user,

            limit

        )

    # ====================================
    # TICKETS
    # ====================================

    def get_school_tickets(
        self,
        school_id,
        role,
        user
    ):


        ticket_filter = get_rbac_filter(
            role,
            user,
            "tickets",
            self.db
        )


        return self.db["tickets"].count_documents({

            "$and":[

                ticket_filter,

                {
                    "schoolId":
                    self._convert_school_id(
                        school_id
                    )
                }

            ]

        })
    # ====================================
    # SUBSCRIPTIONS
    # ====================================

    def get_school_subscriptions(
        self,
        school_id,
        role,
        user
    ):
        subscription_filter = get_rbac_filter(
            role,
            user,
            "devicesubscriptions",
            self.db
        )
        return list(

            self.db["devicesubscriptions"].find({

                "$and":[

                    subscription_filter,

                    {
                        "paidBy":
                        self._convert_school_id(
                            school_id
                        )
                    }

                ]

            })

        )
    
    # ====================================
    # DASHBOARD
    # ====================================

    def get_school_dashboard(
        self,
        school_id,
        role,
        user
    ):


        return {


            "vehicle_count":

            self.get_school_vehicle_count(

                school_id,

                role,

                user

            ),


            "driver_count":

            self.get_school_driver_count(

                school_id,

                role,

                user

            ),


            "route_count":

            len(

                self.get_school_routes(

                    school_id,

                    role,

                    user

                )

            ),


            "geofence_count":

            len(

                self.get_school_geofences(

                    school_id,

                    role,

                    user

                )

            ),


            "ticket_count":

            self.get_school_tickets(

                school_id,

                role,

                user

            )

        }
    def get_route_school_specific_vehicle(
    self,
    school_name,
    vehicle_input,
    role,
    user
):

    # ===============================
    # Find School
    # ===============================
        school = self.find_school(
        school_name,
        role,
        user
    )

        if not school:
            return {
            "success": False,
            "message": f"School '{school_name}' not found."
        }

        school_id = school["_id"]

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

        "$and": [

            device_filter,

            {
                "$or": [
                    {"schoolId": school_id},
                    {"schoolId": str(school_id)}
                ]
            },

            {
                "$or": [

                    {
                        "vehicleNumber": {
                            "$regex": vehicle_input,
                            "$options": "i"
                        }
                    },

                    {
                        "vehicle_name": {
                            "$regex": vehicle_input,
                            "$options": "i"
                        }
                    },

                    {
                        "name": {
                            "$regex": vehicle_input,
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
            "message": "Vehicle not found."
        }

        device_id = device["_id"]

    # ===============================
    # Find Route
    # ===============================
        route = self.db["routes"].find_one({

        "$and": [

            route_filter,

            {
                "$or": [
                    {"schoolId": school_id},
                    {"schoolId": str(school_id)}
                ]
            },

            {
                "$or": [
                    {"deviceObjId": device_id},
                    {"deviceObjId": str(device_id)}
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

        "school": {

            "schoolId": str(school["_id"]),
            "schoolName": school.get("schoolName")

        },

        "route": {

            "routeId": str(route["_id"]),

            "routeNumber": route.get("routeNumber"),

            "routeCompletionTime": route.get("routeCompletionTime"),

            "vehicle": {

                "deviceId": str(device["_id"]),

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
#     def get_school_single_vehicle_km_report(
#     self,
#     school_name,
#     vehicle_input,
#     role,
#     user
# ):
#     # 1. Get vehicle
#         result = self.get_school_single_vehicle(
#         school_name,
#         vehicle_input,
#         role,
#         user
#     )

#         if not result["success"]:
#             return result

#         vehicle = result["vehicle"]

#     # 2. Fetch reports
#         reports = list(
#         self.db["report_distances"]
#         .find({
#             "$and": [
#                 get_rbac_filter(role, user, "report_distances", self.db),
#                 {
#                     "uniqueId": {
#                         "$in": self.normalize_unique_id(vehicle["uniqueId"])
#                     }
#                 }
#             ]
#         })
#         .sort("createdAt", -1)
#     )

#         if not reports:
#             return {
#             "success": False,
#             "message": "No distance reports found."
#         }

#     # 3. Build map (date → record)
#         report_map = {}
#         for r in reports:
#             report_map[r["createdAt"].date()] = r

#         today = datetime.utcnow().date()

#     # 4. ACTIVE / LAST ACTIVE LOGIC
#         if today in report_map:
#             reference_date = today
#             status = "active"
#             message = "Vehicle active today."
#         else:
#             reference_date = reports[0]["createdAt"].date()
#             status = "inactive"
#             message = f"Vehicle inactive today. Last active on {reference_date.strftime('%Y-%m-%d')}."

#     # 5. SAFE KM GETTER
#         def get_km(d):
#             r = report_map.get(d)
#             return round(r.get("distance", 0), 2) if r else 0

#     # 6. SUM FUNCTION (IMPORTANT)
#         def sum_range(start_date, end_date):
#             total = 0.0
#             current = start_date

#             while current <= end_date:
#                 total += get_km(current)
#                 current += timedelta(days=1)

#             return round(total, 2)

#     # 7. DATE CALCULATIONS
#         yesterday = reference_date - timedelta(days=1)

#         week_start = reference_date - timedelta(days=6)
#         week_end = reference_date

#         month_start = reference_date - timedelta(days=29)
#         month_end = reference_date

#     # 8. SMART LABEL (TODAY OR DATE)
#         def format_day(date_value):
#             return {
#             "date": "today" if date_value == today else date_value.strftime("%Y-%m-%d"),
#             "km": get_km(date_value)
#         }

#     # 9. FINAL RESPONSE
#         return {
#         "success": True,
#         "status": status,
#         "message": message,

#         "school": result["school"],

#         "vehicle": {
#             "vehicleName": vehicle.get("vehicleName"),
#             "deviceId": vehicle.get("deviceId"),
#             "uniqueId": vehicle.get("uniqueId"),
#             "status": vehicle.get("status"),
#             "category": vehicle.get("category"),
#             "model": vehicle.get("model")
#         },

#         "distanceReport": {
#             # TODAY OR LAST ACTIVE
#             "current": format_day(reference_date),

#             # YESTERDAY
#             "yesterday": format_day(yesterday),

#             # WEEK TOTAL (SUM ONLY)
#             "week": {
#                 "from": week_start.strftime("%Y-%m-%d"),
#                 "to": week_end.strftime("%Y-%m-%d"),
#                 "totalKm": sum_range(week_start, week_end)
#             },

#             # MONTH TOTAL (SUM ONLY)
#             "month": {
#                 "from": month_start.strftime("%Y-%m-%d"),
#                 "to": month_end.strftime("%Y-%m-%d"),
#                 "totalKm": sum_range(month_start, month_end)
#             }
#         }
#     }
    def get_school_single_vehicle_km_report(
    self,
    school_name,
    vehicle_input,
    role,
    user
):

    # =====================================
    # 1. Get Vehicle
    # =====================================
        result = self.get_school_single_vehicle(
        school_name,
        vehicle_input,
        role,
        user
    ) 
        print(result)

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
            "message": "No distance reports found as the device is inactive."
        }

    # =====================================
    # 3. Build map are in active
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

        "school": result["school"],

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
    
    
    def get_school_today_accurate_distance(
    self,
    school_name,
    vehicle_input,
    role,
    user
):

    # =====================================
    # 1. VEHICLE INPUT
    # =====================================

        if isinstance(vehicle_input, dict):

            vehicle_input = vehicle_input.get(
            "vehicle_input"
        )


        vehicle_input = str(
        vehicle_input or ""
    ).strip()


        if not vehicle_input:

            return {

            "success": False,

            "message": (
                "Please enter vehicle name "
                "or unique ID."
            )

        }


    # =====================================
    # 2. FIND VEHICLE USING SCHOOL RBAC
    # =====================================

        device_rbac_filter = get_rbac_filter(

        role,

        user,

        "devices",

        self.db

    )


        regex = re.compile(

        f"^{re.escape(vehicle_input)}$",

        re.IGNORECASE

    )


        device = self.db["devices"].find_one({

        "$and": [

            device_rbac_filter,

            {

                "$or": [

                    {
                        "name": regex
                    },

                    {
                        "vehicleName": regex
                    },

                    {
                        "vehicleNumber": regex
                    },

                    {
                        "vehicle_name": regex
                    },

                    {
                        "uniqueId": vehicle_input
                    },

                    {

                        "uniqueId": {

                            "$in": (

                                self.normalize_unique_id(

                                    vehicle_input

                                )

                            )

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


    # =====================================
    # 3. UNIQUE ID NORMALIZATION
    # =====================================

        unique_ids = self.normalize_unique_id(

        device.get(

            "uniqueId"

        )

    )


        if not unique_ids:

            return {

            "success": False,

            "message": (

                "Vehicle unique ID not found."

            )

        }


    # =====================================
    # 4. IST TODAY RANGE
    # =====================================

        IST = timezone(

        timedelta(

            hours=5,

            minutes=30

        )

    )


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
    # 5. HISTORY RBAC FILTER
    # =====================================

        history_filter = get_rbac_filter(

        role,

        user,

        "histories",

        self.db

    )


    # =====================================
    # 6. LAST ODOMETER BEFORE TODAY
    # =====================================

        previous_record = (
 
        self.db["histories"].find_one(

            {

                "$and": [

                    history_filter,

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

                            "$lt": today_start

                        }

                    }

                ]

            },

            sort=[

                (

                    "createdAt",

                    -1

                )

            ]

        )

    )


    # =====================================
    # 7. LATEST ODOMETER TODAY
    # =====================================

        today_last_record = (

        self.db["histories"].find_one(

            {

                "$and": [

                    history_filter,

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

            },

            sort=[

                (

                    "createdAt",

                    -1

                )

            ]

        )

    )


        if not today_last_record:

            return {

            "success": False,

            "message": (

                "No history found for today."

            )

        }


    # =====================================
    # 8. START ODOMETER
    # =====================================

        if previous_record:

            start_distance = (

            previous_record[

                "attributes"

            ][

                "totalDistance"

            ]

            / 1000

        )


            first_record = (

            previous_record.get(

                "createdAt"

            )

        )


        else:

        # =================================
        # NO HISTORY BEFORE TODAY
        # USE FIRST RECORD TODAY
        # =================================

            first_today_record = (

            self.db["histories"].find_one(

                {

                    "$and": [

                        history_filter,

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

                },

                sort=[

                    (

                        "createdAt",

                        1

                    )

                ]

            )

        )


            if not first_today_record:

                return {

                "success": False,

                "message": (

                    "No starting history found."

                )

            }


            start_distance = (

            first_today_record[

                "attributes"

            ][

                "totalDistance"

            ]

            / 1000

        )


            first_record = (

            first_today_record.get(

                "createdAt"

            )

        )


    # =====================================
    # 9. END ODOMETER
    # =====================================

        end_distance = (

        today_last_record[

            "attributes"

        ][

            "totalDistance"

        ]

        / 1000

    )


    # =====================================
    # 10. CALCULATE TODAY DISTANCE
    # =====================================

        distance = round(

        end_distance

        - start_distance,

        2

    )


    # =====================================
    # 11. PREVENT NEGATIVE DISTANCE
    # =====================================

        if distance < 0:

            distance = 0


    # =====================================
    # 12. VEHICLE NAME
    # =====================================

        vehicle_name = (

        device.get("name")

        or device.get("vehicleName")

        or device.get("vehicleNumber")

        or device.get("vehicle_name")

        or "N/A"

    )


    # =====================================
    # 13. FINAL RESPONSE
    # =====================================

        return {

        "success": True,


        "school": school_name,


        "vehicle": {

            "vehicleName": vehicle_name,


            "deviceId": str(

                device.get(

                    "_id"

                )

            ),


            "uniqueId": device.get(

                "uniqueId"

            ),


            "status": device.get(

                "status"

            ),


            "category": device.get(

                "category"

            ),


            "model": device.get(

                "model"

            )

        },


        "todayAccurateDistance": {

            "date": now.strftime(

                "%Y-%m-%d"

            ),


            "distanceKm": distance,


            "firstRecord": first_record,


            "lastRecord": (

                today_last_record.get(

                    "createdAt"

                )

            ),


            "startOdometerKm": round(

                start_distance,

                2

            ),


            "endOdometerKm": round(

                end_distance,

                2

            )

        }

    }
    def get_school_with_vehicles_final_for_devices(
        self,
        school_name,
        role,
        user
    ):


        school = self.find_branch(
            school_name,
            role,
            user
        )


        if not school:

            return {

                "success":False,

                "message":
                f"Branch '{school_name}' not found"

            }


        school_id = school["_id"]


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
                                "branchId":school_id
                            },

                            {
                                "branchId":
                                str(school_id)
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
                str(school["_id"]),


                "branchName":
                school.get(
                    "branchName"
                ),


                "username":
                school.get(
                    "username"
                ),


                "mobileNo":
                school.get(
                    "mobileNo"
                )

            },


            "totalVehicles":
            len(vehicle_list),


            "vehicles":
            vehicle_list

        }
#     def get_school_with_branches(
#     self,
    
#     role,
#     user
# ):

#     # ==========================================
#     # Find School
#     # ==========================================

#         school = self.find_school(
        
#         role,
#         user
#     )

#         if not school:
#             return {
#                "success": False,
#             "message": f"School  not found."
#         }

#         school_id = school["_id"]

#     # ==========================================
#     # RBAC Filter
#     # ==========================================

#         branch_filter = get_rbac_filter(
#         role,
#         user,
#         "branches",
#         self.db
#     )

#     # ==========================================
#     # Find Branches
#     # ==========================================

#         branches = list(
#         self.db["branches"].find({
#             "$and": [
#                 branch_filter,
#                 {
#                     "$or": [
#                         {
#                             "schoolId": school_id
#                         },
#                         {
#                             "schoolId": str(school_id)
#                         }
#                     ]
#                 }
#             ]
#         })
#     )

#     # ==========================================
#     # Build Branch List
#     # ==========================================

#         branch_list = []

#         for branch in branches:

#             branch_list.append({

#             "branchId": str(branch["_id"]),

#             "branchName": branch.get("branchName"),

#             "username": branch.get("username"),

#             "email": branch.get("email"),

#             "mobileNo": branch.get("mobileNo"),

#             "assignedCompany": branch.get("assignedCompany"),

#             "active": branch.get("Active")

#         })

#     # ==========================================
#     # Response
#     # ==========================================

#         return {

#         "success": True,

#         "school": {

#             "schoolId": str(school["_id"]),

#             "schoolName": school.get("schoolName"),

#             "username": school.get("username"),

#             "email": school.get("email"),

#             "mobileNo": school.get("mobileNo"),

#             "assignedCompany": school.get("assignedCompany"),

#             "active": school.get("Active")

#         },

#         "totalBranches": len(branch_list),

#         "branches": branch_list

#     }
   

    def get_school_with_branches_final(
    self,
    role,
    user
):
    # Logged in school id
        school_id = user.get("schoolId")

        if not school_id:
            return {
            "success": False,
            "message": "School not found."
        }

    # Convert ObjectId if required
        try:
            school_obj_id = ObjectId(str(school_id))
        except:
            school_obj_id = school_id

    # Get school
        school = self.db["schools"].find_one({
        "_id": school_obj_id
    })

        if not school:
            return {
            "success": False,
            "message": "School not found."
        }

    # Get branches under school
        branches = list(
        self.db["branches"].find({
            "$or": [
                {"schoolId": school_obj_id},
                {"schoolId": str(school_obj_id)}
            ]
        })
    )

        branch_list = []

        for branch in branches:
            branch_list.append({
            "branchId": str(branch.get("_id")),
            "branchName": branch.get("branchName"),
            "username": branch.get("username"),
            "email": branch.get("email"),
            "mobileNo": branch.get("mobileNo"),
            "status": branch.get("Active")
        })

        return {
        "success": True,
        "school": {
            "schoolId": str(school.get("_id")),
            "schoolName": school.get("schoolName")
        },
        "totalBranches": len(branch_list),
        "branches": branch_list
    }
    # def find_school_superadmin(self, school_name, role, user):
    # def find_school_superadmin(self, role, user, school_name=None):

    
    def find_school_superadmin(
    self,
    role,
    user
):

        try:

        # =====================================
        # ONLY SUPERADMIN
        # =====================================

            if role.lower() != "superadmin":

                return {
                "success": False,
                "message": "Only Superadmin can access all school profiles."
            }

            schools = list(
            self.db["schools"].find()
        )

            result = []

            for school in schools:

            # =====================================
            # DECRYPT PASSWORD
            # =====================================

                password = self.decrypt_password(
                school.get("password")
            )

                result.append({

                "schoolId": str(
                    school.get("_id")
                ),

                "schoolName": school.get(
                    "schoolName"
                ),

                "username": school.get(
                    "username"
                ),

                "password": password,

                "email": school.get(
                    "email"
                ),

                "mobileNo": school.get(
                    "mobileNo"
                ),

                "role": school.get(
                    "role"
                ),

                "active": school.get(
                    "Active"
                ),

                # "assignedCompany": (
                #     school.get(
                #         "access",
                #         {}
                #     ).get(
                #         "assignedCompany"
                #     )
                # ),

                "createdAt": school.get(
                    "createdAt"
                ),

                "updatedAt": school.get(
                    "updatedAt"
                )

            })

            return {

            "success": True,

            "count": len(result),

            "schools": result

        }

        except Exception as e:

            print("ERROR :", e)

            return {

            "success": False,

            "error": str(e)

        }

    

    def find_specific_school_superadmin(
    self,
    role,
    user,
    input_value=None
):
    # =====================================
    # VALIDATE INPUT
    # =====================================
        import re

        school_name = re.sub(r"\s+", "", str(input_value or "").strip()).lower()

        if not school_name:
            return {
            "success": False,
            "message": "Please enter a School Name or School ID."
        }

    # =====================================
    # RBAC FILTER
    # =====================================
        if role.lower() == "superadmin":
            base_filter = {}
        else:
            base_filter = get_rbac_filter(
            role,
            user,
            "schools",
            self.db
        ) or {}

    # =====================================
    # PROJECTION
    # =====================================
        projection = {
        "role": 0,
        "fullAccess": 0,
        "subscriptionExpirationDate": 0,
        "fcmToken": 0,
        "lastNotifiedDate": 0,
        "notificationsEnabled": 0,
        "Notification": 0,
        "access": 0,
        "reportEmail": 0,
        "__v": 0
    }

        school = None

    # =====================================
    # SEARCH BY OBJECT ID
    # =====================================
        if ObjectId.is_valid(school_name):
            school = self.db["schools"].find_one(
            {
                **base_filter,
                "_id": ObjectId(school_name)
            },
            projection
        )

    # =====================================
    # SEARCH BY NAME / USERNAME (EXACT MATCH)
    # =====================================
        if school is None:
            school = None

            for s in self.db["schools"].find(base_filter, projection):
                db_school = re.sub(r"\s+", "", s.get("schoolName", "")).lower()
                db_username = re.sub(r"\s+", "", s.get("username", "")).lower()

                if db_school == school_name or db_username == school_name:
                    school = s
                    break

    # =====================================
    # SCHOOL NOT FOUND
    # =====================================
        if school is None:
            return {
            "success": False,
            "message": f"School '{school_name}' not found."
        }

    # =====================================
    # RESPONSE
    # =====================================
        return {
        "success": True,
        "school": {
            "schoolId": str(school.get("_id")),
            "schoolName": school.get("schoolName"),
            "username": school.get("username"),
            "password": self.decrypt_password(school.get("password")),
            "email": school.get("email"),
            "mobileNo": school.get("mobileNo"),
            "address": school.get("address"),
            "createdAt": school.get("createdAt"),
            "Active": school.get("Active")
        }
    }
    def get_school_specific_branch_vehicle_status(
    self,
    branch_name,
    vehicle_input,
    role,
    user,
    limit=100
):

    # =====================================
    # 1. Logged-in School
    # =====================================
        school_id = user.get("schoolId")

        if not school_id:
            return {
            "success": False,
            "message": "School not found."
        }

        school = self.db["schools"].find_one({
        "_id": self._convert_school_id(school_id)
    })

        if not school:
            return {
            "success": False,
            "message": "School not found."
        }

    # =====================================
    # 2. Find Branch Vehicle
    # =====================================
        result = self.get_school_specific_branch_vehicle(
        branch_name,
        vehicle_input,
        role,
        user
    )

        if not result["success"]:
            return result

        vehicle = result["vehicle"]

    # =====================================
    # 3. Fetch Status Reports
    # =====================================
        reports = list(

        self.db["report_statuses"].find({

            "$and": [

                get_rbac_filter(
                    role,
                    user,
                    "report_statuses",
                    self.db
                ),

                {
                    "uniqueId": {
                        "$in": self.vehicle_km_engine.normalize_unique_id(
                            vehicle["uniqueId"]
                        )
                    }
                }

            ]

        })

        .sort("startDateTime", -1)

        .limit(limit)

    )

    # =====================================
    # 4. Response
    # =====================================
        return {

        "success": True,

        "school": result["school"],

        "branch": result["branch"],

        "vehicle": vehicle,

        "statusReport": [
            self.clean(report)
            for report in reports
        ]
    }