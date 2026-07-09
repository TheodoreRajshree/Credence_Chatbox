from datetime import datetime, timedelta, timezone
import re
from bson import ObjectId

from rbac import get_rbac_filter


class VehicleKmEngine:

    def __init__(self, db):
        self.db = db

    # ==========================================
    # UNIQUE ID NORMALIZER
    # ==========================================

    def normalize_unique_id(self, uid):
        """
        Devices/collections store uniqueId inconsistently:
        - devices / report_distances: numeric (e.g. 350644270110506)
        - daily_vehicle_distance_cache: string (e.g. "867440065018202")
        We build every reasonable representation so `$in` matches
        regardless of which collection/type it's stored as.
        """
        ids = []

        if uid is None:
            return ids

        ids.append(uid)
        ids.append(str(uid))

        try:
            ids.append(int(float(uid)))
        except (TypeError, ValueError):
            pass

        try:
            ids.append(float(uid))
        except (TypeError, ValueError):
            pass

        return list(set(ids))

    # ==========================================
    # DEVICE ACCESS
    # ==========================================

    def get_allowed_device(self, unique_id, role, user):

        device_filter = get_rbac_filter(role, user, "devices", self.db)

        return self.db["devices"].find_one({
            "$and": [
                device_filter,
                {"uniqueId": {"$in": self.normalize_unique_id(unique_id)}}
            ]
        })

    # ==========================================
    # DATE PARSER
    # (general-purpose utility for free-text date resolution; not
    #  currently wired into get_km_report, which always returns the
    #  standard today/yesterday/week/month/total buckets)
    # ==========================================

    def resolve_date(self, message):

        now = datetime.now(timezone.utc)

        if not message:
            return now

        msg = message.lower()

        if "today" in msg:
            return now

        if "yesterday" in msg:
            return now - timedelta(days=1)

        if "week ago" in msg or "one week" in msg:
            return now - timedelta(days=7)

        if "month ago" in msg or "one month" in msg:
            return now - timedelta(days=30)

        match = re.search(
            r"(\d{1,2})\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{4})",
            msg
        )

        if match:
            months = {
                "jan": 1, "feb": 2, "mar": 3, "apr": 4,
                "may": 5, "jun": 6, "jul": 7, "aug": 8,
                "sep": 9, "oct": 10, "nov": 11, "dec": 12
            }

            return datetime(
                int(match.group(3)),
                months[match.group(2)],
                int(match.group(1)),
                tzinfo=timezone.utc
            )

        return now

    # ==========================================
    # SHARED UNIQUE-ID FILTER (works for any collection)
    # ==========================================

    def build_uid_filter(self, device):
        return {
            "uniqueId": {
                "$in": self.normalize_unique_id(device.get("uniqueId"))
            }
        }

    # ==========================================
    # HELPERS
    # ==========================================

    def _parse_float(self, value, default=0.0):
        """
        daily_vehicle_distance_cache.totalKm is stored as a STRING
        (e.g. "2019.374"). Summing strings directly either throws
        or silently concatenates — always parse first.
        """
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def _sum_positive_diffs(self, records):
        """
        report_distances.distance is a CUMULATIVE ("current") odometer
        reading, confirmed. To get km travelled in a window we sum only
        the positive steps between consecutive time-sorted readings.

        Why not max-min? If the device resets its counter mid-window
        (reboot / re-registration), the counter can drop then climb
        back up. Diffing consecutive readings and ignoring negative
        steps (resets) is the only version of this that stays correct
        across a reset, and it's immune to a single stray outlier
        skewing the whole window the way max-min is.
        """
        if len(records) < 2:
            return 0.0

        distances = [self._parse_float(r.get("distance", 0)) for r in records]

        total = 0.0
        for i in range(1, len(distances)):
            diff = distances[i] - distances[i - 1]
            if diff > 0:
                total += diff
            # diff <= 0 -> reset or no movement, skip (don't subtract)

        return round(total, 2)

    def _sum_cache_km(self, records):
        """
        daily_vehicle_distance_cache holds one precomputed totalKm
        string per vehicle per completed day. Summing these (after
        parsing to float) gives km for any range of completed days
        without re-deriving anything from raw odometer events.
        """
        return round(sum(self._parse_float(r.get("totalKm", 0)) for r in records), 2)

    # ==========================================
    # MAIN REPORT
    # ==========================================

    def get_km_report(self, unique_id, message, role, user):

        device = self.get_allowed_device(unique_id, role, user)

        if not device:
            return None

        uid_filter = self.build_uid_filter(device)

        distance_access = get_rbac_filter(role, user, "report_distances", self.db)
        cache_access = get_rbac_filter(role, user, "daily_vehicle_distance_caches", self.db)

        result = {}
        now = datetime.now(timezone.utc)

        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - timedelta(days=1)
        week_start = today_start - timedelta(days=7)
        month_start = today_start - timedelta(days=30)

        # ==================================================
        # TODAY: no cache entry exists yet for an in-progress day,
        # so this is computed LIVE from raw report_distances readings.
        # ==================================================
        today_records = list(self.db["report_distances"].find({
            "$and": [
                distance_access,
                uid_filter,
                {"createdAt": {"$gte": today_start, "$lte": now}}
            ]
        }).sort("createdAt", 1))

        today_km = self._sum_positive_diffs(today_records)
        result["today_km"] = today_km

        # ==================================================
        # YESTERDAY: fully completed day -> cache only.
        # ==================================================
        yesterday_cache = list(self.db["daily_vehicle_distance_caches"].find({
            "$and": [
                cache_access,
                uid_filter,
                {"createdAt": {"$gte": yesterday_start, "$lt": today_start}}
            ]
        }))

        result["yesterday_km"] = self._sum_cache_km(yesterday_cache)

        # ==================================================
        # ONE WEEK / ONE MONTH: cache covers the completed days in
        # the window, today's partial day is added live so the
        # window is "up to right now", not "up to yesterday".
        # ==================================================
        week_cache = list(self.db["daily_vehicle_distance_caches"].find({
            "$and": [
                cache_access,
                uid_filter,
                {"createdAt": {"$gte": week_start, "$lt": today_start}}
            ]
        }))

        result["one_week_km"] = round(self._sum_cache_km(week_cache) + today_km, 2)

        month_cache = list(self.db["daily_vehicle_distance_caches"].find({
            "$and": [
                cache_access,
                uid_filter,
                {"createdAt": {"$gte": month_start, "$lt": today_start}}
            ]
        }))

        result["one_month_km"] = round(self._sum_cache_km(month_cache) + today_km, 2)

        # ==================================================
        # TOTAL: every completed day in the cache, plus today live.
        # ==================================================
        all_cache = list(self.db["daily_vehicle_distance_caches"].find({
            "$and": [cache_access, uid_filter]
        }))

        result["total_km_report"] = {
            "vehicle": str(unique_id),
            "totalKm": round(self._sum_cache_km(all_cache) + today_km, 2)
        }

        # ==================================================
        # LAST POSITION
        # ==================================================
        position_filter = get_rbac_filter(role, user, "vehiclelastpositions", self.db)

        last = self.db["vehiclelastpositions"].find_one({
            "$and": [
                position_filter,
                {"uniqueId": {"$in": self.normalize_unique_id(unique_id)}}
            ]
        })

        if last:
            result["last_position"] = {
                "lat": last.get("latitude"),
                "lng": last.get("longitude"),
                "speed": last.get("speed")
            }

        return result

    # ==========================================
    # GROUP REPORT
    # ==========================================

    def get_group_km_report(self, group_type, group_id, message, role, user):

        device_filter = get_rbac_filter(role, user, "devices", self.db)

        vehicles = list(self.db["devices"].find({
            "$and": [
                device_filter,
                {f"{group_type}Id": ObjectId(str(group_id))}
            ]
        }))

        result = []

        for device in vehicles:

            unique_id = device.get("uniqueId")

            if not unique_id:
                continue

            report = self.get_km_report(unique_id, message or "", role, user)

            if report:
                result.append(report)

        return result

    # ==========================================
    # BRANCH REPORT
    # ==========================================

    def get_branch_vehicle_km_report(
    self,
    role,
    user,
    limit=2
):

    # ==========================================
    # Logged-in Branch
    # ==========================================

        branch_id = user.get("branchId")
        # branch_id = "6878ced3cf6cab94db74b243" 

        if not branch_id:
            return {
            "success": False,
            "message": "Branch not found."
        }

    # ==========================================
    # Find Branch
    # ==========================================

        branch = None

        if ObjectId.is_valid(str(branch_id)):
            branch = self.db["branches"].find_one({
            "_id": ObjectId(str(branch_id))
        })

        if not branch:
            branch = self.db["branches"].find_one({
            "_id": branch_id
        })

        if not branch:
            return {
            "success": False,
            "message": "Invalid branch."
        }

    # ==========================================
    # Device RBAC
    # ==========================================

        device_filter = get_rbac_filter(
        role,
        user,
        "devices",
        self.db
    )

    # ==========================================
    # Find Vehicles
    # ==========================================

        branch_filters = [
        {
            "branchId": branch["_id"]
        },
        {
            "branchId": str(branch["_id"])
        }
    ]

        devices = list(

        self.db["devices"].find({

            "$and": [

                device_filter,

                {
                    "$or": branch_filters
                }

            ]

        })

    )

        if not devices:
            return {
            "success": False,
            "message": "No vehicles found for this branch."
        }

    # ==========================================
    # KM Report
    # ==========================================

        reports = []

        for device in devices:

            unique_id = device.get("uniqueId")

            if not unique_id:
                continue

            try:

                km_report = self.get_km_report(
                unique_id,
                "",
                role,
                user
            )

            except Exception:

                km_report = None

            reports.append({

            "deviceId": str(device.get("_id")),

            "vehicleName":
                device.get("vehicleNumber")
                or device.get("vehicle_name")
                or device.get("name")
                or str(unique_id),

            "uniqueId": unique_id,

            "todayKm":
                km_report.get("today_km", 0)
                if km_report else 0,

            "yesterdayKm":
                km_report.get("yesterday_km", 0)
                if km_report else 0,

            "oneWeekKm":
                km_report.get("one_week_km", 0)
                if km_report else 0,

            "oneMonthKm":
                km_report.get("one_month_km", 0)
                if km_report else 0,

            "totalKm":
                km_report.get(
                    "total_km_report",
                    {}
                ).get(
                    "totalKm",
                    0
                ) if km_report else 0

        })

        return {

        "success": True,

        "branchId": str(branch["_id"]),

        "branchName": branch.get(
            "branchName",
            ""
        ),

        "totalVehicles": len(reports),

        "vehicles": reports

    }