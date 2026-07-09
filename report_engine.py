# report_engine.py

from bson import ObjectId
from rbac import get_rbac_filter


class ReportEngine:

    def __init__(self, db):
        self.db = db


    # ==================================================
    # RBAC FIND
    # ==================================================

    def latest(
        self,
        collection,
        query,
        role,
        user
    ):

        try:

            rbac_filter = get_rbac_filter(
                role,
                user,
                collection,
                self.db
            )


            return self.db[collection].find_one(

                {
                    "$and":[

                        rbac_filter,

                        query

                    ]
                },

                sort=[
                    ("createdAt",-1)
                ]

            )


        except Exception:

            return None



    # ==================================================
    # DEVICE
    # ==================================================

    def get_device(
        self,
        device_id,
        role,
        user
    ):

        try:

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
                return {}


            return {

                "vehicleName": device.get("name"),
                "uniqueId": device.get("uniqueId"),
                "model": device.get("model"),
                "category": device.get("category"),
                "status": device.get("status"),
                "sim": device.get("sim"),
                "speedLimit": device.get("speed")

            }


        except Exception:

            return {}



    # ==================================================
    # LAST POSITION
    # ==================================================

    def get_last_position(
        self,
        unique_id,
        role,
        user
    ):

        data = self.latest(

            "vehiclelastpositions",

            {
                "uniqueId":
                str(unique_id)
            },

            role,
            user

        )


        if not data:
            return {}


        return {

            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "speed": data.get("speed"),
            "lastUpdate": str(data.get("lastUpdate")),
            "vehicle": data.get("name")

        }



    # ==================================================
    # DISTANCE REPORT
    # ==================================================

    def get_distance_report(
        self,
        unique_id,
        role,
        user
    ):


        report = self.latest(

            "report_distances",

            {
                "uniqueId":
                str(unique_id)
            },

            role,
            user

        )


        if not report:
            return {}


        return {

            "distance": report.get("distance"),
            "vehicle": report.get("name")

        }



    # ==================================================
    # TRIP REPORT
    # ==================================================

    def get_trip_report(
        self,
        unique_id,
        role,
        user
    ):


        report=self.latest(

            "report_trips",

            {
                "uniqueId":
                str(unique_id)
            },

            role,
            user

        )


        if not report:
            return {}


        return {

            "distance": report.get("distance"),
            "duration": report.get("duration"),
            "maxSpeed": report.get("maxSpeed"),
            "avgSpeed": report.get("avgSpeed"),
            "startTime": str(report.get("startTime")),
            "endTime": str(report.get("endTime"))

        }



    # ==================================================
    # IDLE REPORT
    # ==================================================

    def get_idle_report(
        self,
        unique_id,
        role,
        user
    ):

        report=self.latest(

            "report_idles",

            {
                "uniqueId":
                str(unique_id)
            },

            role,
            user

        )


        if not report:
            return {}


        return {

            "duration": report.get("duration"),
            "idleStart": str(report.get("idleStartTime")),
            "idleEnd": str(report.get("idleEndTime"))

        }



    # ==================================================
    # STOPPAGE REPORT
    # ==================================================

    def get_stoppage_report(
        self,
        unique_id,
        role,
        user
    ):


        report=self.latest(

            "report_stopages",

            {
                "uniqueId":
                str(unique_id)
            },

            role,
            user

        )


        if not report:
            return {}


        return {

            "arrivalTime": str(report.get("arrivalTime")),
            "departureTime": str(report.get("departureTime")),
            "latitude": report.get("latitude"),
            "longitude": report.get("longitude")

        }



    # ==================================================
    # TRAVEL SUMMARY
    # ==================================================

    def get_travel_summary(
        self,
        unique_id,
        role,
        user
    ):


        report=self.latest(

            "report_travelsummaries",

            {
                "uniqueId":
                str(unique_id)
            },

            role,
            user

        )


        if not report:
            return {}


        return {

            "distance": report.get("distance"),
            "workingHours": report.get("workingHours"),
            "runningTime": report.get("runningTime"),
            "stopTime": report.get("stopTime"),
            "idleTime": report.get("idleTime"),
            "maxSpeed": report.get("maxSpeed"),
            "avgSpeed": report.get("avgSpeed")

        }



    # ==================================================
    # SUBSCRIPTION
    # ==================================================

    def get_subscription(
        self,
        device_id,
        role,
        user
    ):

        try:

            sub=self.latest(

                "devicesubscriptions",

                {
                    "deviceId":
                    device_id
                },

                role,
                user

            )


            if not sub:
                return {}


            return {

                "status": sub.get("status"),

                "expiryDate":
                str(
                    sub.get(
                        "newExpirationDate"
                    )
                )

            }


        except Exception:

            return {}



    # ==================================================
    # DAILY DISTANCE CACHE
    # ==================================================

    def get_daily_distance(
        self,
        unique_id,
        role,
        user
    ):


        report=self.latest(

            "daily_vehicle_distance_caches",

            {
                "uniqueId":
                str(unique_id)
            },

            role,
            user

        )


        if not report:
            return {}


        return {

            "totalKm": report.get("totalKm"),
            "startOdo": report.get("startOdo")

        }



    # ==================================================
    # MASTER DRIVER REPORT
    # ==================================================

    def get_driver_report(
        self,
        driver_doc,
        role,
        user
    ):


        try:

            device_id = driver_doc.get(
                "deviceObjId"
            )


            device=self.get_device(

                device_id,

                role,

                user

            )


            if not device:
                return {}


            unique_id=device.get(
                "uniqueId"
            )


            return {

                "device": device,

                "lastPosition":
                self.get_last_position(
                    unique_id,
                    role,
                    user
                ),

                "distanceReport":
                self.get_distance_report(
                    unique_id,
                    role,
                    user
                ),

                "tripReport":
                self.get_trip_report(
                    unique_id,
                    role,
                    user
                ),

                "idleReport":
                self.get_idle_report(
                    unique_id,
                    role,
                    user
                ),

                "stoppageReport":
                self.get_stoppage_report(
                    unique_id,
                    role,
                    user
                ),

                "travelSummary":
                self.get_travel_summary(
                    unique_id,
                    role,
                    user
                ),

                "dailyDistance":
                self.get_daily_distance(
                    unique_id,
                    role,
                    user
                ),

                "subscription":
                self.get_subscription(
                    device_id,
                    role,
                    user
                )

            }


        except Exception as e:

            print(
                "Report Error:",
                e
            )

            return {}