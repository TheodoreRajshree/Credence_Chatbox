from bson import ObjectId
from rbac import get_rbac_filter


class ReportStoppageEngine:

    def __init__(self, db):
        self.db = db
    

    # =====================================
    # CLEAN
    # =====================================
    def unique_id_values(self, value):

        return [
            str(value)
    ]
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
                "$and": [
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
    # VEHICLE STOPPAGE REPORT
    # =====================================

    def get_vehicle_stoppage_report(
        self,
        unique_id,
        role,
        user,
        limit=100
    ):


        # check device permission

        devices = self.get_allowed_devices(

            role,
            user,

            {
                "uniqueId":
                {
                    "$in": self.unique_id_values(unique_id)
                }
            }

        )


        if not devices:
            return []



        stoppage_filter = get_rbac_filter(

            role,
            user,
            "report_stopages",
            self.db

        )


        reports = list(

            self.db["report_stopages"].find({

                "$and":[

                    stoppage_filter,

                    {
                        "uniqueId":
                        {
                            "$in":[
                                unique_id,
                                str(unique_id)
                            ]
                        }
                    }

                ]

            })

            .sort(
                "arrivalTime",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(r)

            for r in reports

        ]



    # =====================================
    # SCHOOL STOPPAGE REPORT
    # =====================================

    def get_school_stoppage_report(
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
            "schoolId": ObjectId(str(school_id))
        }
    )


        if not devices:
            return []


        unique_ids = []

        for device in devices:

            uid = device.get("uniqueId")

            if uid is not None:

        # always search string format
                unique_ids.append(str(uid))

        # search integer format also
                try:
                    unique_ids.append(int(uid))
                except (ValueError, TypeError):
                    pass



        stoppage_filter = get_rbac_filter(
        role,
        user,
        "report_stopages",
        self.db
    )


        reports = list(

            self.db["report_stopages"].find({

            "$and":[

                stoppage_filter,

                {
                    "uniqueId":{
                        "$in": unique_ids
                    }
                }

            ]

        })

        .sort(
            "arrivalTime",
            -1
        )

        .limit(limit)

    )


        return [

        self.clean(r)

        for r in reports

    ]
    # =====================================
    # BRANCH STOPPAGE REPORT
    # =====================================

    def get_branch_stoppage_report(
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
            "$or":[

                {
                    "branchId": ObjectId(str(branch_id))
                },

                {
                    "branchId": str(branch_id)
                }

            ]
        }

    )


        if not devices:
            return []


        unique_ids=[]


        for device in devices:

            uid=device.get("uniqueId")

            if uid:

                unique_ids.append(uid)

                unique_ids.append(str(uid))


        if not unique_ids:
            return []


        stoppage_filter = get_rbac_filter(

        role,
        user,
        "report_stopages",
        self.db

    )


        reports=list(

            self.db["report_stopages"].find({

            "$and":[

                stoppage_filter,

                {
                    "uniqueId":{
                        "$in":unique_ids
                    }
                }

            ]

        })

        .sort(
            "arrivalTime",
            -1
        )

        .limit(limit)

    )


        return [

        self.clean(r)

        for r in reports

    ]


    # =====================================
    # DRIVER STOPPAGE REPORT
    # =====================================

    def get_driver_stoppage_report(
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



        return self.get_vehicle_stoppage_report(

            device.get("uniqueId"),

            role,

            user,

            limit

        )



    # =====================================
    # ALL STOPPAGE REPORTS
    # =====================================

    def get_all_stoppage_reports(
        self,
        role,
        user,
        limit=200
    ):


        stoppage_filter = get_rbac_filter(

            role,
            user,
            "report_stopages",
            self.db

        )


        reports = list(

            self.db["report_stopages"]

            .find(stoppage_filter)

            .sort(
                "arrivalTime",
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

    def get_stoppage_count(
        self,
        unique_id,
        role,
        user
    ):


        return len(

            self.get_vehicle_stoppage_report(

                unique_id,

                role,

                user,

                limit=999999

            )

        )