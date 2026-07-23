from bson import ObjectId
from rbac import get_rbac_filter


class GeofencesEngine:

    def __init__(self, db):
        self.db = db
    def convert_id(self, value):

        try:
            return ObjectId(str(value))
        except:
            return value
    def normalize_unique_id(self, unique_id):

        if unique_id is None:
            return []

        unique_id = str(unique_id)

        values = [
        unique_id
    ]

        try:
            values.append(int(unique_id))
        except:
            pass

        return values
    # =====================================
    # CLEAN
    # =====================================
    def _convert_school_id(self, school_id):

        try:
            return ObjectId(str(school_id))
        except:
            return school_id
    def clean(self, doc):

        if not doc:
            return doc

        result = {}

        for k, v in doc.items():

            if isinstance(v, ObjectId):
                result[k] = str(v)

            else:
                result[k] = v

        return result



    # =====================================
    # RBAC FILTER
    # =====================================

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



    # =====================================
    # SINGLE GEOFENCE
    # =====================================

    def get_geofence(
        self,
        geofence_id,
        role,
        user
    ):


        rbac_filter = self.get_filter(
            role,
            user
        )


        geofence = self.db["geofences"].find_one({

            "$and":[

                rbac_filter,

                {

                    "$or":[

                        {
                            "_id":
                            ObjectId(str(geofence_id))
                        },

                        {
                            "_id":
                            geofence_id
                        }

                    ]

                }

            ]

        })


        return self.clean(geofence)



    # =====================================
    # SCHOOL GEOFENCES
     # =====================================
# SCHOOL GEOFENCES
# =====================================

    # =====================================
# SCHOOL GEOFENCES
# =====================================

    def get_school_geofences(
    self,
    school_id,
    role,
    user
):

        rbac_filter = get_rbac_filter(
        role,
        user,
        "geofences",
        self.db
    )

        geofences = list(

        self.db["geofences"].find({

            "$and":[

                rbac_filter,

                {

                    "schoolId":
                    self._convert_school_id(school_id)

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
    # =====================================
    # BRANCH GEOFENCES
    # =====================================

    def get_branch_geofences(
        self,
        branch_id,
        role,
        user,
        limit=100
    ):


        rbac_filter=self.get_filter(
            role,
            user
        )


        geofences=list(

            self.db["geofences"].find({

                "$and":[

                    rbac_filter,

                    {

                        "branchId":
                        ObjectId(str(branch_id))

                    }

                ]

            })

            .sort(
                "createdAt",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(g)

            for g in geofences

        ]
    
    
    
    def get_specific_vehicle_branch_geofences(
    self,
    branch_id,
    vehicle_input,
    role,
    user
):

        print("========================================")
        print("GET SPECIFIC VEHICLE GEOFENCE")
        print("ROLE:", role)
        print("BRANCH ID:", branch_id)
        print("VEHICLE INPUT:", vehicle_input)
        print("========================================")


    # =====================================================
    # 1. GET DEVICE RBAC FILTER
    # =====================================================

        device_filter = get_rbac_filter(
        role,
        user,
        "devices",
        self.db
    )

        print("DEVICE RBAC FILTER:")
        print(device_filter)


    # =====================================================
    # 2. VEHICLE SEARCH FILTER
    # =====================================================

        vehicle_match_filter = {

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
                    "$regex": vehicle_input,
                    "$options": "i"
                }
            }

        ]

    }


    # =====================================================
    # 3. FIND VEHICLE WITHOUT RBAC
    # =====================================================

        test_device = self.db["devices"].find_one(
        vehicle_match_filter
    )


        print("DEVICE WITHOUT RBAC:")
        print(test_device)


        if not test_device:

            return {

            "success": False,

            "message": "Vehicle not found."

        }


    # =====================================================
    # 4. CHECK VEHICLE BRANCH
    # =====================================================

        device_branch_id = test_device.get(
        "branchId"
    )


        print("DEVICE BRANCH ID:")
        print(device_branch_id)

        print("DEVICE BRANCH TYPE:")
        print(type(device_branch_id))

        print("REQUESTED BRANCH ID:")
        print(branch_id)

        print("REQUESTED BRANCH TYPE:")
        print(type(branch_id))


        if str(device_branch_id) != str(branch_id):

            return {

            "success": False,

            "message": "Vehicle does not belong to this branch."

        }


    # =====================================================
    # 5. CHECK RBAC PERMISSION
    # =====================================================

        rbac_query = {

        "_id": test_device["_id"],

        **device_filter

    }


        print("FINAL RBAC QUERY:")
        print(rbac_query)


        device = self.db["devices"].find_one(
        rbac_query
    )


        print("DEVICE AFTER RBAC:")
        print(device)


        if not device:

            return {

            "success": False,

            "message": "You do not have permission to access this vehicle."

        }


    # =====================================================
    # 6. FIND ROUTE
    # =====================================================

        route = self.db["routes"].find_one({

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

            "message": "Route not assigned to vehicle."

        }


    # =====================================================
    # 7. FIND GEOFENCE
    # =====================================================

        geofence = self.db["geofences"].find_one({

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

            "message": "Vehicle geofence not found."

        }


    # =====================================================
    # 8. FINAL RESPONSE
    # =====================================================

        return {

        "success": True,

        "vehicle": {

            "deviceId": str(
                device["_id"]
            ),

            "deviceName": (

                device.get("vehicleNumber")

                or device.get("vehicle_name")

                or device.get("name")

                or "N/A"

            )

        },

        "route": {

            "routeId": str(
                route["_id"]
            ),

            "routeNumber": route.get(
                "routeNumber"
            )

        },

        "geofence": self.clean(
            geofence
        )

    }
    # =====================================
    # DRIVER GEOFENCES
    # =====================================

    def get_driver_geofences(
        self,
        username,
        role,
        user,
        limit=100
    ):


        driver_filter=get_rbac_filter(

            role,

            user,

            "drivers",

            self.db

        )


        driver=self.db["drivers"].find_one({

            "$and":[

                driver_filter,

                {

                    "username":
                    username

                }

            ]

        })


        if not driver:
            return []



        route_id=driver.get(
            "routeObjId"
        )


        if not route_id:
            return []



        rbac_filter=self.get_filter(
            role,
            user
        )


        geofences=list(

            self.db["geofences"].find({

                "$and":[

                    rbac_filter,

                    {

                        "routeObjId":
                        route_id

                    }

                ]

            })

            .sort(
                "createdAt",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(g)

            for g in geofences

        ]



    # =====================================
    # ALL GEOFENCES
    # =====================================

    def get_all_geofences(
        self,
        role,
        user,
        limit=200
    ):


        rbac_filter=self.get_filter(
            role,
            user
        )


        geofences=list(

            self.db["geofences"]

            .find(rbac_filter)

            .sort(
                "createdAt",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(g)

            for g in geofences

        ]



    # =====================================
    # COUNT
    # =====================================

    def get_geofence_count(
        self,
        role,
        user
    ):


        rbac_filter=self.get_filter(
            role,
            user
        )


        return self.db["geofences"].count_documents(

            rbac_filter

        )



    # =====================================
    # SEARCH BY NAME
    # =====================================

    def search_geofence(
        self,
        name,
        role,
        user
    ):


        rbac_filter=self.get_filter(
            role,
            user
        )


        geofences=list(

            self.db["geofences"].find({

                "$and":[

                    rbac_filter,

                    {

                        "geofenceName":{

                            "$regex":name,

                            "$options":"i"

                        }

                    }

                ]

            })

        )


        return [

            self.clean(g)

            for g in geofences

        ]



    # =====================================
    # ROUTE GEOFENCES
    # =====================================

    def get_route_geofences(
        self,
        route_id,
        role,
        user
    ):


        rbac_filter=self.get_filter(
            role,
            user
        )


        geofences=list(

            self.db["geofences"].find({

                "$and":[

                    rbac_filter,

                    {

                        "routeObjId":
                        ObjectId(str(route_id))

                    }

                ]

            })

        )


        return [

            self.clean(g)

            for g in geofences

        ]
    


  
    from bson import ObjectId


    def get_device_geofence_superadmin(
    self,
    location_name,
    vehicle_name,
    role,
    user
):

    # Find vehicle
        device = self.db["devices"].find_one({
        "name": vehicle_name
    })

        if not device:
            return {
            "success": False,
            "message": "Vehicle not found",
            "data": None
        }


    # Detect school
        school = self.db["schools"].find_one({
        "name": location_name
    })

    # Detect branch
        branch = self.db["branches"].find_one({
        "name": location_name
    })

    # Detect route
        route = self.db["routes"].find_one({
        "name": location_name
    })


        location_filter = {}


        if branch:
            location_filter["branchId"] = branch["_id"]
            location_type = "branch"

        elif school:
            location_filter["schoolId"] = school["_id"]
            location_type = "school"

        elif route:
            location_filter["routeObjId"] = route["_id"]
            location_type = "route"

        else:
            return {
            "success": False,
            "message": "School/Branch/Route not found",
            "data": None
        }


    # Verify vehicle belongs to location
        if location_type == "branch":

            if device.get("branchId") != branch["_id"]:
                return {
                "success": False,
                "message": "Vehicle not assigned to this branch",
                "data": None
            }


        elif location_type == "school":

            if device.get("schoolId") != school["_id"]:
                return {
                "success": False,
                "message": "Vehicle not assigned to this school",
                "data": None
            }


        elif location_type == "route":

            if device.get("routeObjId") != route["_id"]:
                return {
                "success": False,
                "message": "Vehicle not assigned to this route",
                "data": None
            }


    # Find geofence
        geofence = self.db["geofences"].find_one(
        location_filter
    )


        if not geofence:
            return {
            "success": False,
            "message": "Geofence not found",
            "data": None
        }


        return {
        "success": True,
        "vehicle": vehicle_name,
        "locationType": location_type,
        "data": self.clean(geofence)
    }
    def get_school_user_branch_geofences(
    self,
    role,
    user,
    limit=100
):

    # ===============================
    # School RBAC Filter
    # ===============================

        school_filter = get_rbac_filter(
        role,
        user,
        "schools",
        self.db
    )


    # ===============================
    # Find School
    # ===============================

        school = self.db["schools"].find_one(
        school_filter
    )


        if not school:
            return {
            "success": False,
            "message": "School not found.",
            "data": []
        }


        school_id = school["_id"]



    # ===============================
    # Find Branches Under School
    # ===============================

        branches = list(
        self.db["branches"].find({

            "$or":[

                {
                    "schoolId": school_id
                },

                {
                    "schoolId": str(school_id)
                }

            ]

        })
    )


        if not branches:
            return {
            "success": True,
            "schoolId": str(school_id),
            "totalGeofences": 0,
            "geofences": []
        }



        branch_ids = [
        b["_id"]
        for b in branches
    ]



    # ===============================
    # Geofence RBAC Filter
    # ===============================

        geofence_filter = get_rbac_filter(
        role,
        user,
        "geofences",
        self.db
    )


    # ===============================
    # Find Branch Geofences
    # ===============================

        geofences = list(

        self.db["geofences"].find({

            "$and":[

                geofence_filter,

                {
                    "$or":[

                        {
                            "schoolId": school_id
                        },

                        {
                            "schoolId": str(school_id)
                        }

                    ]
                },

                {
                    "branchId":{
                        "$in": branch_ids
                    }
                }

            ]

        })

        .sort(
            "createdAt",
            -1
        )

        .limit(limit)

    )


        return {

        "success": True,

        "school": {

            "schoolId": str(school_id),

            "schoolName": school.get("name")

        },

        "totalBranches": len(branches),

        "totalGeofences": len(geofences),

        "geofences":[

            self.clean(g)

            for g in geofences

        ]

    }
    def get_specific_vehicle_branch_of_school_geofences(
    self,
    branch_name,
    vehicle_input,
    role,
    user
):

    # =====================================
    # Convert School ID
    # =====================================

        school_id = user.get("schoolId")

        try:
            school_obj_id = ObjectId(str(school_id))
        except:
            school_obj_id = school_id


    # =====================================
    # Find Branch Under School
    # =====================================

        branch = self.db["branches"].find_one({

        "$and":[

            {
                "$or":[

                    {
                        "schoolId": school_obj_id
                    },

                    {
                        "schoolId": str(school_obj_id)
                    }

                ]
            },

            {

                "$or":[

                    {
                        "branchName":{
                            "$regex": branch_name,
                            "$options":"i"
                        }
                    },

                    {
                        "name":{
                            "$regex": branch_name,
                            "$options":"i"
                        }
                    }

                ]

            }

        ]

    })


        if not branch:

            return {
            "success":False,
            "message":"Branch not found."
        }


        branch_id = branch["_id"]



    # =====================================
    # Device RBAC
    # =====================================

        device_filter = get_rbac_filter(
        role,
        user,
        "devices",
        self.db
    )



    # =====================================
    # Find Vehicle Under Branch
    # =====================================

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
                            "$regex":vehicle_input,
                            "$options":"i"
                        }
                    },

                    {
                        "vehicle_name":{
                            "$regex":vehicle_input,
                            "$options":"i"
                        }
                    },


                    {
                        "name":{
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

    })


        if not device:

            return {
            "success":False,
            "message":"Vehicle not found in this branch."
        }



        device_id = device["_id"]



    # =====================================
    # Find Route
    # =====================================

        route = self.db["routes"].find_one({

        "$or":[

            {
                "deviceObjId":device_id
            },

            {
                "deviceObjId":str(device_id)
            }

        ]

    })


        if not route:

            return {
            "success":False,
            "message":"Route not assigned to vehicle."
        }



    # =====================================
    # Find Geofence
    # =====================================

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

                    {
                        "routeObjId":route["_id"]
                    },

                    {
                        "routeObjId":str(route["_id"])
                    }

                ]

            },


            {

                "$or":[

                    {
                        "branchId":branch_id
                    },

                    {
                        "branchId":str(branch_id)
                    }

                ]

            }

        ]

    })


        if not geofence:

            return {
            "success":False,
            "message":"Geofence not found for vehicle."
        }



    # =====================================
    # Final Response
    # =====================================

        return {

        "success":True,


        "branch":{

            "branchId":str(branch_id),

            "branchName":(
                branch.get("branchName")
                or branch.get("name")
            )

        },


        "vehicle":{

            "deviceId":str(device["_id"]),

            "deviceName":(
                device.get("vehicleNumber")
                or device.get("vehicle_name")
                or device.get("name")
                or "N/A"
            ),

            "uniqueId":device.get("uniqueId")

        },


        "route":{

            "routeId":str(route["_id"]),

            "routeNumber":route.get("routeNumber")

        },


        "geofence":self.clean(geofence)

    }