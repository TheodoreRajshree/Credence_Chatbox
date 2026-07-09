from bson import ObjectId
class RelationshipEngine:
    def __init__(self, db):
        self.db = db
    # =====================================================
    # SAFE FIND BY OBJECT ID
    # =====================================================
    def _find_by_id(self, collection_name, obj_id):
        try:

            if not obj_id:
                return None

            return self.db[collection_name].find_one({
                "_id": ObjectId(str(obj_id))
            })
        except Exception:
            return None
    # =====================================================
    # SCHOOL
    # =====================================================
    def get_school(self, school_id):

        school = self._find_by_id(
            "schools",
            school_id
        )
        if not school:
            return None

        return {
            "schoolId": str(school["_id"]),
            "schoolName": school.get("schoolName")
        }
    # =====================================================
    # BRANCH
    # =====================================================

    def get_branch(self, branch_id):

        branch = self._find_by_id(
            "branches",
            branch_id
        )

        if not branch:
            return None

        return {
            "branchId": str(branch["_id"]),
            "branchName": branch.get("branchName"),
            "schoolId": str(branch.get("schoolId"))
            if branch.get("schoolId")
            else None
        }
    # =====================================================
    # DEVICE
    # =====================================================
    def get_device(self, device_id):

        device = self._find_by_id(
            "devices",
            device_id
        )

        if not device:
            return None

        return {
            "deviceId": str(device["_id"]),
            "vehicleName": device.get("name"),
            "uniqueId": device.get("uniqueId"),
            "sim": device.get("sim"),
            "status": device.get("status"),
            "model": device.get("model"),
            "category": device.get("category")
        }
    # =====================================================
    # ROUTE
    # =====================================================
    def get_route(self, route_id):

        route = self._find_by_id(
            "routes",
            route_id
        )

        if not route:
            return None

        return {
            "routeId": str(route["_id"]),
            "routeNumber": route.get("routeNumber"),
            "schoolId": str(route.get("schoolId"))
            if route.get("schoolId")
            else None,
            "branchId": str(route.get("branchId"))
            if route.get("branchId")
            else None
        }
    # =====================================================
    # DRIVER PROFILE
    # =====================================================
    def get_driver_profile(self, username):

        try:

            driver = self.db["drivers"].find_one({
                "username": username
            })

            if not driver:
                return {}

            profile = {
                "role": "driver",
                "driverName": driver.get("driverName"),
                "username": driver.get("username"),
                "mobileNo": driver.get("mobileNo"),
                "isApproved": driver.get("isApproved"),
                "active": driver.get("Active")
            }

            school = self.get_school(
                driver.get("schoolId")
            )

            if school:
                profile["school"] = school

            branch = self.get_branch(
                driver.get("branchId")
            )

            if branch:
                profile["branch"] = branch

            device = self.get_device(
                driver.get("deviceObjId")
            )

            if device:
                profile["device"] = device

            route = self.get_route(
                driver.get("routeObjId")
            )

            if route:
                profile["route"] = route

            return profile

        except Exception as e:

            print("Driver Profile Error:", e)

            return {}
    # =====================================================
    # BRANCH PROFILE
    # =====================================================
    def get_branch_profile(self, username):

        try:

            branch = self.db["branches"].find_one({
                "username": username
            })

            if not branch:
                return {}

            profile = {
                "role": "branch",
                "branchName": branch.get("branchName"),
                "username": branch.get("username"),
                "mobileNo": branch.get("mobileNo")
            }

            school = self.get_school(
                branch.get("schoolId")
            )

            if school:
                profile["school"] = school

            return profile

        except Exception:

            return {}
    # =====================================================
    # SCHOOL PROFILE
    # =====================================================
    def get_school_profile(self, username):

        try:

            school = self.db["schools"].find_one({
                "username": username
            })

            if not school:
                return {}

            return {
                "role": "school",
                "schoolName": school.get("schoolName"),
                "username": school.get("username"),
                "mobileNo": school.get("mobileNo"),
                "email": school.get("email")
            }

        except Exception:
            return {}
    # =====================================================
    # MAIN ENTRY POINT
    # =====================================================
    def get_user_profile(self, role, user):

        username = user.get("username")

        role = role.lower()

        if role == "driver":
            return self.get_driver_profile(username)

        if role == "branch":
            return self.get_branch_profile(username)

        if role == "school":
            return self.get_school_profile(username)

        return {
            "role": role,
            "username": username
        }
    

    