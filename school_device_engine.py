# school_device_engine.py

from bson import ObjectId
from rbac import get_rbac_filter
import re
from school_engine import SchoolEngine
from device_engine import DeviceEngine
from vehicle_km_engine import VehicleKmEngine
import re
from bson import ObjectId

class SchoolDeviceEngine:

    def __init__(self, db):
        self.db = db
        self.school_engine = SchoolEngine(db)
        self.device_engine = DeviceEngine(db)
        self.vehicle_km_engine = VehicleKmEngine(db)


    # =====================================================
    # OBJECT ID HELPER
    # =====================================================

    def convert_id(self, value):

        try:
            return ObjectId(value)

        except:
            return value



    # =====================================================
    # GET ALLOWED DEVICES
    # =====================================================

    def get_allowed_devices(
        self,
        role,
        user,
        extra_filter=None
    ):

        device_filter = get_rbac_filter(
            role,
            user,
            "devices",
            self.db
        )


        if extra_filter:

            query = {

                "$and":[

                    device_filter,

                    extra_filter

                ]

            }

        else:

            query = device_filter


        return list(

            self.db["devices"].find(query)

        )



    # =====================================================
    # FIND SCHOOL
    # =====================================================

    def find_school(
        self,
        school_name,
        role,
        user
    ):


        school_filter = get_rbac_filter(

            role,
            user,
            "schools",
            self.db

        )


        school = self.db["schools"].find_one({

            "$and":[

                school_filter,

                {
                    "$or":[

                        {
                            "schoolName":{
                                "$regex":
                                school_name,
                                "$options":
                                "i"
                            }
                        },

                        {
                            "username":{
                                "$regex":
                                school_name,
                                "$options":
                                "i"
                            }
                        }

                    ]
                }

            ]

        })


        return school



    # =====================================================
    # GET SCHOOL + VEHICLES
    # =====================================================

    def get_school_with_vehicles(
        self,
        school_name,
        role,
        user
    ):


        school = self.find_school(

            school_name,

            role,

            user

        )


        if not school:

            return {

                "success":False,

                "message":
                f"School '{school_name}' not found"

            }


        school_id = school["_id"]


        devices = self.get_allowed_devices(

            role,

            user,

            {

                "$or":[

                    {
                        "schoolId":
                        school_id
                    },

                    {
                        "schoolId":
                        str(school_id)
                    }

                ]

            }

        )


        vehicle_list=[]


        for device in devices:


            vehicle_name=(

                device.get("vehicleNumber")

                or device.get("vehicle_name")

                or device.get("name")

                or device.get("uniqueId")

                or ""

            )


            km_report=None


            if vehicle_name:

                try:

                    km_report = self.vehicle_km_engine.get_km_report(
    device.get("uniqueId"),
    "",
    role,
    user
)

                except:

                    km_report=None



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

                "imei":
                device.get("imei"),

                "simNumber":
                device.get("simNumber"),

                "protocol":
                device.get("protocol"),

                "lastUpdate":
                str(
                    device.get(
                        "lastUpdate"
                    )
                ),

                "kmReport":
                km_report

            })


        return {

            "success":True,

            "school":{

                "schoolId":
                str(school["_id"]),

                "schoolName":
                school.get("schoolName"),

                "username":
                school.get("username"),

                "email":
                school.get("email"),

                "mobileNo":
                school.get("mobileNo"),

                "assignedCompany":
                school.get(
                    "assignedCompany"
                ),

                "active":
                school.get("Active")

            },

            "totalVehicles":
            len(vehicle_list),

            "vehicles":
            vehicle_list

        }



    # =====================================================
    # GET SCHOOL DEVICES
    # =====================================================

    def get_school_devices(
        self,
        school_id,
        role,
        user
    ):


        school_id_obj = self.convert_id(
            school_id
        )


        devices = self.get_allowed_devices(

            role,

            user,

            {

                "$or":[

                    {
                        "schoolId":
                        school_id_obj
                    },

                    {
                        "schoolId":
                        str(school_id_obj)
                    }

                ]

            }

        )


        return {

            "schoolId":
            str(school_id),

            "totalDevices":
            len(devices),

            "devices":[

                self.clean(d)

                for d in devices

            ]

        }



    # =====================================================
    # DEVICE SUMMARY
    # =====================================================

    def get_school_device_summary(
        self,
        school_id,
        role,
        user
    ):


        devices = self.get_school_devices(

            school_id,

            role,

            user

        )


        all_devices = devices["devices"]


        active = len([

            d for d in all_devices

            if d.get("status")=="active"

        ])


        inactive = len([

            d for d in all_devices

            if d.get("status")=="inactive"

        ])


        return {

            "schoolId":
            str(school_id),

            "totalDevices":
            len(all_devices),

            "activeDevices":
            active,

            "inactiveDevices":
            inactive

        }



    # =====================================================
    # DASHBOARD
    # =====================================================

    def get_school_dashboard(
        self,
        school_name,
        role,
        user
    ):


        school=self.find_school(

            school_name,

            role,

            user

        )


        if not school:
            return None


        school_id=school["_id"]


        return {

            "schoolName":
            school.get(
                "schoolName"
            ),

            "vehicleCount":
            self.school_engine
            .get_school_vehicle_count(

                school_id,

                role,

                user

            ),


            "driverCount":
            self.school_engine
            .get_school_driver_count(

                school_id,

                role,

                user

            ),


            "routeCount":
            len(

                self.school_engine
                .get_school_routes(

                    school_id,

                    role,

                    user

                )

            ),


            "geofenceCount":
            len(

                self.school_engine
                .get_school_geofences(

                    school_id,

                    role,

                    user

                )

            )

        }



    # =====================================================
    # CLEAN
    # =====================================================

    def clean(self, doc):

        if not doc:
            return doc


        cleaned={}


        for key,value in doc.items():

            if isinstance(value,ObjectId):

                cleaned[key]=str(value)

            else:

                cleaned[key]=value


        return cleaned
#     def get_school_with_branches_final(
#     self,
#     role,
#     user
# ):

#     # ==========================================
#     # Logged-in School
#     # ==========================================

#         school_id = user.get("schoolId")

#         if not school_id:
#             return {
#             "success": False,
#             "message": "School not found."
#         }

#     # ==========================================
#     # Find School
#     # ==========================================

#         school = None

#         if ObjectId.is_valid(str(school_id)):
#             school = self.db["schools"].find_one({
#             "_id": ObjectId(str(school_id))
#         })

#         if not school:
#             school = self.db["schools"].find_one({
#             "_id": school_id
#         })

#         if not school:
#             return {
#             "success": False,
#             "message": "Invalid school."
#         }

#     # ==========================================
#     # RBAC
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
#                             "schoolId": school["_id"]
#                         },
#                         {
#                             "schoolId": str(school["_id"])
#                         }
#                     ]
#                 }
#             ]
#         })
#     )

#     # ==========================================
#     # Branch List
#     # ==========================================

#         branch_list = []

#         for branch in branches:

#             branch_list.append({

#             "branchId": str(branch.get("_id")),

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
     


    
   
 
    
    
    


    def get_school_single_branch(
    self,
    branch_name,
    role,
    user
):
        try:

        # =====================================
        # VALIDATE BRANCH NAME
        # =====================================

            if branch_name is None:
                return {
                "success": False,
                "message": "Branch name is required."
            }

            def normalize(text):
                return re.sub(r"\s+", "", str(text or "")).lower()

            normalized_input = normalize(branch_name)

            if not normalized_input:
                return {
                "success": False,
                "message": "Branch name is required."
            }

            print("NORMALIZED INPUT =", normalized_input)

        # =====================================
        # GET SCHOOL ID
        # =====================================

            school_id = (
            user.get("schoolId")
            or user.get("id")
            or user.get("_id")
        )

            if not school_id:
                return {
                "success": False,
                "message": "School ID not found in user."
            }

        # =====================================
        # NORMALIZE SCHOOL ID
        # =====================================

            school_ids = []

            try:
                school_ids.append(ObjectId(str(school_id)))
            except Exception:
                pass

            school_ids.append(str(school_id))

        # =====================================
        # FETCH BRANCHES OF THIS SCHOOL
        # =====================================

            branches = self.db["branches"].find({
            "schoolId": {
                "$in": school_ids
            }
        })

            branch = None

            for b in branches:

                db_branch = normalize(b.get("branchName"))
                db_username = normalize(b.get("username"))

                if (
                    db_branch == normalized_input or
                    db_username == normalized_input
            ):
                    branch = b
                    break

            if not branch:
                return {
                "success": False,
                "message": f"Branch '{branch_name}' not found under this school."
            }

        # =====================================
        # RETURN BRANCH
        # =====================================

            return {
            "success": True,
            "branch": {
                "branchId": str(branch["_id"]),
                "branchName": branch.get("branchName"),
                "username": branch.get("username"),
                "email": branch.get("email"),
                "mobileNo": branch.get("mobileNo"),
                "schoolId": str(branch.get("schoolId")) if branch.get("schoolId") else None,
                "active": branch.get("Active"),
                "createdAt": branch.get("createdAt")
            }
        }

        except Exception as e:
            print("ERROR get_school_single_branch =", repr(e))
            return {
            "success": False,
            "error": str(e)
        }
            
    def get_school_all_branches(
    self,
    role,
    user
):

    # =====================================
    # GET SCHOOL ID FROM LOGIN USER
    # =====================================

        school_id = user.get("schoolId")

        if not school_id:
            return {
            "success": False,
            "message": "School ID not found."
        }

    # =====================================
    # FIND SCHOOL
    # =====================================

        school = self.db["schools"].find_one({
        "_id": ObjectId(school_id)
    })

        if not school:
            return {
            "success": False,
            "message": "School not found."
        }

    # =====================================
    # RBAC FILTER
    # =====================================

        branch_filter = get_rbac_filter(
        role,
        user,
        "branches",
        self.db
    ) or {}

    # =====================================
    # GET ALL BRANCHES OF SCHOOL
    # =====================================

        branches = list(
        self.db["branches"].find({

            "$and": [

                branch_filter,

                {
                    "$or": [
                        {"schoolId": ObjectId(school_id)},
                        {"schoolId": school_id}
                    ]
                }

            ]

        })
    )

        if not branches:
            return {
            "success": False,
            "message": "No branches found."
        }

        result = []

        for branch in branches:

            result.append({

            "branchId": str(branch["_id"]),
            "branchName": branch.get("branchName"),
            "username": branch.get("username"),
            "email": branch.get("email"),
            "mobileNo": branch.get("mobileNo"),
            "createdAt": branch.get("createdAt")

        })

        return {

        "success": True,

        "school": {

            "schoolId": str(school["_id"]),
            "schoolName": school.get("schoolName")

        },

        "count": len(result),

        "branches": result

    }
    def get_school_all_branch_devices(
    self,
    role,
    user
):

    # =====================================
    # GET SCHOOL ID FROM LOGIN USER
    # =====================================

        school_id = user.get("schoolId")

        if not school_id:
            return {
            "success": False,
            "message": "School ID not found."
        }

        school_id_obj = self.convert_id(school_id)

    # =====================================
    # GET ALL BRANCHES OF SCHOOL
    # =====================================

        branches = list(
        self.db["branches"].find({
            "$or": [
                {"schoolId": school_id_obj},
                {"schoolId": str(school_id_obj)}
            ]
        })
    )

        if not branches:
            return {
            "success": False,
            "message": "No branches found for this school."
        }

        branch_ids = [
        branch["_id"]
        for branch in branches
    ]

    # =====================================
    # GET ALL DEVICES OF ALL BRANCHES
    # =====================================

        devices = self.get_allowed_devices(

        role,

        user,

        {
            "$or": [
                {
                    "branchId": {
                        "$in": branch_ids
                    }
                },
                {
                    "branchId": {
                        "$in": [str(i) for i in branch_ids]
                    }
                }
            ]
        }

    )

    # =====================================
    # RESPONSE
    # =====================================

        return {

        "success": True,

        "schoolId": str(school_id),

        "totalBranches": len(branches),

        "totalDevices": len(devices),

        "devices": [
    {
        key: value
        for key, value in self.clean(device).items()
        if key not in [
            "positionId",
            "parkingMode",
            "toeingMode",
            "keyFeature",
            "TD",
            "TDTime",
            "schoolId",
            "branchId",
            "__v",
            "createdAt",
            "updatedAt",
            "installationdate",
            "TotalKmOfDevice",
            "expirationdate"
        ]
    }
    for device in devices
]
        

    }
    import re

    def get_school_specific_branch_vehicle(
    self,
    branch_name,
    vehicle_input,
    role,
    user
):

    # =====================================
    # NORMALIZE FUNCTION
    # =====================================

        def normalize(text):
            return re.sub(r"\s+", "", str(text or "")).lower()

        branch_input = normalize(branch_name)
        vehicle_input = normalize(vehicle_input)

    # =====================================
    # GET LOGIN SCHOOL
    # =====================================

        school_id = user.get("schoolId")

        if not school_id:
            return {
            "success": False,
            "message": "School not found."
        }

        school_id = self.convert_id(school_id)

    # =====================================
    # FIND BRANCH OF LOGIN SCHOOL
    # =====================================

        branches = self.db["branches"].find({
        "$or": [
            {"schoolId": school_id},
            {"schoolId": str(school_id)}
        ]
    })

        branch = None

        for b in branches:
            if (
            normalize(b.get("branchName")) == branch_input or
            normalize(b.get("username")) == branch_input
        ):
                branch = b
                break

        if not branch:
            return {
            "success": False,
            "message": "Branch not found under this school."
        }

        branch_id = branch["_id"]

    # =====================================
    # FIND VEHICLE
    # =====================================

        devices = self.db["devices"].find({
        "$and": [
            get_rbac_filter(
                role,
                user,
                "devices",
                self.db
            ),
            {
                "$or": [
                    {"branchId": branch_id},
                    {"branchId": str(branch_id)}
                ]
            }
        ]
    })

        device = None

        for d in devices:

            vehicle_number = normalize(d.get("vehicleNumber"))
            vehicle_name = normalize(d.get("vehicleName"))
            name = normalize(d.get("name"))
            unique_id = normalize(d.get("uniqueId"))

            if (
            vehicle_input == vehicle_number or
            vehicle_input == vehicle_name or
            vehicle_input == name or
            vehicle_input == unique_id
        ):
                device = d
                break

        if not device:
            return {
            "success": False,
            "message": "Vehicle not found in this branch."
        }

        return {
    "success": True,
    # "school": {
    #     "schoolId": str(school_id)
        
    # },
    "branch": {
        # "branchId": str(branch["_id"]),
        "branchName": branch.get("branchName")
    },
    "vehicle": {
        "vehicleName": (
            device.get("vehicleNumber")
            or device.get("vehicleName")
            or device.get("name")
            or device.get("uniqueId")
        ),
        "deviceId": device.get("deviceId"),
        "uniqueId": device.get("uniqueId"),
        "status": device.get("status"),
        "model": device.get("model"),
        "category": device.get("category"),
        "speed": device.get("speed")
    }
}
    from bson import ObjectId

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

        try:
            school_id = ObjectId(str(school_id))
        except:
            return {
            "success": False,
            "message": "Invalid School ID."
        }

        school = self.db["schools"].find_one({
        "_id": school_id
    })

        if not school:
            return {
            "success": False,
            "message": "School not found."
        }

    # =====================================
    # 2. Find Vehicle from Branch
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

        "school": {
            "schoolId": str(school["_id"]),
            "schoolName": school.get("schoolName"),
            "username": school.get("username"),
            "email": school.get("email")
        },

        "branch": result["branch"],

        "vehicle": {
            "vehicleName": vehicle.get("vehicleName"),
            "deviceId": vehicle.get("deviceId"),
            "uniqueId": vehicle.get("uniqueId"),
            "status": vehicle.get("status"),
            "category": vehicle.get("category"),
            "model": vehicle.get("model")
        },

        "statusReport": [
            self.clean(report)
            for report in reports
        ]
    }
    def get_school_all_branch_vehicle_status_reports(
    self,
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
        "_id": self.convert_id(school_id)
    })

        if not school:
            return {
            "success": False,
            "message": "School not found."
        }

    # =====================================
    # Get all branches of school
    # =====================================
        branches = list(
        self.db["branches"].find({
            "$or": [
                {"schoolId": school["_id"]},
                {"schoolId": str(school["_id"])}
            ]
        })
    )

        if not branches:
            return {
            "success": False,
            "message": "No branches found."
        }

        branch_ids = []

        for b in branches:
            branch_ids.append(b["_id"])
            branch_ids.append(str(b["_id"]))

    # =====================================
    # Get all vehicles of all branches
    # =====================================
        devices = list(
        self.db["devices"].find({
            "$and": [
                get_rbac_filter(
                    role,
                    user,
                    "devices",
                    self.db
                ),
                {
                    "branchId": {
                        "$in": branch_ids
                    }
                }
            ]
        })
    )

        if not devices:
            return {
            "success": False,
            "message": "No vehicles found."
        }

        unique_ids = []

        for d in devices:
            unique_ids.extend(
            self.vehicle_km_engine.normalize_unique_id(
                d.get("uniqueId")
            )
        )

    # Remove duplicates
        unique_ids = list(set(unique_ids))

    # =====================================
    # Fetch Status Reports
    # =====================================
        reports = list(
        self.db["report_statuses"]
        .find({
            "$and": [
                get_rbac_filter(
                    role,
                    user,
                    "report_statuses",
                    self.db
                ),
                {
                    "uniqueId": {
                        "$in": unique_ids
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
            "schoolName": school.get("schoolName")
        },
        "totalBranches": len(branches),
        "totalVehicles": len(devices),
        "totalReports": len(reports),
        "statusReports": [
            self.clean(r)
            for r in reports
        ]
    }