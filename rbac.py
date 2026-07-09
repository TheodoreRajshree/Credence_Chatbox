# rbac/rbac.py

from bson import ObjectId

from relationshipMap import RELATIONSHIP_MAP
from deviceRelationshipMap import DEVICE_RELATIONSHIP_MAP
from globalCollections import GLOBAL_COLLECTIONS



# ==========================================
# ID NORMALIZER
# ==========================================

def normalize_id(value):

    if isinstance(value, ObjectId):
        return value

    try:
        return ObjectId(str(value))

    except:
        return value



# ==========================================
# GLOBAL COLLECTION CHECK
# ==========================================

def is_global_collection(collection_name):

    return collection_name in GLOBAL_COLLECTIONS



# ==========================================
# SUPER ADMIN CHECK
# ==========================================

def is_super_admin(role):

    if not role:
        return False

    role = str(role).strip().lower()

    return role in ["superadmin", "super_admin", "super-admin"]



# ==========================================
# GET DIRECT RELATIONSHIP FIELD
# ==========================================

def get_direct_field(
    role,
    collection_name
):

    role_config = RELATIONSHIP_MAP.get(role)

    if not role_config:
        return None


    return role_config.get(
        "direct",
        {}
    ).get(collection_name)



# ==========================================
# DEVICE UNIQUE ID COLLECTION
# ==========================================

def is_unique_id_collection(
    collection_name
):

    return (
        collection_name
        in DEVICE_RELATIONSHIP_MAP["uniqueIdCollections"]
    )



# ==========================================
# DEVICE ID COLLECTION
# ==========================================

def is_device_id_collection(
    collection_name
):

    return (
        collection_name
        in DEVICE_RELATIONSHIP_MAP["deviceIdCollections"]
    )



# ==========================================
# DEVICE OBJECT ID COLLECTION
# ==========================================

def is_device_objid_collection(
    collection_name
):

    return (
        collection_name
        in DEVICE_RELATIONSHIP_MAP["deviceObjIdCollections"]
    )



# ==========================================
# RBAC FILTER GENERATOR
# ==========================================

def get_rbac_filter(
    role,
    user,
    collection_name,
    db
):

    role = (role or "").strip().lower()
    rbac_filter = {}
    print("ROLE =", role)
    print("RELATIONSHIP_MAP KEYS =", RELATIONSHIP_MAP.keys())
    # ======================================
    # SUPER ADMIN
    # ======================================

    if is_super_admin(role):

        return {}



    # ======================================
    # GLOBAL COLLECTION
    # ======================================

    if is_global_collection(collection_name):

        return {}

    

    role_config = RELATIONSHIP_MAP.get(role)


    if not role_config:

        raise Exception(
            f"Unsupported role: {role}"
        )



    # ======================================
    # DIRECT RELATIONSHIPS
    # ======================================

    direct_field = get_direct_field(
        role,
        collection_name
    )


    if direct_field:


        # ==============================
        # SCHOOL
        # ==============================

        if role == "school":

            return {

                direct_field:
                normalize_id(
                    user["_id"]
                )

            }



        # ==============================
        # BRANCH
        # ==============================

        if role == "branch":

            return {

                direct_field:
                normalize_id(
                    user["_id"]
                )

            }


         # ==============================
# BRANCH GROUP
# ==============================

        if role == "branchgroup":

            return {

                direct_field:
                normalize_id(
                    user["_id"]
        )

    }
        # ==============================
        # DRIVER
        # ==============================

        if role == "driver":


            if collection_name == "drivers":

                return {

                    "_id":
                    normalize_id(
                        user["_id"]
                    )

                }



            if collection_name == "devices":

                return {

                    "_id":
                    normalize_id(
                        user["deviceObjId"]
                    )

                }



            if collection_name == "routes":

                return {

                    "_id":
                    normalize_id(
                        user["routeObjId"]
                    )

                }



    # ======================================
    # DEVICE -> UNIQUE ID COLLECTIONS
    # ======================================

    if is_unique_id_collection(collection_name):


        device_filter = {}


        if role == "school":

            device_filter["schoolId"] = normalize_id(
            user["_id"]
        )


        elif role == "branch":

            device_filter["branchId"] = normalize_id(
            user["_id"]
        )


        elif role == "driver":

            device_filter["_id"] = normalize_id(
            user["deviceObjId"]
        )


        devices = db.devices.find(
        device_filter,
        {
            "uniqueId":1
        }
    ).to_list(None)


        unique_ids = []


        for device in devices:

            uid = device.get("uniqueId")

            if uid is None:
                continue

            unique_ids.append(str(uid))

            try:
                number = int(str(uid))

        # Only add if it fits MongoDB Int64
                if -(2**63) <= number <= (2**63 - 1):
                    unique_ids.append(number)

            except Exception:
                pass



        return {

            "uniqueId": {

            "$in": list(set(unique_ids))

        }

    }

    # ======================================
    # DEVICE ID COLLECTIONS
    # ======================================

    if is_device_id_collection(
        collection_name
    ):


        device_filter = {}



        if role == "school":

            device_filter["schoolId"] = normalize_id(
                user["_id"]
            )


        elif role == "branch":

            device_filter["branchId"] = normalize_id(
                user["_id"]
            )


        elif role == "driver":

            device_filter["_id"] = normalize_id(
                user["deviceObjId"]
            )



        devices = db.devices.find(
            device_filter,
            {
                "deviceId":1
            }
        )



        device_ids = [

            str(device["deviceId"])

            for device in devices

        ]



        return {

            "deviceId":
            {
                "$in": device_ids
            }

        }



    # ======================================
    # DEVICE OBJECT ID COLLECTIONS
    # ======================================

    if is_device_objid_collection(
        collection_name
    ):


        device_filter = {}



        if role == "school":

            device_filter["schoolId"] = normalize_id(
                user["_id"]
            )


        elif role == "branch":

            device_filter["branchId"] = normalize_id(
                user["_id"]
            )


        elif role == "driver":

            device_filter["_id"] = normalize_id(
                user["deviceObjId"]
            )



        devices = db.devices.find(
            device_filter,
            {
                "_id":1
            }
        ).to_list(None)



        device_obj_ids = [

            device["_id"]

            for device in devices

        ]



        return {

            "deviceObjId":
            {
                "$in": device_obj_ids
            }

        }
   


    # ======================================
    # UNKNOWN COLLECTION
    # ======================================

    return {

        "_id": None

    }