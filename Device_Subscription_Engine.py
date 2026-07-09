from bson import ObjectId
from rbac import get_rbac_filter


class DeviceSubscriptionEngine:

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
    # DEVICE SUBSCRIPTION
    # =====================================

    def get_device_subscription(
        self,
        device_id,
        role,
        user
    ):


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
                    ObjectId(str(device_id))

                }

            ]

        })


        if not device:
            return None



        subscription_filter = get_rbac_filter(
            role,
            user,
            "devicesubscriptions",
            self.db
        )


        subscription = self.db["devicesubscriptions"].find_one({

            "$and":[

                subscription_filter,

                {

                    "$or":[

                        {
                            "deviceId":
                            device["_id"]
                        },

                        {
                            "deviceId":
                            str(device["_id"])
                        }

                    ]

                }

            ]

        })


        return self.clean(subscription)



    # =====================================
    # GET USER DEVICES
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
    # SCHOOL SUBSCRIPTIONS
    # =====================================

    def get_school_subscriptions(
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


        device_ids = [

            d["_id"]

            for d in devices

        ]


        if not device_ids:
            return []



        subscription_filter = get_rbac_filter(

            role,

            user,

            "devicesubscriptions",

            self.db

        )


        subscriptions=list(

            self.db["devicesubscriptions"].find({

                "$and":[

                    subscription_filter,

                    {

                        "deviceId":
                        {

                            "$in":
                            device_ids

                        }

                    }

                ]

            })

            .sort(
                "paidAt",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(s)

            for s in subscriptions

        ]



    # =====================================
    # BRANCH SUBSCRIPTIONS
    # =====================================

    def get_branch_subscriptions(
        self,
        branch_id,
        role,
        user,
        limit=10
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



        subscription_filter = get_rbac_filter(

            role,

            user,

            "devicesubscriptions",

            self.db

        )


        subscriptions=list(

            self.db["devicesubscriptions"].find({

                "$and":[

                    subscription_filter,

                    {

                        "deviceId":
                        {

                            "$in":
                            device_ids

                        }

                    }

                ]

            })

            .sort(
                "paidAt",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(s)

            for s in subscriptions

        ]



    # =====================================
    # DRIVER SUBSCRIPTION
    # =====================================

    def get_driver_subscription(
        self,
        username,
        role,
        user
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
            return None



        device_id = driver.get(
            "deviceObjId"
        )


        if not device_id:
            return None



        return self.get_device_subscription(

            device_id,

            role,

            user

        )



    # =====================================
    # ALL SUBSCRIPTIONS
    # =====================================

    def get_all_subscriptions(
        self,
        role,
        user,
        limit=200
    ):


        subscription_filter = get_rbac_filter(

            role,

            user,

            "devicesubscriptions",

            self.db

        )


        subscriptions=list(

            self.db["devicesubscriptions"].find(
                subscription_filter
            )

            .sort(
                "paidAt",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(s)

            for s in subscriptions

        ]



    # =====================================
    # COUNT
    # =====================================

    def get_subscription_count(
        self,
        role,
        user
    ):


        subscription_filter = get_rbac_filter(

            role,

            user,

            "devicesubscriptions",

            self.db

        )


        return self.db["devicesubscriptions"].count_documents(

            subscription_filter

        )



    # =====================================
    # PAID SUBSCRIPTIONS
    # =====================================

    def get_paid_subscriptions(
        self,
        role,
        user,
        limit=100
    ):


        subscription_filter = get_rbac_filter(

            role,

            user,

            "devicesubscriptions",

            self.db

        )


        subscriptions=list(

            self.db["devicesubscriptions"].find({

                "$and":[

                    subscription_filter,

                    {
                        "status":
                        "PAID"
                    }

                ]

            })

            .sort(
                "paidAt",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(s)

            for s in subscriptions

        ]



    # =====================================
    # EXPIRED SUBSCRIPTIONS
    # =====================================

    def get_expired_subscriptions(
        self,
        role,
        user
    ):


        subscription_filter = get_rbac_filter(

            role,

            user,

            "devicesubscriptions",

            self.db

        )


        subscriptions=self.db["devicesubscriptions"].find({

            "$and":[

                subscription_filter,

                {

                    "status":
                    "EXPIRED"

                }

            ]

        })


        return [

            self.clean(s)

            for s in subscriptions

        ]