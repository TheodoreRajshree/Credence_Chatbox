# school_device_engine.py

from bson import ObjectId
from rbac import get_rbac_filter
import re
from school_engine import SchoolEngine
from device_engine import DeviceEngine
from vehicle_km_engine import VehicleKmEngine


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
    school_name,
    branch_name,
    role,
    user
):

    # =====================================
    # RBAC Filter
    # =====================================
        school_filter = get_rbac_filter(
        role,
        user,
        "schools",
        self.db
    ) 
        print("school_name =", school_name)
        print("branch_name =", branch_name)

    # =====================================
    # Find School
    # =====================================
        school = self.db["schools"].find_one({

        "$and": [

            school_filter,

            {
                "$or": [

                    {
                        "schoolName": {
                            "$regex": f"^{re.escape(str(school_name))}$",
                            "$options": "i"
                        }
                    },

                    {
                        "username": {
                            "$regex": f"^{re.escape(str(school_name))}$",
                            "$options": "i"
                        }
                    },

                    {
                        "_id": ObjectId(str(school_name))
                    } if ObjectId.is_valid(str(school_name)) else {
                        "schoolName": "__NO_MATCH__"
                    }

                ]
            }

        ]

    })

        if not school:
            return {
            "success": False,
            "message": f"School '{school_name}' not found."
        }

        school_id = school["_id"]

    # =====================================
    # RBAC Branch Filter
    # =====================================
        branch_filter = get_rbac_filter(
        role,
        user,
        "branches",
        self.db
    )

    # =====================================
    # Find Branch
    # =====================================
        branch = self.db["branches"].find_one({

        "$and": [

            branch_filter,

            {
                "$or": [
                    {"schoolId": school_id},
                    {"schoolId": str(school_id)}
                ]
            },

            {
                "$or": [

                    {
                        "branchName": {
                            "$regex": f"^{re.escape(str(branch_name))}$",
                            "$options": "i"
                        }
                    },

                    {
                        "username": {
                            "$regex": f"^{re.escape(str(branch_name))}$",
                            "$options": "i"
                        }
                    },

                    {
                        "_id": ObjectId(str(branch_name))
                    } if ObjectId.is_valid(str(branch_name)) else {
                        "branchName": "__NO_MATCH__"
                    }

                ]
            }

        ]

    })

        if not branch:
            return {
            "success": False,
            "message": f"Branch '{branch_name}' not found in school '{school_name}'."
        }

        return {

        "success": True,

        "school": {

            "schoolId": str(school["_id"]),
            "schoolName": school.get("schoolName"),
            "username": school.get("username"),
            "email": school.get("email"),
           
           
            "createdAt": school.get("createdAt")

        },

        "branch": {

            "branchId": str(branch["_id"]),
            "branchName": branch.get("branchName"),
            "username": branch.get("username"),
            "email": branch.get("email"),
           
            "createdAt": branch.get("createdAt")

        }

    }