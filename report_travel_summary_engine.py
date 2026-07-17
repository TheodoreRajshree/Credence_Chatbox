from bson import ObjectId
from rbac import get_rbac_filter
class ReportTravelSummaryEngine:

    def __init__(self, db):
        self.db = db


    # =====================================
    # CLEAN
    # =====================================
   


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
    # VEHICLE TRAVEL SUMMARY
    # =====================================

    def get_vehicle_travel_summary(
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


        summary_filter = get_rbac_filter(

            role,
            user,
            "report_travelsummaries",
            self.db

        )


        reports = list(

            self.db["report_travelsummaries"].find({

                "$and":[

                    summary_filter,

                    {
                        "uniqueId":
                        str(unique_id)
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
    # SCHOOL TRAVEL SUMMARY
    # =====================================

    def get_school_travel_summary(
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


        summary_filter = get_rbac_filter(

            role,
            user,
            "report_travelsummaries",
            self.db

        )


        reports = list(

            self.db["report_travelsummaries"].find({

                "$and":[

                    summary_filter,

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
    # BRANCH TRAVEL SUMMARY
    # =====================================

    def get_branch_travel_summary(
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


        summary_filter = get_rbac_filter(

            role,
            user,
            "report_travelsummaries",
            self.db

        )


        reports = list(

            self.db["report_travelsummaries"].find({

                "$and":[

                    summary_filter,

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
    # DRIVER TRAVEL SUMMARY
    # =====================================

    def get_driver_travel_summary(
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


        return self.get_vehicle_travel_summary(

            device.get("uniqueId"),

            role,

            user,

            limit

        )



    # =====================================
    # ALL TRAVEL SUMMARIES
    # =====================================

   
    
    

    def get_all_travel_summaries(self, role, user):

        summary_filter = get_rbac_filter(
        role,
        user,
        "report_travelsummaries",
        self.db
    )

        pipeline = [
        {
            "$match": summary_filter
        },
        {
            "$sort": {
                "startTime": -1
            }
        },
        {
            "$group": {
                "_id": "$uniqueId",
                "vehicleName": {
                    "$first": {
                        "$ifNull": [
                            "$vehicleName",
                            "$name"
                        ]
                    }
                },
                "travelHistory": {
                    "$push": "$$ROOT"
                }
            }
        }
    ]

        vehicles = []

        for doc in self.db["report_travelsummaries"].aggregate(
        pipeline,
        allowDiskUse=True
    ):
            vehicles.append({
            "vehicleName": doc.get("vehicleName"),
            "uniqueId": str(doc["_id"]),
            "travelHistory": [self.clean(x) for x in doc["travelHistory"]]
        })

        return {
        "success": True,
        "vehicleCount": len(vehicles),
        "vehicles": vehicles
    }
    # =====================================
    # REPORT COUNT
    # =====================================

    def get_summary_count(
        self,
        unique_id,
        role,
        user
    ):


        reports = self.get_vehicle_travel_summary(

            unique_id,

            role,

            user,

            limit=999999

        )


        return len(reports)