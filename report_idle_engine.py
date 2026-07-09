from bson import ObjectId
from rbac import get_rbac_filter


class ReportIdleEngine:

    def __init__(self, db):
        self.db = db

        # =====================================
    # UNIQUE ID NORMALIZER
    # =====================================
    
    def normalize_unique_id(self, uid):

        if uid is None:
            return []

        ids = [str(uid)]

        try:
            number = int(str(uid))

        # Only include integer if it fits BSON Int64
            if -(2**63) <= number <= (2**63 - 1):
                ids.append(number)

        except Exception:
            pass

        return ids
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
    # VEHICLE IDLE REPORT
    # =====================================

    def get_vehicle_idle_report(
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


        idle_filter = get_rbac_filter(

            role,

            user,

            "report_idles",

            self.db

        )


        reports = list(

            self.db["report_idles"].find({

                "$and":[

                    idle_filter,

                    {
    "uniqueId":{
        "$in": self.normalize_unique_id(unique_id)
    }
}

                ]

            })

            .sort(
                "idleStartTime",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(r)

            for r in reports

        ]



    # =====================================
    # SCHOOL IDLE REPORT
    # =====================================

    def get_school_idle_report(
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


        unique_ids = []

        for device in devices:

            uid = device.get("uniqueId")

            if uid:

                unique_ids.extend(
            self.normalize_unique_id(uid)
        )


        if not unique_ids:
            return []


        idle_filter = get_rbac_filter(

            role,

            user,

            "report_idles",

            self.db

        )


        reports = list(

            self.db["report_idles"].find({

                "$and":[

                    idle_filter,

                    {
                        "uniqueId":{
                            "$in":
                            unique_ids
                        }
                    }

                ]

            })

            .sort(
                "idleStartTime",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(r)

            for r in reports

        ]



    # =====================================
    # BRANCH IDLE REPORT
    # =====================================

    def get_branch_idle_report(
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


        unique_ids = []

        for device in devices:

            uid = device.get("uniqueId")

            if uid:

                unique_ids.extend(
            self.normalize_unique_id(uid)
        )

        if not unique_ids:
            return []


        idle_filter = get_rbac_filter(

            role,

            user,

            "report_idles",

            self.db

        )


        reports = list(

            self.db["report_idles"].find({

                "$and":[

                    idle_filter,

                    {
                        "uniqueId":{
                            "$in":
                            unique_ids
                        }
                    }

                ]

            })

            .sort(
                "idleStartTime",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(r)

            for r in reports

        ]



    # =====================================
    # DRIVER IDLE REPORT
    # =====================================

    def get_driver_idle_report(
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


        return self.get_vehicle_idle_report(

            device.get("uniqueId"),

            role,

            user,

            limit

        )



    # =====================================
    # ALL IDLE REPORTS
    # =====================================

    def get_all_idle_reports(
        self,
        role,
        user,
        limit=200
    ):


        idle_filter = get_rbac_filter(

            role,

            user,

            "report_idles",

            self.db

        )


        reports = list(

            self.db["report_idles"]

            .find(idle_filter)

            .sort(
                "idleStartTime",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(r)

            for r in reports

        ]



    # =====================================
    # REPORT COUNT
    # =====================================

    def get_idle_count(
        self,
        unique_id,
        role,
        user
    ):


        reports = self.get_vehicle_idle_report(

            unique_id,

            role,

            user,

            limit=999999

        )


        return len(reports)