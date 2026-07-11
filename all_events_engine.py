from bson import ObjectId
from rbac import get_rbac_filter


class AllEventsEngine:

    def __init__(self, db):
        self.db = db
        # =====================================
    # UNIQUE ID NORMALIZER
    # =====================================

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

    # =====================================
    # CLEAN
    # =====================================

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
    # VEHICLE EVENTS
    # =====================================

    def get_vehicle_events(
        self,
        unique_id,
        role,
        user,
        limit=50
    ):

        rbac_filter = get_rbac_filter(
            role,
            user,
            "allevents",
            self.db
        )


        query = {

            "$and": [

                rbac_filter,

            {
    "uniqueId": {
        "$in": self.normalize_unique_id(unique_id)
    }
}  

            ]

        }


        events = list(

            self.db["allevents"]

            .find(query)

            .sort(
                "eventTime",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(e)

            for e in events

        ]



    # =====================================
    # SCHOOL EVENTS
    # =====================================

    def get_school_events(
        self,
        school_id,
        role,
        user,
        limit=100
    ):


        device_filter = get_rbac_filter(
            role,
            user,
            "devices",
            self.db
        )


        devices = list(

            self.db["devices"]

            .find({

                "$and": [

                    device_filter,

                    {
                        "schoolId":
                        ObjectId(str(school_id))
                    }

                ]

            })

        )


        unique_ids = []

        for d in devices:

            uid = d.get("uniqueId")

            if uid:

                unique_ids.extend(
            self.normalize_unique_id(uid)
        )


        if not unique_ids:
            return []



        event_filter = get_rbac_filter(
            role,
            user,
            "allevents",
            self.db
        )


        events = list(

            self.db["allevents"]

            .find({

                "$and": [

                    event_filter,

                    {

                        "uniqueId":
                        {
                            "$in": unique_ids
                        }

                    }

                ]

            })

            .sort(
                "eventTime",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(e)

            for e in events

        ]



    # =====================================
    # BRANCH EVENTS
    # =====================================

    def get_branch_events(
        self,
        branch_id,
        role,
        user,
        limit=100
    ):
    

        device_filter = get_rbac_filter(
            role,
            user,
            "devices",
            self.db
        )


        devices = list(

            self.db["devices"]

            .find({

                "$and":[

                    device_filter,

                    {

                        "branchId":
                        ObjectId(str(branch_id))

                    }

                ]

            })

        )


        unique_ids = []

        for d in devices:

            uid = d.get("uniqueId")

            if uid:

                unique_ids.extend(
            self.normalize_unique_id(uid)
        )


        if not unique_ids:
            return []



        event_filter = get_rbac_filter(
            role,
            user,
            "allevents",
            self.db
        )


        events = list(

            self.db["allevents"]

            .find({

                "$and":[

                    event_filter,

                    {

                        "uniqueId":
                        {
                            "$in": unique_ids
                        }

                    }

                ]

            })

            .sort(
                "eventTime",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(e)

            for e in events

        ]



    # =====================================
    # DRIVER EVENTS
    # =====================================

    def get_driver_events(
        self,
        username,
        role,
        user,
        limit=50
    ):


        driver_filter = get_rbac_filter(
            role,
            user,
            "drivers",
            self.db
        )


        driver = self.db["drivers"].find_one({

            "$and":[

                driver_filter,

                {
                    "username": username
                }

            ]

        })


        if not driver:
            return []



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

                    "_id":
                    driver.get(
                        "deviceObjId"
                    )

                }

            ]

        })


        if not device:
            return []



        return self.get_vehicle_events(

            device.get("uniqueId"),

            role,

            user,

            limit

        )



    # =====================================
    # SUPER ADMIN / ALL EVENTS
    # =====================================

    def get_all_events(
        self,
        role,
        user,
        limit=200
    ):


        rbac_filter = get_rbac_filter(
            role,
            user,
            "allevents",
            self.db
        )


        events = list(

            self.db["allevents"]

            .find(rbac_filter)

            .sort(
                "eventTime",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(e)

            for e in events

        ]



    # =====================================
    # EVENT COUNT
    # =====================================

    def get_event_count_by_vehicle(
        self,
        unique_id,
        role,
        user
    ):


        rbac_filter = get_rbac_filter(
            role,
            user,
            "allevents",
            self.db
        )


        return self.db["allevents"].count_documents({

            "$and":[

                rbac_filter,

                {
    "uniqueId": {
        "$in": self.normalize_unique_id(unique_id)
    }
}

            ]

        })



    # =====================================
    # EVENT SUMMARY
    # =====================================

    def get_event_summary(
        self,
        unique_id,
        role,
        user
    ):


        rbac_filter = get_rbac_filter(
            role,
            user,
            "allevents",
            self.db
        )


        pipeline = [

            {

                "$match":{

                    "$and":[

                        rbac_filter,

                        {
    "uniqueId": {
        "$in": self.normalize_unique_id(unique_id)
    }
}

                    ]

                }

            },


            {

                "$group":{

                    "_id":
                    "$eventType",

                    "count":
                    {
                        "$sum":1
                    }

                }

            }

        ]


        return list(

            self.db["allevents"]

            .aggregate(
                pipeline
            )

        )