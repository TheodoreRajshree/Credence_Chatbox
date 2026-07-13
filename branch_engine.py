from bson import ObjectId
from rbac import get_rbac_filter
from vehicle_km_engine import VehicleKmEngine
from datetime import datetime, timedelta
import re
import re
import os
from dotenv import load_dotenv
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
load_dotenv()
from report_status_engine import ReportStatusEngine
class BranchEngine:

    def __init__(self, db):
        self.db = db
        self.vehicle_km_engine = VehicleKmEngine(db)
        self.report_status_engine =ReportStatusEngine(db)
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
    # ====================================
    # ID CONVERT
    # ====================================
    
    def _convert_branch_id(self, branch_id):

        try:
            return ObjectId(str(branch_id))

        except:
            return branch_id


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
# SINGLE BRANCH VEHICLE STATUS
# =====================================

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
    def get_branch_single_vehicle(
    self,
    branch_name,
    vehicle_input,
    role,
    user
):
    # Find branch
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

    # RBAC filter
        device_filter = get_rbac_filter(
        role,
        user,
        "devices",
        self.db
    )

    # Search vehicle within this branch
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
                            "$in": [vehicle_input, str(vehicle_input)]
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
        "totalKm": device.get("TotalKmOfDevice", 0)
    }

        return {
        "success": True,
        "vehicle": vehicle
    }
    # ====================================
    # BRANCH PROFILE
    # ====================================
    def get_branch_km_report(
    self,
    branch_id,
    message,
    role,
    user
):
        return self.vehicle_km_engine.get_group_km_report(
        "branch",
        branch_id,
        message,
        role,
        user
    )
    def get_branch_profile(
        self,
        branch_id,
        role,
        user
    ):
        print("ROLE:", role)
        print("USER ID:", user["_id"])
        print("BRANCH ID:", branch_id)
          

        rbac_filter = get_rbac_filter(
            role,
            user,
            "branches",
            self.db
        )
        print("RBAC FILTER:", rbac_filter)
        converted_id = self._convert_branch_id(branch_id)

        print("CONVERTED ID:", converted_id)
        branch = self.db["branches"].find_one({

            "$and":[

                rbac_filter,

                {
                    "_id":
                    self._convert_branch_id(branch_id)
                }

            ]

        })

        print("FOUND:", branch)
        if not branch:
            return None


        return {

            "branchName":
            branch.get("branchName"),

            "username":
            branch.get("username"),

            "email":
            branch.get("email"),

            "mobileNo":
            branch.get("mobileNo"),

            "role":
            branch.get("role"),

            "active":
            branch.get("Active"),

            "schoolId":
            str(branch.get("schoolId"))

        }



    # ====================================
    # VEHICLES
    # ====================================
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
    def get_branch_vehicles(
        self,
        branch_id,
        role,
        user
    ):

        rbac_filter = get_rbac_filter(
            role,
            user,
            "devices",
            self.db
        )


        vehicles = list(

            self.db["devices"].find({

                "$and":[

                    rbac_filter,

                    {
                        "branchId":
                        self._convert_branch_id(branch_id)
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
                v.get("category"),

                "totalKm":
                v.get(
                    "TotalKmOfDevice",
                    0
                )

            }

            for v in vehicles

        ]



    def get_branch_vehicle_count(
        self,
        branch_id,
        role,
        user
    ):

        rbac_filter = get_rbac_filter(
            role,
            user,
            "devices",
            self.db
        )


        return self.db["devices"].count_documents({

            "$and":[

                rbac_filter,

                {

                    "branchId":
                    self._convert_branch_id(branch_id)

                }

            ]

        })



    # ====================================
    # DRIVERS
    # ====================================

    def get_branch_drivers(
        self,
        branch_id,
        role,
        user
    ):

        rbac_filter = get_rbac_filter(
            role,
            user,
            "drivers",
            self.db
        )


        drivers=list(

            self.db["drivers"].find({

                "$and":[

                    rbac_filter,

                    {

                        "branchId":
                        self._convert_branch_id(branch_id)

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



    def get_branch_driver_count(
        self,
        branch_id,
        role,
        user
    ):

        rbac_filter = get_rbac_filter(
            role,
            user,
            "drivers",
            self.db
        )


        return self.db["drivers"].count_documents({

            "$and":[

                rbac_filter,

                {

                    "branchId":
                    self._convert_branch_id(branch_id)

                }

            ]

        })



    # ====================================
    # ROUTES
    # ====================================

    def get_branch_routes(
        self,
        branch_id,
        role,
        user
    ):

        rbac_filter = get_rbac_filter(
            role,
            user,
            "routes",
            self.db
        )


        routes=list(

            self.db["routes"].find({

                "$and":[

                    rbac_filter,

                    {

                        "branchId":
                        self._convert_branch_id(branch_id)

                    }

                ]

            })

        )


        return [

            {

                "routeNumber":
                r.get("routeNumber"),

                "routeCompletionTime":
                r.get("routeCompletionTime")

            }

            for r in routes

        ]



    # ====================================
    # GEOFENCES
    # ====================================

    def get_branch_geofences(
        self,
        branch_id,
        role,
        user
    ):

        rbac_filter = get_rbac_filter(
            role,
            user,
            "geofences",
            self.db
        )


        geofences=list(

            self.db["geofences"].find({

                "$and":[

                    rbac_filter,

                    {

                        "branchId":
                        self._convert_branch_id(branch_id)

                    }

                ]

            })

        )


        return [

            {

                "name":
                g.get("geofenceName"),

                "address":
                g.get("address")

            }

            for g in geofences

        ]



    # ====================================
    # TICKETS
    # ====================================

    def get_branch_tickets(
        self,
        branch_id,
        role,
        user
    ):

        rbac_filter = get_rbac_filter(
            role,
            user,
            "tickets",
            self.db
        )


        return self.db["tickets"].count_documents({

            "$and":[

                rbac_filter,

                {

                    "branchId":
                    self._convert_branch_id(branch_id)

                }

            ]

        })



    # ====================================
    # DASHBOARD
    # ====================================

    def get_branch_dashboard(
        self,
        branch_id,
        role,
        user
    ):

        return {

            "vehicle_count":
            self.get_branch_vehicle_count(
                branch_id,
                role,
                user
            ),


            "driver_count":
            self.get_branch_driver_count(
                branch_id,
                role,
                user
            ),


            "route_count":
            len(
                self.get_branch_routes(
                    branch_id,
                    role,
                    user
                )
            ),


            "geofence_count":
            len(
                self.get_branch_geofences(
                    branch_id,
                    role,
                    user
                )
            ),


            "ticket_count":
            self.get_branch_tickets(
                branch_id,
                role,
                user
            )

        }



    # ====================================
    # COMPLETE DETAILS
    # ====================================

    def get_branch_details(
        self,
        branch_id,
        role,
        user
    ):

        return {

            "profile":
            self.get_branch_profile(
                branch_id,
                role,
                user
            ),


            "vehicles":
            self.get_branch_vehicles(
                branch_id,
                role,
                user
            ),


            "drivers":
            self.get_branch_drivers(
                branch_id,
                role,
                user
            ),


            "routes":
            self.get_branch_routes(
                branch_id,
                role,
                user
            ),


            "geofences":
            self.get_branch_geofences(
                branch_id,
                role,
                user
            ),


            "dashboard":
            self.get_branch_dashboard(
                branch_id,
                role,
                user
            )

        }
    
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
    # =====================================
# BRANCH VEHICLE DAILY KM REPORT
# =====================================

    def get_branch_distance_report_per_day(
    self,
    branch_id,
    unique_id,
    report_date,
    role,
    user,
    limit=100
):

    # Step 1: Get allowed devices under branch
        devices = self.get_allowed_devices(
        role,
        user,
        self.id_filter("branchId", branch_id)
    )

    # Step 2: Collect valid unique IDs
        allowed_unique_ids = []

        for d in devices:
            uid = d.get("uniqueId")
            if uid:
                allowed_unique_ids.extend(
                self.normalize_unique_id(uid)
            )

        if not allowed_unique_ids:
            return []

    # Step 3: Normalize vehicle filter
        vehicle_ids = self.normalize_unique_id(unique_id)

    # Step 4: Build report filter
        report_filter = get_rbac_filter(
        role,
        user,
        "report_distances",
        self.db
    )

    # Step 5: Query (DATE + VEHICLE + RBAC + BRANCH devices)
        query = {
        "$and": [
            report_filter,
            {
                "uniqueId": {
                    "$in": vehicle_ids
                }
            },
            {
                "uniqueId": {
                    "$in": allowed_unique_ids
                }
            },
            {
                "date": report_date   # IMPORTANT: your DB must store "date"
            }
        ]
    }

        reports = list(
        self.db["report_distances"]
        .find(query)
        .sort("createdAt", -1)
        .limit(limit)
    )

        return [
            self.clean(r)
            for r in reports
    ]
    
    

    def find_branch_superadmin(
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
                "message": "Only Superadmin can access all branch profiles."
            }

            branches = list(
            self.db["branches"].find()
        )

            result = []

            for branch in branches:

            # =====================================
            # DECRYPT PASSWORD
            # =====================================

                password = self.decrypt_password(
                branch.get("password")
            )

                result.append({

                "branchId": str(
                    branch.get("_id")
                ),

                "branchName": (
                    branch.get("branchName")
                    or branch.get("name")
                ),

                "username": branch.get(
                    "username"
                ),

                "password": password,

                "email": branch.get(
                    "email"
                ),

                "mobileNo": branch.get(
                    "mobileNo"
                ),

                "schoolId": (
                    str(branch.get("schoolId"))
                    if branch.get("schoolId")
                    else None
                ),

                "role": branch.get(
                    "role"
                ),

                "active": branch.get(
                    "Active"
                ),

                # "assignedCompany": (
                #     branch.get(
                #         "access",
                #         {}
                #     ).get(
                #         "assignedCompany"
                #     )
                # ),

                "createdAt": branch.get(
                    "createdAt"
                ),

                "updatedAt": branch.get(
                    "updatedAt"
                )

            })

            return {

            "success": True,

            "count": len(result),

            "branches": result

        }

        except Exception as e:

            return {

            "success": False,

            "error": str(e)

        }
    
    def find_specific_branch_superadmin(self, role, user, input_value=None):

        branch_name = str(input_value or "").strip()

    # RBAC FILTER
        if role.lower() == "superadmin":
            base_filter = {}
        else:
            base_filter = get_rbac_filter(
            role,
            user,
            "branches",
            self.db
        ) or {}

        branch = None

    # -------------------------
    # 1. OBJECTID MATCH
    # -------------------------
        if ObjectId.is_valid(branch_name):
            branch = self.db["branches"].find_one({
            "$and": [
                base_filter,
                {"_id": ObjectId(branch_name)}
            ]
        })

    # -------------------------
    # 2. NAME MATCH
    # -------------------------
        if not branch:

            regex = re.compile(re.escape(branch_name), re.IGNORECASE)

            branch = self.db["branches"].find_one({
            "$and": [
                base_filter,
                {
                    "$or": [
                        {"branchName": regex},
                        {"name": regex}
                    ]
                }
            ]
        })

        return branch