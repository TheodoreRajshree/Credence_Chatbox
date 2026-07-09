from bson import ObjectId
from rbac import get_rbac_filter


class DailyDistanceCacheEngine:

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
    # ID FILTER
    # =====================================

    def id_filter(self, field, value):

        try:
            obj = ObjectId(str(value))
        except:
            obj = value

        return {
            "$or": [
                {field: obj},
                {field: str(value)}
            ]
        }

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
    # VEHICLE DAILY DISTANCE
    # =====================================

    def get_vehicle_daily_distance(
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
                "uniqueId": {
                    "$in": self.normalize_unique_id(unique_id)
                }
            }

        )

        if not devices:
            return []

        reports = list(

            self.db["daily_distance_cache"].find({

                "uniqueId": {
                    "$in": self.normalize_unique_id(unique_id)
                }

            })

            .sort(
                "createdAt",
                -1
            )

            .limit(limit)

        )

        return [

            self.clean(r)

            for r in reports

        ]

    # =====================================
    # SCHOOL DAILY DISTANCE
    # =====================================

    def get_school_daily_distance(
        self,
        school_id,
        role,
        user,
        limit=100
    ):

        devices = self.get_allowed_devices(

            role,
            user,

            self.id_filter(
                "schoolId",
                school_id
            )

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

        reports = list(

            self.db["daily_vehicle_distance_caches"].find({

                "uniqueId": {
                    "$in": unique_ids
                }

            })

            .sort(
                "createdAt",
                -1
            )

            .limit(limit)

        )

        return [

            self.clean(r)

            for r in reports

        ]

    # =====================================
    # BRANCH DAILY DISTANCE
    # =====================================

    def get_branch_daily_distance(
        self,
        branch_id,
        role,
        user,
        limit=100
    ):

        devices = self.get_allowed_devices(

            role,
            user,

            self.id_filter(
                "branchId",
                branch_id
            )

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

        reports = list(

            self.db["daily_vehicle_distance_caches"].find({

                "uniqueId": {
                    "$in": unique_ids
                }

            })

            .sort(
                "createdAt",
                -1
            )

            .limit(limit)

        )

        return [

            self.clean(r)

            for r in reports

        ]
  
    # =====================================
    # DRIVER DAILY DISTANCE
    # =====================================

    def get_driver_daily_distance(
        self,
        username,
        role,
        user,
        limit=100
    ):

        driver = self.db["drivers"].find_one({

            "$and": [

                get_rbac_filter(
                    role,
                    user,
                    "drivers",
                    self.db
                ),

                {
                    "username": username
                }

            ]

        })

        if not driver:
            return []

        device = self.db["devices"].find_one({

            "$and": [

                get_rbac_filter(
                    role,
                    user,
                    "devices",
                    self.db
                ),

                {
                    "_id": driver.get("deviceObjId")
                }

            ]

        })

        if not device:
            return []

        return self.get_vehicle_daily_distance(

            device.get("uniqueId"),

            role,

            user,

            limit

        )

    # =====================================
    # ALL DAILY DISTANCE
    # =====================================

    def get_all_daily_distance(
        self,
        role,
        user,
        limit=200
    ):

        reports = list(

            self.db["daily_distance_cache"]

            .find()

            .sort(
                "createdAt",
                -1
            )

            .limit(limit)

        )

        return [

            self.clean(r)

            for r in reports

        ]

    # =====================================
    # TOTAL KM
    # =====================================

    def get_total_km(
        self,
        unique_id,
        role,
        user
    ):

        reports = self.get_vehicle_daily_distance(

            unique_id,

            role,

            user,

            limit=999999

        )

        total = 0

        for report in reports:

            try:
                total += float(
                    report.get("totalKm", 0)
                )
            except:
                pass

        return round(total, 2)

    # =====================================
    # REPORT COUNT
    # =====================================

    def get_daily_distance_count(
        self,
        unique_id,
        role,
        user
    ):

        reports = self.get_vehicle_daily_distance(

            unique_id,

            role,

            user,

            limit=999999

        )

        return len(reports)