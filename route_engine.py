from bson import ObjectId
from rbac import get_rbac_filter
import traceback

class RouteEngine:

    def __init__(self, db):
        self.db = db
    
    
# ====================================
# ID NORMALIZER
# ====================================

    def normalize_id(self, value):

        ids = []

        if value is None:
            return ids

        ids.append(value)

        ids.append(str(value))

        try:
            ids.append(ObjectId(str(value)))
        except:
            pass

        return list(set(ids))
    # ====================================
    # SAFE OBJECT ID
    # ====================================

    def _convert_id(self, value):

        try:
            return ObjectId(value)

        except:

            return value



    # ====================================
    # GET ALLOWED ROUTE
    # ====================================

    def get_route(
        self,
        route_id,
        role,
        user
    ):


        route_filter = get_rbac_filter(

            role,
            user,
            "routes",
            self.db

        )


        return self.db["routes"].find_one({

            "$and":[

                route_filter,

                {
    "_id": {
        "$in": self.normalize_id(route_id)
    }
}

            ]

        })



    # ====================================
    # ROUTE PROFILE
    # ====================================
    from bson import ObjectId

# ====================================
# SUPER ADMIN ROUTE PROFILE
# ====================================

    

   

    def get_superadmin_route_profile(self):

        routes = self.db["routes"].find({})

        data = []

        for route in routes:

            item = {}

            for key, value in route.items():

                if isinstance(value, ObjectId):
                    item[key] = str(value)
                elif isinstance(value, list):
                    item[key] = [
                    str(x) if isinstance(x, ObjectId) else x
                    for x in value
                ]
                else:
                    item[key] = value

            data.append(item)

        return data
    def get_route_profile(
        self,
        route_id,
        role,
        user
    ):


        route = self.get_route(

            route_id,

            role,

            user

        )


        if not route:
            return None


        return {

            "routeNumber": route.get("routeNumber"),

            "routeCompletionTime":
            route.get("routeCompletionTime"),

            "schoolId":
            str(route.get("schoolId")),

            "branchId":
            str(route.get("branchId")),

            "deviceObjId":
            str(route.get("deviceObjId"))

        }



    # ====================================
    # DEVICE
    # ====================================

    def get_route_device(
        self,
        route_id,
        role,
        user
    ):


        route = self.get_route(

            route_id,

            role,

            user

        )


        if not route:
            return None


        device_filter = get_rbac_filter(

            role,

            user,

            "devices",

            self.db

        )


        device = self.db["devices"].find_one({

            "$and":[

                device_filter,

                {
    "_id": {
        "$in": self.normalize_id(
            route.get("deviceObjId")
        )
    }
}

            ]

        })


        if not device:
            return None


        return {

            "vehicleName": device.get("name"),

            "uniqueId": device.get("uniqueId"),

            "status": device.get("status"),

            "model": device.get("model"),

            "category": device.get("category")

        }



    # ====================================
    # BRANCH
    # ====================================

    def get_route_branch(
        self,
        route_id,
        role,
        user
    ):


        route = self.get_route(

            route_id,

            role,

            user

        )


        if not route:
            return None


        branch_filter = get_rbac_filter(

            role,

            user,

            "branches",

            self.db

        )


        branch = self.db["routes"].find_one({

            "$and":[

                branch_filter,

                {
    "_id": {
        "$in": self.normalize_id(
            route.get("branchId")
        )
    }
}

            ]

        })


        if not branch:
            return None


        return {

            "branchName":
            branch.get("branchName"),

            "username":
            branch.get("username"),

            "mobileNo":
            branch.get("mobileNo")

        }



    # ====================================
    # SCHOOL
    # ====================================

  

    def get_route_school(self, role, user):

        school_filter = get_rbac_filter(
        role,
        user,
        "routes",
        self.db
    )

        school_id = user.get("_id")

        routes = list(
        self.db["routes"].find({
            "$and": [
                school_filter,
                {
                    "$or": [
                        {
                            "schoolId": school_id
                        },
                        {
                            "schoolId": ObjectId(school_id)
                        } if ObjectId.is_valid(str(school_id)) else {
                            "schoolId": school_id
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

            "deviceObjId": str(route.get("deviceObjId"))
            if route.get("deviceObjId") else "",

            "schoolId": str(route.get("schoolId"))
            if route.get("schoolId") else "",

            "branchId": str(route.get("branchId"))
            if route.get("branchId") else "",

            "routeCompletionTime": route.get("routeCompletionTime"),

            "createdAt": route.get("createdAt")

        })

        return {

        "success": True,

        "totalRoutes": len(data),

        "routes": data

    }



    # ====================================
    # SEARCH BY ROUTE NUMBER
    # ====================================

    def find_route(
        self,
        route_number,
        role,
        user
    ):


        route_filter = get_rbac_filter(

            role,

            user,

            "routes",

            self.db

        )


        route = self.db["routes"].find_one({

            "$and":[

                route_filter,

                {
                    "routeNumber":{

                        "$regex":
                        route_number,

                        "$options":
                        "i"

                    }
                }

            ]

        })


        if not route:
            return None


        return self.get_route_details(

            route["_id"],

            role,

            user

        )



    # ====================================
    # TOTAL ROUTES
    # ====================================

    def get_route_count(
        self,
        role,
        user
    ):


        return self.db["routes"].count_documents(

            get_rbac_filter(

                role,

                user,

                "routes",

                self.db

            )

        )