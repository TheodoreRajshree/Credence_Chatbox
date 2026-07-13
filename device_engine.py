from bson import ObjectId
from rbac import get_rbac_filter
import re
from unique_id import normalize_unique_id
from datetime import datetime, timedelta, timezone
import re
class DeviceEngine:

    def __init__(self, db):
        self.db = db

    # ==========================================
    # FIND DEVICE BY NAME
    # ==========================================
     
    def find_device(self, text, role, user):

        text = text.strip().lower()

        rbac_filter = get_rbac_filter(
            role,
            user,
            "devices",
            self.db
        )

        regex = re.compile(re.escape(text), re.IGNORECASE)

        pipeline = [
            {
                "$match": rbac_filter
            },
            {
                "$match": {
                    "$or": [
                        {"name": regex},
                        {"uniqueId": text}
                    ]
                }
            },
            {
                "$lookup": {
                    "from": "schools",
                    "localField": "schoolId",
                    "foreignField": "_id",
                    "as": "school"
                }
            },
            {
                "$lookup": {
                    "from": "branches",
                    "localField": "branchId",
                    "foreignField": "_id",
                    "as": "branch"
                }
            },
            {
                "$unwind": {
                    "path": "$school",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$unwind": {
                    "path": "$branch",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$limit": 1
            }
        ]

        result = list(self.db["devices"].aggregate(pipeline))

        return result[0] if result else None

    # ==========================================
    # DEVICE DETAILS
    # ==========================================

    # def get_device_details(self, device):

    #     if not device:
    #         return None

    #     school = None
    #     branch = None

    #     if device.get("schoolId"):
    #         school = self.db["schools"].find_one(
    #         {"_id": device.get("schoolId")}
    #     )

    #     if device.get("branchId"):
    #         branch = self.db["branches"].find_one(
    #         {"_id": device.get("branchId")}
    #     )

    #     return {
    #     "deviceId": str(device["_id"]),
    #     "vehicleName": device.get("name"),
    #     "uniqueId": device.get("uniqueId"),
    #     "sim": device.get("sim"),
    #     "model": device.get("model"),
    #     "category": device.get("category"),
    #     "status": device.get("status"),
    #     "speed": device.get("speed"),
    #     "average": device.get("average"),

    #     # totalKm removed

    #     "installationDate": device.get("installationdate"),
    #     "expirationDate": device.get("expirationdate"),

    #     "schoolId": str(device.get("schoolId")) if device.get("schoolId") else None,
    #     "schoolName": school.get("schoolName") if school else None,

    #     "branchId": str(device.get("branchId")) if device.get("branchId") else None,
    #     "branchName": branch.get("branchName") if branch else None
    # }

    def get_device_details(self,device):

        pipeline = [
        {
            "$match": {
                "_id": device["_id"]
            }
        },
        {
            "$lookup": {
                "from": "schools",
                "localField": "schoolId",
                "foreignField": "_id",
                "as": "school"
            }
        },
        {
            "$lookup": {
                "from": "branches",
                "localField": "branchId",
                "foreignField": "_id",
                "as": "branch"
            }
        },
        {
            "$unwind": {
                "path": "$school",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$unwind": {
                "path": "$branch",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$project": {
                "_id": 0,
                "deviceId": {
                    "$toString": "$_id"
                },
                "vehicleName": "$name",
                "uniqueId": 1,
                "sim": 1,
                "model": 1,
                "category": 1,
                "status": 1,
                "speed": 1,
                "average": 1,
                "installationDate": "$installationdate",
                "expirationDate": "$expirationdate",
                "schoolId": {
                    "$cond": [
                        {
                            "$ifNull": [
                                "$schoolId",
                                False
                            ]
                        },
                        {
                            "$toString": "$schoolId"
                        },
                        None
                    ]
                },
                "schoolName": "$school.schoolName",
                "branchId": {
                    "$cond": [
                        {
                            "$ifNull": [
                                "$branchId",
                                False
                            ]
                        },
                        {
                            "$toString": "$branchId"
                        },
                        None
                    ]
                },
                "branchName": "$branch.branchName"
            }
        }
    ]

        return list(self.db["devices"].aggregate(pipeline))
    
    # def get_superadmin_vehicle_details(self, role, user, vehicle_input=None):

    #     if isinstance(vehicle_input, dict):
    #         vehicle_input = vehicle_input.get("vehicle_input")

    #     if not vehicle_input:
    #         return None

    #     vehicle_input = vehicle_input.strip().lower()
    #     devices=self.db.devices.find({})

    #     matched = []

    #     for device in devices:

    #             name = (device.get("name") or "").strip().lower()
    #             unique_id = str(device.get("uniqueId") or "").strip().lower()

    #     # match by vehicle name OR uniqueId
    #             if vehicle_input in name or vehicle_input == unique_id:

    #                 matched.append({
    #             "deviceId": str(device["_id"]),
    #             "vehicleName": device.get("name"),
    #             "uniqueId": device.get("uniqueId"),
    #             "sim": device.get("sim"),
    #             "model": device.get("model"),
    #             "category": device.get("category"),
    #             "status": device.get("status"),
    #             "speed": device.get("speed"),
    #             "average": device.get("average"),
    #             # "totalKm": device.get("TotalKmOfDevice"),
    #             "installationDate": device.get("installationdate"),
    #             "expirationDate": device.get("expirationdate"),
    #             # "schoolId": str(device.get("schoolId")) if device.get("schoolId") else None,
    #             # "branchId": str(device.get("branchId")) if device.get("branchId") else None
    #             "schoolName": self.db["schools"].find_one(
    #             {"_id": device.get("schoolId")},
    #             {"schoolName": 1}
    #             ).get("schoolName") if device.get("schoolId") else None,

    #             "branchName": self.db["branches"].find_one(
    #             {"_id": device.get("branchId")},
    #             {"branchName": 1}
    #             ).get("branchName") if device.get("branchId") else None,
    #         })

    #     return matched  if matched else None
    def get_superadmin_vehicle_details(self, role, user, vehicle_input=None):

        if isinstance(vehicle_input, dict):
            vehicle_input = vehicle_input.get("vehicle_input")

        if not vehicle_input:
            return None

        vehicle_input = vehicle_input.strip().lower()

        devices = self.db["devices"].find({})

        matched = []

        for device in devices:

            name = (device.get("name") or "").strip().lower()
            unique_id = str(device.get("uniqueId") or "").strip().lower()

        # Match by vehicle name or uniqueId
            if vehicle_input in name or vehicle_input == unique_id:

            # Get latest history for total distance
                history = self.db["histories"].find_one(
                {
                    "uniqueId": {
                        "$in": self.normalize_unique_id(
                            device.get("uniqueId")
                        )
                    },
                    "attributes.totalDistance": {
                        "$ne": None
                    }
                },
                sort=[("createdAt", -1)]
            )

                total_km = (
                round(
                    history.get("attributes", {}).get("totalDistance", 0) / 1000,
                    2
                )
                if history else 0
            )

                school = (
                self.db["schools"].find_one(
                    {"_id": device.get("schoolId")},
                    {"schoolName": 1}
                )
                if device.get("schoolId")
                else None
            )

                branch = (
                self.db["branches"].find_one(
                    {"_id": device.get("branchId")},
                    {"branchName": 1}
                )
                if device.get("branchId")
                else None
            )

                matched.append({

                "deviceId": str(device["_id"]),
                
                
                "vehicleName": device.get("name"),
                "uniqueId": device.get("uniqueId"),
                "sim": device.get("sim"),
                "model": device.get("model"),
                "category": device.get("category"),
                "status": device.get("status"),
                "speed": device.get("speed"),
                "average": device.get("average"),

                # Latest total distance (KM)
                "todayKm": total_km,

                "installationDate": device.get("installationdate"),
                "expirationDate": device.get("expirationdate"),

                "schoolName": school.get("schoolName") if school else None,
                "branchName": branch.get("branchName") if branch else None,
            })

        return matched if matched else None
    # ==========================================
    # ALL DEVICES
    # ==========================================

    def get_all_devices(self, role, user):

        rbac_filter = get_rbac_filter(
            role,
            user,
            "devices",
            self.db
        )
        
        pipeline = [
        {
            "$match": rbac_filter
        },
        {
            "$lookup": {
                "from": "schools",
                "localField": "schoolId",
                "foreignField": "_id",
                "as": "school"
            }
        },
        {
            "$lookup": {
                "from": "branches",
                "localField": "branchId",
                "foreignField": "_id",
                "as": "branch"
            }
        },
        {
            "$unwind": {
                "path": "$school",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$unwind": {
                "path": "$branch",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$project": {
                "_id": 0,
                # "deviceId": {
                #     "$toString": "$_id"
                # },
                "vehicleName": "$name",
                "uniqueId": 1,
                "sim": 1,
                "model": 1,
                "category": 1,
                # "status": 1,
                # "speed": 1,
                # "average": 1,
                # "installationDate": "$installationdate",
                "expirationDate": "$expirationdate",
                
                "schoolName": "$school.schoolName",
                # "branchId": {
                #     "$cond": [
                #         {
                #             "$ifNull": [
                #                 "$branchId",
                #                 False
                #             ]
                #         },
                #         {
                #             "$toString": "$branchId"
                #         },
                #         None
                #     ]
                # },
                "branchName": "$branch.branchName"
            }
        }
    ]


        return list(self.db.devices.aggregate(pipeline))


    # ==========================================
    # SCHOOL DEVICES
    # ==========================================

    def get_school_devices(self, school_id):

        devices = []

        rbac_filter = get_rbac_filter(
            "school",
            {"_id": ObjectId(str(school_id))},
            "devices",
            self.db
        )

        query = {
            "$and": [
                rbac_filter,
                {"schoolId": ObjectId(str(school_id))}
            ]
        }

        for d in self.db["devices"].find(query):
            devices.append(self.get_device_details(d))

        return devices

    # ==========================================
    # BRANCH DEVICES
    # ==========================================

    def get_branch_devices(self, branch_id):

        devices = []

        rbac_filter = get_rbac_filter(
            "branch",
            {"_id": ObjectId(str(branch_id))},
            "devices",
            self.db
        )

        query = {
            "$and": [
                rbac_filter,
                {"branchId": ObjectId(str(branch_id))}
            ]
        }

        for d in self.db["devices"].find(query):
            devices.append(self.get_device_details(d))

        return devices

    # ==========================================
    # DRIVER DEVICE
    # ==========================================

    def get_driver_device(self, username):

        driver = self.db["drivers"].find_one({
            "username": username
        })

        if not driver:
            return {}

        rbac_filter = get_rbac_filter(
            "driver",
            driver,
            "devices",
            self.db
        )

        device = self.db["devices"].find_one({
            "$and": [
                rbac_filter,
                {
                    "_id": driver.get("deviceObjId")
                }
            ]
        })

        return self.get_device_details(device)

    # ==========================================
    # LAST POSITION
    # ==========================================

    def get_last_position(self, unique_id, role, user):

        rbac_filter = get_rbac_filter(
            role,
            user,
            "vehiclelastpositions",
            self.db
        )

        query = {
            "$and": [
                rbac_filter,
                {
                    "$or": [
                        {"uniqueId": unique_id},
                        {"uniqueId": str(unique_id)}
                    ]
                }
            ]
        }

        position = self.db["vehiclelastpositions"].find_one(query)

        if not position:
            return {}

        return {
            "latitude": position.get("latitude"),
            "longitude": position.get("longitude"),
            "speed": position.get("speed"),
            "lastUpdate": position.get("lastUpdate"),
            "course": position.get("course")
        }

    # ==========================================
    # DEVICE SUMMARY
    # ==========================================
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
        
    }

        return {
        "success": True,
        "vehicle": vehicle
    }
    def get_device_summary(self, unique_id, role, user):

        distance_filter = get_rbac_filter(
            role,
            user,
            "report_distances",
            self.db
        )

        travel_filter = get_rbac_filter(
            role,
            user,
            "report_travelsummaries",
            self.db
        )

        trip_filter = get_rbac_filter(
            role,
            user,
            "report_trips",
            self.db
        )

        idle_filter = get_rbac_filter(
            role,
            user,
            "report_idles",
            self.db
        )

        distance = self.db["report_distances"].find_one({
            "$and": [
                distance_filter,
                {
 "uniqueId":{
    "$in": normalize_unique_id(unique_id)
 }
}
            ]
        })

        travel = self.db["report_travelsummaries"].find_one({
            "$and": [
                travel_filter,
                {"uniqueId": int(unique_id)}
            ]
        })

        trip = self.db["report_trips"].find_one({
            "$and": [
                trip_filter,
                {"uniqueId": int(unique_id)}
            ]
        })

        idle = self.db["report_idles"].find_one({
            "$and": [
                idle_filter,
                {"uniqueId": int(unique_id)}
            ]
        })

        return {
            "distance": distance,
            "travelSummary": travel,
            "trip": trip,
            "idle": idle
        }
    
    def get_all_branch_groups_profile(
    self,
    role,
    user
):

    # ====================================
    # STEP 1: SUPERADMIN ACCESS CHECK
    # ====================================

            if role != "superadmin":
                return {
            "success": False,
            "message": "Access denied"
        }


    # ====================================
    # STEP 2: FETCH ALL BRANCH GROUPS
    # ====================================

            groups = list(
            self.db["branchgroups"].find({})
    )


            if not groups:
                return {
            "success": False,
            "message": "No branch groups found"
        }


    # ====================================
    # STEP 3: FORMAT RESPONSE
    # ====================================

            profiles = []


            for group in groups:

                profiles.append({

            "groupId":
                str(group["_id"]),


            "branchGroupName":
                group.get("branchGroupName"),


            "schoolId":
                str(group.get("schoolId"))
                if group.get("schoolId")
                else None,


            "mobileNo":
                group.get("mobileNo"),


            "username":
                group.get("username"),


            "email":
                group.get("email"),


            "role":
                group.get("role"),


            "active":
                group.get("Active"),


            "access":
                group.get("access"),


            "notification":
                group.get("Notification"),


            "fcmToken":
                group.get("fcmToken"),


            "createdAt":
                group.get("createdAt")

        })


    # ====================================
    # STEP 4: RESPONSE
    # ====================================

            return {

        "success": True,

        "count": len(profiles),

        "profiles": profiles

    }
    
    def get_specific_branch_group_profile_1(
    self,
    role,
    user,
    input_value=None
):

    # ====================================
    # STEP 1: GET BRANCH GROUP NAME INPUT
    # ====================================

        if isinstance(input_value, dict):

            group_name = (
            input_value.get("group_name")
            or input_value.get("branchGroupName")
            or ""
        )

        else:

            group_name = input_value or ""


        group_name = str(group_name).strip()


        print("========== SPECIFIC BRANCH GROUP DEBUG ==========")
        print("GROUP SEARCH =", group_name)
        print("ROLE =", role)
        print("USER =", user)
        print("=================================================")


        if not group_name:

            return {

            "success": False,

            "message": "Please enter branch group name"

        }



    # ====================================
    # STEP 2: ROLE HANDLING
    # ====================================

        if isinstance(role, dict):

            role_name = role.get("role", "")

        else:

            role_name = role



    # ====================================
    # STEP 3: RBAC FILTER
    # ====================================

        if role_name.lower() == "superadmin":

            base_filter = {}

        else:

            base_filter = get_rbac_filter(
            role_name,
            user,
            "branchgroups",
            self.db
        ) or {}



        branchgroup = None



    # ====================================
    # STEP 4: OBJECT ID SEARCH
    # ====================================

        if ObjectId.is_valid(group_name):

            branchgroup = self.db["branchgroups"].find_one({

            "$and": [

                base_filter,

                {
                    "_id": ObjectId(group_name)
                }

            ]

        })



    # ====================================
    # STEP 5: NAME / USERNAME SEARCH
    # ====================================

        if not branchgroup:

            regex = re.compile(
            re.escape(group_name),
            re.IGNORECASE
        )


            branchgroup = self.db["branchgroups"].find_one({

            "$and": [

                base_filter,

                {

                    "$or": [

                        {
                            "branchGroupName": regex
                        },

                        {
                            "username": regex
                        }

                    ]

                }

            ]

        })



    # ====================================
    # STEP 6: NOT FOUND
    # ====================================

        if not branchgroup:

            return {

            "success": False,

            "message": "Branch group not found"

        }



    # ====================================
    # STEP 7: RESPONSE
    # ====================================

        return {

        "success": True,

        "profile": {

            "groupId":
                str(branchgroup["_id"]),


            "branchGroupName":
                branchgroup.get(
                    "branchGroupName"
                ),


            "schoolId":
                str(branchgroup.get("schoolId"))
                if branchgroup.get("schoolId")
                else None,


            "username":
                branchgroup.get(
                    "username"
                ),


            "mobileNo":
                branchgroup.get(
                    "mobileNo"
                ),


            "email":
                branchgroup.get(
                    "email"
                ),


            "role":
                branchgroup.get(
                    "role"
                ),


            "active":
                branchgroup.get(
                    "Active"
                ),


            "access":
                branchgroup.get(
                    "access"
                ),


            "notification":
                branchgroup.get(
                    "Notification"
                ),


            "createdAt":
                branchgroup.get(
                    "createdAt"
                )

        }

    }
    
    def get_specific_vehicle_last_position(
    self,
    role,
    user,
    vehicle_input=None
):


    # ====================================
    # STEP 1: VEHICLE INPUT
    # ====================================

        vehicle_name = str(vehicle_input or "").strip()


        if not vehicle_name:

            return {

            "success": False,

            "message": "Please enter vehicle name or unique ID"

        }



    # ====================================
    # STEP 2: POSITION FILTER
    # ====================================

        base_filter = self.get_position_filter(

        role,

        user

    )



    # ====================================
    # STEP 3: VEHICLE SEARCH
    # ====================================

        regex = re.compile(

        re.escape(vehicle_name),

        re.IGNORECASE

    )


        query = {

        "$and": [

            base_filter,

            {

                "$or": [

                    {
                        "name": regex
                    },

                    {
                        "uniqueId": regex
                    }

                ]

            }

        ]

    }



        vehicle = self.db["vehiclelastpositions"].find_one(

        query

    )



        if not vehicle:

            return {

            "success": False,

            "message": "Vehicle not found"

        }



    # ====================================
    # STEP 4: RESPONSE
    # ====================================

        return {

        "success": True,

        "vehicle": {

            "vehicleName":
                vehicle.get("name"),


            "uniqueId":
                vehicle.get("uniqueId"),


            "latitude":
                vehicle.get("latitude"),


            "longitude":
                vehicle.get("longitude"),


            "speed":
                vehicle.get("speed"),


            "lastUpdate":
                vehicle.get("lastUpdate")

        }

    }
    def get_specific_active_vehicle(
    self,
    role,
    user,
    vehicle_input=None
):


    # ====================================
    # STEP 1: VEHICLE INPUT
    # ====================================

        vehicle_name = str(vehicle_input or "").strip()


        if not vehicle_name:

            return {

            "success": False,

            "message": "Please enter vehicle name or unique ID"

        }



    # ====================================
    # STEP 2: SEARCH VEHICLE
    # ====================================

        regex = re.compile(

        re.escape(vehicle_name),

        re.IGNORECASE

    )


        vehicles = list(

        self.db["vehiclelastpositions"].find({

            "$and": [

                self.get_position_filter(

                    role,

                    user

                ),

                {

                    "speed": {

                        "$gt": 0

                    }

                },

                {

                    "$or": [

                        {

                            "name": regex

                        },

                        {

                            "uniqueId": regex

                        }

                    ]

                }

            ]

        })

    )



        if not vehicles:

            return {

            "success": False,

            "message": "Active vehicle not found"

        }



    # ====================================
    # STEP 3: RESPONSE
    # ====================================

        return {

        "success": True,

        "vehicles": [

            {

                "vehicleName":
                    v.get("name"),


                "uniqueId":
                    v.get("uniqueId"),


                "speed":
                    v.get("speed"),


                "latitude":
                    v.get("latitude"),


                "longitude":
                    v.get("longitude")

            }

                for v in vehicles

        ]

    }
    def get_position_filter(
        self,
        role,
        user
    ):

        return get_rbac_filter(

            role,

            user,

            "vehiclelastpositions",

            self.db

        )
    def get_specific_stopped_vehicle(
    self,
    role,
    user,
    vehicle_input=None
):

    # ====================================
    # STEP 1: VEHICLE INPUT
    # ====================================

        vehicle_name = str(vehicle_input or "").strip()


        if not vehicle_name:

            return {

            "success": False,

            "message": "Please enter vehicle name or unique ID"

        }


    # ====================================
    # STEP 2: SEARCH VEHICLE
    # ====================================

        regex = re.compile(

        re.escape(vehicle_name),

        re.IGNORECASE

    )


        vehicle = self.db["vehiclelastpositions"].find_one({

        "$and": [

            self.get_position_filter(

                role,

                user

            ),

            {

                "speed": 0

            },

            {

                "$or": [

                    {

                        "name": regex

                    },

                    {

                        "uniqueId": regex

                    }

                ]

            }

        ]

    })


        if not vehicle:

            return {

            "success": False,

            "message": "Stopped vehicle not found"

        }


    # ====================================
    # STEP 3: RESPONSE
    # ====================================

        return {

        "success": True,

        "vehicle": {

            "vehicleName":
                vehicle.get("name"),

            "uniqueId":
                vehicle.get("uniqueId"),

            "latitude":
                vehicle.get("latitude"),

            "longitude":
                vehicle.get("longitude"),

            "lastUpdate":
                vehicle.get("lastUpdate"),

            "speed":
                vehicle.get("speed")

        }

    }
    def get_specific_status_report(
    self,
    role,
    user,
    vehicle_input=None,
    limit=200
):

    # ====================================
    # STEP 1: VEHICLE INPUT
    # ====================================

        vehicle_name = str(vehicle_input or "").strip()


        if not vehicle_name:

            return {

            "success": False,

            "message": "Please enter vehicle name or unique ID"

        }


    # ====================================
    # STEP 2: RBAC FILTER
    # ====================================

        status_filter = get_rbac_filter(

        role,

        user,

        "report_statuses",

        self.db

    )


        regex = re.compile(

        re.escape(vehicle_name),

        re.IGNORECASE

    )


        query = {

        "$and": [

            status_filter,

            {

                "$or": [

                    {

                        "vehicleName": regex

                    },

                    {

                        "name": regex

                    },

                    {

                        "uniqueId": regex

                    }

                ]

            }

        ]

    }


    # ====================================
    # STEP 3: FETCH REPORT
    # ====================================

        reports = list(

        self.db["report_statuses"]

        .find(query)

        .sort(

            "startDateTime",

            -1

        )

        .limit(limit)

    )


        if not reports:

            return {

            "success": False,

            "message": "No status report found"

        }


    # ====================================
    # STEP 4: RESPONSE
    # ====================================

        return {

        "success": True,

        "reports": [

            self.clean(r)

            for r in reports

        ]

    }
   

    def clean(self, doc):

        if not doc:
            return doc

        result = {}

        for k, v in doc.items():

            if isinstance(v, ObjectId):
                result[k] = str(v)
            else:
                result[k] = v

    # ==========================================
    # Populate School Name
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

            except Exception:
                pass

    # ==========================================
    # Populate Branch Name
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

            except Exception:
                pass

        return result
    
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
    # accurate today distance
    def get_specific_distance_report(
    self,
    role,
    user,
    vehicle_input=None
):

    # =====================================
    # 1. Vehicle Input
    # =====================================

        if isinstance(vehicle_input, dict):
            vehicle_input = vehicle_input.get("vehicle_input")

        vehicle_input = str(vehicle_input or "").strip()

        if not vehicle_input:
            return {
            "success": False,
            "message": "Please enter vehicle name or unique ID."
        }

    # =====================================
    # 2. Find Vehicle
    # =====================================

        regex = re.compile(
        re.escape(vehicle_input),
        re.IGNORECASE
    )

        device = self.db["devices"].find_one({

        "$and": [

            get_rbac_filter(
                role,
                user,
                "devices",
                self.db
            ),

            {

                "$or": [

                    {
                        "name": regex
                    },

                    {
                        "vehicleName": regex
                    },

                    {
                        "uniqueId": vehicle_input
                    },

                    {
                        "uniqueId": {
                            "$in": self.normalize_unique_id(vehicle_input)
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

        unique_ids = self.normalize_unique_id(
        device["uniqueId"]
    )

    # =====================================
    # 3. Today's IST Time
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
    # 4. Aggregate History
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

        "vehicle": {

            "vehicleName": device.get("name"),
            "deviceId": str(device.get("_id")),
            "uniqueId": device.get("uniqueId"),
            "status": device.get("status"),
            "category": device.get("category"),
            "model": device.get("model")

        },

        "todayAccurateDistance": {

            "date": now.strftime("%Y-%m-%d"),

            "distanceKm": report["todayDistance"],

            "firstRecord": report["firstRecord"],

            "lastRecord": report["lastRecord"]

        }

    }
#     self,
#     role,
#     user,
#     vehicle_input=None,
#     limit=200
# ):

#     # ====================================
#     # STEP 1: VEHICLE INPUT
#     # ====================================

#         vehicle_name = str(vehicle_input or "").strip()


#         if not vehicle_name:

#             return {

#             "success": False,

#             "message": "Please enter vehicle name or unique ID"

#         }


#     # ====================================
#     # STEP 2: RBAC FILTER
#     # ====================================

#         report_filter = get_rbac_filter(

#         role,

#         user,

#         "report_distances",

#         self.db

#     )


#         regex = re.compile(

#         re.escape(vehicle_name),

#         re.IGNORECASE

#     )


#         query = {

#         "$and": [

#             report_filter,

#             {

#                 "$or": [

#                     {

#                         "vehicleName": regex

#                     },

#                     {

#                         "name": regex

#                     },

#                     {

#                         "uniqueId": regex

#                     }

#                 ]

#             }

#         ]

#     }


#     # ====================================
#     # STEP 3: FETCH REPORTS
#     # ====================================

#         reports = list(

#         self.db["report_distances"]

#         .find(query)

#         .sort(

#             "createdAt",

#             -1

#         )

#         .limit(limit)

#     )


#         if not reports:

#             return {

#             "success": False,

#             "message": "No distance report found"

#         }


#     # ====================================
#     # STEP 4: RESPONSE
#     # ====================================

#         return {

#         "success": True,

#         "reports": [

#             self.clean(report)

#             for report in reports

#         ]

#     }
    def get_specific_trip_report(
    self,
    role,
    user,
    vehicle_input=None,
    limit=200
):

    # ====================================
    # STEP 1: VEHICLE INPUT
    # ====================================

        vehicle_name = str(vehicle_input or "").strip()


        if not vehicle_name:

            return {

            "success": False,

            "message": "Please enter vehicle name or unique ID"

        }


    # ====================================
    # STEP 2: RBAC FILTER
    # ====================================

        trip_filter = get_rbac_filter(

        role,

        user,

        "report_trips",

        self.db

    )


        regex = re.compile(

        re.escape(vehicle_name),

        re.IGNORECASE

    )


        query = {

        "$and": [

            trip_filter,

            {

                "$or": [

                    {

                        "vehicleName": regex

                    },

                    {

                        "name": regex

                    },

                    {

                        "uniqueId": regex

                    }

                ]

            }

        ]

    }


    # ====================================
    # STEP 3: FETCH REPORTS
    # ====================================

        reports = list(

        self.db["report_trips"]

        .find(query)

        .sort(

            "startTime",

            -1

        )

        .limit(limit)

    )


        if not reports:

            return {

            "success": False,

            "message": "No trip report found"

        }


    # ====================================
    # STEP 4: RESPONSE
    # ====================================

        return {

        "success": True,

        "reports": [

            self.clean(report)

            for report in reports

        ]

    }
    def get_specific_idle_report(
    self,
    role,
    user,
    vehicle_input=None,
    limit=200
):

    # ====================================
    # STEP 1: VEHICLE INPUT
    # ====================================

        vehicle_name = str(vehicle_input or "").strip()


        if not vehicle_name:

            return {

            "success": False,

            "message": "Please enter vehicle name or unique ID"

        }


    # ====================================
    # STEP 2: RBAC FILTER
    # ====================================

        idle_filter = get_rbac_filter(

        role,

        user,

        "report_idles",

        self.db

    )


        regex = re.compile(

        re.escape(vehicle_name),

        re.IGNORECASE

    )


        query = {

        "$and": [

            idle_filter,

            {

                "$or": [

                    {

                        "vehicleName": regex

                    },

                    {

                        "name": regex

                    },

                    {

                        "uniqueId": regex

                    }

                ]

            }

        ]

    }


    # ====================================
    # STEP 3: FETCH REPORTS
    # ====================================

        reports = list(

        self.db["report_idles"]

        .find(query)

        .sort(

            "idleStartTime",

            -1

        )

        .limit(limit)

    )


        if not reports:

            return {

            "success": False,

            "message": "No idle report found"

        }


    # ====================================
    # STEP 4: RESPONSE
    # ====================================

        return {

        "success": True,

        "reports": [

            self.clean(report)

            for report in reports

        ]

    }
    def get_specific_travel_summary(
    self,
    role,
    user,
    vehicle_input=None,
    limit=200
):

    # ====================================
    # STEP 1: VEHICLE INPUT
    # ====================================

        vehicle_name = str(vehicle_input or "").strip()


        if not vehicle_name:

            return {

            "success": False,

            "message": "Please enter vehicle name or unique ID"

        }


    # ====================================
    # STEP 2: RBAC FILTER
    # ====================================

        summary_filter = get_rbac_filter(

        role,

        user,

        "report_travelsummaries",

        self.db

    )


        regex = re.compile(

        re.escape(vehicle_name),

        re.IGNORECASE

    )


        query = {

        "$and": [

            summary_filter,

            {

                "$or": [

                    {

                        "vehicleName": regex

                    },

                    {

                        "name": regex

                    },

                    {

                        "uniqueId": regex

                    }

                ]

            }

        ]

    }


    # ====================================
    # STEP 3: FETCH REPORTS
    # ====================================

        reports = list(

        self.db["report_travelsummaries"]

        .find(query)

        .sort(

            "startTime",

            -1

        )

        .limit(limit)

    )


        if not reports:

            return {

            "success": False,

            "message": "No travel summary found"

        }


    # ====================================
    # STEP 4: RESPONSE
    # ====================================

        return {

        "success": True,

        "reports": [

            self.clean(report)

            for report in reports

        ]

    }
    def get_specific_vehicle_geofences(
    self,
    role,
    user,
    vehicle_input=None,
    limit=200
):

    # ====================================
    # STEP 1: VEHICLE INPUT
    # ====================================

        vehicle_name = str(vehicle_input or "").strip()


        if not vehicle_name:

            return {

            "success": False,

            "message": "Please enter vehicle name or unique ID"

        }


    # ====================================
    # STEP 2: RBAC FILTER
    # ====================================

        rbac_filter = self.get_filter(

        role,

        user

    )


        regex = re.compile(

        re.escape(vehicle_name),

        re.IGNORECASE

    )


        query = {

        "$and": [

            rbac_filter,

            {

                "$or": [

                    {

                        "vehicleName": regex

                    },

                    {

                        "name": regex

                    },

                    {

                        "uniqueId": regex

                    }

                ]

            }

        ]

    }


    # ====================================
    # STEP 3: FETCH GEOFENCES
    # ====================================

        geofences = list(

        self.db["geofences"]

        .find(query)

        .sort(

            "createdAt",

            -1

        )

        .limit(limit)

    )


        if not geofences:

            return {

            "success": False,

            "message": "No geofence found for this vehicle"

        }


    # ====================================
    # STEP 4: RESPONSE
    # ====================================

        return {

        "success": True,

        "geofences": [

            self.clean(g)

            for g in geofences

        ]

    }
    
    def get_filter(
        self,
        role,
        user
    ):

        return get_rbac_filter(
            role,
            user,
            "geofences",
            self.db
        )
    def get_specific_branch_group_profile(
    self,
    role,
    user,
    branchgroup_input=None
):

    # ====================================
    # STEP 1: SUPERADMIN ACCESS CHECK
    # ====================================

        if role != "superadmin":
            return {
            "success": False,
            "message": "Access denied"
        }


    # ====================================
    # STEP 2: GET BRANCH GROUP INPUT
    # ====================================

        print("========== BRANCH GROUP DEBUG ==========")
        print("RAW INPUT =", branchgroup_input)
        print("INPUT TYPE =", type(branchgroup_input))


        if isinstance(branchgroup_input, dict):

            branchgroup_input = (
                branchgroup_input.get("branch_group_input")
            or branchgroup_input.get("branchgroup_input")
            or branchgroup_input.get("branchGroupName")
            or branchgroup_input.get("branch_group_name")
        )


        print("FINAL BRANCH GROUP INPUT =", branchgroup_input)
        print("========================================")


        if not branchgroup_input:

            return {
            "success": False,
            "message": "Branch group name is required"
        }


        branchgroup_input = str(branchgroup_input).strip()


    # ====================================
    # STEP 3: FIND BRANCH GROUP
    # ====================================

        group = self.db["branchgroups"].find_one(
        {
            "branchGroupName": {
                "$regex": f"^{branchgroup_input}$",
                "$options": "i"
            }
        }
    )


        if not group:

            return {
            "success": False,
            "message": "Branch group not found"
        }


    # ====================================
    # STEP 4: FORMAT PROFILE
    # ====================================

        profile = {

        "groupId": str(group["_id"]),

        "branchGroupName": group.get(
            "branchGroupName"
        ),

        "schoolId": (
            str(group.get("schoolId"))
            if group.get("schoolId")
            else None
        ),

        "mobileNo": group.get(
            "mobileNo"
        ),

        "username": group.get(
            "username"
        ),

        "email": group.get(
            "email"
        ),

        "role": group.get(
            "role"
        ),

        "active": group.get(
            "Active"
        ),

        "access": group.get(
            "access"
        ),

        "notification": group.get(
            "Notification"
        ),

        "fcmToken": group.get(
            "fcmToken"
        ),

        "createdAt": group.get(
            "createdAt"
        )
    }


    # ====================================
    # STEP 5: RESPONSE
    # ====================================

        return {
        "success": True,
        "profile": profile
    }


