from bson import ObjectId
from rbac import get_rbac_filter


class DeviceSubscriptionHistoryEngine:

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

            self.db["devices"]

            .find(query)

        )



    # =====================================
    # DEVICE HISTORY
    # =====================================

    def get_device_subscription_history(
        self,
        device_id,
        role,
        user,
        limit=10
    ):


        devices = self.get_allowed_devices(

            role,

            user,

            {

                "_id":
                ObjectId(str(device_id))

            }

        )


        if not devices:
            return []



        history_filter = get_rbac_filter(

            role,

            user,

            "devicesubscriptionhistories",

            self.db

        )


        histories=list(

            self.db["devicesubscriptionhistories"]

            .find({

                "$and":[

                    history_filter,

                    {

                        "$or":[

                            {

                                "deviceObjId":
                                devices[0]["_id"]

                            },

                            {

                                "deviceObjId":
                                str(devices[0]["_id"])

                            }

                        ]

                    }

                ]

            })

            .sort(
                "changedAt",
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

    def get_school_subscription_history(
        self,
        school_id,
        role,
        user,
        limit=100
    ):


        devices = self.get_allowed_devices(

            role,

            user,

            {

                "schoolId":
                ObjectId(str(school_id))

            }

        )


        device_ids=[

            d["_id"]

            for d in devices

        ]


        if not device_ids:
            return []



        history_filter = get_rbac_filter(

            role,

            user,

            "devicesubscriptionhistories",

            self.db

        )


        histories=list(

            self.db["devicesubscriptionhistories"]

            .find({

                "$and":[

                    history_filter,

                    {

                        "deviceObjId":
                        {

                            "$in":
                            device_ids

                        }

                    }

                ]

            })

            .sort(
                "changedAt",
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

    def get_branch_subscription_history(
        self,
        branch_id,
        role,
        user,
        limit=100
    ):


        devices = self.get_allowed_devices(

            role,

            user,

            {

                "branchId":
                ObjectId(str(branch_id))

            }

        )


        device_ids=[

            d["_id"]

            for d in devices

        ]


        if not device_ids:
            return []



        history_filter = get_rbac_filter(

            role,

            user,

            "devicesubscriptionhistories",

            self.db

        )


        histories=list(

            self.db["devicesubscriptionhistories"]

            .find({

                "$and":[

                    history_filter,

                    {

                        "deviceObjId":
                        {

                            "$in":
                            device_ids

                        }

                    }

                ]

            })

            .sort(
                "changedAt",
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

    def get_driver_subscription_history(
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


        device_id=driver.get(
            "deviceObjId"
        )


        if not device_id:
            return []


        return self.get_device_subscription_history(

            device_id,

            role,

            user,

            limit

        )



    # =====================================
    # ALL HISTORY
    # =====================================

    def get_all_subscription_history(
        self,
        role,
        user,
        limit=200
    ):


        history_filter = get_rbac_filter(

            role,

            user,

            "devicesubscriptionhistories",

            self.db

        )


        histories=list(

            self.db["devicesubscriptionhistories"]

            .find(history_filter)

            .sort(
                "changedAt",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(h)

            for h in histories

        ]



    # =====================================
    # COUNT
    # =====================================

    def get_history_count(
        self,
        device_id,
        role,
        user
    ):


        histories = self.get_device_subscription_history(

            device_id,

            role,

            user,

            limit=999999

        )


        return len(histories)



    # =====================================
    # LATEST CHANGE
    # =====================================

    def get_latest_subscription(
        self,
        device_id,
        role,
        user
    ):


        histories = self.get_device_subscription_history(

            device_id,

            role,

            user,

            limit=1

        )


        if histories:
            return histories[0]


        return None