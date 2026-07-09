from bson import ObjectId
from rbac import get_rbac_filter


class GeofencesEngine:

    def __init__(self, db):
        self.db = db


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