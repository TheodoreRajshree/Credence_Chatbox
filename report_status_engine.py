from bson import ObjectId
from rbac import get_rbac_filter


class ReportStatusEngine:

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
    # VEHICLE STATUS REPORT
    # =====================================

    def get_vehicle_status_report(
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


        status_filter = get_rbac_filter(

            role,
            user,
            "report_statuses",
            self.db

        )


        reports = list(

            self.db["report_statuses"].find({

                "$and":[

                    status_filter,

                    {
    "uniqueId":{
        "$in": self.normalize_unique_id(unique_id)
    }
}

                ]

            })

            .sort(
                "startDateTime",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(r)

            for r in reports

        ]

    def get_school_status_report(
            self,
        school_id,
    role,
    user,
    limit=100
):

        print("SCHOOL ID:", school_id)
        print("USER ID:", user["_id"])


    # get RBAC allowed devices only
        devices = self.get_allowed_devices(
        role,
        user
    )


        print(
        "DEVICES FOUND:",
        len(devices)
    )


        unique_ids = []


        for device in devices:

            uid = device.get("uniqueId")

            if uid:

                unique_ids.extend(
            self.normalize_unique_id(uid)
        )


        print(
        "UNIQUE IDS:",
        unique_ids
    )


        if not unique_ids:
            return []



        reports = list(

            self.db["report_statuses"].find({

            "uniqueId":{

                "$in":unique_ids

            }

        })

        .sort(
            "startDateTime",
            -1
        )

        .limit(limit)

    )


        print(
        "REPORTS FOUND:",
        len(reports)
    )


        return [

        self.clean(r)

        for r in reports

    ]

    # =====================================
    # SCHOOL STATUS REPORT
    # =====================================

    

# =====================================
# SINGLE BRANCH VEHICLE STATUS REPORT
# =====================================
    # from bson import ObjectId

    def get_single_branch_vehicle_status_report(
    self,
    branch_id,
    unique_id,
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

        branch_conditions = [
        {"branchId": str(branch_id)}
    ]

        try:
            branch_conditions.append(
            {"branchId": ObjectId(str(branch_id))}
        )
        except:
            pass

    # Verify vehicle belongs to this branch
        device = self.db["devices"].find_one({

        "$and": [

            device_filter,

            {
                "$or": branch_conditions
            },

            {
                "uniqueId": {
                    "$in": self.normalize_unique_id(unique_id)
                }
            }

        ]

    })

        if not device:
            return []

        status_filter = get_rbac_filter(
        role,
        user,
        "report_statuses",
        self.db
    )

        reports = list(

        self.db["report_statuses"].find({

            "$and":[

                status_filter,

                {
                    "uniqueId":{
                        "$in": self.normalize_unique_id(unique_id)
                    }
                }

            ]

        })

        .sort("startDateTime", -1)
        .limit(limit)

    )

        return [

        self.clean(report)

        for report in reports

    ]
    # =====================================
    # BRANCH STATUS REPORT
    # =====================================

    def get_branch_status_report(
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


        status_filter = get_rbac_filter(

            role,
            user,
            "report_statuses",
            self.db

        )


        reports = list(

            self.db["report_statuses"].find({

                "$and":[

                    status_filter,

                    {
                        "uniqueId":{
                            "$in":
                            unique_ids
                        }
                    }

                ]

            })

            .sort(
                "startDateTime",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(r)

            for r in reports

        ]



    # =====================================
    # DRIVER STATUS REPORT
    # =====================================

    def get_driver_status_report(
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


        return self.get_vehicle_status_report(

            device.get("uniqueId"),

            role,

            user,

            limit

        )



    # =====================================
    # ALL STATUS REPORTS
    # =====================================

    def get_all_status_reports(
        self,
        role,
        user,
        limit=200
    ):


        status_filter = get_rbac_filter(

            role,
            user,
            "report_statuses",
            self.db

        )


        reports = list(

            self.db["report_statuses"]

            .find(status_filter)

            .sort(
                "startDateTime",
                -1
            )

            .limit(limit)

        )


        return [

            self.clean(r)

            for r in reports

        ]



    # =====================================
    # STATUS COUNT
    # =====================================

    def get_status_count(
        self,
        unique_id,
        role,
        user
    ):


        reports = self.get_vehicle_status_report(

            unique_id,

            role,

            user,

            limit=999999

        )


        return len(reports)
    






