from bson import ObjectId
import re
from rbac import get_rbac_filter
def find_school(self, school_name, role, user):

    school_name = str(school_name or "").strip()

    # -----------------------------
    # SUPERADMIN: NO RBAC FILTER
    # -----------------------------
    if role.lower() == "superadmin":
        base_filter = {}
    else:
        base_filter = get_rbac_filter(
            role,
            user,
            "schools",
            self.db
        ) or {}

    school = None

    # -----------------------------
    # 1. TRY OBJECTID MATCH
    # -----------------------------
    if ObjectId.is_valid(school_name):
        try:
            school = self.db["schools"].find_one({
                "$and": [
                    base_filter,
                    {"_id": ObjectId(school_name)}
                ]
            })
        except:
            pass

    # -----------------------------
    # 2. TRY NAME / USERNAME MATCH
    # -----------------------------
    if not school and school_name:

        regex = re.compile(re.escape(school_name), re.IGNORECASE)

        school = self.db["schools"].find_one({
            "$and": [
                base_filter,
                {
                    "$or": [
                        {"schoolName": regex},
                        {"username": regex}
                    ]
                }
            ]
        })

    return school
def get_all_branch_groups_profile_1(
    self,
    role,
    user
):

    # ====================================
    # STEP 1: SUPERADMIN ACCESS CHECK
    # ====================================

        if role != "superadmin":
            return {
            "success": False,
            "message": "Access denied"
        }


    # ====================================
    # STEP 2: FETCH ALL BRANCH GROUPS
    # ====================================

        groups = list(
        self.db["branchgroups"].find({})
    )


        if not groups:
            return {
            "success": False,
            "message": "No branch groups found"
        }


    # ====================================
    # STEP 3: FORMAT RESPONSE
    # ====================================

        profiles = []


        for group in groups:

            profiles.append({

            "groupId":
                str(group["_id"]),


            "branchGroupName":
                group.get("branchGroupName"),


            "schoolId":
                str(group.get("schoolId"))
                if group.get("schoolId")
                else None,


            "mobileNo":
                group.get("mobileNo"),


            "username":
                group.get("username"),


            "email":
                group.get("email"),


            "role":
                group.get("role"),


            "active":
                group.get("Active"),


            "access":
                group.get("access"),


            "notification":
                group.get("Notification"),


            "fcmToken":
                group.get("fcmToken"),


            "createdAt":
                group.get("createdAt")

        })


    # ====================================
    # STEP 4: RESPONSE
    # ====================================

        return {

        "success": True,

        "count": len(profiles),

        "profiles": profiles

    }