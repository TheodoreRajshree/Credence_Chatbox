from bson import ObjectId


class UnifiedFleetEngine:

    def __init__(self, db):
        self.db = db

    # =========================
    # SAFE OBJECTID
    # =========================
    def _id(self, value):
        try:
            return ObjectId(value)
        except:
            return value

    # =========================
    # RBAC CORE FILTER
    # =========================
    def rbac_filter(self, role, user, collection):

        role = role.lower()

        if role in ["superadmin", "superadmins"]:
            return {}

        school_id = self._id(user.get("schoolId"))
        branch_id = self._id(user.get("branchId"))
        device_id = self._id(user.get("deviceObjId"))
        user_id = self._id(user.get("_id"))

        # -------------------------
        # SCHOOL LEVEL ACCESS
        # -------------------------
        if role in ["school", "schools"]:
            return {
                "$or": [
                    {"schoolId": school_id},
                    {"schoolObjId": school_id}
                ]
            }

        # -------------------------
        # BRANCH LEVEL ACCESS
        # -------------------------
        if role in ["branch", "branches"]:
            return {
                "$or": [
                    {"branchId": branch_id},
                    {"branchObjId": branch_id}
                ]
            }

        # -------------------------
        # DRIVER LEVEL ACCESS
        # -------------------------
        if role == "driver":
            return {
                "$or": [
                    {"deviceObjId": device_id},
                    {"uniqueId": user.get("uniqueId")},
                    {"branchId": branch_id},
                    {"schoolId": school_id}
                ]
            }

        return {"_id": None}

    # =========================
    # GENERIC FETCH
    # =========================
    def fetch(self, collection, role, user, limit=50):

        if collection not in self.db.list_collection_names():
            return []

        query = self.rbac_filter(role, user, collection)

        data = list(
            self.db[collection]
            .find(query)
            .limit(limit)
        )

        return [self.clean(doc) for doc in data]

    # =========================
    # CLEAN DATA
    # =========================
    def clean(self, doc):
        doc["_id"] = str(doc["_id"])
        return doc

    # =========================
    # SCHOOL FULL GRAPH
    # =========================
    def school_graph(self, school_id, role, user):

        school_id = self._id(school_id)

        if role != "superadmin":
            school_id = self._id(user.get("schoolId"))

        return {
            "school": self.db["schools"].find_one({"_id": school_id}),

            "branches": self.fetch("branches", role, user),
            "devices": self.fetch("devices", role, user),
            "drivers": self.fetch("drivers", role, user),
            "routes": self.fetch("routes", role, user),
            "geofences": self.fetch("geofences", role, user),
            "tickets": self.fetch("tickets", role, user),
        }

    # =========================
    # BRANCH FULL GRAPH
    # =========================
    def branch_graph(self, branch_id, role, user):

        branch_id = self._id(branch_id)

        branch = self.db["branches"].find_one({"_id": branch_id})

        if not branch:
            return None

        return {
            "branch": branch,

            "devices": list(self.db["devices"].find({"branchId": branch_id})),
            "drivers": list(self.db["drivers"].find({"branchId": branch_id})),
            "routes": list(self.db["routes"].find({"branchId": branch_id})),
            "geofences": list(self.db["geofences"].find({"branchId": branch_id})),
            "tickets": list(self.db["tickets"].find({"branchId": branch_id})),
        }

    # =========================
    # DEVICE FULL GRAPH (MOST IMPORTANT)
    # =========================
    def device_graph(self, unique_id, role, user):

        device = self.db["devices"].find_one({"uniqueId": unique_id})

        if not device:
            return None

        # RBAC HARD CHECK
        if role != "superadmin":

            if str(device.get("schoolId")) != str(user.get("schoolId")) and \
               str(device.get("branchId")) != str(user.get("branchId")):
                return None

        device_id = device["_id"]

        return {
            "device": device,

            "last_position": self.db["vehiclelastpositions"].find_one({"uniqueId": unique_id}),

            "histories": list(self.db["histories"].find({"uniqueId": unique_id}).limit(20)),

            "trips": list(self.db["report_trips"].find({"uniqueId": unique_id}).limit(20)),

            "distance_reports": list(self.db["report_distances"].find({"uniqueId": unique_id}).limit(20)),

            "idle_reports": list(self.db["report_idles"].find({"uniqueId": unique_id}).limit(20)),

            "status_reports": list(self.db["report_statuses"].find({"uniqueId": unique_id}).limit(20)),

            "travel_summary": list(self.db["report_travelsummaries"].find({"uniqueId": unique_id}).limit(20)),

            "subscriptions": list(self.db["Devicesubsceeiptions"].find({"deviceId": device_id})),

            "subscription_history": list(
                self.db["Devicesubscriptionhistories"].find({"deviceObjId": device_id})
            ),

            "geofence_reports": list(
                self.db["geofencesreports"].find({"uniqueId": unique_id})
            ),

            "vehicle_last_position": self.db["Vehiclelastpositions"].find_one({"uniqueId": unique_id})
        }

    # =========================
    # CHAT GRAPH
    # =========================
    def chat_graph(self, user_id):

        chats = list(self.db["Chats"].find({
            "participants": self._id(user_id)
        }))

        chat_ids = [c["_id"] for c in chats]

        messages = list(self.db["Messages"].find({
            "chatId": {"$in": chat_ids}
        }))

        return {
            "chats": chats,
            "messages": messages
        }

    # =========================
    # USER SESSION GRAPH
    # =========================
    def session_graph(self, user_id):

        return list(self.db["Usersessionlogs"].find({
            "userId": self._id(user_id)
        }))