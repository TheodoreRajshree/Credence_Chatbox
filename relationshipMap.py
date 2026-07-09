RELATIONSHIP_MAP = {

    # ==========================================
    # SUPER ADMIN
    # ==========================================
    "superAdmin": {
        "accessAll": True
    },


    # ==========================================
    # SCHOOL LEVEL
    # ==========================================
    "school": {

        "direct": {

            # own profile
            "schools": "_id",

            # child collections
            "branches": "schoolId",
            "branchgroups": "schoolId",

            "devices": "schoolId",
            "drivers": "schoolId",

            "routes": "schoolId",
            "geofences": "schoolId",

            "audits": "schoolId",
            "auditsectionwises": "schoolId",

            "tickets": "schoolId",

            "children": "schoolId",
            "attendances": "schoolId",
            "contacts": "schoolId",

            "supervisors": "schoolId",
            "users": "schoolId",

            "chatbot_chats": "schoolId",
            
        },

        "throughDevice": True
    },


    # ==========================================
    # BRANCH LEVEL
    # ==========================================
    "branch": {

        "direct": {

            # own profile
            "branches": "_id",

            # child collections
            "devices": "branchId",
            "drivers": "branchId",

            "routes": "branchId",
            "geofences": "branchId",

            "audits": "branchId",
            "auditsectionwises": "branchId",

            "tickets": "branchId",

            "children": "branchId",
            "attendances": "branchId",
            "contacts": "branchId",

            "supervisors": "branchId",
            "users": "branchId",

            "chatbot_chats": "branchId"
        },

        "throughDevice": True
    },


    # ==========================================
    # DRIVER LEVEL
    # ==========================================
    "driver": {

        "direct": {

            # own profile
            "drivers": "_id",

            # assigned objects
            "devices": "_id",
            "routes": "_id"
        },

        "driverDeviceField": "deviceObjId",
        "driverRouteField": "routeObjId",

        "throughDevice": True
    },
    # ==========================================
# BRANCH GROUP LEVEL
# ==========================================
"branchgroup": {

    "direct": {

        "branchgroups": "_id",
        "schools": "schoolId"
    },

    "branchArrayField": "AssignedBranch",

    "branchCollections": {

        "branches": "_id",

        "devices": "branchId",
        "drivers": "branchId",

        "routes": "branchId",
        "geofences": "branchId",

        "audits": "branchId",
        "auditsectionwises": "branchId",

        "tickets": "branchId",

        "children": "branchId",
        "attendances": "branchId",
        "contacts": "branchId",

        "supervisors": "branchId",
        "users": "branchId",

        "chatbot_chats": "branchId"
    },

    "throughDevice": True
}
}