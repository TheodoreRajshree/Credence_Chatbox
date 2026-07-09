from bson import ObjectId
from rbac import get_rbac_filter

from unique_id import normalize_unique_id
class DeviceEngine:

    def __init__(self, db):
        self.db = db

    # ==========================================
    # FIND DEVICE BY NAME
    # ==========================================
     
    def find_device(self, text, role, user):

        text = text.lower()

        rbac_filter = get_rbac_filter(
            role,
            user,
            "devices",
            self.db
        )

        for device in self.db["devices"].find(rbac_filter):
            name = device.get("name", "").lower()

            if name and name in text:
                return device

        return None

    # ==========================================
    # DEVICE DETAILS
    # ==========================================

    def get_device_details(self, device):

        if not device:
            return None

        return {
            "deviceId": str(device["_id"]),
            "vehicleName": device.get("name"),
            "uniqueId": device.get("uniqueId"),
            "sim": device.get("sim"),
            "model": device.get("model"),
            "category": device.get("category"),
            "status": device.get("status"),
            "speed": device.get("speed"),
            "average": device.get("average"),
            "totalKm": device.get("TotalKmOfDevice"),
            "installationDate": device.get("installationdate"),
            "expirationDate": device.get("expirationdate"),
            "schoolId": str(device.get("schoolId"))
            if device.get("schoolId") else None,
            "branchId": str(device.get("branchId"))
            if device.get("branchId") else None
        }
    def get_superadmin_vehicle_details(self, role, user, vehicle_input=None):

        if isinstance(vehicle_input, dict):
            vehicle_input = vehicle_input.get("vehicle_input")

        if not vehicle_input:
            return None

        vehicle_input = vehicle_input.strip().lower()
        devices=self.db.devices.find({})

        matched = []

        for device in devices:

                name = (device.get("name") or "").strip().lower()
                unique_id = str(device.get("uniqueId") or "").strip().lower()

        # match by vehicle name OR uniqueId
                if vehicle_input in name or vehicle_input == unique_id:

                    matched.append({
                "deviceId": str(device["_id"]),
                "vehicleName": device.get("name"),
                "uniqueId": device.get("uniqueId"),
                "sim": device.get("sim"),
                "model": device.get("model"),
                "category": device.get("category"),
                "status": device.get("status"),
                "speed": device.get("speed"),
                "average": device.get("average"),
                "totalKm": device.get("TotalKmOfDevice"),
                "installationDate": device.get("installationdate"),
                "expirationDate": device.get("expirationdate"),
                "schoolId": str(device.get("schoolId")) if device.get("schoolId") else None,
                "branchId": str(device.get("branchId")) if device.get("branchId") else None
            })

        return matched  if matched else None
    # ==========================================
    # ALL DEVICES
    # ==========================================

    def get_all_devices(self, role, user):

        devices = []

        rbac_filter = get_rbac_filter(
            role,
            user,
            "devices",
            self.db
        )

        for d in self.db["devices"].find(rbac_filter):
            devices.append(self.get_device_details(d))

        return devices

    # ==========================================
    # SCHOOL DEVICES
    # ==========================================

    def get_school_devices(self, school_id):

        devices = []

        rbac_filter = get_rbac_filter(
            "school",
            {"_id": ObjectId(str(school_id))},
            "devices",
            self.db
        )

        query = {
            "$and": [
                rbac_filter,
                {"schoolId": ObjectId(str(school_id))}
            ]
        }

        for d in self.db["devices"].find(query):
            devices.append(self.get_device_details(d))

        return devices

    # ==========================================
    # BRANCH DEVICES
    # ==========================================

    def get_branch_devices(self, branch_id):

        devices = []

        rbac_filter = get_rbac_filter(
            "branch",
            {"_id": ObjectId(str(branch_id))},
            "devices",
            self.db
        )

        query = {
            "$and": [
                rbac_filter,
                {"branchId": ObjectId(str(branch_id))}
            ]
        }

        for d in self.db["devices"].find(query):
            devices.append(self.get_device_details(d))

        return devices

    # ==========================================
    # DRIVER DEVICE
    # ==========================================

    def get_driver_device(self, username):

        driver = self.db["drivers"].find_one({
            "username": username
        })

        if not driver:
            return {}

        rbac_filter = get_rbac_filter(
            "driver",
            driver,
            "devices",
            self.db
        )

        device = self.db["devices"].find_one({
            "$and": [
                rbac_filter,
                {
                    "_id": driver.get("deviceObjId")
                }
            ]
        })

        return self.get_device_details(device)

    # ==========================================
    # LAST POSITION
    # ==========================================

    def get_last_position(self, unique_id, role, user):

        rbac_filter = get_rbac_filter(
            role,
            user,
            "vehiclelastpositions",
            self.db
        )

        query = {
            "$and": [
                rbac_filter,
                {
                    "$or": [
                        {"uniqueId": unique_id},
                        {"uniqueId": str(unique_id)}
                    ]
                }
            ]
        }

        position = self.db["vehiclelastpositions"].find_one(query)

        if not position:
            return {}

        return {
            "latitude": position.get("latitude"),
            "longitude": position.get("longitude"),
            "speed": position.get("speed"),
            "lastUpdate": position.get("lastUpdate"),
            "course": position.get("course")
        }

    # ==========================================
    # DEVICE SUMMARY
    # ==========================================
    def get_branch_single_vehicle(
    self,
    branch_name,
    vehicle_input,
    role,
    user
):
    # Find branch
        branch = self.find_branch(
        branch_name,
        role,
        user
    )

        if not branch:
            return {
            "success": False,
            "message": f"Branch '{branch_name}' not found"
        }

        branch_id = branch["_id"]

    # RBAC filter
        device_filter = get_rbac_filter(
        role,
        user,
        "devices",
        self.db
    )

    # Search vehicle within this branch
        device = self.db["devices"].find_one({
        "$and": [
            device_filter,
            {
                "$or": [
                    {"branchId": branch_id},
                    {"branchId": str(branch_id)}
                ]
            },
            {
                "$or": [
                    {
                        "vehicleNumber": {
                            "$regex": vehicle_input,
                            "$options": "i"
                        }
                    },
                    {
                        "vehicle_name": {
                            "$regex": vehicle_input,
                            "$options": "i"
                        }
                    },
                    {
                        "name": {
                            "$regex": vehicle_input,
                            "$options": "i"
                        }
                    },
                    {
                        "uniqueId": {
                            "$in": [vehicle_input, str(vehicle_input)]
                        }
                    }
                ]
            }
        ]
    })

        if not device:
            return {
            "success": False,
            "message": "Vehicle not found."
        }

        vehicle = {
        "vehicleName": (
            device.get("vehicleNumber")
            or device.get("vehicle_name")
            or device.get("name")
            or device.get("uniqueId")
        ),
        "deviceId": str(device.get("_id")),
        "uniqueId": device.get("uniqueId"),
        "status": device.get("status"),
        "model": device.get("model"),
        "category": device.get("category"),
        "speed": device.get("speed"),
        "totalKm": device.get("TotalKmOfDevice", 0)
    }

        return {
        "success": True,
        "vehicle": vehicle
    }
    def get_device_summary(self, unique_id, role, user):

        distance_filter = get_rbac_filter(
            role,
            user,
            "report_distances",
            self.db
        )

        travel_filter = get_rbac_filter(
            role,
            user,
            "report_travelsummaries",
            self.db
        )

        trip_filter = get_rbac_filter(
            role,
            user,
            "report_trips",
            self.db
        )

        idle_filter = get_rbac_filter(
            role,
            user,
            "report_idles",
            self.db
        )

        distance = self.db["report_distances"].find_one({
            "$and": [
                distance_filter,
                {
 "uniqueId":{
    "$in": normalize_unique_id(unique_id)
 }
}
            ]
        })

        travel = self.db["report_travelsummaries"].find_one({
            "$and": [
                travel_filter,
                {"uniqueId": int(unique_id)}
            ]
        })

        trip = self.db["report_trips"].find_one({
            "$and": [
                trip_filter,
                {"uniqueId": int(unique_id)}
            ]
        })

        idle = self.db["report_idles"].find_one({
            "$and": [
                idle_filter,
                {"uniqueId": int(unique_id)}
            ]
        })

        return {
            "distance": distance,
            "travelSummary": travel,
            "trip": trip,
            "idle": idle
        }