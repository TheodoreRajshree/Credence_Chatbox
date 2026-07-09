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