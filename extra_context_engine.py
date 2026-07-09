from bson import ObjectId


class ExtraContextEngine:

    def __init__(self, db):
        self.db = db

    def latest(self, collection, query=None):

        if query is None:
            query = {}

        try:
            return self.db[collection].find_one(
                query,
                sort=[("createdAt", -1)]
            )
        except:
            return None

    # ==========================================
    # ATTENDANCE
    # ==========================================

    def get_attendance(self, driver_id):

        try:

            count = self.db["attendances"].count_documents({
                "driverId": driver_id
            })

            return {
                "attendanceRecords": count
            }

        except:
            return {}

    # ==========================================
    # EVENTS
    # ==========================================

    def get_latest_event(self, unique_id):

        try:

            event = self.latest(
                "allevents",
                {"uniqueId": str(unique_id)}
            )

            if not event:
                return {}

            return {
                "eventType": event.get("eventType"),
                "eventTime": str(event.get("eventTime")),
                "latitude": event.get("latitude"),
                "longitude": event.get("longitude")
            }

        except:
            return {}

    # ==========================================
    # LAST POSITION
    # ==========================================

    def get_last_position(self, unique_id):

        try:

            pos = self.latest(
                "vehiclelastpositions",
                {"uniqueId": str(unique_id)}
            )

            if not pos:
                return {}

            return {
                "latitude": pos.get("latitude"),
                "longitude": pos.get("longitude"),
                "speed": pos.get("speed"),
                "lastUpdate": str(pos.get("lastUpdate"))
            }

        except:
            return {}

    # ==========================================
    # DISTANCE
    # ==========================================

    def get_distance(self, unique_id):

        try:

            report = self.latest(
                "report_distances",
                {"uniqueId": str(unique_id)}
            )

            if not report:
                return {}

            return {
                "distance": report.get("distance"),
                "vehicle": report.get("name")
            }

        except:
            return {}

    # ==========================================
    # TRIP
    # ==========================================

    def get_trip(self, unique_id):

        try:

            report = self.latest(
                "report_trips",
                {"uniqueId": str(unique_id)}
            )

            if not report:
                return {}

            return {
                "distance": report.get("distance"),
                "duration": report.get("duration"),
                "maxSpeed": report.get("maxSpeed"),
                "avgSpeed": report.get("avgSpeed")
            }

        except:
            return {}

    # ==========================================
    # IDLE
    # ==========================================

    def get_idle(self, unique_id):

        try:

            report = self.latest(
                "report_idles",
                {"uniqueId": str(unique_id)}
            )

            if not report:
                return {}

            return {
                "duration": report.get("duration"),
                "idleStart": str(report.get("idleStartTime")),
                "idleEnd": str(report.get("idleEndTime"))
            }

        except:
            return {}

    # ==========================================
    # STOPPAGE
    # ==========================================

    def get_stoppage(self, unique_id):

        try:

            report = self.latest(
                "report_stopages",
                {"uniqueId": str(unique_id)}
            )

            if not report:
                return {}

            return {
                "arrivalTime": str(report.get("arrivalTime")),
                "departureTime": str(report.get("departureTime"))
            }

        except:
            return {}

    # ==========================================
    # TRAVEL SUMMARY
    # ==========================================

    def get_travel_summary(self, unique_id):

        try:

            report = self.latest(
                "report_travelsummaries",
                {"uniqueId": str(unique_id)}
            )

            if not report:
                return {}

            return {
                "distance": report.get("distance"),
                "workingHours": report.get("workingHours"),
                "runningTime": report.get("runningTime"),
                "stopTime": report.get("stopTime"),
                "idleTime": report.get("idleTime")
            }

        except:
            return {}

    # ==========================================
    # GEOFENCE
    # ==========================================

    def get_geofence_events(self, unique_id):

        try:

            count = self.db["geofencereports"].count_documents({
                "uniqueId": str(unique_id)
            })

            return {
                "geofenceEvents": count
            }

        except:
            return {}

    # ==========================================
    # TICKETS
    # ==========================================

    def get_ticket_count(self, school_id):

        try:

            count = self.db["tickets"].count_documents({
                "schoolId": school_id
            })

            return {
                "ticketsRaised": count
            }

        except:
            return {}

    # ==========================================
    # MASTER CONTEXT
    # ==========================================

    def build_extra_context(
        self,
        driver,
        device
    ):

        if not driver:
            return {}

        if not device:
            return {}

        unique_id = str(
            device.get("uniqueId")
        )

        return {

            "latestEvent":
                self.get_latest_event(unique_id),

            "lastPosition":
                self.get_last_position(unique_id),

            "distance":
                self.get_distance(unique_id),

            "trip":
                self.get_trip(unique_id),

            "idle":
                self.get_idle(unique_id),

            "stoppage":
                self.get_stoppage(unique_id),

            "travelSummary":
                self.get_travel_summary(unique_id),

            "geofence":
                self.get_geofence_events(unique_id),

            "attendance":
                self.get_attendance(
                    str(driver.get("_id"))
                ),

            "tickets":
                self.get_ticket_count(
                    driver.get("schoolId")
                )
        }