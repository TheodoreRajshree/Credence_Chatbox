from bson import ObjectId
from rbac import get_rbac_filter


class ReportTripEngine:

    def __init__(self, db):
        self.db = db

        # =====================================
    # UNIQUE ID NORMALIZER
    # =====================================

    def normalize_unique_id(self, uid):

        ids = []

        if uid is None:
            return ids


        # original value
        ids.append(uid)


        # string value
        ids.append(str(uid))


        # integer value
        try:
            ids.append(int(float(uid)))
        except:
            pass


        # float value (Mongo report_trips has float uniqueId)
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
        print("ROLE:", role)
        print("USER:", user)
        print("DEVICE RBAC:", device_filter)
        print("EXTRA FILTER:", extra_filter)


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
    # VEHICLE TRIPS
    # =====================================

    def get_vehicle_trips(
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
                "$in": self.normalize_unique_id(unique_id)
            }
        }
    )


        if not devices:
            return []


        trip_filter = get_rbac_filter(
        role,
        user,
        "report_trips",
        self.db
    )


        reports = list(

        self.db["report_trips"].find({

            "$and":[

                trip_filter,

                {
                    "uniqueId":{
                        "$in": self.normalize_unique_id(unique_id)
                    }
                }

            ]

        })

        .sort(
            "startTime",
            -1
        )

        .limit(limit)

    )


        return [

        self.clean(r)

        for r in reports

    ]


    # =====================================
    # SCHOOL TRIPS
    # =====================================

    def get_school_trips(
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
        unique_ids = [

            str(device.get("uniqueId"))

            for device in devices

            if device.get("uniqueId")

        ]


        if not unique_ids:
            return []


        trip_filter = get_rbac_filter(

            role,
            user,
            "report_trips",
            self.db

        )


        reports = list(

            self.db["report_trips"].find({

                "$and":[

                    trip_filter,

                    {
                        "uniqueId":{
                            "$in":
                            unique_ids
                        }
                    }

                ]

            })

            .sort(
                "startTime",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(r)

            for r in reports

        ]


    # =====================================
    # BRANCH TRIPS
    # =====================================

    def get_branch_trips(
    self,
    branch_id,
    role,
    user,
    limit=100
):


        branch_filter = {

        "branchId":
        ObjectId(str(branch_id))

    }


        devices = self.get_allowed_devices(
        role,
        user,
        branch_filter
    )


        print("BRANCH DEVICES:", len(devices))


        unique_ids = []


        for device in devices:

            uid = device.get("uniqueId")


            if uid:

                unique_ids.extend(
                self.normalize_unique_id(uid)
            )


        print(
        "TRIP UNIQUE IDS:",
        unique_ids[:10]
    )


        if not unique_ids:

            return []


        trip_filter = get_rbac_filter(

        role,
        user,
        "report_trips",
        self.db

    )


        print(
        "REPORT RBAC:",
        trip_filter
    )


        reports = list(

        self.db["report_trips"].find({

            "$and":[

                trip_filter,

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
            "startTime",
            -1
        )

        .limit(limit)

    )


        print(
        "TRIPS FOUND:",
        len(reports)
    )


        return [

        self.clean(r)

        for r in reports

    ]
    # =====================================
    # DRIVER TRIPS
    # =====================================

    def get_driver_trips(
        self,
        username,
        role,
        user,
        limit=100
    ):


        driver = self.db["drivers"].find_one({

            "$and":[

                get_rbac_filter(

                    role,
                    user,
                    "drivers",
                    self.db

                ),

                {
                    "username":
                    username
                }

            ]

        })


        if not driver:
            return []


        device = self.db["devices"].find_one({

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


        return self.get_vehicle_trips(

            device.get("uniqueId"),

            role,

            user,

            limit

        )



    # =====================================
    # ALL TRIPS
    # =====================================

    def get_all_trips(
        self,
        role,
        user,
        limit=200
    ):


        trip_filter = get_rbac_filter(

            role,
            user,
            "report_trips",
            self.db

        )


        reports = list(

            self.db["report_trips"]

            .find(trip_filter)

            .sort(
                "startTime",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(r)

            for r in reports

        ]



    # =====================================
    # COUNT
    # =====================================

    def get_trip_count(
        self,
        unique_id,
        role,
        user
    ):


        reports = self.get_vehicle_trips(

            unique_id,

            role,

            user,

            limit=999999

        )


        return len(reports)
    
