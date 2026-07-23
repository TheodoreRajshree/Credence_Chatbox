from bson import ObjectId
from rbac import get_rbac_filter
import re

from datetime import datetime, timezone, timedelta

class ReportDistanceEngine:

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
    # ID FILTER HELPER
    # =====================================

    def id_filter(self, field, value):

        try:
            obj = ObjectId(str(value))
        except:
            obj = value


        return {
            "$or": [
                {
                    field: obj
                },
                {
                    field: str(value)
                }
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
    # VEHICLE DISTANCE REPORT
    # =====================================

    def get_vehicle_distance_report(
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


        report_filter = get_rbac_filter(
            role,
            user,
            "report_distances",
            self.db
        )


        reports = list(

            self.db["report_distances"].find({

                "$and": [

                    report_filter,

                    {
    "uniqueId": {
        "$in": self.normalize_unique_id(unique_id)
    }
}

                ]

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
    # SCHOOL DISTANCE REPORT
    # =====================================

    def get_school_distance_report(
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

        report_filter = get_rbac_filter(
        role,
        user,
        "report_distances",
        self.db
    )

        reports = list(

            self.db["report_distances"].find({

            "$and": [

                report_filter,

                {
                    "uniqueId": {
                        "$in": unique_ids
                    }
                }

            ]

        })
        .sort("createdAt", -1)
        .limit(limit)

    )

        return [

        self.clean(r)

        for r in reports

    ]

    # =====================================
    # BRANCH DISTANCE REPORT
    # =====================================

    def get_branch_distance_report(
    self,
    branch_id,
    role,
    user
):

    # =====================================
    # 1. GET ALLOWED DEVICES OF BRANCH
    # =====================================

        devices = self.get_allowed_devices(

        role,

        user,

        self.id_filter(

            "branchId",

            branch_id

        )

    )


        if not devices:

            return []


    # =====================================
    # 2. IST TODAY RANGE
    # =====================================

        IST = timezone(

        timedelta(

            hours=5,

            minutes=30

        )

    )


        now = datetime.now(IST)


        today_start = now.replace(

        hour=0,

        minute=0,

        second=0,

        microsecond=0

    )


        today_end = now.replace(

        hour=23,

        minute=59,

        second=59,

        microsecond=999999

    )


    # =====================================
    # 3. HISTORY RBAC FILTER
    # =====================================

        history_filter = get_rbac_filter(

        role,

        user,

        "histories",

        self.db

    )


        result = []


    # =====================================
    # 4. PROCESS EACH VEHICLE
    # =====================================

        for device in devices:


            unique_id = device.get(

            "uniqueId"

        )


            if not unique_id:

                continue


            unique_ids = self.normalize_unique_id(

            unique_id

        )


            if not unique_ids:

                continue


        # =================================
        # 5. LAST ODOMETER BEFORE TODAY
        # =================================

            previous_record = (

            self.db["histories"].find_one(

                {

                    "$and": [

                        history_filter,

                        {

                            "uniqueId": {

                                "$in": unique_ids

                            }

                        },

                        {

                            "attributes.totalDistance": {

                                "$ne": None

                            }

                        },

                        {

                            "createdAt": {

                                "$lt": today_start

                            }

                        }

                    ]

                },

                sort=[

                    (

                        "createdAt",

                        -1

                    )

                ]

            )

        )


        # =================================
        # 6. LATEST ODOMETER TODAY
        # =================================

            today_last_record = (

            self.db["histories"].find_one(

                {

                    "$and": [

                        history_filter,

                        {

                            "uniqueId": {

                                "$in": unique_ids

                            }

                        },

                        {

                            "attributes.totalDistance": {

                                "$ne": None

                            }

                        },

                        {

                            "createdAt": {

                                "$gte": today_start,

                                "$lte": today_end

                            }

                        }

                    ]

                },

                sort=[

                    (

                        "createdAt",

                        -1

                    )

                ]

            )

        )


        # =================================
        # 7. NO HISTORY TODAY
        # =================================

            if not today_last_record:

                result.append({

                "vehicleName": (

                    device.get("name")

                    or device.get("vehicleName")

                    or device.get("vehicleNumber")

                    or "N/A"

                ),

                "deviceId": str(

                    device.get("_id")

                ),

                "uniqueId": device.get(

                    "uniqueId"

                ),

                "status": device.get(

                    "status"

                ),

                "category": device.get(

                    "category"

                ),

                "model": device.get(

                    "model"

                ),

                "todayDistanceKm": 0,

                "startOdometerKm": None,

                "endOdometerKm": None,

                "message": (

                    "No history found for today."

                )

            })


                continue


        # =================================
        # 8. START ODOMETER
        # =================================

            if previous_record:

                start_distance = (

                previous_record[

                    "attributes"

                ][

                    "totalDistance"

                ]

                / 1000

            )


                start_record_time = (

                previous_record.get(

                    "createdAt"

                )

            )


            else:


            # =============================
            # FIRST RECORD OF TODAY
            # =============================

                first_today_record = (

                self.db["histories"].find_one(

                    {

                        "$and": [

                            history_filter,

                            {

                                "uniqueId": {

                                    "$in": unique_ids

                                }

                            },

                            {

                                "attributes.totalDistance": {

                                    "$ne": None

                                }

                            },

                            {

                                "createdAt": {

                                    "$gte": today_start,

                                    "$lte": today_end

                                }

                            }

                        ]

                    },

                    sort=[

                        (

                            "createdAt",

                            1

                        )

                    ]

                )

            )


                if not first_today_record:

                    result.append({

                    "vehicleName": (

                        device.get("name")

                        or device.get("vehicleName")

                        or device.get("vehicleNumber")

                        or "N/A"

                    ),

                    "deviceId": str(

                        device.get("_id")

                    ),

                    "uniqueId": device.get(

                        "uniqueId"

                    ),

                    "todayDistanceKm": 0,

                    "startOdometerKm": None,

                    "endOdometerKm": None,

                    "message": (

                        "No starting history found."

                    )

                })


                    continue


                start_distance = (

                    first_today_record[

                    "attributes"

                ][

                    "totalDistance"

                ]

                / 1000

            )


                start_record_time = (

                first_today_record.get(

                    "createdAt"

                )

            )


        # =================================
        # 9. END ODOMETER
        # =================================

            end_distance = (

            today_last_record[

                "attributes"

            ][

                "totalDistance"

            ]

            / 1000

        )


        # =================================
        # 10. CALCULATE TODAY DISTANCE
        # =================================

            today_distance = round(

            end_distance

            - start_distance,

            2

        )


        # =================================
        # 11. PREVENT NEGATIVE DISTANCE
        # =================================

            if today_distance < 0:

                today_distance = 0


        # =================================
        # 12. ADD VEHICLE REPORT
        # =================================

            result.append({

            "vehicleName": (

                device.get("name")

                or device.get("vehicleName")

                or device.get("vehicleNumber")

                or "N/A"

            ),

            "deviceId": str(

                device.get("_id")

            ),

            "uniqueId": device.get(

                "uniqueId"

            ),

            "status": device.get(

                "status"

            ),

            "category": device.get(

                "category"

            ),

            "model": device.get(

                "model"

            ),

            "todayDistanceKm": today_distance,

            "startOdometerKm": round(

                start_distance,

                2

            ),

            "endOdometerKm": round(

                end_distance,

                2

            ),

            "firstRecord": start_record_time,

            "lastRecord": (

                today_last_record.get(

                    "createdAt"

                )

            )

        })


    # =====================================
    # 13. RETURN ALL VEHICLES
    # =====================================

        return result



    # =====================================
    # DRIVER DISTANCE REPORT
    # =====================================

    def get_driver_distance_report(
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


        return self.get_vehicle_distance_report(

            device.get("uniqueId"),

            role,

            user,

            limit

        )



    # =====================================
    # ALL REPORTS
    # =====================================

    def get_all_distance_reports(
        self,
        role,
        user,
        limit=200
    ):


        report_filter = get_rbac_filter(
            role,
            user,
            "report_distances",
            self.db
        )


        reports = list(

            self.db["report_distances"]
            .find(report_filter)
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
    # REPORT COUNT
    # =====================================

    def get_report_count(
        self,
        unique_id,
        role,
        user
    ):

        reports = self.get_vehicle_distance_report(

            unique_id,

            role,

            user,

            limit=999999

        )

        return len(reports)



    # =====================================
    # TOTAL DISTANCE
    # =====================================

    def get_total_distance(
        self,
        unique_id,
        role,
        user
    ):

        reports = self.get_vehicle_distance_report(

            unique_id,

            role,

            user,

            limit=999999

        )


        total = 0


        for report in reports:

            try:

                total += float(
                    report.get(
                        "distance",
                        0
                    )
                )

            except:

                pass


        return round(total,2)