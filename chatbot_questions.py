# config/chatbot_questions.py


QUESTION_MAP = {


# =====================================================
# SUPER ADMIN
# =====================================================

"superAdmin": [

    {
        "id": "all_schools",
        "question": "Show all schools",
        "engine": "school_engine",
        "function": "get_all_schools"
    },


    {
        "id": "all_branches",
        "question": "Show all branches",
        "engine": "branch_engine",
        "function": "get_all_branches"
    },


    {
        "id": "all_vehicles",
        "question": "Show all vehicles",
        "engine": "device_engine",
        "function": "get_all_devices"
    },


    {
        "id": "vehicle_status",
        "question": "Show vehicle status",
        "engine": "report_status_engine",
        "function": "get_all_status"
    },


    {
        "id": "live_location",
        "question": "Show live vehicle location",
        "engine": "vehiclelastposition_engine",
        "function": "get_all_positions"
    },


    {
        "id": "vehicle_distance",
        "question": "Show distance report",
        "engine": "report_distance_engine",
        "function": "get_all_distance"
    },


    {
        "id": "vehicle_trip",
        "question": "Show trip reports",
        "engine": "report_trip_engine",
        "function": "get_all_trips"
    },


    {
        "id": "idle_report",
        "question": "Show idle reports",
        "engine": "report_idle_engine",
        "function": "get_all_idle"
    },


    {
       "id": "geofence_report",
        "question": "Show geofence reports",
        "engine": "geofence_report_engine",
        "function": "get_all_geofence_reports"
    },


    {
        "id": "tickets",
        "question": "Show tickets",
        "engine": "tickets_engine",
        "function": "get_all_tickets"
    }

],




# =====================================================
# SCHOOL
# =====================================================

"school":[


    {
        "id":"my_vehicles",
        "question":"Show my vehicles",
        "engine":"school_device_engine",
        "function":"get_school_devices"
    },


    {
        "id":"my_drivers",
        "question":"Show my drivers",
        "engine":"school_engine",
        "function":"get_school_drivers"
    },


    {
        "id":"vehicle_location",
        "question":"Show vehicle location",
        "engine":"vehiclelastposition_engine",
        "function":"get_school_locations"
    },


    {
        "id":"vehicle_distance",
        "question":"Show distance report",
        "engine":"report_distance_engine",
        "function":"get_school_distance"
    },


    {
        "id":"trip_report",
        "question":"Show trip reports",
        "engine":"report_trip_engine",
        "function":"get_school_trips"
    },


    {
        "id":"geofence",
        "question":"Show geofence events",
        "engine":"geofence_report_engine",
        "function":"get_school_geofence_report"
    },


    {
        "id":"tickets",
        "question":"Show tickets",
        "engine":"tickets_engine",
        "function":"get_school_tickets"
    }

],




# =====================================================
# BRANCH
# =====================================================

"branch":[


    {
        "id":"branch_vehicle",
        "question":"Show branch vehicles",
        "engine":"branch_device_engine",
        "function":"get_branch_devices"
    },


    {
        "id":"branch_drivers",
        "question":"Show branch drivers",
        "engine":"branch_engine",
        "function":"get_branch_drivers"
    },


    {
        "id":"vehicle_status",
        "question":"Show vehicle status",
        "engine":"report_status_engine",
        "function":"get_branch_status"
    },


    {
        "id":"vehicle_location",
        "question":"Show live location",
        "engine":"vehiclelastposition_engine",
        "function":"get_branch_locations"
    },


    {
        "id":"distance",
        "question":"Show distance report",
        "engine":"report_distance_engine",
        "function":"get_branch_distance"
    },


    {
        "id":"trips",
        "question":"Show trips",
        "engine":"report_trip_engine",
        "function":"get_branch_trips"
    },


    {
        "id":"geofence",
        "question":"Show geofence report",
        "engine":"geofence_report_engine",
        "function":"get_branch_geofence_report"
    }


],





# =====================================================
# DRIVER
# =====================================================


"driver":[


    {
        "id":"my_vehicle",
        "question":"Show my vehicle",
        "engine":"device_engine",
        "function":"get_driver_device"
    },


    {
        "id":"my_location",
        "question":"Show my location",
        "engine":"vehiclelastposition_engine",
        "function":"get_driver_location"
    },


    {
        "id":"my_history",
        "question":"Show my history",
        "engine":"histories_engine",
        "function":"get_driver_history"
    },


    {
        "id":"my_trip",
        "question":"Show my trips",
        "engine":"report_trip_engine",
        "function":"get_driver_trips"
    },


    {
        "id":"my_distance",
        "question":"Show distance",
        "engine":"report_distance_engine",
        "function":"get_driver_distance"
    }


]

}