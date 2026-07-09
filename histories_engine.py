from bson import ObjectId
from rbac import get_rbac_filter


class HistoriesEngine:

    def __init__(self, db):
        self.db = db


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
    # GET ALLOWED DEVICES
    # =====================================

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



    # =====================================
    # VEHICLE HISTORY
    # =====================================

    def get_vehicle_history(
        self,
        unique_id,
        role,
        user,
        limit=100
    ):


        devices = self.get_allowed_devices(

            role,
            user,

            {
                "uniqueId":{
                    "$in":[
                        unique_id,
                        str(unique_id)
                    ]
                }
            }
        )


        if not devices:
            return []


        history_filter = get_rbac_filter(
            role,
            user,
            "histories",
            self.db
        )


        histories=list(

            self.db["histories"].find({

                "$and":[

                    history_filter,

                    {
                        "uniqueId":
                        str(unique_id)
                    }

                ]

            })

            .sort(
                "fixTime",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(h)

            for h in histories

        ]



    # =====================================
    # SCHOOL HISTORY
    # =====================================

    def get_school_history(
        self,
        school_id,
        role,
        user,
        limit=100
    ):


        devices=self.get_allowed_devices(

            role,
            user,

            {
                "schoolId":
                ObjectId(str(school_id))
            }

        )


        unique_ids=[

            str(d.get("uniqueId"))

            for d in devices

            if d.get("uniqueId")

        ]


        if not unique_ids:
            return []


        history_filter=get_rbac_filter(

            role,
            user,
            "histories",
            self.db

        )


        histories=list(

            self.db["histories"].find({

                "$and":[

                    history_filter,

                    {
                        "uniqueId":
                        {
                            "$in":
                            unique_ids
                        }
                    }

                ]

            })

            .sort(
                "fixTime",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(h)

            for h in histories

        ]



    # =====================================
    # BRANCH HISTORY
    # =====================================

    def get_branch_history(
        self,
        branch_id,
        role,
        user,
        limit=100
    ):


        devices=self.get_allowed_devices(

            role,
            user,

            {
                "branchId":
                ObjectId(str(branch_id))
            }

        )


        unique_ids=[

            str(d.get("uniqueId"))

            for d in devices

            if d.get("uniqueId")

        ]


        if not unique_ids:
            return []


        history_filter=get_rbac_filter(

            role,
            user,
            "histories",
            self.db

        )


        histories=list(

            self.db["histories"].find({

                "$and":[

                    history_filter,

                    {

                        "uniqueId":

                        {
                            "$in":
                            unique_ids
                        }

                    }

                ]

            })

            .sort(
                "fixTime",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(h)

            for h in histories

        ]



    # =====================================
    # DRIVER HISTORY
    # =====================================

    def get_driver_history(
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


        device=self.db["devices"].find_one({

            "$and":[

                get_rbac_filter(
                    role,
                    user,
                    "devices",
                    self.db
                ),

                {
                    "_id":
                    driver.get("deviceObjId")
                }

            ]

        })


        if not device:
            return []


        return self.get_vehicle_history(

            device.get("uniqueId"),

            role,

            user,

            limit

        )



    # =====================================
    # ALL HISTORY
    # =====================================

    def get_all_history(
        self,
        role,
        user,
        limit=200
    ):


        history_filter=get_rbac_filter(

            role,
            user,
            "histories",
            self.db

        )


        histories=list(

            self.db["histories"]

            .find(history_filter)

            .sort(
                "fixTime",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(h)

            for h in histories

        ]



    # =====================================
    # HISTORY COUNT
    # =====================================

    def get_history_count(
        self,
        unique_id,
        role,
        user
    ):


        histories=self.get_vehicle_history(

            unique_id,

            role,

            user,

            limit=999999

        )


        return len(histories)



    # =====================================
    # LATEST HISTORY
    # =====================================

    def get_latest_history(
        self,
        unique_id,
        role,
        user
    ):


        histories=self.get_vehicle_history(

            unique_id,

            role,

            user,

            limit=1

        )


        if histories:
            return histories[0]


        return None