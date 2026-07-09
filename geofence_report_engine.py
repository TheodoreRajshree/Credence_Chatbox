from bson import ObjectId

from rbac import get_rbac_filter
from geofences_engine import GeofencesEngine
class GeofenceReportEngine:

    def __init__(self, db):

        self.db = db
        self.geofences_engine = GeofencesEngine(db)
    def normalize_unique_id(self, uid):

        ids = set()

        if uid is None:
            return []

        ids.add(uid)
        ids.add(str(uid))

        try:
            ids.add(int(float(uid)))
        except Exception:
            pass

        try:
            ids.add(float(uid))
        except Exception:
            pass

        return list(ids)
    def clean(self, doc):

        if doc is None:
            return None

        if isinstance(doc, list):
            return [self.clean(x) for x in doc]

        if not isinstance(doc, dict):
            return doc

        result = {}

        for key, value in doc.items():

            if isinstance(value, ObjectId):
                result[key] = str(value)

            elif isinstance(value, dict):
                result[key] = self.clean(value)

            elif isinstance(value, list):
                result[key] = [self.clean(v) for v in value]

            else:
                result[key] = value

        return result
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

        query = device_filter

        if extra_filter:
            query = {
            "$and": [
                device_filter,
                extra_filter
            ]
        }

        return list(
        self.db["devices"].find(query)
    )

    def get_driver_geofence_report(
    self,
    username,
    role,
    user,
    limit=100
):

        driver_filter = get_rbac_filter(
        role,
        user,
        "drivers",
        self.db
    )

        driver = self.db["drivers"].find_one({

        "$and": [

            driver_filter,

            {
                "username": username
            }

        ]

    })

        if not driver:
            return []

        route_id = driver.get("routeObjId")

        if not route_id:
            return []

        geofences = self.geofences_engine.get_route_geofences(

        route_id,

        role,

        user

    )

        geofence_ids = []

        for geofence in geofences:

            gid = geofence.get("_id")

            if gid:

                try:
                    geofence_ids.append(ObjectId(str(gid)))
                except Exception:
                    geofence_ids.append(gid)

        if not geofence_ids:
            return []

        return self.get_reports_by_geofence_ids(

        geofence_ids,

        role,

        user,

        limit

    )

    def get_reports_by_geofence_ids(
    self,
    geofence_ids,
    role,
    user,
    limit=100
):

        if not geofence_ids:
            return []

        report_filter = get_rbac_filter(
        role,
        user,
        "geofencereports",
        self.db
    )

        reports = list(

        self.db["geofencereports"].find({

            "$and": [

                report_filter,

                {
                    "geofenceId": {
                        "$in": geofence_ids
                    }
                }

            ]

        }).sort(
            "timestamp",
            -1
        ).limit(limit)

    )

        return [self.clean(r) for r in reports]
    # =====================================
# VEHICLE GEOFENCE REPORT
# =====================================

    def get_vehicle_geofence_reports(
    self,
    unique_id,
    role,
    user,
    limit=100
):

        report_filter = get_rbac_filter(
        role,
        user,
        "geofencereports",
        self.db
    )

        reports = list(

        self.db["geofencereports"].find({

            "$and": [

                report_filter,

                {
                    "uniqueId": {
                        "$in": self.normalize_unique_id(unique_id)
                    }
                }

            ]

        })

        .sort("timestamp", -1)

        .limit(limit)

    )

        return [

        self.clean(report)

        for report in reports

    ]


# =====================================
# SCHOOL REPORT
# =====================================

    def get_school_geofence_reports(
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
    "schoolId": str(school_id)
}

    )

        unique_ids = set()

        for device in devices:

            uid = device.get("uniqueId")

            if uid:

                unique_ids.update(
                self.normalize_unique_id(uid)
            )

        if not unique_ids:

            return []

        report_filter = get_rbac_filter(

        role,

        user,

        "geofencereports",

        self.db

    )

        reports = list(

        self.db["geofencereports"].find({

            "$and": [

                report_filter,

                {

                    "uniqueId": {

                        "$in": list(unique_ids)

                    }

                }

            ]

        })

        .sort("timestamp", -1)

        .limit(limit)

    )

        return [

        self.clean(report)

        for report in reports

    ]


# =====================================
# BRANCH REPORT
# =====================================

    def get_branch_geofence_reports(
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
            "branchId": ObjectId(str(branch_id))
        }

    )

        unique_ids = set()

        for device in devices:

            uid = device.get("uniqueId")

            if uid:

                unique_ids.update(
                self.normalize_unique_id(uid)
            )

        if not unique_ids:

            return []

        report_filter = get_rbac_filter(

        role,

        user,

        "geofencereports",

        self.db

    )

        reports = list(

        self.db["geofencereports"].find({

            "$and": [

                report_filter,

                {

                    "uniqueId": {

                        "$in": list(unique_ids)

                    }

                }

            ]

        })

        .sort("timestamp", -1)

        .limit(limit)

    )

        return [

        self.clean(report)

        for report in reports

    ]
    def get_all_geofence_reports(
    self,
    role,
    user,
    limit=200
):

        report_filter = get_rbac_filter(

        role,

        user,

        "geofencereports",

        self.db

    )

        reports = list(

        self.db["geofencereports"]

        .find(report_filter)

        .sort(

            "timestamp",

            -1

        )

        .limit(limit)

    )

        return [

        self.clean(report)

        for report in reports

    ]