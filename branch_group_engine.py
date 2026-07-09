from bson import ObjectId
from rbac import get_rbac_filter
from datetime import datetime, timezone, timedelta

class BranchGroupEngine:

    def __init__(self, db):
        self.db = db


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