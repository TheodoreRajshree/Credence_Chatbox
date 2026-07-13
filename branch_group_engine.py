from bson import ObjectId
from rbac import get_rbac_filter
from datetime import datetime, timezone, timedelta
from report_status_engine import ReportStatusEngine
from branch_engine import BranchEngine
from device_engine import DeviceEngine
from vehicle_km_engine import VehicleKmEngine
from report_status_engine import ReportStatusEngine
class BranchGroupEngine:

    def __init__(self, db):
        self.db = db
        self.report_status_engine =ReportStatusEngine(db)
       
        self.vehicle_km_engine = VehicleKmEngine(db)
    def get_address(self, latitude, longitude):

        try:

            location = self.geolocator.reverse(
            f"{latitude}, {longitude}",
            language="en",
            exactly_one=True,
            timeout=10
        )

            if location:
                return location.address

        except Exception as e:

            print("Reverse Geocoding Error:", e)

        return "Address Not Available"
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
    # def normalize_unique_id(self, uid):

    # ids = []

    # if uid is None:
    #     return ids


    # ids.append(uid)
    # ids.append(str(uid))


    # try:
    #     ids.append(int(float(uid)))
    # except:
    #     pass


    # try:
    #     ids.append(float(uid))
    # except:
    #     pass


    # return list(set(ids))
    # ====================================
    # CONVERT ID
    # ====================================
    def _convert_group_id(self, group_id):

        try:
            return ObjectId(str(group_id))

        except:
            return group_id



    # ====================================
    # GET BRANCH GROUP PROFILE
    # ====================================
    def get_branch_group_profile_only(
    self,
    group_id,
    role,
    user
):

    # ====================================
    # STEP 1: AUTO GROUP ID
    # ====================================

        if not group_id:

            group_id = (
            user.get("groupId")
            or user.get("branchGroupId")
            or user.get("_id")
        )


        try:
            group_value = ObjectId(str(group_id))
        except:
            group_value = str(group_id)



    # ====================================
    # STEP 2: RBAC FILTER
    # ====================================

        rbac_filter = get_rbac_filter(
        role,
        user,
        "branchgroups",
        self.db
    )



    # ====================================
    # STEP 3: QUERY
    # ====================================

        query = {

        "$and":[

            rbac_filter,

            {

                "$or":[

                    {
                        "_id": group_value
                    },

                    {
                        "_id": str(group_id)
                    },

                    {
                        "branchGroupName": str(group_id)
                    },

                    {
                        "username": str(group_id)
                    }

                ]

            }

        ]

    }


        print("========== BRANCH GROUP PROFILE DEBUG ==========")
        print("USER =", user)
        print("ROLE =", role)
        print("GROUP ID =", group_id)
        print("RBAC =", rbac_filter)
        print("QUERY =", query)
        print("==============================================")



    # ====================================
    # STEP 4: FIND GROUP
    # ====================================

        group = self.db["branchgroups"].find_one(
        query
    )


        if not group:

            return {

            "success": False,

            "message": "Branch group not found"

        }



    # ====================================
    # STEP 5: RESPONSE ONLY PROFILE
    # ====================================

        return {

        "success": True,


        "profile":{

            "groupId":
                str(group["_id"]),


            "branchGroupName":
                group.get(
                    "branchGroupName"
                ),


            "schoolId":
                str(group.get("schoolId"))
                if group.get("schoolId")
                else None,


            "mobileNo":
                group.get(
                    "mobileNo"
                ),


            "username":
                group.get(
                    "username"
                ),


            "email":
                group.get(
                    "email"
                ),


            "role":
                group.get(
                    "role"
                ),


            "active":
                group.get(
                    "Active"
                ),


            "access":
                group.get(
                    "access"
                ),


            "notification":
                group.get(
                    "Notification"
                ),


            "fcmToken":
                group.get(
                    "fcmToken"
                ),


            "createdAt":
                group.get(
                    "createdAt"
                )

        }

    }
    def get_branch_group_profile(
    self,
    group_id,
    role,
    user
):

    # ====================================
    # STEP 1: AUTO GROUP ID
    # ====================================

        if not group_id:

            group_id = (
            user.get("groupId")
            or user.get("branchGroupId")
            or user.get("_id")
        )

        group_value = self._convert_group_id(
        group_id
    )

    # ====================================
    # STEP 2: RBAC FILTER
    # ====================================

        rbac_filter = get_rbac_filter(
        role,
        user,
        "branchgroups",
        self.db
    )

    # ====================================
    # STEP 3: QUERY
    # ====================================

        query = {

        "$and": [

            rbac_filter,

            {

                "$or": [

                    {
                        "_id": group_value
                    },

                    {
                        "branchGroupName": str(group_id)
                    },

                    {
                        "username": str(group_id)
                    }

                ]

            }

        ]

    }

    # ====================================
    # DEBUG
    # ====================================

        print("========== DEBUG ==========")
        print("USER =", user)
        print("ROLE =", role)
        print("GROUP ID =", group_id)
        print("GROUP VALUE =", group_value)
        print("RBAC FILTER =", rbac_filter)
        print("QUERY =", query)
        print("===========================")

    # ====================================
    # STEP 4: FETCH GROUP
    # ====================================

        group = self.db["branchgroups"].find_one(
        query
    )

        if not group:

            return {

            "success": False,

            "error": "Branch group not found"

        }

    # ====================================
    # STEP 5: FETCH ASSIGNED BRANCH DETAILS
    # ====================================

        assigned_branch_ids = group.get(
        "AssignedBranch",
        []
    )

        branches = list(

        self.db["branches"].find(

            {

                "_id": {

                    "$in": assigned_branch_ids

                }

            },

            {

                "branchName": 1,
                "username": 1,
                "mobileNo": 1,
                "email": 1,
                "Active": 1

            }

        )

    )

        assigned_branches = []

        for branch in branches:

            assigned_branches.append({

            "branchId": str(branch["_id"]),

            "branchName": branch.get("branchName"),

            "username": branch.get("username"),

            "mobileNo": branch.get("mobileNo"),

            "email": branch.get("email"),

            "active": branch.get("Active")

        })

    # ====================================
    # STEP 6: RESPONSE
    # ====================================

        return {

        "success": True,

        "groupId": str(
            group["_id"]
        ),

        "branchGroupName": group.get(
            "branchGroupName"
        ),

        "schoolId": (
            str(group["schoolId"])
            if group.get("schoolId")
            else None
        ),

        "totalAssignedBranches": len(
            assigned_branches
        ),

        "assignedBranches": assigned_branches,

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
    # GET ALL ASSIGNED BRANCHES
    # ====================================
    def get_assigned_branches(
    self,
    group_id,
    role,
    user
):

        try:
            group_id = ObjectId(str(group_id))
        except:
            pass


    # ===============================
    # FIND GROUP
    # ===============================

        branch_group = self.db.branchgroups.find_one(
        {
            "_id": group_id
        }
    )


        if not branch_group:
            return {
            "success": False,
            "error": "Branch group not found"
        }


        print("GROUP DATA =", branch_group)


        branch_ids = branch_group.get(
        "AssignedBranch",
        []
    )


        print("ASSIGNED IDS =", branch_ids)


        if not branch_ids:
            return {
            "success": True,
            "count":0,
            "branches":[]
        }


    # ===============================
    # RBAC FILTER
    # ===============================

        rbac_filter = get_rbac_filter(
        role,
        user,
        "branches",
        self.db
    )


        print(
        "BRANCH RBAC FILTER =",
        rbac_filter
    )


    # ===============================
    # FIND BRANCHES
    # ===============================

        query = {

        "$and":[

            rbac_filter,

            {
                "_id":{
                    "$in":branch_ids
                }
            }

        ]

    }


        print("BRANCH QUERY =",query)


        branches = list(
        self.db.branches.find(query)
    )


        result=[]


        for branch in branches:

            result.append({

            "branchId":str(
                branch["_id"]
            ),

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
                ),

            "schoolId":
                str(branch.get("schoolId"))
                if branch.get("schoolId")
                else None,

            "active":
                branch.get("Active")

        })


        return {

        "success":True,

        "count":len(result),

        "branches":result

    }
    def get_specific_branch_by_name(
    self,
    branch_name,
    role,
    user
):

        print("ROLE =", role)
        print("USER =", user)
        print("BRANCH NAME =", branch_name)


    # ===============================
    # RBAC FILTER
    # ===============================

        rbac_filter = get_rbac_filter(
        role,
        user,
        "branches",
        self.db
    )


        print(
        "RBAC FILTER =",
        rbac_filter
    )


    # ===============================
    # QUERY
    # ===============================

        query = {

        "$and":[

            rbac_filter,

            {
                "branchName":
                {
                    "$regex": f"^{branch_name}$",
                    "$options": "i"
                }
            }

        ]

    }


        print(
        "QUERY =",
        query
    )


        branch = self.db.branches.find_one(
        query
    )


        print(
        "FOUND BRANCH =",
        branch
    )


        if not branch:

            return {

            "success":False,

            "error":
            "Branch not found"

        }



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


            "email":
            branch.get(
                "email"
            ),


            "mobileNo":
            branch.get(
                "mobileNo"
            ),


            "schoolId":
            str(branch.get("schoolId"))
            if branch.get("schoolId")
            else None,


            "active":
            branch.get(
                "Active"
            ),


            "role":
            branch.get(
                "role"
            )

        }

    }
    def get_assigned_school_super(
    self,
    group_id,
    role,
    user
):

        try:
            group_id = ObjectId(str(group_id))
        except:
            pass


    # ===============================
    # FIND BRANCH GROUP
    # ===============================

        branch_group = self.db.branchgroups.find_one(
        {
            "_id": group_id
        },
        {
            "schoolId": 1
        }
    )


        if not branch_group:

            return {
            "success": False,
            "error": "Branch group not found"
        }


        school_id = branch_group.get(
        "schoolId"
    )


        if not school_id:

            return {
            "success": True,
            "schools": []
        }


        print(
        "SCHOOL ID =",
        school_id
    )


    # ===============================
    # RBAC FILTER
    # ===============================

        rbac_filter = get_rbac_filter(
        role,
        user,
        "schools",
        self.db
    )


        print(
        "SCHOOL RBAC =",
        rbac_filter
    )


    # ===============================
    # FIND SCHOOL
    # ===============================

        query = {

        "$and":[

            rbac_filter,

            {
                "_id": school_id
            }

        ]

    }


        print(
        "SCHOOL QUERY =",
        query
    )


        school = self.db.schools.find_one(
        query
    )


        if not school:

            return {
            "success":False,
            "error":"School not found"
        }


        return {

        "success":True,

        "school":{

            "schoolId":
            str(
                school["_id"]
            ),

            "schoolName":
            school.get(
                "schoolName"
            ),

            "username":
            school.get(
                "username"
            ),

            "email":
            school.get(
                "email"
            ),

            "mobileNo":
            school.get(
                "mobileNo"
            ),

            "active":
            school.get(
                "Active"
            )

        }

    }
    def get_branchgroup_devices(
    self,
    group_id
):

    # ===============================
    # CONVERT GROUP ID
    # ===============================

        try:
            group_id = ObjectId(str(group_id))
        except:
            pass



    # ===============================
    # FIND BRANCH GROUP
    # ===============================

        branch_group = self.db["branchgroups"].find_one(
        {
            "_id": group_id
        },
        {
            "AssignedBranch": 1
        }
    )


        if not branch_group:

            return {
            "success": False,
            "error": "Branch group not found"
        }



        assigned_branches = branch_group.get(
        "AssignedBranch",
        []
    )


        if not assigned_branches:

            return {
            "success": True,
            "count": 0,
            "devices": []
        }



    # ===============================
    # CONVERT BRANCH IDS
    # ===============================

        branch_ids = []

        for b in assigned_branches:

            try:
                branch_ids.append(
                ObjectId(str(b))
            )

            except:
                pass



    # ===============================
    # FIND DEVICES
    # ===============================

        devices = self.db["devices"].find(
        {
            "branchId": {
                "$in": branch_ids
            }
        }
    )


        result = []


        for device in devices:

            result.append({

            "deviceId": str(
                device["_id"]
            ),

            "vehicleName":
                device.get("name"),


            "uniqueId":
                str(device.get("uniqueId"))
                if device.get("uniqueId")
                else None,


            "deviceNumber":
                device.get("deviceId"),


            "branchId":
                str(device.get("branchId"))
                if device.get("branchId")
                else None,


            "schoolId":
                str(device.get("schoolId"))
                if device.get("schoolId")
                else None,


            "status":
                device.get("status"),


            "model":
                device.get("model"),


            "category":
                device.get("category")

        })


        return {

        "success": True,

        "count": len(result),

        "devices": result

    }
    
    def get_branchgroup_vehicle_school_branch(
    self,
    group_id,
    vehicle_input,
    role,
    user
):

        print("GROUP ID:", group_id)
        print("VEHICLE INPUT:", vehicle_input)


    # =====================================
    # VALIDATE GROUP ID
    # =====================================

        if not group_id:

            return {
            "success": False,
            "error": "Branch group id missing"
        }


        try:

            group_id = ObjectId(
            str(group_id)
        )

        except Exception:

            return {
            "success": False,
            "error": "Invalid branch group id"
        }


         
    # =====================================
    # FIND BRANCH GROUP
    # =====================================

        group = self.db.branchgroups.find_one(
        {
            "_id": group_id
        }
    )


        if not group:

            return {
            "success": False,
            "error": "Branch group not found"
        }



        print("GROUP DATA =", group)



    # =====================================
    # SCHOOL ID CONVERSION
    # =====================================

        school_id = group.get(
        "schoolId"
    )


        try:

            school_id = ObjectId(
            str(school_id)
        )

        except:

            pass



    # =====================================
    # ASSIGNED BRANCHES CONVERSION
    # =====================================

        assigned_branches = group.get(
        "AssignedBranch",
        []
    )


        branch_ids = []


        for b in assigned_branches:

            try:

                branch_ids.append(
                ObjectId(str(b))
            )

            except:

                branch_ids.append(b)



        print("SCHOOL ID =", school_id)

        print(
        "BRANCH IDS =",
        branch_ids
    )



    # =====================================
    # DEVICE ACCESS QUERY
    # =====================================

        query = {

        "$or":[

            # school devices

            {
                "schoolId": school_id
            },


            # assigned branch devices

            {
                "branchId":
                {
                    "$in": branch_ids
                }
            }

        ]

    }



    # =====================================
    # VEHICLE SEARCH
    # =====================================

        if vehicle_input:


            vehicle_input = str(
            vehicle_input
        ).strip()



            query = {

            "$and":[


                query,


                {

                "$or":[


                    {
                    "name":
                    {
                        "$regex": vehicle_input,
                        "$options":"i"
                    }
                    },


                    {
                    "deviceId":
                    {
                        "$regex": vehicle_input,
                        "$options":"i"
                    }
                    },


                    {

                    "$expr":
                    {

                        "$regexMatch":
                        {

                            "input":
                            {
                                "$toString":
                                "$uniqueId"
                            },

                            "regex":
                            vehicle_input,

                            "options":"i"

                        }

                    }

                    }


                ]

                }


            ]

        }



        print(
        "FINAL DEVICE QUERY =",
        query
    )



    # =====================================
    # FETCH DEVICES
    # =====================================

        devices = list(
        self.db.devices.find(
            query
        )
    )



        result = []



        for device in devices:


            source = "branch"


            if device.get(
            "schoolId"
        ) == school_id:

                source = "school"



            result.append({

            "deviceId":
            str(
                device["_id"]
            ),


            "vehicle":
            device.get(
                "name"
            ),


            "uniqueId":
            device.get(
                "uniqueId"
            ),


            "deviceNumber":
            device.get(
                "deviceId"
            ),


            "source":
            source,


            "schoolId":
            str(
                device.get("schoolId")
            )
            if device.get("schoolId")
            else None,


            "branchId":
            str(
                device.get("branchId")
            )
            if device.get("branchId")
            else None,


            "status":
            device.get(
                "status"
            )


        })



        return {


        "success": True,


        "search":
        vehicle_input,


        "count":
        len(result),


        "devices":
        result

    }
    

    def get_branchgroup_vehicle_today_distance(
    self,
    group_id,
    role,
    user
):

        print("GROUP ID =", group_id)


    # =====================================
    # VALIDATE GROUP
    # =====================================

        if not group_id:

            return {
            "success": False,
            "error": "Branch group id missing"
        }


        try:

            group_id = ObjectId(
            str(group_id)
        )

        except:

            return {
            "success": False,
            "error": "Invalid group id"
        }



    # =====================================
    # FIND BRANCH GROUP
    # =====================================

        group = self.db.branchgroups.find_one(
        {
            "_id": group_id
        }
    )


        if not group:

            return {
            "success":False,
            "error":"Branch group not found"
        }



        school_id = group.get(
        "schoolId"
    )


        assigned_branches = group.get(
        "AssignedBranch",
        []
    )



        try:

            school_id = ObjectId(
            str(school_id)
        )

        except:

            pass



        branch_ids=[]


        for b in assigned_branches:

            try:

                branch_ids.append(
                ObjectId(str(b))
            )

            except:

                branch_ids.append(b)



    # =====================================
    # GET ALL DEVICES
    # SCHOOL + ASSIGNED BRANCH
    # =====================================


        devices = list(
        self.db.devices.find(

            {

            "$or":[

                {
                    "schoolId":school_id
                },

                {
                    "branchId":
                    {
                        "$in":branch_ids
                    }
                }

            ]

            }

        )
    )



        if not devices:

            return {

            "success":True,

            "count":0,

            "vehicles":[]

        }



        IST = timezone(
        timedelta(hours=5,minutes=30)
    )


        now=datetime.now(IST)


        start = now.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )


        end = now.replace(
        hour=23,
        minute=59,
        second=59,
        microsecond=999999
    )



        output=[]



    # =====================================
    # LOOP ALL VEHICLES
    # =====================================

        for device in devices:


            unique_id = device.get(
            "uniqueId"
        )


            if not unique_id:
                continue



            history_query = {


            "$and":[


                get_rbac_filter(
                    role,
                    user,
                    "histories",
                    self.db
                ),


                {
                    "uniqueId":unique_id
                },


                {
                    "createdAt":
                    {
                        "$gte":start,
                        "$lte":end
                    }
                },


                {
                    "attributes.totalDistance":
                    {
                        "$ne":None
                    }
                }


            ]

        }



            history=list(
            self.db.histories.find(
                history_query
            )
            .sort(
                "createdAt",
                1
            )
        )



            if not history:
                continue



            start_distance = (
            history[0]
            .get("attributes",{})
            .get("totalDistance",0)
        )


            end_distance = (
            history[-1]
            .get("attributes",{})
            .get("totalDistance",0)
        )



            distance = round(
            (
                end_distance -
                start_distance
            ) / 1000,
            2
        )



            output.append({


            "vehicleName":
                device.get("name"),


            "uniqueId":
                device.get("uniqueId"),


            "source":
                (
                    "school"
                    if device.get("schoolId")==school_id
                    else "branch"
                ),


            "schoolId":
                str(device.get("schoolId"))
                if device.get("schoolId")
                else None,


            "branchId":
                str(device.get("branchId"))
                if device.get("branchId")
                else None,


            "todayDistanceKm":
                distance

        })



        return {

        "success":True,

        "date":
            now.strftime("%Y-%m-%d"),

        "count":
            len(output),

        "vehicles":
            output

    }
    from bson import ObjectId

    def get_branchgroup_geofences(
    self,
    group_id,
    role,
    user
):

    # =====================================
    # VALIDATE GROUP ID
    # =====================================

        if not group_id:
            group_id = (
            user.get("groupId")
            or user.get("branchGroupId")
            or user.get("_id")
        )

        try:
            group_id = ObjectId(str(group_id))
        except Exception:
            return {
            "success": False,
            "error": "Invalid branch group id"
        }

    # =====================================
    # FIND BRANCH GROUP
    # =====================================

        group = self.db["branchgroups"].find_one({
        "_id": group_id
    })

        if not group:
            return {
            "success": False,
            "error": "Branch group not found"
        }

        school_id = group.get("schoolId")
        assigned_branches = group.get("AssignedBranch", [])

    # =====================================
    # CONVERT IDS
    # =====================================

        try:
            school_id = ObjectId(str(school_id))
        except:
            pass

        branch_ids = []

        for branch in assigned_branches:
            try:
                branch_ids.append(ObjectId(str(branch)))
            except:
                branch_ids.append(branch)

        print("GROUP =", group_id)
        print("SCHOOL =", school_id)
        print("BRANCH IDS =", branch_ids)

    # =====================================
    # QUERY
    # =====================================

        query = {
        "$or": [

            # School Geofences
            {
                "$or": [
                    {"schoolId": school_id},
                    {"schoolId": str(school_id)}
                ]
            },

            # Branch Geofences
            {
                "$or": [
                    {
                        "branchId": {
                            "$in": branch_ids
                        }
                    },
                    {
                        "branchId": {
                            "$in": [str(x) for x in branch_ids]
                        }
                    }
                ]
            }

        ]
    }

        print("QUERY =", query)

        geofences = list(
        self.db["geofences"].find(query).sort("createdAt", -1)
    )

        print("TOTAL GEOFENCES =", len(geofences))

        result = []

        for geo in geofences:

            result.append({

            "geofenceId": str(geo["_id"]),

            "geofenceName": (
                geo.get("geofenceName")
                or geo.get("name")
            ),

            "address": geo.get("address"),

            "description": geo.get("description"),

            "schoolId": (
                str(geo.get("schoolId"))
                if geo.get("schoolId")
                else None
            ),

            "branchId": (
                str(geo.get("branchId"))
                if geo.get("branchId")
                else None
            ),

            "type": geo.get("type"),

            "coordinates": geo.get("coordinates"),

            "active": geo.get("Active")
        })

        return {
    
        "success": True,

        "branchGroup": {
            "groupId": str(group["_id"]),
            "branchGroupName": group.get("branchGroupName")
        },

        "count": len(result),

        "geofences": result

    }


    def get_branchgroup_specific_branch_geofences(
    self,
    group_id,
    branch_name,
    role,
    user
):

    # =====================================
    # GET GROUP ID
    # =====================================

        if not group_id:
            group_id = (
            user.get("groupId")
            or user.get("branchGroupId")
            or user.get("_id")
        )

        try:
            group_id = ObjectId(str(group_id))
        except:
            return {
            "success": False,
            "message": "Invalid Branch Group ID"
        }

    # =====================================
    # FIND BRANCH GROUP
    # =====================================

        group = self.db["branchgroups"].find_one({
        "_id": group_id
    })

        if not group:
            return {
            "success": False,
            "message": "Branch Group not found."
        }

        assigned_branches = group.get("AssignedBranch", [])

    # =====================================
    # FIND BRANCH
    # =====================================

        branch = self.db["branches"].find_one({

        "$or": [

            {
                "branchName": {
                    "$regex": branch_name,
                    "$options": "i"
                }
            },

            {
                "name": {
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

    })

        if not branch:
            return {
            "success": False,
            "message": "Branch not found."
        }

        branch_id = branch["_id"]

    # =====================================
    # CHECK BRANCH BELONGS TO GROUP
    # =====================================

        if branch_id not in assigned_branches:

            if str(branch_id) not in [str(x) for x in assigned_branches]:

                return {
                "success": False,
                "message": "This branch is not assigned to your Branch Group."
            }

    # =====================================
    # RBAC FILTER
    # =====================================

        rbac_filter = get_rbac_filter(
        role,
        user,
        "geofences",
        self.db
    )

    # =====================================
    # FIND GEOFENCES
    # =====================================

        query = {

        "$and": [

            rbac_filter,

            {

                "$or": [

                    {
                        "branchId": branch_id
                    },

                    {
                        "branchId": str(branch_id)
                    }

                ]

            }

        ]

    }

        geofences = list(

        self.db["geofences"]
        .find(query)
        .sort("createdAt", -1)

    )

        result = []

        for geo in geofences:

            result.append({

            "geofenceId": str(geo["_id"]),

            "geofenceName": (
                geo.get("geofenceName")
                or geo.get("name")
            ),

            "address": geo.get("address"),

            "description": geo.get("description"),

            "branchId": str(geo.get("branchId"))
            if geo.get("branchId")
            else None,

            "schoolId": str(geo.get("schoolId"))
            if geo.get("schoolId")
            else None,

            "coordinates": geo.get("coordinates"),

            "type": geo.get("type"),

            "active": geo.get("Active")

        })

        return {

        "success": True,

        "branchGroup": {

            "groupId": str(group["_id"]),

            "branchGroupName": group.get("branchGroupName")

        },

        "branch": {

            "branchId": str(branch["_id"]),

            "branchName": (
                branch.get("branchName")
                or branch.get("name")
            )

        },

        "count": len(result),

        "geofences": result

    }
    def get_branchgroup_travel_summary(
    self,
    group_id,
    role,
    user,
    limit=100
):

        print("GROUP ID =", group_id)


    # =====================================
    # VALIDATE GROUP
    # =====================================

        if not group_id:

            return {
            "success": False,
            "error": "Branch group id missing"
        }


        try:

            group_id = ObjectId(
            str(group_id)
        )

        except:

            return {
            "success": False,
            "error": "Invalid group id"
        }



    # =====================================
    # FIND BRANCH GROUP
    # =====================================

        group = self.db.branchgroups.find_one(
        {
            "_id": group_id
        }
    )


        if not group:

            return {
            "success": False,
            "error": "Branch group not found"
        }



        school_id = group.get(
        "schoolId"
    )


        assigned_branches = group.get(
        "AssignedBranch",
        []
    )



    # =====================================
    # CONVERT IDS
    # =====================================

        try:

            school_id = ObjectId(
            str(school_id)
        )

        except:

            pass



        branch_ids = []


        for b in assigned_branches:

            try:

                branch_ids.append(
                ObjectId(str(b))
            )

            except:

                branch_ids.append(b)



    # =====================================
    # GET DEVICES
    # SCHOOL + BRANCH
    # =====================================


        device_query = {


        "$or":[


            {
                "schoolId": school_id
            },


            {
                "branchId":
                {
                    "$in": branch_ids
                }
            }

        ]

    }



        devices = list(

        self.db.devices.find(
            device_query
        )

    )



        if not devices:

            return {

            "success": True,

            "count":0,

            "reports":[]

        }



        unique_ids=[]


        for d in devices:

            if d.get("uniqueId"):

                unique_ids.append(
                str(d.get("uniqueId"))
            )



    # =====================================
    # TRAVEL SUMMARY RBAC
    # =====================================


        summary_filter = get_rbac_filter(

        role,

        user,

        "report_travelsummaries",

        self.db

    )



        query = {


        "$and":[


            summary_filter,


            {

                "uniqueId":
                {
                    "$in":unique_ids
                }

            }

        ]

    }



        print(
        "TRAVEL QUERY =",
        query
    )



        reports = list(

        self.db.report_travelsummaries.find(
            query
        )

        .sort(
            "startTime",
            -1
        )

        .limit(limit)

    )



        result=[]



        for report in reports:


            result.append({

            "reportId":
            str(report["_id"]),


            "uniqueId":
            report.get(
                "uniqueId"
            ),


            "vehicleName":
            report.get(
                "name"
            ),


            "startTime":
            report.get(
                "startTime"
            ),


            "endTime":
            report.get(
                "endTime"
            ),


            "distance":
            report.get(
                "distance"
            ),


            "duration":
            report.get(
                "duration"
            ),


            "startLocation":
            report.get(
                "startLocation"
            ),


            "endLocation":
            report.get(
                "endLocation"
            )

        })



        return {


        "success":True,


        "count":
        len(result),


        "reports":
        result

    }
    def get_branchgroup_vehicle_status_report(
    self,
    group_id,
    role,
    user,
    limit=100
):

        print("GROUP ID =", group_id)


    # =====================================
    # VALIDATE GROUP
    # =====================================

        if not group_id:

            return {
            "success": False,
            "error": "Branch group id missing"
        }


        try:

            group_id = ObjectId(
            str(group_id)
        )

        except:

            return {
            "success": False,
            "error": "Invalid group id"
        }



    # =====================================
    # FIND BRANCH GROUP
    # =====================================

        group = self.db.branchgroups.find_one(
        {
            "_id": group_id
        }
    )


        if not group:

            return {
            "success": False,
            "error": "Branch group not found"
        }



        school_id = group.get(
        "schoolId"
    )


        assigned_branches = group.get(
        "AssignedBranch",
        []
    )



    # =====================================
    # CONVERT IDS
    # =====================================

        try:

            school_id = ObjectId(
            str(school_id)
        )

        except:

            pass



        branch_ids = []


        for b in assigned_branches:

            try:

                branch_ids.append(
                ObjectId(str(b))
            )

            except:

                branch_ids.append(b)



    # =====================================
    # FIND DEVICES
    # SCHOOL + BRANCH
    # =====================================

        device_query = {

        "$or":[

            {
                "schoolId": school_id
            },


            {
                "branchId":
                {
                    "$in": branch_ids
                }
            }

        ]

    }



        devices = list(

        self.db.devices.find(
            device_query
        )

    )


        if not devices:

            return {

            "success": True,

            "count":0,

            "reports":[]

        }



        unique_ids = []


        for d in devices:

            if d.get("uniqueId"):

                unique_ids.append(
                str(d.get("uniqueId"))
            )



    # =====================================
    # STATUS REPORT RBAC
    # =====================================

        status_filter = get_rbac_filter(

        role,

        user,

        "report_statuses",

        self.db

    )



        query = {

        "$and":[

            status_filter,


            {

                "uniqueId":
                {
                    "$in": unique_ids
                }

            }

        ]

    }



        print(
        "STATUS QUERY =",
        query
    )



        reports = list(

        self.db.report_statuses.find(
            query
        )

        .sort(
            "startDateTime",
            -1
        )

        .limit(limit)

    )



        result=[]



        for r in reports:


            result.append({

            "reportId":
            str(r["_id"]),


            "uniqueId":
            r.get(
                "uniqueId"
            ),


            "vehicleName":
            r.get(
                "name"
            ),


            "status":
            r.get(
                "status"
            ),


            "startDateTime":
            r.get(
                "startDateTime"
            ),


            "endDateTime":
            r.get(
                "endDateTime"
            ),


            "duration":
            r.get(
                "duration"
            )

        })



        return {

        "success": True,

        "count":
        len(result),

        "reports":
        result

    }
    def get_branchgroup_vehicle_last_positions(
        self,
        group_id,
        role,
        user,
        limit=100
):

        print("GROUP ID =", group_id)


    # =====================================
    # VALIDATE GROUP
    # =====================================

        if not group_id:
            return {
            "success": False,
            "error": "Branch group id missing"
        }


        try:
            group_id = ObjectId(str(group_id))

        except:
            return {
            "success": False,
            "error": "Invalid group id"
        }



    # =====================================
    # FIND BRANCH GROUP
    # =====================================

        group = self.db.branchgroups.find_one(
        {
            "_id": group_id
        }
    )


        if not group:
            return {
            "success": False,
            "error": "Branch group not found"
        }



        school_id = group.get("schoolId")

        assigned_branches = group.get(
        "AssignedBranch",
        []
    )



    # =====================================
    # CONVERT IDS
    # =====================================

        try:
            school_id = ObjectId(str(school_id))

        except:
            pass



        branch_ids = []


        for b in assigned_branches:

            try:
                branch_ids.append(
                ObjectId(str(b))
            )

            except:
                branch_ids.append(b)



    # =====================================
    # FIND DEVICES
    # SCHOOL + BRANCH
    # =====================================

        device_query = {

        "$or":[

            {
                "schoolId": school_id
            },

            {
                "branchId":
                {
                    "$in": branch_ids
                }
            }

        ]

    }


        devices = list(
        self.db.devices.find(
            device_query
        )
    )



        if not devices:

            return {

            "success": True,
            "count": 0,
            "vehicles": []

        }



        unique_ids = []


        for d in devices:

            if d.get("uniqueId"):

                unique_ids.append(
                str(d.get("uniqueId"))
            )



    # =====================================
    # RBAC POSITION FILTER
    # =====================================

        position_filter = self.get_position_filter(
        role,
        user
    )



    # =====================================
    # FIND LAST POSITIONS
    # =====================================

        query = {

        "$and":[

            position_filter,

            {

                "uniqueId":
                {
                    "$in": unique_ids
                }

            }

        ]

    }


        print(
        "POSITION QUERY =",
        query
    )


        vehicles = list(

        self.db.vehiclelastpositions.find(
            query
        )
        .limit(limit)

    )



        result = []



        for vehicle in vehicles:

            result.append({

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


            "course":
            vehicle.get("course"),


            "accuracy":
            vehicle.get("accuracy"),


            "altitude":
            vehicle.get("altitude"),


            "address":
            vehicle.get("address"),


            "protocol":
            vehicle.get("protocol"),


            "deviceTime":
            vehicle.get("deviceTime"),


            "fixTime":
            vehicle.get("fixTime"),


            "serverTime":
            vehicle.get("serverTime"),


            "lastUpdate":
            vehicle.get("lastUpdate"),


            "valid":
            vehicle.get("valid"),


            "outdated":
            vehicle.get("outdated")

        })



        return {

        "success": True,

        "count": len(result),

        "vehicles": result

    }
    def get_branchgroup_routes(
        self,
        group_id,
        role,
        user,
        limit=100
):

    # =====================================
    # VALIDATE GROUP
    # =====================================

        if not group_id:

            return {
            "success": False,
            "error": "Branch group id missing"
        }


        try:

            group_id = ObjectId(
            str(group_id)
        )

        except:

            return {
            "success": False,
            "error": "Invalid group id"
        }



    # =====================================
    # FIND BRANCH GROUP
    # =====================================

        group = self.db.branchgroups.find_one(
        {
            "_id": group_id
        }
    )


        if not group:

            return {
            "success": False,
            "error": "Branch group not found"
        }



        school_id = group.get(
        "schoolId"
    )


        assigned_branches = group.get(
        "AssignedBranch",
        []
    )



    # =====================================
    # CONVERT IDS
    # =====================================

        try:

            school_id = ObjectId(
            str(school_id)
        )

        except:

            pass



        branch_ids = []


        for b in assigned_branches:

            try:

                branch_ids.append(
                ObjectId(str(b))
            )

            except:

                branch_ids.append(b)



    # =====================================
    # RBAC FILTER
    # =====================================

        route_filter = get_rbac_filter(

        role,

        user,

        "routes",

        self.db

    )



    # =====================================
    # FIND ROUTES
    # SCHOOL + BRANCH
    # =====================================

        query = {

        "$and":[

            route_filter,


            {

                "$or":[

                    {
                        "schoolId": school_id
                    },


                    {

                        "branchId":
                        {
                            "$in": branch_ids
                        }

                    }

                ]

            }

        ]

    }



        print(
        "ROUTE QUERY =",
        query
    )



        routes = list(

        self.db.routes.find(
            query
        )
        .limit(limit)

    )



        result = []



        for r in routes:

            result.append({

            "routeId":
            str(r["_id"]),


            "name":
            r.get("name"),


            "schoolId":
            r.get("schoolId"),


            "branchId":
            r.get("branchId"),


            "startPoint":
            r.get("startPoint"),


            "endPoint":
            r.get("endPoint"),


            "stops":
            r.get("stops"),


            "createdAt":
            r.get("createdAt")

        })



        return {

        "success": True,

        "count":
        len(result),

        "routes":
        result

    }
    def get_branchgroup_specific_branch(
    self,
    branch_name,
    role,
    user
):

        try:

        # =====================================
        # CLEAN INPUT
        # =====================================

            branch_name = str(branch_name).strip()


            if not branch_name:

                return {

                "success": False,

                "message": "Branch name missing"

            }



        # =====================================
        # GET GROUP ID
        # =====================================

            group_id = (
            user.get("groupId")
            or user.get("_id")
        )


            try:

                group_id = ObjectId(
                str(group_id)
            )

            except:

                return {

                "success": False,

                "message": "Invalid branch group id"

            }



        # =====================================
        # FIND BRANCH GROUP
        # =====================================

            branch_group = self.db.branchgroups.find_one(
            {
                "_id": group_id
            }
        )


            if not branch_group:

                return {

                "success":False,

                "message":"Branch group not found"

            }



        # =====================================
        # GET ASSIGNED BRANCH IDS
        # =====================================

            assigned_branches = branch_group.get(
            "AssignedBranch",
            []
        )


            if not assigned_branches:

                return {

                "success":False,

                "message":"No branches assigned"

            }



        # =====================================
        # NORMALIZE IDS
        # =====================================

            branch_object_ids = []


            for branch_id in assigned_branches:

                try:

                    branch_object_ids.append(
                    ObjectId(str(branch_id))
                )

                except:

                    branch_object_ids.append(
                    branch_id
                )



        # =====================================
        # SEARCH QUERY
        # =====================================

            query = {


            "_id":{

                "$in": branch_object_ids

            },


            "$or":[


                {
                    "branchName":{
                        "$regex":branch_name,
                        "$options":"i"
                    }
                },


                {
                    "username":{
                        "$regex":branch_name,
                        "$options":"i"
                    }
                },


                {
                    "vehicleName":{
                        "$regex":branch_name,
                        "$options":"i"
                    }
                },


                {
                    "name":{
                        "$regex":branch_name,
                        "$options":"i"
                    }
                }


            ]

        }



            print("BRANCH SEARCH QUERY =",query)



        # =====================================
        # FIND BRANCH
        # =====================================

            branch = self.db.branches.find_one(
            query
        )



            if not branch:


                return {


                "success":False,


                "message":
                "Branch not found in this branch group"


            }



        # =====================================
        # RESPONSE
        # =====================================


            return {


            "success":True,


            "branch":{


                "branchId":
                str(branch["_id"]),


                "branchName":
                branch.get("branchName"),


                "username":
                branch.get("username"),


                "vehicleName":
                branch.get("vehicleName"),


                "mobileNo":
                branch.get("mobileNo"),


                "email":
                branch.get("email"),


                "schoolId":
                str(branch.get("schoolId"))
                if branch.get("schoolId")
                else None,


                "active":
                branch.get("Active")


            }


        }



        except Exception as e:


            print(
            "ERROR get_branchgroup_specific_branch =",
            e
        )


            return {

            "success":False,

            "message":str(e)

        }
    def get_assigned_school_branchgroup(
    self,
    role,
    user
):

        print("ROLE =", role)

        group_id = user.get("groupId")


        if not group_id:
            return {
            "success": False,
            "error": "Group id not found"
        }


        try:
            group_id = ObjectId(str(group_id))

        except Exception as e:
            return {
            "success": False,
            "error": "Invalid group id"
        }


    # ALWAYS initialize before use
        branch_group = self.db.branchgroups.find_one(
        {
            "_id": group_id
        }
    )


        if not branch_group:
            return {
            "success": False,
            "error": "Branch group not found"
        }


        school_id = branch_group.get("schoolId")


        if not school_id:
            return {
            "success": True,
            "school": None
        }


        try:
            school_id = ObjectId(str(school_id))
        except:
            pass


        school = self.db.schools.find_one(
        {
            "_id": school_id
        }
    )


        if not school:
            return {
            "success": False,
            "error": "School not found"
        }


        return {
        "success": True,

        "branchGroup": {
            "branchGroupId": str(branch_group["_id"]),
            "branchGroupName": branch_group.get("name")
        },

        "school": {
            "schoolId": str(school["_id"]),
            "schoolName": school.get("schoolName"),
            "username": school.get("username"),
            "email": school.get("email"),
            "mobileNo": school.get("mobileNo"),
            "active": school.get("Active")
        }
    }
    
    def get_branchgroup_specific_branch_vehicles(
    self,
    branch_name,
    vehicle_input,
    role,
    user
):

        try:

        # ===============================
        # CLEAN INPUT
        # ===============================

            branch_name = str(branch_name).strip()
            vehicle_input = str(vehicle_input).strip()


            if not branch_name or not vehicle_input:

                return {
                "success": False,
                "message": "Branch name and vehicle name required"
            }


        # ===============================
        # GET GROUP ID
        # ===============================

            group_id = (
            user.get("groupId")
            or user.get("_id")
        )


            group_id = ObjectId(str(group_id))


        # ===============================
        # FIND BRANCH GROUP
        # ===============================

            branch_group = self.db.branchgroups.find_one(
            {
                "_id": group_id
            }
        )


            if not branch_group:

                return {
                "success": False,
                "message": "Branch group not found"
            }


            assigned_branches = branch_group.get(
            "AssignedBranch",
            []
        )


            branch_ids = []

            for b in assigned_branches:

                try:
                    branch_ids.append(
                    ObjectId(str(b))
                )
                except:
                    pass



        # ===============================
        # FIND BRANCH
        # ===============================

            branch = self.db.branches.find_one(
            {

                "_id": {
                    "$in": branch_ids
                },

                "branchName": {

                    "$regex": branch_name,

                    "$options": "i"
                }

            }
        )


            if not branch:

                return {
                "success": False,
                "message": "Branch not found"
            }



        # ===============================
        # FIND VEHICLE
        # ===============================

            vehicle = self.db.devices.find_one(

            {

                "branchId": branch["_id"],

                "$or": [

                    {
                        "name": {
                            "$regex": vehicle_input,
                            "$options": "i"
                        }
                    },

                    {
                        "deviceId": {
                            "$regex": vehicle_input,
                            "$options": "i"
                        }
                    },

                    {
                        "uniqueId": {
                            "$regex": vehicle_input,
                            "$options": "i"
                        }
                    }

                ]

            }

        )


            if not vehicle:

                return {
                "success": False,
                "message": "Vehicle not found in this branch"
            }



            return {

            "success": True,

            "branch": {

                "branchId": str(branch["_id"]),

                "branchName":
                    branch.get("branchName")

            },

            "vehicle": {

                "deviceId":
                    str(vehicle["_id"]),

                "vehicleName":
                    vehicle.get("name"),

                "uniqueId":
                    vehicle.get("uniqueId"),

                "deviceNumber":
                    vehicle.get("deviceId"),

                "status":
                    vehicle.get("status"),

                "model":
                    vehicle.get("model")

            }

        }


        except Exception as e:

            return {
            "success": False,
            "error": str(e)
        }
   
    

    def get_branchgroup_branch_vehicles_1(
    self,
    role,
    user
):

        try:

        # ===============================
        # GET GROUP ID
        # ===============================
            group_id = user.get("groupId") or user.get("_id")

            if not group_id:
                return {
                "success": False,
                "message": "Branch Group ID not found."
            }

            branch_group = self.db["branchgroups"].find_one({
            "_id": ObjectId(str(group_id))
        })

            if not branch_group:
                return {
                "success": False,
                "message": "Branch Group not found."
            }

        # ===============================
        # GET ASSIGNED BRANCHES
        # ===============================
            branch_ids = []

            for branch_id in branch_group.get("AssignedBranch", []):
                try:
                    branch_ids.append(ObjectId(str(branch_id)))
                except:
                    pass

            if not branch_ids:
                return {
                "success": False,
                "message": "No branches assigned."
            }

        # ===============================
        # GET ALL BRANCHES
        # ===============================
            branches = {
            branch["_id"]: branch
            for branch in self.db["branches"].find({
                "_id": {"$in": branch_ids}
            })
        }

        # ===============================
        # GET ALL VEHICLES
        # ===============================
            vehicles = self.db["devices"].find({
            "branchId": {"$in": branch_ids}
        })

            data = []

            for vehicle in vehicles:

                branch = branches.get(vehicle.get("branchId"))

                data.append({

                "deviceId": str(vehicle["_id"]),
                "vehicleName": vehicle.get("name"),
                "uniqueId": vehicle.get("uniqueId"),
                "deviceNumber": vehicle.get("deviceId"),
                "status": vehicle.get("status"),
                "model": vehicle.get("model"),
                "category": vehicle.get("category"),
                "speed": vehicle.get("speed"),
                "average": vehicle.get("average"),
                "sim": vehicle.get("sim"),
                "installationDate": vehicle.get("installationdate"),
                "expirationDate": vehicle.get("expirationdate"),

                "branchId": str(vehicle.get("branchId")),
                "branchName": branch.get("branchName") if branch else None
            })

            return {
            "success": True,
            "totalVehicles": len(data),
            "vehicles": data
        }

        except Exception as e:

            return {
            "success": False,
            "error": str(e)
        }
    from bson import ObjectId

    def get_branchgroup_school_all_vehicles_1(
    self,
    role,
    user
):

        try:

        # ===============================
        # GET SCHOOL ID
        # ===============================
            school_id = user.get("schoolId")

            if not school_id:
                return {
                "success": False,
                "message": "School ID not found."
            }

            school_id = ObjectId(str(school_id))

        # ===============================
        # GET SCHOOL
        # ===============================
            school = self.db["schools"].find_one({
            "_id": school_id
        })

            if not school:
                return {
                "success": False,
                "message": "School not found."
            }

        # ===============================
        # GET BRANCHES
        # ===============================
            branches = {
            branch["_id"]: branch
            for branch in self.db["branches"].find({
                "schoolId": school_id
            })
        }

        # ===============================
        # GET ALL SCHOOL VEHICLES
        # ===============================
            vehicles = self.db["devices"].find({
            "schoolId": school_id
        })

            data = []

            for vehicle in vehicles:

                branch = branches.get(vehicle.get("branchId"))

                data.append({

                "deviceId": str(vehicle["_id"]),
                "vehicleName": vehicle.get("name"),
                "uniqueId": vehicle.get("uniqueId"),
                "deviceNumber": vehicle.get("deviceId"),
                "status": vehicle.get("status"),
                "model": vehicle.get("model"),
                "category": vehicle.get("category"),
                "speed": vehicle.get("speed"),
                "average": vehicle.get("average"),
                "sim": vehicle.get("sim"),
                "installationDate": vehicle.get("installationdate"),
                "expirationDate": vehicle.get("expirationdate"),

                "schoolId": str(vehicle.get("schoolId")),
                "schoolName": school.get("schoolName"),

                "branchId": str(vehicle.get("branchId")) if vehicle.get("branchId") else None,
                "branchName": branch.get("branchName") if branch else None
            })

            return {
            "success": True,
            "totalVehicles": len(data),
            "vehicles": data
        }

        except Exception as e:

            return {
            "success": False,
            "error": str(e)
        }
    def get_branchgroup_school_vehicle(
    self,
    vehicle_input,
    role,
    user
):

        try:

        # ===============================
        # CLEAN INPUT
        # ===============================

            if isinstance(vehicle_input, dict):

                vehicle_input = (
                vehicle_input.get("vehicle_input")
                or vehicle_input.get("vehicle")
                or vehicle_input.get("vehicle_name")
            )

            vehicle_input = str(vehicle_input).strip()

            if not vehicle_input:

                return {
                "success": False,
                "message": "Vehicle name required"
            }


        # ===============================
        # GET SCHOOL ID
        # ===============================

            school_id = user.get("schoolId")

            if not school_id:

                return {
                "success": False,
                "message": "School id not found"
            }

            school_id = ObjectId(str(school_id))


        # ===============================
        # FIND SCHOOL
        # ===============================

            school = self.db.schools.find_one(
            {
                "_id": school_id
            }
        )

            if not school:

                return {
                "success": False,
                "message": "School not found"
            }


        # ===============================
        # FIND VEHICLE
        # ===============================

            vehicle = self.db.devices.find_one(

            {

                "schoolId": school_id,

                "$or": [

                    {
                        "name": {
                            "$regex": vehicle_input,
                            "$options": "i"
                        }
                    },

                    {
                        "deviceId": {
                            "$regex": vehicle_input,
                            "$options": "i"
                        }
                    },

                    {
                        "uniqueId": {
                            "$regex": vehicle_input,
                            "$options": "i"
                        }
                    }

                ]

            }

        )


            if not vehicle:

                return {
                "success": False,
                "message": "Vehicle not found in this school"
            }


        # ===============================
        # FIND BRANCH (OPTIONAL)
        # ===============================

            branch = None

            if vehicle.get("branchId"):

                branch = self.db.branches.find_one(
                {
                    "_id": vehicle.get("branchId")
                },
                {
                    "branchName": 1
                }
            )


        # ===============================
        # RESPONSE
        # ===============================

            return {

            "success": True,

            "school": {

                "schoolId": str(school["_id"]),

                "schoolName": school.get("schoolName")

            },

            "branch": {

                "branchId":
                    str(branch["_id"])
                    if branch
                    else None,

                "branchName":
                    branch.get("branchName")
                    if branch
                    else None

            },

            "vehicle": {

                "deviceId":
                    str(vehicle["_id"]),

                "vehicleName":
                    vehicle.get("name"),

                "uniqueId":
                    vehicle.get("uniqueId"),

                "deviceNumber":
                    vehicle.get("deviceId"),

                "status":
                    vehicle.get("status"),

                "model":
                    vehicle.get("model"),

                "category":
                    vehicle.get("category")

            }

        }

        except Exception as e:

            return {

            "success": False,

            "error": str(e)

        }
    def get_branchgroup_specific_vehicle(
    self,
    group_id,
    vehicle_input
):

    # ===============================
    # CONVERT GROUP ID
    # ===============================

        try:
            group_id = ObjectId(str(group_id))
        except:
            pass


    # ===============================
    # CLEAN VEHICLE INPUT
    # ===============================

        if isinstance(vehicle_input, dict):

            vehicle_input = (
            vehicle_input.get("vehicle_input")
            or vehicle_input.get("vehicle")
            or vehicle_input.get("vehicle_name")
        )

        vehicle_input = str(vehicle_input).strip()

        if not vehicle_input:

            return {
            "success": False,
            "error": "Vehicle name required"
        }


    # ===============================
    # FIND BRANCH GROUP
    # ===============================

        branch_group = self.db["branchgroups"].find_one(
        {
            "_id": group_id
        },
        {
            "AssignedBranch": 1
        }
    )

        if not branch_group:

            return {
            "success": False,
            "error": "Branch group not found"
        }


        assigned_branches = branch_group.get(
        "AssignedBranch",
        []
    )

        if not assigned_branches:

            return {
            "success": False,
            "error": "No branches assigned"
        }


    # ===============================
    # CONVERT BRANCH IDS
    # ===============================

        branch_ids = []

        for b in assigned_branches:

            try:
                branch_ids.append(
                ObjectId(str(b))
            )
            except:
                pass


    # ===============================
    # FIND VEHICLE
    # ===============================

        device = self.db["devices"].find_one(

        {

            "branchId": {

                "$in": branch_ids

            },

            "$or": [

                {
                    "name": {
                        "$regex": vehicle_input,
                        "$options": "i"
                    }
                },

                {
                    "deviceId": {
                        "$regex": vehicle_input,
                        "$options": "i"
                    }
                },

                {
                    "uniqueId": {
                        "$regex": vehicle_input,
                        "$options": "i"
                    }
                }

            ]

        }

    )


        if not device:

            return {

            "success": False,

            "error": "Vehicle not found"

        }


        return {
 
        "success": True,

        "vehicle": {

            "deviceId":
                str(device["_id"]),

            "vehicleName":
                device.get("name"),

            "uniqueId":
                str(device.get("uniqueId"))
                if device.get("uniqueId")
                else None,

            "deviceNumber":
                device.get("deviceId"),

            "branchId":
                str(device.get("branchId"))
                if device.get("branchId")
                else None,

            "schoolId":
                str(device.get("schoolId"))
                if device.get("schoolId")
                else None,

            "status":
                device.get("status"),

            "model":
                device.get("model"),

            "category":
                device.get("category")

        }

    }
    

    def get_branchgroup_specific_vehicle_geofence(
    self,
    group_id,
    vehicle_input,
    role,
    user
):

    # ==========================
    # CONVERT GROUP ID
    # ==========================

        try:
            group_object_id = ObjectId(str(group_id))
        except:
            group_object_id = group_id

    # ==========================
    # CLEAN INPUT
    # ==========================

        if isinstance(vehicle_input, dict):

            vehicle_input = (
            vehicle_input.get("vehicle_input")
            or vehicle_input.get("vehicle")
            or vehicle_input.get("vehicle_name")
        )

        vehicle_input = str(vehicle_input).strip()

        if not vehicle_input:

            return {
            "success": False,
            "message": "Vehicle name required."
        }

    # ==========================
    # VERIFY BRANCH GROUP
    # ==========================

        branch_group = self.db["branchgroups"].find_one(
        {
            "_id": group_object_id
        }
    )

        if not branch_group:

            return {
            "success": False,
            "message": "Branch group not found."
        }

    # ==========================
    # RBAC FILTER
    # ==========================

        device_filter = get_rbac_filter(
        role,
        user,
        "devices",
        self.db
    )

    # ==========================
    # FIND VEHICLE
    # ==========================

        query = {

        "$and": [

            device_filter,

            {

                "$or": [

                    {
                        "groupId": group_object_id
                    },

                    {
                        "groupId": str(group_object_id)
                    }

                ]

            },

            {

                "$or": [

                    {
                        "name": {
                            "$regex": f"^{vehicle_input}$",
                            "$options": "i"
                        }
                    },

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
                        "deviceId": {
                            "$regex": f"^{vehicle_input}$",
                            "$options": "i"
                        }
                    },

                    {
                        "uniqueId": vehicle_input
                    }

                ]

            }

        ]

    }

        device = self.db["devices"].find_one(query)

        if not device:

            return {
            "success": False,
            "message": "Vehicle not found in this branch group."
        }

    # ==========================
    # GET GEOFENCE
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

        geofence_query = {

        "$and": [

            geofence_filter,

            {

                "$or": [

                    {
                        "_id": geofence_id
                    }

                ]

            }

        ]

    }

        if ObjectId.is_valid(str(geofence_id)):

            geofence_query["$and"][1]["$or"].append(
            {
                "_id": ObjectId(str(geofence_id))
            }
        )

        geofence = self.db["geofences"].find_one(
        geofence_query
    )

        if not geofence:

            return {
            "success": False,
            "message": "Geofence not found."
        }

        return {

        "success": True,

        "branchGroup": {

            "groupId": str(branch_group["_id"]),

            "branchGroupName": branch_group.get("branchGroupName")

        },

        "vehicle": {

            "deviceId": str(device["_id"]),

            "vehicleName": (
                device.get("name")
                or device.get("vehicle_name")
                or device.get("vehicleNumber")
            ),

            "uniqueId": device.get("uniqueId"),

            "deviceNumber": device.get("deviceId"),

            "status": device.get("status")

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
    

    def get_branchgroup_specific_branch_vehicle_geofence(
    self,
    group_id,
    branch_name,
    vehicle_input,
    role,
    user
):

        try:

        # =====================================
        # CLEAN INPUT
        # =====================================

            branch_name = str(branch_name).strip()
            vehicle_input = str(vehicle_input).strip()

            if not branch_name or not vehicle_input:
                return {
                "success": False,
                "message": "Branch name and vehicle name required."
            }

        # =====================================
        # GROUP ID
        # =====================================

            try:
                group_id = ObjectId(str(group_id))
            except:
                pass

        # =====================================
        # FIND BRANCH GROUP
        # =====================================

            branch_group = self.db.branchgroups.find_one(
            {
                "_id": group_id
            }
        )

            if not branch_group:
                return {
                "success": False,
                "message": "Branch group not found."
            }

            assigned_branches = branch_group.get(
            "AssignedBranch",
            []
        )

            if not assigned_branches:
                return {
                "success": False,
                "message": "No branches assigned."
            }

        # =====================================
        # CONVERT IDS
        # =====================================

            branch_ids = []
 
            for b in assigned_branches:

                try:
                    branch_ids.append(
                    ObjectId(str(b))
                )
                except:
                    pass

            print("BRANCH IDS =", branch_ids)
            print("BRANCH INPUT =", branch_name)

        # =====================================
        # FIND BRANCH
        # =====================================

            branch = self.db.branches.find_one({

            "_id": {
                "$in": branch_ids
            },

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
                },

                {
                    "name": {
                        "$regex": branch_name,
                        "$options": "i"
                    }
                }

            ]

        })

            print("FOUND BRANCH =", branch)

            if not branch:
                return {
                "success": False,
                "message": "Branch not found in this branch group."
            }

        # =====================================
        # DEVICE RBAC
        # =====================================

            device_filter = get_rbac_filter(
            role,
            user,
            "devices",
            self.db
        )

        # =====================================
        # FIND VEHICLE
        # =====================================

            
            device = self.db.devices.find_one({

    "$and": [

        {
            "$or": [
                {"branchId": branch["_id"]},
                {"branchId": str(branch["_id"])}
            ]
        },

        {
            "$or": [

                {
                    "name": {
                        "$regex": f"^{vehicle_input.strip()}$",
                        "$options": "i"
                    }
                },

                {
                    "deviceId": {
                        "$regex": f"^{vehicle_input.strip()}$",
                        "$options": "i"
                    }
                },

                {
                    "uniqueId": {
                        "$regex": f"^{vehicle_input.strip()}$",
                        "$options": "i"
                    }
                }

            ] 
        }

    ]

})
        # =====================================
        # FIND ROUTE
        # =====================================

            route = self.db.routes.find_one({

            "$or": [

                {
                    "deviceObjId": device["_id"]
                },

                {
                    "deviceObjId": str(device["_id"])
                }

            ]

        })

            if not route:
                return {
                "success": False,
                "message": "Route not assigned."
            }

        # =====================================
        # FIND GEOFENCE
        # =====================================

            geofence = self.db.geofences.find_one({

            "$or": [

                {
                    "routeObjId": route["_id"]
                },

                {
                    "routeObjId": str(route["_id"])
                }

            ]

        })

            if not geofence:
                return {
                "success": False,
                "message": "Geofence not found."
            }

        # =====================================
        # RESPONSE
        # =====================================

            return {

            "success": True,

            "branch": {

                "branchId": str(branch["_id"]),
                "branchName": branch.get("branchName")

            },

            "vehicle": {

                "deviceId": str(device["_id"]),
                "vehicleName": (
                    device.get("vehicleNumber")
                    or device.get("vehicle_name")
                    or device.get("name")
                ),
                "uniqueId": device.get("uniqueId")

            },

            "route": {

                "routeId": str(route["_id"]),
                "routeNumber": route.get("routeNumber")

            },

            "geofence": self.clean(geofence)

        }

        except Exception as e:

            print("ERROR =", e)

            return {
            "success": False,
            "error": str(e)
        }
    def get_branchgroup_school_vehicle_geofence(
    self,
    group_id,
    vehicle_input,
    role,
    user
):

        try:

        # =====================================
        # CLEAN INPUT
        # =====================================

            vehicle_input = str(vehicle_input).strip()

            if not vehicle_input:

                return {
                "success": False,
                "message": "Vehicle name required."
            }



        # =====================================
        # GROUP ID CONVERSION
        # =====================================

            try:
                group_id = ObjectId(str(group_id))

            except:
                pass



        # =====================================
        # FIND BRANCH GROUP
        # =====================================

            branch_group = self.db.branchgroups.find_one(
            {
                "_id": group_id
            }
        )


            if not branch_group:

                return {
                "success": False,
                "message": "Branch group not found."
            }



        # =====================================
        # GET ASSIGNED BRANCHES
        # =====================================

            assigned_branches = branch_group.get(
            "AssignedBranch",
            []
        )


            if not assigned_branches:

                return {
                "success": False,
                "message": "No branches assigned."
            }



            print(
            "ASSIGNED BRANCHES =",
            assigned_branches
        )



        # =====================================
        # CONVERT BRANCH IDS
        # =====================================

            branch_ids = []


            for b in assigned_branches:

                try:

                    branch_ids.append(
                    ObjectId(str(b))
                )

                except:

                    pass



            if not branch_ids:

                return {
                "success":False,
                "message":"Invalid branch ids."
            }



            print(
            "BRANCH IDS =",
            branch_ids
        )



        # =====================================
        # DEVICE RBAC
        # =====================================

            device_filter = get_rbac_filter(
            role,
            user,
            "devices",
            self.db
        )


            if device_filter.get("_id") is None:

                device_filter = {}



        # =====================================
        # FIND VEHICLE
        # =====================================


            device_query = {


            "$and":[


                {

                    "$or":[


                        {
                            "branchId":{
                                "$in":branch_ids
                            }
                        },


                        {
                            "branchId":{
                                "$in":[
                                    str(x)
                                    for x in branch_ids
                                ]
                            }
                        }


                    ]

                },


                {


                    "$or":[


                        {
                            "name":{
                                "$regex":vehicle_input,
                                "$options":"i"
                            }
                        },


                        {
                            "vehicleNumber":{
                                "$regex":vehicle_input,
                                "$options":"i"
                            }
                        },


                        {
                            "deviceId":{
                                "$regex":vehicle_input,
                                "$options":"i"
                            }
                        },


                        {
                            "uniqueId":{
                                "$regex":vehicle_input,
                                "$options":"i"
                            }
                        }


                    ]


                }


            ]

        }



            if device_filter:

                device_query["$and"].append(
                device_filter
            )



            print(
            "DEVICE QUERY =",
            device_query
        )



            device = self.db.devices.find_one(
            device_query
        )



            if not device:

                return {

                "success":False,

                "message":
                    "Vehicle not found in branchgroup school."

            }



            print(
            "DEVICE FOUND =",
            device
        )



        # =====================================
        # FIND ROUTE
        # =====================================


            route = self.db.routes.find_one(

            {

                "$or":[

                    {
                        "deviceObjId":
                            device["_id"]
                    },


                    {
                        "deviceObjId":
                            str(device["_id"])
                    }

                ]

            }

        )



            if not route:

                return {

                "success":False,

                "message":
                    "Route not assigned."

            }



        # =====================================
        # FIND GEOFENCE
        # =====================================


            geofence = self.db.geofences.find_one(

            {

                "$or":[


                    {
                        "routeObjId":
                            route["_id"]
                    },


                    {
                        "routeObjId":
                            str(route["_id"])
                    }


                ]

            }

        )



            if not geofence:

                return {

                "success":False,

                "message":
                    "Geofence not found."

            }



        # =====================================
        # RESPONSE
        # =====================================


            return {


            "success":True,


            "vehicle":{


                "deviceId":
                    str(device["_id"]),


                "vehicleName":
                    (
                        device.get("vehicleNumber")
                        or
                        device.get("vehicle_name")
                        or
                        device.get("name")
                    ),


                "uniqueId":
                    device.get("uniqueId")

            },


            "route":{


                "routeId":
                    str(route["_id"]),


                "routeNumber":
                    route.get("routeNumber")

            },


            "geofence":
                self.clean(geofence)

        }



        except Exception as e:


            print(
            "ERROR =",
            e
        )


            return {

            "success":False,

            "error":
                str(e)

        }
    def get_branchgroup_specific_branch_vehicle_today_distance(
    self,
    group_id,
    branch_name,
    vehicle_input,
    role,
    user
):

        try:

        # =====================================
        # CLEAN INPUT
        # =====================================

            branch_name = str(branch_name).strip()
            vehicle_input = str(vehicle_input).strip()

            if not branch_name or not vehicle_input:
                return {
                "success": False,
                "message": "Branch name and vehicle name required."
            }


        # =====================================
        # GROUP ID
        # =====================================

            try:
                group_id = ObjectId(str(group_id))
            except:
                pass


        # =====================================
        # FIND BRANCH GROUP
        # =====================================

            branch_group = self.db.branchgroups.find_one(
            {
                "_id": group_id
            }
        )


            if not branch_group:
                return {
                "success": False,
                "message": "Branch group not found."
            }


            assigned_branches = branch_group.get(
            "AssignedBranch",
            []
        )


            if not assigned_branches:
                return {
                "success": False,
                "message": "No branches assigned."
            }



        # =====================================
        # CONVERT BRANCH IDS
        # =====================================

            branch_ids = []

            for b in assigned_branches:

                try:
                    branch_ids.append(
                    ObjectId(str(b))
                )

                except:
                    pass



        # =====================================
        # FIND BRANCH
        # =====================================

            branch = self.db.branches.find_one(

            {

                "_id": {
                    "$in": branch_ids
                },

                "$or":[

                    {
                        "branchName":{
                            "$regex":branch_name,
                            "$options":"i"
                        }
                    },

                    {
                        "username":{
                            "$regex":branch_name,
                            "$options":"i"
                        }
                    },

                    {
                        "name":{
                            "$regex":branch_name,
                            "$options":"i"
                        }
                    }

                ]

            }

        )


            if not branch:

                return {
                "success":False,
                "message":"Branch not found in this branch group."
            }




        # =====================================
        # FIND DEVICE
        # =====================================

            device_filter = get_rbac_filter(
            role,
            user,
            "devices",
            self.db
        )


            if device_filter.get("_id") is None:
                device_filter = {}



            device_query = {

            "$and":[


                {

                    "$or":[

                        {
                            "branchId":branch["_id"]
                        },

                        {
                            "branchId":str(branch["_id"])
                        }

                    ]

                },


                {

                    "$or":[

                        {
                            "name":{
                                "$regex":vehicle_input,
                                "$options":"i"
                            }
                        },

                        {
                            "vehicleNumber":{
                                "$regex":vehicle_input,
                                "$options":"i"
                            }
                        },

                        {
                            "deviceId":{
                                "$regex":vehicle_input,
                                "$options":"i"
                            }
                        },

                        {
                            "uniqueId":{
                                "$regex":vehicle_input,
                                "$options":"i"
                            }
                        }

                    ]

                }

            ]

        }



            if device_filter:

                device_query["$and"].append(
                device_filter
            )



            print(
            "DEVICE QUERY =",
            device_query
        )



            device = self.db.devices.find_one(
            device_query
        )



            if not device:

                return {

                "success":False,
                "message":"Vehicle not found in this branch."

            }



        # =====================================
        # UNIQUE IDS
        # =====================================

            unique_ids = self.normalize_unique_id(
            device.get("uniqueId")
        )



        # =====================================
        # TODAY IST TIME
        # =====================================

            IST = timezone(
            timedelta(hours=5, minutes=30)
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
        # HISTORY AGGREGATION
        # =====================================

            pipeline = [

            {

                "$match":{

                    "$and":[


                        get_rbac_filter(
                            role,
                            user,
                            "histories",
                            self.db
                        ),


                        {

                            "uniqueId":{
                                "$in":unique_ids
                            }

                        },


                        {

                            "attributes.totalDistance":{
                                "$ne":None
                            }

                        },


                        {

                            "createdAt":{

                                "$gte":today_start,
                                "$lte":today_end

                            }

                        }

                    ]

                }

            },


            {

                "$sort":{

                    "createdAt":1

                }

            },


            {

                "$project":{

                    "_id":0,

                    "name":1,

                    "createdAt":1,


                    "totalDistanceKm":{

                        "$divide":[

                            "$attributes.totalDistance",
                            1000

                        ]

                    }

                }

            },


            {

                "$group":{


                    "_id":None,


                    "vehicleName":{

                        "$first":"$name"

                    },


                    "startDistance":{

                        "$first":"$totalDistanceKm"

                    },


                    "endDistance":{

                        "$last":"$totalDistanceKm"

                    },


                    "firstRecord":{

                        "$first":"$createdAt"

                    },


                    "lastRecord":{

                        "$last":"$createdAt"

                    }


                }

            },


            {

                "$project":{


                    "_id":0,


                    "vehicleName":1,


                    "firstRecord":1,


                    "lastRecord":1,


                    "todayDistance":{

                        "$round":[


                            {

                                "$subtract":[

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
            self.db.histories.aggregate(
                pipeline
            )
        )



            if not report:

                return {

                "success":False,

                "message":"No history found for today."

            }



            report = report[0]



        # =====================================
        # RESPONSE
        # =====================================

            return {


            "success":True,


            "branch":{

                "branchId":str(branch["_id"]),

                "branchName":branch.get("branchName")

            },


            "vehicle":{


                "deviceId":str(device["_id"]),

                "vehicleName":(
                    device.get("vehicleNumber")
                    or device.get("vehicle_name")
                    or device.get("name")
                ),

                "uniqueId":device.get("uniqueId")

            },


            "todayAccurateDistance":{


                "date":now.strftime("%Y-%m-%d"),

                "distanceKm":report.get(
                    "todayDistance"
                ),

                "firstRecord":report.get(
                    "firstRecord"
                ),

                "lastRecord":report.get(
                    "lastRecord"
                )

            }

        }



        except Exception as e:

            print(
            "ERROR =",
            e
        )

            return {

            "success":False,
            "error":str(e)

        }
    def get_branchgroup_vehicle_today_distance(
    self,
    group_id,
    vehicle_input,
    role,
    user
):

        try:

        # =====================================
        # FIND VEHICLE
        # =====================================

            result = self.get_branchgroup_specific_vehicle(
            group_id,
            vehicle_input
        )

            if not result["success"]:
                return result

            vehicle = result["vehicle"]

            unique_ids = self.normalize_unique_id(
            vehicle["uniqueId"]
        )

        # =====================================
        # TODAY IST
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
        # HISTORY PIPELINE
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
            self.db.histories.aggregate(
                pipeline
            )
        )

            if not report:
                return {
                "success": False,
                "message": "No history found for today."
            }

            report = report[0]

        # =====================================
        # RESPONSE
        # =====================================

            return {

            "success": True,

            "vehicle": {

                "deviceId": vehicle.get("deviceId"),

                "vehicleName": vehicle.get("vehicleName"),

                "uniqueId": vehicle.get("uniqueId")

            },

            "todayAccurateDistance": {

                "date": now.strftime("%Y-%m-%d"),

                "distanceKm": report["todayDistance"],

                "firstRecord": report["firstRecord"],

                "lastRecord": report["lastRecord"]

            }

        }

        except Exception as e:

            print(e)

            return {
            "success": False,
            "error": str(e)
        }
    
    def get_branchgroup_specific_branch_vehicle_km_report(
    self,
    group_id,
    branch_name,
    vehicle_input,
    role,
    user
):

        try:

        # =====================================
        # CLEAN INPUT
        # =====================================

            branch_name = str(branch_name).strip()
            vehicle_input = str(vehicle_input).strip()


            if not branch_name or not vehicle_input:
                return {
                "success": False,
                "message": "Branch name and vehicle name required."
            }


        # =====================================
        # GROUP ID
        # =====================================

            try:
                group_id = ObjectId(str(group_id))
            except:
                pass


        # =====================================
        # FIND BRANCH GROUP
        # =====================================

            branch_group = self.db.branchgroups.find_one(
            {
                "_id": group_id
            }
        )


            if not branch_group:
                return {
                "success": False,
                "message": "Branch group not found."
            }


            assigned_branches = branch_group.get(
            "AssignedBranch",
            []
        )


            branch_ids = []


            for b in assigned_branches:

                try:
                    branch_ids.append(
                    ObjectId(str(b))
                )
                except:
                    pass



        # =====================================
        # FIND BRANCH
        # =====================================

            branch = self.db.branches.find_one(

            {

                "_id": {
                    "$in": branch_ids
                },


                "$or":[

                    {
                        "branchName":{
                            "$regex":branch_name,
                            "$options":"i"
                        }
                    },

                    {
                        "name":{
                            "$regex":branch_name,
                            "$options":"i"
                        }
                    },

                    {
                        "username":{
                            "$regex":branch_name,
                            "$options":"i"
                        }
                    }

                ]

            }

        )


            if not branch:
                return {
                "success":False,
                "message":"Branch not found in this branch group."
            }



        # =====================================
        # DEVICE RBAC
        # =====================================

            device_filter = get_rbac_filter(
            role,
            user,
            "devices",
            self.db
        )


        # remove invalid RBAC

            if (
            not device_filter
            or (
                "_id" in device_filter
                and device_filter["_id"] is None
            )
        ):

                device_filter = {}



        # =====================================
        # FIND VEHICLE
        # =====================================

            device_query = {

            "$and":[


                {
                    "$or":[

                        {
                            "branchId":branch["_id"]
                        },

                        {
                            "branchId":str(branch["_id"])
                        }

                    ]
                },


                {

                    "$or":[


                        {
                            "name":{
                                "$regex":vehicle_input,
                                "$options":"i"
                            }
                        },


                        {
                            "vehicleNumber":{
                                "$regex":vehicle_input,
                                "$options":"i"
                            }
                        },


                        {
                            "deviceId":{
                                "$regex":vehicle_input,
                                "$options":"i"
                            }
                        },


                        {
                            "uniqueId":{
                                "$regex":vehicle_input,
                                "$options":"i"
                            }
                        }

                    ]

                }

            ]

        }



            if device_filter:

                device_query["$and"].append(
                device_filter
            )


            print(
            "FINAL DEVICE QUERY =",
            device_query
        )


            device = self.db.devices.find_one(
            device_query
        )


            if not device:

                return {

                "success":False,
                "message":"Vehicle not found in this branch."

            }



        # =====================================
        # UNIQUE ID
        # =====================================

            unique_ids = self.normalize_unique_id(
            device.get("uniqueId")
        )



        # =====================================
        # GET REPORT DISTANCES
        # =====================================


            report_distances = list(

            self.db["report_distances"].find(

                {

                    "$and":[


                        get_rbac_filter(
                            role,
                            user,
                            "report_distances",
                            self.db
                        ),


                        {
                            "uniqueId":{
                                "$in":unique_ids
                            }
                        }

                    ]

                }

            )

            .sort(
                "createdAt",
                -1
            )

        )



            if not report_distances:

                return {

                "success":False,
                "message":"No distance reports found for vehicle."

            }




        # =====================================
        # BUILD DATE MAP
        # =====================================


            report_map = {}


            for r in report_distances:

                date = r["createdAt"].date()

                report_map[date] = (

                    report_map.get(date,0)

                +

                float(
                    r.get(
                        "distance",
                        0
                    )
                )

            )



            today = datetime.utcnow().date()



            available_dates = sorted(
            report_map.keys()
        )



        # =====================================
        # ACTIVE STATUS
        # =====================================


            if today in report_map:

                analysis_date = today
                status = "active"
                message = "Vehicle is active today."


            else:

                analysis_date = available_dates[-1]

                status = "inactive"

                message = (
                f"Vehicle not active today. "
                f"Last active {analysis_date}"
            )



            current_km = round(
            report_map.get(
                analysis_date,
                0
            ),
            2
        )



        # =====================================
        # PREVIOUS DAY
        # =====================================


            previous_date = None


            for d in reversed(available_dates):

                if d < analysis_date:

                    previous_date = d
                    break



            yesterday_km = round(

            report_map.get(
                previous_date,
                0
            ),

            2

        )



        # =====================================
        # WEEK
        # =====================================


            week_start = (
            analysis_date
            -
            timedelta(
                days=analysis_date.weekday()
            )
        )


            week_total = 0


            for d,v in report_map.items():

                if week_start <= d <= analysis_date:

                    week_total += v



            week_total = round(
            week_total,
            2
        )



        # =====================================
        # MONTH 30 DAYS
        # =====================================


            month_start = (

            analysis_date
            -
            timedelta(
                days=29
            )

        )


            month_total = 0


            for d,v in report_map.items():

                if month_start <= d <= analysis_date:

                    month_total += v



            month_total = round(
            month_total,
            2
        )



        # =====================================
        # RESPONSE
        # =====================================


            return {


            "success":True,


            "status":status,


            "message":message,


            "branch":{

                "branchId":str(branch["_id"]),

                "branchName":
                    branch.get("branchName")

            },


            "vehicle":{

                "deviceId":
                    str(device["_id"]),

                "vehicleName":
                    (
                        device.get("vehicleNumber")
                        or device.get("name")
                    ),

                "uniqueId":
                    device.get("uniqueId"),

                "status":
                    device.get("status"),

                "model":
                    device.get("model")

            },


            "distanceReport":{


                "current":{

                    "label":
                        "Today"
                        if status=="active"
                        else "Last Active",

                    "km":
                        current_km

                },


                "yesterday":{

                    "date":
                        (
                            previous_date.strftime("%Y-%m-%d")
                            if previous_date
                            else None
                        ),

                    "km":
                        yesterday_km

                },


                "week":{

                    "from":
                        week_start.strftime("%Y-%m-%d"),

                    "to":
                        analysis_date.strftime("%Y-%m-%d"),

                    "totalKm":
                        week_total

                },


                "month":{

                    "type":
                        "rolling_30_days",

                    "from":
                        month_start.strftime("%Y-%m-%d"),

                    "to":
                        analysis_date.strftime("%Y-%m-%d"),

                    "totalKm":
                        month_total

                }

            }

        }



        except Exception as e:


            print(
            "ERROR =",
            e
        )


            return {

            "success":False,
            "error":str(e)

            }
    def get_branchgroup_vehicle_km_report(
    self,
    group_id,
    vehicle_input,
    role,
    user
):

        try:

        # =====================================
        # 1. FIND VEHICLE (BRANCHGROUP)
        # =====================================

            result = self.get_branchgroup_specific_vehicle(
            group_id,
            vehicle_input
        )

            if not result["success"]:
                return result

            vehicle = result["vehicle"]

            unique_ids = self.normalize_unique_id(
            vehicle["uniqueId"]
        )

        # =====================================
        # 2. FETCH REPORT DISTANCES
        # =====================================

            report_distances = list(
            self.db.report_distances.find({

                "$and": [

                    get_rbac_filter(
                        role,
                        user,
                        "report_distances",
                        self.db
                    ),

                    {
                        "uniqueId": {
                            "$in": unique_ids
                        }
                    }

                ]

            }).sort("createdAt", -1)
        )

            if not report_distances:

                return {
                "success": False,
                "message": "No distance reports found."
            }

        # =====================================
        # 3. BUILD DATE MAP
        # =====================================

            report_map = {

            r["createdAt"].date():
            float(r.get("distance", 0))

                for r in report_distances

        }

            today = datetime.utcnow().date()

            available_dates = sorted(
            report_map.keys()
        )

        # =====================================
        # 4. ACTIVE / INACTIVE
        # =====================================

            if today in report_map:

                status = "active"

                analysis_base_date = today

                message = "Vehicle is active today."

            else:

                status = "inactive"

                analysis_base_date = available_dates[-1]

                message = (
                f"Vehicle is not active today. "
                f"Last active was on {analysis_base_date}"
            )

            current_km = round(
            report_map.get(
                analysis_base_date,
                0
            ),
            2
        )

            previous_active_date = None

            for d in reversed(available_dates):

                if d < analysis_base_date:

                    previous_active_date = d

                    break

            yesterday_km = round(

                report_map.get(
                previous_active_date,
                0
            ),

            2

        ) if previous_active_date else 0

        # =====================================
        # 5. WEEK TOTAL
        # =====================================

            week_start = analysis_base_date - timedelta(
            days=analysis_base_date.weekday()
        )

            week_end = week_start + timedelta(days=6)

            week_total = round(

                sum(

                float(r.get("distance", 0))

                    for r in report_distances

                    if week_start <=
                r["createdAt"].date()
                <= week_end

            ),

            2

        )

        # =====================================
        # 6. MONTH TOTAL
        # =====================================

            month_start = analysis_base_date - timedelta(days=29)

            month_total = round(

            sum(

                float(r.get("distance", 0))

                for r in report_distances

                if month_start <=
                r["createdAt"].date()
                <= analysis_base_date

            ),

            2

        )

        # =====================================
        # 7. RESPONSE
        # =====================================

            return {

            "success": True,

            "status": status,

            "message": message,

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

                    "label": (
                        "Today"
                        if status == "active"
                        else "Last Active"
                    ),

                    "km": current_km

                },

                "yesterday": {

                    "date": (
                        previous_active_date.strftime("%Y-%m-%d")
                        if previous_active_date
                        else None
                    ),

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

                    "to": analysis_base_date.strftime("%Y-%m-%d"),

                    "totalKm": month_total

                }

            }

        }

        except Exception as e:

            print("ERROR =", e)

            return {

            "success": False,

            "error": str(e)

        }
    
    def get_branchgroup_specific_branch_vehicles_g(
    self,
    branch_name,
    vehicle_input,
    role,
    user
):

        try:

            branch_name = str(branch_name).strip()
            vehicle_input = str(vehicle_input).strip()


            if not branch_name or not vehicle_input:
                return {
                "success": False,
                "message": "Branch name and vehicle name required"
            }


        # ===============================
        # GROUP ID
        # ===============================

            group_id = (
            user.get("groupId")
            or user.get("branchGroupId")
            or user.get("_id")
        )


            try:
                group_id = ObjectId(str(group_id))
            except:
                pass



        # ===============================
        # FIND GROUP
        # ===============================

            branch_group = self.db["branchgroups"].find_one(
            {
                "_id": group_id
            }
        )


            if not branch_group:

                return {
                "success":False,
                "message":"Branch group not found"
            }



            assigned_branches = branch_group.get(
            "AssignedBranch",
            []
        )


            branch_ids=[]


            for b in assigned_branches:

                try:
                    branch_ids.append(
                    ObjectId(str(b))
                )
                except:
                    pass



        # ===============================
        # FIND BRANCH
        # ===============================

            branch = self.db["branches"].find_one(

            {

                "_id":{
                    "$in":branch_ids
                },


                "$or":[

                    {
                        "branchName":{
                            "$regex":branch_name,
                            "$options":"i"
                        }
                    },

                    {
                        "name":{
                            "$regex":branch_name,
                            "$options":"i"
                        }
                    }

                ]

            }

        )


            if not branch:

                return {
                "success":False,
                "message":"Branch not found in branch group"
            }



        # ===============================
        # DEVICE RBAC
        # ===============================

            device_filter = get_rbac_filter(
            role,
            user,
            "devices",
            self.db
        )


        # ===============================
        # FIND VEHICLE
        # ===============================


            vehicle = self.db["devices"].find_one(

            {

                "$and":[

                    {

                        "$or":[

                            {
                                "branchId":branch["_id"]
                            },

                            {
                                "branchId":str(branch["_id"])
                            }

                        ]

                    },


                    {

                        "$or":[

                            {
                                "name":{
                                    "$regex":vehicle_input,
                                    "$options":"i"
                                }
                            },

                            {
                                "vehicleNumber":{
                                    "$regex":vehicle_input,
                                    "$options":"i"
                                }
                            },


                            {
                                "deviceId":{
                                    "$regex":vehicle_input,
                                    "$options":"i"
                                }
                            },


                            {
                                "uniqueId":{
                                    "$regex":vehicle_input,
                                    "$options":"i"
                                }
                            }

                        ]

                    },

                    device_filter

                ]

            }

        )



            if not vehicle:

                return {
                "success":False,
                "message":"Vehicle not found in this branch"
            }



            return {


            "success":True,


            "branch":{

                "branchId":str(branch["_id"]),

                "branchName":
                    branch.get("branchName")

            },


            "vehicle":{

                "deviceId":
                    str(vehicle["_id"]),


                "vehicleName":
                    (
                        vehicle.get("vehicleNumber")
                        or vehicle.get("name")
                    ),


                "uniqueId":
                    vehicle.get("uniqueId"),


                "deviceNumber":
                    vehicle.get("deviceId"),


                "status":
                    vehicle.get("status"),


                "model":
                    vehicle.get("model")

            }

        }



        except Exception as e:


            return {

            "success":False,
            "error":str(e)

        }
    def get_branchgroup_specific_branch_vehicle_distance_report(
    self,
    branch_name,
    vehicle_input,
    role,
    user,
    limit=100
):

        try:


        # ===============================
        # FIND VEHICLE
        # ===============================


            result = self.get_branchgroup_specific_branch_vehicles(

            branch_name,

            vehicle_input,

            role,

            user

        )


            if not result["success"]:
                return result



            vehicle = result["vehicle"]



        # ===============================
        # UNIQUE IDS
        # ===============================


            unique_ids = self.normalize_unique_id(

            vehicle.get("uniqueId")

        )


            print(
            "REPORT UNIQUE IDS =",
            unique_ids
        )



        # ===============================
        # REPORT FILTER
        # ===============================


            report_filter = get_rbac_filter(

            role,

            user,

            "report_distances",

            self.db

        )



            reports = list(

            self.db["report_distances"].find(

                {

                    "$and":[


                        report_filter,


                        {

                            "uniqueId":{

                                "$in":unique_ids

                            }

                        }


                    ]

                }

            )

            .sort(
                "createdAt",
                -1
            )

            .limit(limit)

        )



            print(
            "DISTANCE REPORT COUNT =",
            len(reports)
        )



            return {


            "success":True,


            "branch":

                result["branch"],



            "vehicle":

                vehicle,



            "reports":[

                self.clean(r)

                for r in reports

            ]

        }



        except Exception as e:


            return {

            "success":False,

            "error":str(e)

        }
    def get_branchgroup_specific_branch_vehicle_status(
    self,
    branch_name,
    vehicle_input,
    role,
    user,
    limit=100
):

        try:

        # =====================================
        # 1. FIND VEHICLE USING EXISTING FUNCTION
        # =====================================

            result = self.get_branchgroup_specific_branch_vehicles(
            branch_name,
            vehicle_input,
            role,
            user
        )


            if not result["success"]:
                return result



            vehicle = result["vehicle"]

            branch = result["branch"]



        # =====================================
        # 2. CALL EXISTING STATUS REPORT LOGIC
        # =====================================

            status_report = self.report_status_engine.get_single_branch_vehicle_status_report(

            branch["branchId"],

            vehicle["uniqueId"],

            role,

            user,

            limit

        )



        # =====================================
        # 3. RESPONSE
        # =====================================

            return {


            "success": True,


            "branch": branch,


            "vehicle": vehicle,


            "statusReport": status_report

        }



        except Exception as e:


            return {

            "success": False,

            "error": str(e)

        }
    def get_branchgroup_specific_branch_vehicle_travel_summary(
    self,
    branch_name,
    vehicle_input,
    role,
    user,
    limit=100
):

        try:

        # =====================================
        # 1. FIND VEHICLE FROM BRANCHGROUP BRANCH
        # =====================================

            result = self.get_branchgroup_specific_branch_vehicles(
            branch_name,
            vehicle_input,
            role,
            user
        )


            if not result["success"]:
                return result



            vehicle = result["vehicle"]

            branch = result["branch"]



        # =====================================
        # 2. TRAVEL SUMMARY RBAC
        # =====================================

            summary_filter = get_rbac_filter(
            role,
            user,
            "report_travelsummaries",
            self.db
        )



        # =====================================
        # 3. FETCH TRAVEL SUMMARY
        # =====================================

            reports = list(

            self.db["report_travelsummaries"].find(

                {

                    "$and":[

                        summary_filter,


                        {

                            "uniqueId":{

                                "$in":
                                self.normalize_unique_id(
                                    vehicle["uniqueId"]
                                )

                            }

                        }

                    ]

                }

            )

            .sort(
                "startTime",
                -1
            )

            .limit(limit)

        )



        # =====================================
        # 4. RESPONSE
        # =====================================

            return {


            "success":True,


            "branch":branch,


            "vehicle":{

                "deviceId":
                    vehicle.get("deviceId"),


                "vehicleName":
                    vehicle.get("vehicleName"),


                "name":
                    vehicle.get("vehicleName"),


                "deviceNumber":
                    vehicle.get("deviceNumber"),


                "uniqueId":
                    vehicle.get("uniqueId"),


                "model":
                    vehicle.get("model")

            },


            "travelSummary":[

                self.clean(r)

                for r in reports

            ]

        }



        except Exception as e:


            return {

            "success":False,

            "error":str(e)

        }
    def get_branchgroup_specific_branch_vehicle_last_position(
    self,
    branch_name,
    vehicle_input,
    role,
    user
):

        try:

        # =====================================
        # 1. FIND VEHICLE FROM BRANCHGROUP
        # =====================================

            result = self.get_branchgroup_specific_branch_vehicles(
            branch_name,
            vehicle_input,
            role,
            user
        )


            if not result["success"]:
                return result


            vehicle = result["vehicle"]

            branch = result["branch"]



        # =====================================
        # 2. FIND LAST POSITION
        # =====================================

            position = self.db["vehiclelastpositions"].find_one(

            {

                "$and":[


                    get_rbac_filter(
                        role,
                        user,
                        "vehiclelastpositions",
                        self.db
                    ),


                    {

                        "uniqueId":
                        str(vehicle["uniqueId"])

                    }

                ]

            }

        )



            if not position:

                return {

                "success":False,

                "message":"No last position found."

            }



        # =====================================
        # 3. ADDRESS FALLBACK
        # =====================================

            address = position.get("address")


            if not address:

                latitude = position.get("latitude")

                longitude = position.get("longitude")


                if latitude is not None and longitude is not None:

                    address = self.get_address(
                    latitude,
                    longitude
                )



        # =====================================
        # 4. RESPONSE
        # =====================================

            return {


            "success":True,


            "branch":branch,


            "vehicle":{

                "deviceId":
                    vehicle.get("deviceId"),


                "vehicleName":
                    vehicle.get("vehicleName"),


                "name":
                    vehicle.get("vehicleName"),


                "deviceNumber":
                    vehicle.get("deviceNumber"),


                "uniqueId":
                    vehicle.get("uniqueId"),


                "model":
                    vehicle.get("model")

            },


            "lastPosition":{


                "latitude":
                    position.get("latitude"),


                "longitude":
                    position.get("longitude"),


                "speed":
                    position.get("speed"),


                "course":
                    position.get("course"),


                "accuracy":
                    position.get("accuracy"),


                "altitude":
                    position.get("altitude"),


                "address":
                    address,


                "protocol":
                    position.get("protocol"),


                "deviceTime":
                    position.get("deviceTime"),


                "fixTime":
                    position.get("fixTime"),


                "serverTime":
                    position.get("serverTime"),


                "lastUpdate":
                    position.get("lastUpdate"),


                "valid":
                    position.get("valid"),


                "outdated":
                    position.get("outdated")

            }


        }



        except Exception as e:


            return {

            "success":False,

            "error":str(e)

        }
    from bson import ObjectId
   
    

    def get_branchgroup_specific_vehicle_geofences(
    self,
    group_id,
    vehicle_input,
    role,
    user
):

        try:

        # =====================================
        # GET GROUP ID
        # =====================================

            if not group_id:
                group_id = (
                user.get("groupId")
                or user.get("branchGroupId")
                or user.get("_id")
            )

            try:
                group_id = ObjectId(str(group_id))
            except:
                return {
                "success": False,
                "message": "Invalid Branch Group ID"
            }

        # =====================================
        # CLEAN INPUT
        # =====================================

            if isinstance(vehicle_input, dict):

                vehicle_input = (
                vehicle_input.get("vehicle_input")
                or vehicle_input.get("vehicle")
                or vehicle_input.get("vehicle_name")
            )

            vehicle_input = str(vehicle_input).strip()

            if not vehicle_input:
                return {
                "success": False,
                "message": "Vehicle name is required."
            }

        # =====================================
        # FIND BRANCH GROUP
        # =====================================

            group = self.db["branchgroups"].find_one(
            {"_id": group_id}
        )

            if not group:
                return {
                "success": False,
                "message": "Branch Group not found."
            }

            assigned_branches = group.get("AssignedBranch", [])

            if not assigned_branches:
                return {
                "success": False,
                "message": "No branches assigned."
            }

        # =====================================
        # CONVERT BRANCH IDS
        # =====================================

            branch_ids = []

            for b in assigned_branches:
                try:
                    branch_ids.append(ObjectId(str(b)))
                except:
                    pass

        # =====================================
        # FIND VEHICLE
        # =====================================

            vehicle = self.db["devices"].find_one({

            "branchId": {
                "$in": branch_ids
            },

            "$or": [

                {
                    "name": {
                        "$regex": vehicle_input,
                        "$options": "i"
                    }
                },

                {
                    "deviceId": {
                        "$regex": vehicle_input,
                        "$options": "i"
                    }
                },

                {
                    "uniqueId": {
                        "$regex": vehicle_input,
                        "$options": "i"
                    }
                }

            ]

        })

            if not vehicle:
                return {
                "success": False,
                "message": "Vehicle not found in your Branch Group."
            }

        # =====================================
        # GET UNIQUE ID
        # =====================================

            unique_id = vehicle.get("uniqueId")

        # =====================================
        # FIND GEOFENCES
        # =====================================

            geofences = list(

            self.db["geofences"].find({

                "$or": [

                    {
                        "uniqueId": unique_id
                    },

                    {
                        "uniqueId": str(unique_id)
                    }

                ]

            }).sort("createdAt", -1)

        )

        # =====================================
        # FORMAT RESULT
        # =====================================

            result = []

            for geo in geofences:

                result.append({

                "geofenceId": str(geo["_id"]),

                "geofenceName": geo.get("geofenceName") or geo.get("name"),

                "address": geo.get("address"),

                "description": geo.get("description"),

                "schoolId": str(geo.get("schoolId")) if geo.get("schoolId") else None,

                "branchId": str(geo.get("branchId")) if geo.get("branchId") else None,

                "coordinates": geo.get("coordinates"),

                "type": geo.get("type"),

                "active": geo.get("Active")

            })

        # =====================================
        # RESPONSE
        # =====================================

            return {

            "success": True,

            "branchGroup": {

                "groupId": str(group["_id"]),

                "branchGroupName": group.get("branchGroupName")

            },

            "vehicle": {

                "deviceId": str(vehicle["_id"]),

                "vehicleName": vehicle.get("name"),

                "deviceNumber": vehicle.get("deviceId"),

                "uniqueId": str(vehicle.get("uniqueId")),

                "branchId": str(vehicle.get("branchId")) if vehicle.get("branchId") else None

            },

            "count": len(result),

            "geofences": result

        }

        except Exception as e:

            return {
            "success": False,
            "error": str(e)
        }
    from bson import ObjectId

    def get_branchgroup_school_vehicle_geofences(
    self,
    group_id,
    role,
    user
):

        try:

        # =====================================
        # GROUP ID
        # =====================================

            if not group_id:
                group_id = (
                user.get("groupId")
                or user.get("branchGroupId")
                or user.get("_id")
            )

            try:
                group_id = ObjectId(str(group_id))
            except:
                pass

        # =====================================
        # FIND BRANCH GROUP
        # =====================================

            branch_group = self.db.branchgroups.find_one({
            "_id": group_id
        })

            if not branch_group:
                return {
                "success": False,
                "message": "Branch group not found."
            }

            assigned_branches = branch_group.get("AssignedBranch", [])

            if not assigned_branches:
                return {
                "success": False,
                "message": "No branches assigned."
            }

        # =====================================
        # CONVERT BRANCH IDS
        # =====================================

            branch_ids = []

            for b in assigned_branches:
                try:
                    branch_ids.append(ObjectId(str(b)))
                except:
                    pass

        # =====================================
        # RBAC
        # =====================================

            device_filter = get_rbac_filter(
            role,
            user,
            "devices",
            self.db
        )

            if device_filter.get("_id") is None:
                device_filter = {}

        # =====================================
        # FIND DEVICES
        # =====================================

            device_query = {

            "$and": [

                {

                    "$or": [

                        {
                            "branchId": {
                                "$in": branch_ids
                            }
                        },

                        {
                            "branchId": {
                                "$in": [str(x) for x in branch_ids]
                            }
                        }

                    ]

                }

            ]

        }

            if device_filter:
                device_query["$and"].append(device_filter)

            devices = list(
            self.db.devices.find(device_query)
        )

            result = []

        # =====================================
        # DEVICE LOOP
        # =====================================

            for device in devices:

                route = self.db.routes.find_one({

                "$or": [

                    {
                        "deviceObjId": device["_id"]
                    },

                    {
                        "deviceObjId": str(device["_id"])
                    }

                ]

            })

                if not route:
                    continue

                geofence = self.db.geofences.find_one({

                "$or": [

                    {
                        "routeObjId": route["_id"]
                    },

                    {
                        "routeObjId": str(route["_id"])
                    }

                ]

            })

                if not geofence:
                    continue

                result.append({

                "vehicle": {

                    "deviceId": str(device["_id"]),

                    "vehicleName": (
                        device.get("vehicleNumber")
                        or device.get("vehicle_name")
                        or device.get("name")
                    ),

                    "uniqueId": device.get("uniqueId")

                },

                "route": {

                    "routeId": str(route["_id"]),

                    "routeNumber": route.get("routeNumber")

                },

                "geofence": self.clean(geofence)

            })

        # =====================================
        # RESPONSE
        # =====================================

            return {

            "success": True,

            "branchGroup": {

                "groupId": str(branch_group["_id"]),

                "branchGroupName": branch_group.get("branchGroupName")

            },

            "count": len(result),

            "vehicles": result

        }

        except Exception as e:

            print("ERROR =", e)

            return {

            "success": False,

            "error": str(e)

        }
    from datetime import datetime, timedelta, timezone

    def get_branchgroup_school_vehicle_today_distance(
    self,
    group_id,
    vehicle_input,
    role,
    user
):

        try:

        # =====================================
        # FIND SCHOOL VEHICLE UNDER BRANCH GROUP
        # =====================================

            result = self.get_branchgroup_specific_vehicle(
            group_id,
            vehicle_input
        )

            if not result["success"]:
                return result

            vehicle = result["vehicle"]

            unique_ids = self.normalize_unique_id(
            vehicle["uniqueId"]
        )

        # =====================================
        # TODAY (IST)
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
        # HISTORY PIPELINE
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

                    "vehicleName": "$name",

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
                        "$first": "$vehicleName"
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
            self.db.histories.aggregate(pipeline)
        )

            if not report:

                return {

                "success": False,

                "message": "No history found for today."

            }

            report = report[0]

        # =====================================
        # RESPONSE
        # =====================================

            return {

            "success": True,

            "vehicle": {

                "deviceId": vehicle.get("deviceId"),

                "vehicleName": vehicle.get("vehicleName"),

                "uniqueId": vehicle.get("uniqueId")

            },

            "todayDistance": {

                "date": now.strftime("%Y-%m-%d"),

                "distanceKm": report["todayDistance"],

                "firstRecord": report["firstRecord"],

                "lastRecord": report["lastRecord"]

            }

        }

        except Exception as e:

            print(e)

            return {

            "success": False,

            "error": str(e)

        }
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
    def get_branchgroup_school_specific_vehicle_distance_report(
    self,
    group_id,
    vehicle_input,
    role,
    user,
    limit=100
):

        try:

        # ===============================
        # FIND SCHOOL VEHICLE
        # ===============================

            result = self.get_branchgroup_specific_vehicle(
            group_id,
            vehicle_input
        )

            if not result["success"]:
                return result

            vehicle = result["vehicle"]

        # ===============================
        # UNIQUE IDS
        # ===============================

            unique_ids = self.normalize_unique_id(
            vehicle.get("uniqueId")
        )

            print("REPORT UNIQUE IDS =", unique_ids)

        # ===============================
        # RBAC FILTER
        # ===============================

            report_filter = get_rbac_filter(
            role,
            user,
            "report_distances",
            self.db
        )

        # ===============================
        # GET REPORTS
        # ===============================

            reports = list(

            self.db["report_distances"].find(

                {

                    "$and": [

                        report_filter,

                        {
                            "uniqueId": {
                                "$in": unique_ids
                            }
                        }

                    ]

                }

            )

            .sort("createdAt", -1)

            .limit(limit)

        )

            print("DISTANCE REPORT COUNT =", len(reports))

        # ===============================
        # BRANCH GROUP DETAILS
        # ===============================

            branch_group = self.db["branchgroups"].find_one({
            "_id": ObjectId(str(group_id))
        })

        # ===============================
        # RESPONSE
        # ===============================

            return {

            "success": True,

            "branchGroup": {

                "groupId": str(branch_group["_id"]),

                "branchGroupName": branch_group.get("branchGroupName")

            },

            "vehicle": vehicle,

            "reports": [

                self.clean(report)

                for report in reports

            ]

        }

        except Exception as e:

            return {

            "success": False,

            "error": str(e)

        }
    def get_branchgroup_school_specific_vehicle_km_report(
    self,
    group_id,
    vehicle_input,
    role,
    user
):

    # =====================================
    # GET SCHOOL VEHICLE UNDER BRANCH GROUP
    # =====================================

        result = self.get_branchgroup_specific_vehicle(
        group_id,
        vehicle_input
    )

        if not result["success"]:
            return result

        vehicle = result["vehicle"]

        unique_ids = self.normalize_unique_id(
        vehicle["uniqueId"]
    )

    # =====================================
    # FETCH REPORT DISTANCES
    # =====================================

        report_distances = list(

        self.db["report_distances"]

        .find({

            "$and":[

                get_rbac_filter(
                    role,
                    user,
                    "report_distances",
                    self.db
                ),

                {
                    "uniqueId":{
                        "$in":unique_ids
                    }
                }

            ]

        })

        .sort("createdAt",-1)

    )

        if not report_distances:

            return {
            "success":False,
            "message":"No distance reports found as the device is inactive."
        }

    # =====================================
    # BUILD REPORT MAP
    # =====================================

        report_map = {

        r["createdAt"].date():
        float(r.get("distance",0))

            for r in report_distances

    }

        today = datetime.utcnow().date()

        available_dates = sorted(report_map.keys())

    # =====================================
    # ACTIVE / INACTIVE
    # =====================================

        if today in report_map:

            status = "active"

            analysis_base_date = today

            message = "Vehicle is active today."

        else:

            status = "inactive"

            analysis_base_date = available_dates[-1]

            message = (
            f"Vehicle is not active today. "
            f"Last active was on {analysis_base_date}"
        )

        current_km = round(
        report_map.get(
            analysis_base_date,
            0
        ),
        2
    )

        previous_active_date = None

        for d in reversed(available_dates):

            if d < analysis_base_date:

                previous_active_date = d

                break

        yesterday_km = round(

            report_map.get(
            previous_active_date,
            0
        ),

        2

    ) if previous_active_date else 0

    # =====================================
    # WEEK
    # =====================================

        week_start = analysis_base_date - timedelta(
        days=analysis_base_date.weekday()
    )

        week_end = week_start + timedelta(days=6)

        week_total = 0

        for r in report_distances:

            d = r["createdAt"].date()

            if week_start <= d <= week_end:

                week_total += float(
                r.get("distance",0)
            )

        week_total = round(week_total,2)

    # =====================================
    # MONTH
    # =====================================

        month_start = analysis_base_date - timedelta(days=29)

        month_end = analysis_base_date

        month_total = 0

        for r in report_distances:

            d = r["createdAt"].date()

            if month_start <= d <= month_end:

                month_total += float(
                r.get("distance",0)
            )

        month_total = round(month_total,2)

    # =====================================
    # BRANCH GROUP DETAILS
    # =====================================

        branch_group = self.db["branchgroups"].find_one({

        "_id": ObjectId(str(group_id))

    })

    # =====================================
    # RESPONSE
    # =====================================

        return {

        "success":True,

        "status":status,

        "message":message,

        "branchGroup":{

            "groupId":str(branch_group["_id"]),

            "branchGroupName":
                branch_group.get("branchGroupName")

        },

        "vehicle":{

            "vehicleName":
                vehicle.get("vehicleName"),

            "deviceId":
                vehicle.get("deviceId"),

            "uniqueId":
                vehicle.get("uniqueId"),

            "status":
                vehicle.get("status"),

            "category":
                vehicle.get("category"),

            "model":
                vehicle.get("model")

        },

        "reference":{

            "date":
                analysis_base_date.strftime("%Y-%m-%d"),

            "isTodayActive":
                status=="active",

            "lastActiveDate":
                analysis_base_date.strftime("%Y-%m-%d")

        },

        "distanceReport":{

            "current":{

                "label":
                    "Today"
                    if status=="active"
                    else "Last Active",

                "km":
                    current_km

            },

            "yesterday":{

                "date":
                    previous_active_date.strftime("%Y-%m-%d")
                    if previous_active_date
                    else None,

                "km":
                    yesterday_km

            },

            "week":{

                "from":
                    week_start.strftime("%Y-%m-%d"),

                "to":
                    week_end.strftime("%Y-%m-%d"),

                "totalKm":
                    week_total

            },

            "month":{

                "type":"rolling_30_days",

                "from":
                    month_start.strftime("%Y-%m-%d"),

                "to":
                    month_end.strftime("%Y-%m-%d"),

                "totalKm":
                    month_total

            }

        }

    }
    def get_branchgroup_specific_vehicle_distance_report(
    self,
    group_id,
    vehicle_input,
    role,
    user,
    limit=100
):

        try:

        # ===============================
        # FIND VEHICLE
        # ===============================

            result = self.get_branchgroup_specific_vehicle(
            group_id,
            vehicle_input
        )

            if not result["success"]:
                return result

            vehicle = result["vehicle"]

        # ===============================
        # UNIQUE IDS
        # ===============================

            unique_ids = self.normalize_unique_id(
            vehicle.get("uniqueId")
        )

            print("REPORT UNIQUE IDS =", unique_ids)

        # ===============================
        # RBAC FILTER
        # ===============================

            report_filter = get_rbac_filter(
            role,
            user,
            "report_distances",
            self.db
        )

        # ===============================
        # GET REPORTS
        # ===============================

            reports = list(

            self.db["report_distances"]

            .find({

                "$and": [

                    report_filter,

                    {
                        "uniqueId": {
                            "$in": unique_ids
                        }
                    }

                ]

            })

            .sort("createdAt", -1)

            .limit(limit)

        )

            print("DISTANCE REPORT COUNT =", len(reports))

        # ===============================
        # BRANCH GROUP DETAILS
        # ===============================

            branch_group = self.db["branchgroups"].find_one({
            "_id": ObjectId(str(group_id))
        })

        # ===============================
        # RESPONSE
        # ===============================

            return {

            "success": True,

            "branchGroup": {

                "groupId": str(branch_group["_id"]),

                "branchGroupName": branch_group.get("branchGroupName")

            },

            "vehicle": vehicle,

            "reports": [

                self.clean(report)

                for report in reports

            ]

        }

        except Exception as e:

            return {

            "success": False,

            "error": str(e)

        }
    def get_branchgroup_school_specific_vehicle_status(
    self,
    group_id,
    vehicle_input,
    role,
    user,
    limit=100
):

        try:

        # =====================================
        # FIND SCHOOL VEHICLE UNDER BRANCH GROUP
        # =====================================

            result = self.get_branchgroup_specific_vehicle(
            group_id,
            vehicle_input
        )

            if not result["success"]:
                return result

            vehicle = result["vehicle"]

        # =====================================
        # BRANCH GROUP DETAILS
        # =====================================

            branch_group = self.db["branchgroups"].find_one({
            "_id": ObjectId(str(group_id))
        })

        # =====================================
        # GET STATUS REPORT
        # =====================================

            status_report = self.report_status_engine.get_single_branch_vehicle_status_report(

            vehicle["branchId"],

            vehicle["uniqueId"],

            role,

            user,

            limit

        )

        # =====================================
        # RESPONSE
        # =====================================

            return {

            "success": True,

            "branchGroup": {

                "groupId": str(branch_group["_id"]),

                "branchGroupName": branch_group.get("branchGroupName")

            },

            "vehicle": vehicle,

            "statusReport": status_report

        }

        except Exception as e:

            return {

            "success": False,

            "error": str(e)

        }
    def get_branchgroup_specific_vehicle_status(
    self,
    group_id,
    vehicle_input,
    role,
    user,
    limit=100
):

        try:

        # =====================================
        # FIND VEHICLE
        # =====================================

            result = self.get_branchgroup_specific_vehicle(
            group_id,
            vehicle_input
        )

            if not result["success"]:
                return result

            vehicle = result["vehicle"]

        # =====================================
        # BRANCH GROUP DETAILS
        # =====================================

            branch_group = self.db["branchgroups"].find_one({
            "_id": ObjectId(str(group_id))
        })

        # =====================================
        # STATUS REPORT
        # =====================================

            status_report = self.report_status_engine.get_single_branch_vehicle_status_report(

            vehicle["branchId"],

            vehicle["uniqueId"],

            role,

            user,

            limit

        )

        # =====================================
        # RESPONSE
        # =====================================

            return {

            "success": True,

            "branchGroup": {

                "groupId": str(branch_group["_id"]),

                "branchGroupName": branch_group.get("branchGroupName")

            },

            "vehicle": vehicle,

            "statusReport": status_report

        }

        except Exception as e:

            return {

            "success": False,

            "error": str(e)

        }
    
    def get_branchgroup_school_specific_vehicle_travel_summary(
    self,
    group_id,
    vehicle_input,
    role,
    user,
    limit=100
):

        try:

    # =====================================
    # FIND SCHOOL VEHICLE UNDER BRANCH GROUP
    # =====================================

            result = self.get_branchgroup_specific_vehicle(
            group_id,
            vehicle_input
        )

            if not result["success"]:
                return result

            vehicle = result["vehicle"]

    # =====================================
    # BRANCH GROUP DETAILS
    # =====================================

            branch_group = self.db["branchgroups"].find_one({
            "_id": ObjectId(str(group_id))
        })

    # =====================================
    # RBAC FILTER
    # =====================================

            summary_filter = get_rbac_filter(
            role,
            user,
            "report_travelsummaries",
            self.db
        )

    # =====================================
    # FETCH TRAVEL SUMMARY
    # =====================================

            reports = list(

            self.db["report_travelsummaries"].find(

                {

                    "$and": [

                        summary_filter,

                        {

                            "uniqueId": {

                                "$in": self.normalize_unique_id(
                                    vehicle["uniqueId"]
                                )

                            }

                        }

                    ]

                }

            )

            .sort("startTime", -1)

            .limit(limit)

        )

    # =====================================
    # RESPONSE
    # =====================================

            return {

            "success": True,

            "branchGroup": {

                "groupId": str(branch_group["_id"]),

                "branchGroupName": branch_group.get(
                    "branchGroupName"
                )

            },

            "vehicle": vehicle,

            "travelSummary": [

                self.clean(report)

                for report in reports

            ]

        }

        except Exception as e:

            return {

            "success": False,

            "error": str(e)

        }
    def get_branchgroup_specific_vehicle_travel_summary(
    self,
    group_id,
    vehicle_input,
    role,
    user,
    limit=100
):

        try:

    # =====================================
    # FIND BRANCHGROUP VEHICLE
    # =====================================

            result = self.get_branchgroup_specific_vehicle(
            group_id,
            vehicle_input
        )

            if not result["success"]:
                return result

            vehicle = result["vehicle"]

    # =====================================
    # BRANCH GROUP DETAILS
    # =====================================

            branch_group = self.db["branchgroups"].find_one({
            "_id": ObjectId(str(group_id))
        })

    # =====================================
    # RBAC FILTER
    # =====================================

            summary_filter = get_rbac_filter(
            role,
            user,
            "report_travelsummaries",
            self.db
        )

    # =====================================
    # FETCH TRAVEL SUMMARY
    # =====================================

            reports = list(

            self.db["report_travelsummaries"].find(

                {

                    "$and": [

                        summary_filter,

                        {

                            "uniqueId": {

                                "$in": self.normalize_unique_id(
                                    vehicle["uniqueId"]
                                )

                            }

                        }

                    ]

                }

            )

            .sort("startTime", -1)

            .limit(limit)

        )

    # =====================================
    # RESPONSE
    # =====================================

            return {

            "success": True,

            "branchGroup": {

                "groupId": str(branch_group["_id"]),

                "branchGroupName": branch_group.get("branchGroupName")

            },

            "vehicle": {

                "deviceId": vehicle.get("deviceId"),

                "vehicleName": vehicle.get("vehicleName"),

                "deviceNumber": vehicle.get("deviceNumber"),

                "uniqueId": vehicle.get("uniqueId"),

                "status": vehicle.get("status"),

                "model": vehicle.get("model"),

                "category": vehicle.get("category"),

                "branchId": vehicle.get("branchId"),

                "schoolId": vehicle.get("schoolId")

            },

            "count": len(reports),

            "travelSummary": [

                self.clean(report)

                for report in reports

            ]

        }

        except Exception as e:

            return {

            "success": False,

            "error": str(e)

        }
    def get_branchgroup_school_specific_vehicle_last_position(
    self,
    group_id,
    vehicle_input,
    role,
    user
):

        try:

    # =====================================
    # FIND SCHOOL VEHICLE UNDER BRANCHGROUP
    # =====================================

            result = self.get_branchgroup_school_vehicle(
            group_id,
            vehicle_input,
            role,
            user
        )

            if not result["success"]:
                return result

            vehicle = result["vehicle"]
            school = result["school"]
            branch = result["branch"]

    # =====================================
    # FIND LAST POSITION
    # =====================================

            position = self.db["vehiclelastpositions"].find_one(

            {

                "$and": [

                    get_rbac_filter(
                        role,
                        user,
                        "vehiclelastpositions",
                        self.db
                    ),

                    {
                        "uniqueId": str(vehicle["uniqueId"])
                    }

                ]

            }

        )

            if not position:

                return {

                "success": False,

                "message": "No last position found."

            }

    # =====================================
    # ADDRESS FALLBACK
    # =====================================

            address = position.get("address")

            if not address:

                latitude = position.get("latitude")
                longitude = position.get("longitude")

                if latitude is not None and longitude is not None:

                    address = self.get_address(
                    latitude,
                    longitude
                )

    # =====================================
    # RESPONSE
    # =====================================

            return {

            "success": True,

            "branchGroup": {

                "groupId": str(group_id),

                "branchGroupName": user.get("username")

            },

            "school": school,

            "branch": branch,

            "vehicle": {

                "deviceId": vehicle.get("deviceId"),

                "vehicleName": vehicle.get("vehicleName"),

                "deviceNumber": vehicle.get("deviceNumber"),

                "uniqueId": vehicle.get("uniqueId"),

                "model": vehicle.get("model"),

                "category": vehicle.get("category")

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

        except Exception as e:

            return {

            "success": False,

            "error": str(e)

        }