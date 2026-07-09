# chatbot_engine.py

from pymongo import MongoClient
from bson import ObjectId
import json
import re
import os
import inspect
from relationship_engine import RelationshipEngine
from report_engine import ReportEngine
from extra_context_engine import ExtraContextEngine
from fleet_analytics_engine import FleetAnalyticsEngine
from device_engine import DeviceEngine
from intent_detector import detect_intent
from school_engine import SchoolEngine
from school_device_engine import SchoolDeviceEngine
from vehicle_km_engine import VehicleKmEngine
from branch_engine import BranchEngine
from branch_device_engine import BranchDeviceEngine
from all_events_engine import AllEventsEngine
from Device_SubscriptionHistory_Engine import DeviceSubscriptionHistoryEngine
from Device_Subscription_Engine import DeviceSubscriptionEngine
from geofences_engine import GeofencesEngine
from geofence_report_engine import GeofenceReportEngine
from histories_engine import HistoriesEngine
from report_distance_engine import ReportDistanceEngine
from report_idle_engine import ReportIdleEngine
from report_status_engine import ReportStatusEngine
from report_stoppage_engine import ReportStoppageEngine
from report_travel_summary_engine import ReportTravelSummaryEngine
from report_trip_engine import ReportTripEngine
from route_engine import RouteEngine
from subscription_config_engine import SubscriptionConfigEngine
from tickets_engine import TicketsEngine
from usersessionlogs_engine import UserSessionLogsEngine
from vehiclelastposition_engine import VehicleLastPositionEngine
from branch_group_engine import BranchGroupEngine
from rbac import get_rbac_filter
import inspect
from predefined_questions import QUESTIONS
from engine_registry import ENGINE_REGISTRY
from bson import ObjectId
import re
# ==========================================
# MONGO
# ==========================================
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "credence3_0"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
# ==========================================
# COLLECTIONS
# ==========================================
ALL_COLLECTIONS = [

    "allevents",
    "attendances",
    "audits",
    "auditsectionwises",
    "authorized_users",
    "branches",
    "branchgroups",
    "categories",
    "children",
    "contacts",
    "daily_vehicle_distance_caches",
    "devices",
    "devicesubscriptions",
    "devicesubscriptionhistories",
    "drivers",
    "faqs",
    "geofences",
    "geofencereports",
    "histories",
    "messages",
    "models",
    "report_distances",
    "report_idles",
    "report_statuses",
    "report_stoppages",          # Fixed spelling
    "report_travelsummaries",
    "report_trips",
    "routes",
    "schools",
    "subscriptions_config",
    "tickets",
    "tickettypes",
    "usersessionlogs",
    "vehiclelastpositions",
    "branchgroups",
]

# ==========================================
# ENGINES
# ==========================================

relationship_engine = RelationshipEngine(db)
report_engine = ReportEngine(db)
extra_engine = ExtraContextEngine(db)
fleet_engine = FleetAnalyticsEngine(db)
device_engine = DeviceEngine(db)
school_engine = SchoolEngine(db)
school_device_engine = SchoolDeviceEngine(db)
vehicle_km_engine = VehicleKmEngine(db)
branch_engine = BranchEngine(db)
branch_device_engine = BranchDeviceEngine(db)
all_events_engine = AllEventsEngine(db)
device_subscription_history_engine = DeviceSubscriptionHistoryEngine(db)
Device_Subscription_Engine = DeviceSubscriptionEngine(db)
geofences_engine = GeofencesEngine(db)
geofence_report_engine = GeofenceReportEngine(db)
histories_engine =HistoriesEngine(db)
report_distance_engine = ReportDistanceEngine(db)
report_idle_engine = ReportIdleEngine(db)
report_status_engine = ReportStatusEngine(db)
report_stoppage_engine = ReportStoppageEngine(db)
report_travel_summary_engine = ReportTravelSummaryEngine(db)
report_trip_engine = ReportTripEngine(db)
route_engine = RouteEngine(db)
subscription_engine = SubscriptionConfigEngine(db)
tickets_engine = TicketsEngine(db)
user_session_engine = UserSessionLogsEngine(db)
vehiclelastposition_engine = VehicleLastPositionEngine(db)
branch_group_engine = BranchGroupEngine(db)




def normalize_vehicle_number(vehicle):
    if not vehicle:
        return ""

    # Remove leading and trailing spaces
    vehicle = vehicle.strip()

    # Remove ALL spaces, hyphens, dots, underscores, etc.
    vehicle = re.sub(r'[^A-Za-z0-9]', '', vehicle)

    # Convert to uppercase
    return vehicle.upper()
def apply_rbac(query, role, user, collection_name):

    rbac_filter = get_rbac_filter(
        role=role,
        user=user,
        collection_name=collection_name,
        db=db
    )

    if rbac_filter:
        query.update(rbac_filter)

    return query


print(
    inspect.signature(get_rbac_filter)
)
def get_question(role, question_id):

    role = (role or "").strip().lower()

    questions = QUESTIONS.get(role, [])

    for q in questions:
        if q["id"] == question_id:
            return q

    return None
def serialize(data):

    if isinstance(data, list):

        return [
            serialize(x)
            for x in data
        ]


    if isinstance(data, dict):

        result = {}

        for k,v in data.items():

            if isinstance(v, ObjectId):
                result[k] = str(v)

            else:
                result[k] = serialize(v)


        return result


    return data
def resolve_param(user, message, key):
    if isinstance(message, dict):
        if message.get(key):
            return message.get(key)

    return user.get(key) or user.get(key.lower())
def execute_engine(engine_method, role, user, message=None):

    signature = inspect.signature(engine_method)

    args = []

    print("ENGINE:", engine_method)
    print("SIGNATURE:", signature)

    for name in signature.parameters.keys():

        if name == "branch_id":

            args.append(
                user.get("branchId")
            )
        elif name == "route_id":

            args.append(
        user.get("routeObjId")
    )

        elif name == "school_id":

            args.append(
                user.get("schoolId")
            )
        elif name == "group_id":

            group_id = user.get("groupId") or user.get("branchGroupId")

            if group_id and ObjectId.is_valid(str(group_id)):
                group_id = str(group_id)
            else:
                group_id = None

            args.append(group_id)

        elif name == "unique_id":

            args.append(
                user.get("deviceObjId")
            )


        elif name == "username":

            args.append(
                user.get("username")
            )
        elif name == "vehicle_input":
            args.append(message)


        elif name == "message":

            args.append(
                message
            )


        elif name == "role":

            args.append(
                role
            )


        elif name == "user":

            args.append(
                user
            )
        


    print("FINAL ARGS:", args)

    return engine_method(*args)



def execute_predefined_question(
    role,
    user,
    question_id,
    input_value=None
):

    question = get_question(
        role,
        question_id
    )
    if not question:
        return {
        "success": False,
        "message": "Question not found"
    }

    if "options" in question:
        return {
        "success": True,
        "type": "nested_question",
        "question": question["question"],
        "options": question["options"]
    }

    if not question:
        return {
            "success": False,
            "message": "Question not found"
        }

    function_name = question["function"]

    engine_method = ENGINE_REGISTRY.get(
        function_name
    )

    if not engine_method:
        return {
            "success": False,
            "message": f"{function_name} not registered"
        }

    try:

        if function_name in (

            # Branch
            "get_branch_single_vehicle",
            "get_single_branch_vehicle_status",
            "get_specific_vehicle_distance_report",
            "get_specific_vehicle_travel_summary",
            "get_specific_vehicle_idle_report",
            "get_specific_vehicle_last_position",
            "get_specific_branch_geofence",
            "get_specific_vehicle_daily_distance",
            "get_route_branch_specific_vehicle",
            "get_branch_single_vehicle_km_report",
            "calculate_week_month_distance",
            "get_branch_today_accurate_distance",
           "get_specific_branch_by_name",
           "get_branchgroup_vehicle_school_branch",

            # School
            "get_school_single_vehicle",
            "get_single_school_vehicle_status",
            # "get_school_single_vehicle_km_report",
            # "get_school_specific_vehicle_distance_report",
            "get_specific_vehicle_idle_report",
            "get_specific_vehicle_travel_summary",
            "get_school_specific_vehicle_idle_report",
            "get_school_specific_vehicle_last_position",
            "get_school_specific_vehicle_daily_distance",
            "get_school_specific_geofence",
            "get_route_school_specific_vehicle",
            "get_specific_school_vehicle_distance_report",
            "get_school_single_vehicle_km_report",
            "get_vehicle_km_custom_report",
            "get_school_today_accurate_distance",
            "get_school_with_vehicles_final_for_devices",
            "get_school_with_branches",
            "get_school_with_branches_final",
            "get_school_single_branch",
            " get_branchgroup_vehicle_today_distance",

        ):

            if not input_value:
                return {
                    "success": False,
                    "message": "Please enter vehicle name or unique ID"
                }
            if function_name == "get_school_single_branch":

                print("========== DEBUG ==========")
                print("input_value =", input_value)
                print("type =", type(input_value))

                school_name = (
        input_value.get("school_name")
        or input_value.get("schoolId")
        or user.get("schoolName")
        or user.get("schoolId")
    )

                branch_name = (
        input_value.get("branch_name")
        or input_value.get("branchId")
        or user.get("branchName")
        or user.get("branchId")
    )

                print("school_name =", school_name)
                print("branch_name =", branch_name)
                print("===========================")

                result = engine_method(
        school_name,
        branch_name,
        role,
        user
    )
            elif function_name == "get_branchgroup_vehicle_today_distance":


                print("INPUT VALUE =", input_value)


                if isinstance(input_value, dict):

                    vehicle_input = (
            input_value.get("vehicle_input")
            or input_value.get("vehicle")
            or ""
        )

                else:

                    vehicle_input = input_value



                print(
        "FINAL VEHICLE INPUT =",
        vehicle_input
    )


                group_id = (
        user.get("groupId")
        or user.get("branchGroupId")
    )


                result = engine_method(

        group_id,

        vehicle_input,

        role,

        user

    )
            # ---------------- SCHOOL ----------------
            elif function_name.startswith("get_school"):

                if isinstance(input_value, dict):

                    school_name = (
                        input_value.get("school_name")
                        or user.get("schoolName")
                        or user.get("schoolId")
                    )

                   

                    vehicle_input = re.sub(
    r'[^A-Za-z0-9]',
    '',
    input_value.get("vehicle_input", "")
).upper()
                else:

                    school_name = (
                        user.get("schoolName")
                        or user.get("schoolId")
                    )

                    vehicle_input = re.sub(
    r'[^A-Za-z0-9]',
    '',
    input_value
).upper()

                result = engine_method(
                    school_name,
    
                    vehicle_input,
                    role,
                    user
                )
            
            elif function_name == "get_branchgroup_devices":

                location_name = input_value.get(
        "location_name"
    )

                vehicle_input = input_value.get(
        "vehicle_input"
    )


                result = engine_method(
        user.get("groupId"),
        location_name,
        vehicle_input,
        role,
        user
    )
            elif function_name == "get_branchgroup_vehicle_school_branch":

            
                    vehicle_input = input_value.get(
        "vehicle_input"
    )


                    result = engine_method(
        user.get("groupId"),
       
        vehicle_input,
        role,
        user
    )
            # ---------------- BRANCH ----------------
            else:

                if isinstance(input_value, dict):

                    branch_name = (
                        input_value.get("branch_name")
                        or user.get("branchName")
                        or user.get("branchId")
                    )

                    vehicle_input = input_value.get("vehicle_input")

                else:

                    branch_name = (
                        user.get("branchName")
                        or user.get("branchId")
                    )

                    vehicle_input = input_value

                result = engine_method(
                    branch_name,
                    vehicle_input,
                    role,
                    user
                )

        # -------- NORMAL FUNCTIONS --------
        else:

            result = execute_engine(
                engine_method,
                role,
                user,
                input_value
            )

        return {
            "success": True,
            "question": question["question"],
            # "function": function_name,
            "data": serialize(result)
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
# ==========================================
# CLEAN DOC
# ==========================================

def clean_doc(doc):

    data = {}

    for k, v in doc.items():

        if k == "_id":
            continue

        data[k] = str(v)

    return data

# ==========================================
# BUILD CONTEXT
# ==========================================

def build_context(
    role,
    user,
    message
):

    context = {}
    msg_lower = message.lower()
    msg_upper = message.upper()
    
    vehicle_match = re.search(
    r"\b[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}\b",
    msg_upper
)

    vehicle_number = vehicle_match.group() if vehicle_match else None

   

    collections = detect_intent(
        message
    )

    print("QUESTION:", message)
    print("COLLECTIONS:", collections)
    # =====================================
# ALL EVENTS ENGINE
# =====================================

    if "allevents" in collections:

        try:

            if role.lower() == "superAdmin":

                context["all_events"] = (
                all_events_engine.get_all_events( role,
        user)
            )

            elif role.lower() == "school":

                context["all_events"] = (
                all_events_engine.get_school_events(
                    user.get("schoolId"),
                     role,
        user
                )
            )
            elif role.lower() == "branchgroup":

                context["all_events"] = (
        all_events_engine.get_branchgroup_events(
            user.get("groupId") or user.get("branchGroupId"),
            role,
            user
        )
    )
            elif role.lower() == "branch":

                context["all_events"] = (
                all_events_engine.get_branch_events(
                    user.get("branchId"),
                     role,
        user
                )
            )

            elif role.lower() == "driver":

                context["all_events"] = (
                all_events_engine.get_driver_events(
                    user.get("username"),
                     role,
        user
                )
            )

                context["active_module"] = "all_events_engine"

        except Exception as e:

            print(
            "All Events Error:",
            e
        )
        # =====================================
# TRIP REPORT ENGINE
# =====================================
    # =====================================
# BRANCH GROUP ENGINE
# =====================================

    if "branchgroups" in collections:

        try:

            if role.lower() == "superadmin":

                context["branch_group"] = (
                branch_group_engine.get_all_groups(
                    role,
                    user
                )
            )

            elif role.lower() == "school":

                context["branch_group"] = (
                branch_group_engine.get_school_groups(
                    user.get("schoolId"),
                    role,
                    user
                )
            )

            elif role.lower() == "branch":

                context["branch_group"] = (
                branch_group_engine.get_branch_groups(
                    user.get("branchId"),
                    role,
                    user
                )
            )

            elif role.lower() == "driver":

                context["branch_group"] = (
                branch_group_engine.get_driver_groups(
                    user.get("username"),
                    role,
                    user
                )
            )

            elif role.lower() == "branchgroup":

                context["branch_group"] = (
                branch_group_engine.get_group_profile(
                    user.get("groupId") or user.get("branchGroupId"),
                    role,
                    user
                )
            )

            context["active_module"] = "branch_group_engine"

        except Exception as e:

            print("Branch Group Engine Error:", e)
    if "report_trips" in collections:

        try:

            if role.lower() == "superAdmin":

                context["report_trips"] = (

                report_trip_engine
                .get_all_trips( role,
        user)

            )

            elif role.lower() == "school":

                context["report_trips"] = (

                report_trip_engine
                .get_school_trips(

                    user.get("schoolId"),
                     role,
        user

                )

            )

            elif role.lower() == "branch":

                context["report_trips"] = (

                report_trip_engine
                .get_branch_trips(

                    user.get("branchId"),
                     role,
        user

                )

            )

            elif role.lower() == "driver":

                context["report_trips"] = (

                report_trip_engine
                .get_driver_trips(

                    user.get("username"),
                     role,
        user

                )

            )

            context["active_module"] = "report_trip_engine"

        except Exception as e:

            print(

            "Trip Report Engine Error:",

            e

        )    
            
# =====================================
# ROUTE SEARCH
# =====================================

    route_match = re.search(
    r"([A-Za-z0-9_-]+)\s+route",
    message,
    re.I
)

    if route_match:

        route_number = route_match.group(1).strip()

        route_filter = get_rbac_filter(
        role,
        user,
        "routes",
        db
    )


        route = db["routes"].find_one({

        "$and":[

            route_filter,

            {
                "routeNumber": {
                    "$regex": f"^{re.escape(route_number)}$",
                    "$options": "i"
                }
            }

        ]

    })


    print("ROUTE FOUND:", route)


    if route:

        route_id = str(route["_id"])

        context["route_details"] = (
            route_engine.get_route_details(
                route_id,
                role,
                user
            )
        )

        context["active_module"] = "route_engine"
            # =====================================
# STOPPAGE REPORT ENGINE
# =====================================

    if "report_stoppages" in collections:

        try:

            if role.lower() == "superAdmin":

                context["report_stoppages"] = (

                report_stoppage_engine
                .get_all_stoppage_reports(  role,
    user)

            )
            elif role.lower() == "branchgroup":

                context["all_events"] = (
        all_events_engine.get_branchgroup_events(
            user.get("groupId") or user.get("branchGroupId"),
            role,
            user
        )
    )

            elif role.lower() == "school":

                context["report_stoppages"] = (

                report_stoppage_engine
                .get_school_stoppage_report(

                    user.get("schoolId"),
                      role,
    user

                )

            )

            elif role.lower() == "branch":

                context["report_stoppages"] = (

                report_stoppage_engine
                .get_branch_stoppage_report(

                    user.get("branchId"),
                      role,
    user

                )

            )

            elif role.lower() == "driver":

                context["report_stoppages"] = (

                report_stoppage_engine
                .get_driver_stoppage_report(

                    user.get("username"),
                      role,
    user

                )

            )

            context["active_module"] = "report_stoppage_engine"

        except Exception as e:

            print(
            "Stoppage Report Engine Error:",
            e
        )
            
            # =====================================
# GEOFENCES ENGINE
# =====================================

    if "geofences" in collections:

        try:

            if role.lower() == "superAdmin":

                context["geofences"] = (

                geofences_engine
                .get_all_geofences( role,
    user)

            )
            elif role.lower() == "branchgroup":

                context["all_events"] = (
        all_events_engine.get_branchgroup_events(
            user.get("groupId") or user.get("branchGroupId"),
            role,
            user
        )
    )

            elif role.lower() == "school":

                context["geofences"] = (

                geofences_engine
                .get_school_geofences(

                    user.get("schoolId"),
                     role,
    user

                )

            )

            elif role.lower() == "branch":

                context["geofences"] = (

                geofences_engine
                .get_branch_geofences(

                    user.get("branchId"),
                     role,
    user

                )

            )

            elif role.lower() == "driver":

                context["geofences"] = (

                geofences_engine
                .get_driver_geofences(

                    user.get("username"),
                     role,
    user

                )

            )

            context["active_module"] = "geofences_engine"

        except Exception as e:

            print(
            "Geofences Engine Error:",
            e
        )
# =====================================
# STATUS REPORT ENGINE
# =====================================

    if "report_statuses" in collections:

        try:

            if role.lower() == "superAdmin":

                context["report_statuses"] = (
                report_status_engine
                .get_all_status_reports(  role,
    user)

            )
            elif role.lower() == "branchgroup":

                context["all_events"] = (
        all_events_engine.get_branchgroup_events(
            user.get("groupId") or user.get("branchGroupId"),
            role,
            user
        )
    )
            elif role.lower() == "school":

                context["report_statuses"] = (

                report_status_engine
                .get_school_status_report(

                    user.get("schoolId"),
                      role,
    user

                )
            )
            elif role.lower() == "branch":

                context["report_statuses"] = (

                report_status_engine
                .get_branch_status_report(

                    user.get("branchId"),
                      role,
    user
                )
            )
            elif role.lower() == "driver":

                context["report_statuses"] = (

                report_status_engine
                .get_driver_status_report(

                    user.get("username")
                    ,  role,
    user

                )

            )

            context["active_module"] = "report_status_engine"

        except Exception as e:

            print(
            "Status Report Engine Error:",
            e
        )      
# =====================================
# DISTANCE REPORT ENGINE
# =====================================

    if "report_distances" in collections:

        try:

            if role.lower() == "superAdmin":

                context["report_distances"] = (

                report_distance_engine
                .get_all_distance_reports( role,
    user)

            )
            elif role.lower() == "branchgroup":

                context["all_events"] = (
        all_events_engine.get_branchgroup_events(
            user.get("groupId") or user.get("branchGroupId"),
            role,
            user
        )
    )

            elif role.lower() == "school":

                context["report_distances"] = (

                report_distance_engine
                .get_school_distance_report(

                    user.get("schoolId"),
                     role,
    user

                )

            )

            elif role.lower() == "branch":

                context["report_distances"] = (

                report_distance_engine
                .get_branch_distance_report(

                    user.get("branchId"),
                     role,
    user

                )

            )

            elif role.lower() == "driver":

                context["report_distances"] = (

                report_distance_engine
                .get_driver_distance_report(

                    user.get("username"),
                     role,
    user

                )

            )

            context["active_module"] = "report_distance_engine"

        except Exception as e:

            print(
            "Distance Report Engine Error:",
            e
        )
            
            # =====================================
# TRAVEL SUMMARY ENGINE
# =====================================

    if "report_travelsummaries" in collections:

        try:

            if role.lower() == "superAdmin":

                context["report_travelsummaries"] = (

                report_travel_summary_engine
                .get_all_travel_summaries(  role,
                    user)

            )

            elif role.lower() == "school":

                context["report_travelsummaries"] = (

                report_travel_summary_engine
                .get_school_travel_summary(

                    user.get("schoolId"),
                      role,
    user

                )

            )
            elif role.lower() == "branchgroup":

                context["all_events"] = (
        all_events_engine.get_branchgroup_events(
            user.get("groupId") or user.get("branchGroupId"),
            role,
            user
        )
    )
            elif role.lower() == "branch":

                context["report_travelsummaries"] = (

                report_travel_summary_engine
                .get_branch_travel_summary(

                    user.get("branchId"),
                      role,
    user

                )

            )

            elif role.lower() == "driver":

                context["report_travelsummaries"] = (

                report_travel_summary_engine
                .get_driver_travel_summary(

                    user.get("username"),
                      role,
    user

                )

            )

            context["active_module"] = "report_travel_summary_engine"

        except Exception as e:

            print(

            "Travel Summary Engine Error:",

            e

        )
            # =====================================
# GEOFENCE REPORT ENGINE
# =====================================

    if "geofencereports" in collections:

        try:

            if role.lower() == "superAdmin":

                context["geofence_reports"] = (

                geofence_report_engine
                .get_all_geofence_reports(  role,
    user)

            )

            elif role.lower() == "school":

                context["geofence_reports"] = (

                geofence_report_engine
                .get_school_geofence_report(

                    user.get("schoolId"),
                      role,
    user

                )

            )
            elif role.lower() == "branchgroup":

                context["all_events"] = (
        all_events_engine.get_branchgroup_events(
            user.get("groupId") or user.get("branchGroupId"),
            role,
            user
        )
    )

            elif role.lower() == "branch":

                context["geofence_reports"] = (

                geofence_report_engine
                .get_branch_geofence_report(

                    user.get("branchId"),
                      role,
    user

                )

            )

            elif role.lower() == "driver":

                context["geofence_reports"] = (

                geofence_report_engine
                .get_driver_geofence_report(

                    user.get("username"),
                      role,
    user

                )

            )

            context["active_module"] = "geofence_report_engine"

        except Exception as e:

            print("Geofence Report Error:", e)

# =====================================
# USER SESSION LOGS ENGINE
# =====================================

    if (
    "session" in message.lower()
    or "login" in message.lower()
    or "logout" in message.lower()
):

        if role.lower() == "superAdmin":

            context["user_sessions"] = (
            user_session_engine.get_all_sessions(  role,
        user)
        )

            context["session_dashboard"] = (
            user_session_engine.get_dashboard(  role,
        user)
        )

        else:

            context["user_sessions"] = (
                user_session_engine.get_user_sessions(
                user.get("_id"),
                  role,
        user
            )
        )

        context["active_module"] = "user_session_engine"
            # =====================================
# TICKETS ENGINE
# =====================================

    if "ticket" in message.lower():

        if role.lower() == "superAdmin":

            context["tickets"] = (
            tickets_engine.get_all_tickets( role,
        user)
        )
        elif role.lower() == "branchgroup":

            context["all_events"] = (
        all_events_engine.get_branchgroup_events(
            user.get("groupId") or user.get("branchGroupId"),
            role,
            user
        )
    )

        elif role.lower() == "school":

            context["tickets"] = (
                tickets_engine.get_school_tickets(
                    user.get("schoolId"),
                     role,
        user
            )
        )

        elif role.lower() == "branch":

            context["tickets"] = (
                tickets_engine.get_branch_tickets(
                    user.get("branchId"),
                     role,
        user
            )
        )

        context["ticket_dashboard"] = (
            tickets_engine.get_ticket_dashboard( role,
        user)
    )

        context["active_module"] = "tickets_engine"


        # =====================================
# VEHICLE LAST POSITION ENGINE
# =====================================

    if "vehiclelastpositions" in collections:

        try:

            if role.lower() == "superAdmin":

                context["vehiclelastpositions"] = (

                vehiclelastposition_engine
                .get_all_last_positions(   role,
    user)

            )
            elif role.lower() == "branchgroup":

                context["all_events"] = (
        all_events_engine.get_branchgroup_events(
            user.get("groupId") or user.get("branchGroupId"),
            role,
            user
        )
    )
            elif role.lower() == "school":

                context["vehiclelastpositions"] = (

                vehiclelastposition_engine
                .get_school_last_positions(

                    user.get("schoolId"),
                       role,
    user

                )

            )

            elif role.lower() == "branch":

                context["vehiclelastpositions"] = (

                vehiclelastposition_engine
                .get_branch_last_positions(

                    user.get("branchId"),
                       role,
    user

                )

            )

            elif role.lower() == "driver":

                context["vehiclelastpositions"] = (

                vehiclelastposition_engine
                .get_driver_last_position(

                    user.get("username"),
                       role,
    user

                )

            )

            context["active_module"] = "vehiclelastposition_engine"

        except Exception as e:

            print(
            "Vehicle Last Position Engine Error:",
            e
        )
    # =====================================
# DEVICE SUBSCRIPTION ENGINE
# =====================================

    if "devicesubscriptions" in collections:

        try:

            if role.lower() == "superAdmin":

                context["device_subscription"] = (

                Device_Subscription_Engine
                .get_all_subscriptions(   role,
    user)

            )
            elif role.lower() == "branchgroup":

                context["all_events"] = (
        all_events_engine.get_branchgroup_events(
            user.get("groupId") or user.get("branchGroupId"),
            role,
            user
        )
    )
            elif role.lower() == "school":

                context["device_subscription"] = (

                   Device_Subscription_Engine
                .get_school_subscriptions(

                    user.get("schoolId"),
                       role,
    user

                )

            )

            elif role.lower() == "branch":

                context["device_subscription"] = (

                   Device_Subscription_Engine
                .get_branch_subscriptions(

                    user.get("branchId"),
                       role,
    user

                )

            )

            elif role.lower() == "driver":

                context["device_subscription"] = (

                   Device_Subscription_Engine
                .get_driver_subscription(

                    user.get("username"),
                       role,
    user

                )

            )

            context["active_module"] = "device_subscription_engine"

        except Exception as e:

            print(
            "Device Subscription Error:",
            e
        )
            
# =====================================
# HISTORIES ENGINE
# =====================================

    if "histories" in collections:

        try:

            if role.lower() == "superAdmin":

                context["histories"] = (

                histories_engine
                .get_all_history(   role,
    user)

            )
            elif role.lower() == "branchgroup":

                context["all_events"] = (
        all_events_engine.get_branchgroup_events(
            user.get("groupId") or user.get("branchGroupId"),
            role,
            user
        )
    )
            elif role.lower() == "school":

                context["histories"] = (

                histories_engine
                .get_school_history(

                    user.get("schoolId"),
                       role,
    user

                )

            )

            elif role.lower() == "branch":

                context["histories"] = (

                histories_engine
                .get_branch_history(

                    user.get("branchId"),
                       role,
    user

                )

            )

            elif role.lower() == "driver":

                context["histories"] = (

                histories_engine
                .get_driver_history(

                    user.get("username"),
                       role,
    user

                )

            )

            context["active_module"] = "histories_engine"

        except Exception as e:

            print(
            "Histories Engine Error:",
            e
        )
            

            # =====================================
# DEVICE SUBSCRIPTION HISTORY
# =====================================
# =====================================
# IDLE REPORT ENGINE
# =====================================

    if "report_idles" in collections:

        try:

            if role.lower() == "superAdmin":

                context["report_idles"] = (

                report_idle_engine
                .get_all_idle_reports(   role,
    user)

            )

            elif role.lower() == "school":

                context["report_idles"] = (

                report_idle_engine
                .get_school_idle_report(

                    user.get("schoolId"),
                       role,
    user

                )

            )
            elif role.lower() == "branchgroup":

                context["all_events"] = (
        all_events_engine.get_branchgroup_events(
            user.get("groupId") or user.get("branchGroupId"),
            role,
            user
        )
    )
            elif role.lower() == "branch":

                context["report_idles"] = (

                report_idle_engine
                .get_branch_idle_report(

                    user.get("branchId"),
                       role,
    user

                )

            )

            elif role.lower() == "driver":

                context["report_idles"] = (

                report_idle_engine
                .get_driver_idle_report(

                    user.get("username"),
                       role,
    user

                )

            )

            context["active_module"] = "report_idle_engine"

        except Exception as e:

            print(
            "Idle Report Engine Error:",
            e
        )

    if "devicesubscriptionhistories" in collections:

        try:

            if role.lower() == "superadmin":

                context["device_subscription_history"] = (

                device_subscription_history_engine
                .get_all_subscription_history(   role,
    user)

            )
            elif role.lower() == "branchgroup":

                context["all_events"] = (
        all_events_engine.get_branchgroup_events(
            user.get("groupId") or user.get("branchGroupId"),
            role,
            user
        )
    )
            elif role.lower() == "school":

                context["device_subscription_history"] = (

                device_subscription_history_engine
                .get_school_subscription_history(

                    user.get("schoolId"),
                       role,
    user

                )

            )

            elif role.lower() == "branch":

                context["device_subscription_history"] = (

                device_subscription_history_engine
                .get_branch_subscription_history(

                    user.get("branchId"),
                       role,
    user

                )

            )

            elif role.lower() == "driver":

                context["device_subscription_history"] = (

                device_subscription_history_engine
                .get_driver_subscription_history(

                    user.get("username"),
                       role,
    user

                )

            )

            context["active_module"] = "device_subscription_history_engine"

        except Exception as e:

            print(
            "Subscription History Error:",
            e
        )
    # =====================================
    # COLLECTION DATA
    # =====================================
    branch_engine = BranchEngine(db)
    for col in collections:

        try:

            if col not in ALL_COLLECTIONS:
                continue
            rbac_filter = get_rbac_filter(
    role,
    user,
    col,
    db
)
            records = list(
                db[col]
                .find(rbac_filter)
                .limit(20)
            )

            context[col] = {

                "count":
                db[col].count_documents(
                    rbac_filter
                ),

                "sample_records": [
                    clean_doc(x)
                    for x in records
                ]
            }

        except Exception as e:

            print(
                f"{col} error:",
                e
            )

    # =====================================
    # USER PROFILE
    # =====================================

    try:

        context["logged_in_user"] = (

            relationship_engine
            .get_user_profile(
                role,
                user
            )

        )

    except Exception as e:

        print(
            "Profile Error",
            e
        )
# =====================================
# SUBSCRIPTION CONFIG SEARCH
# =====================================

        subscription_match = re.search(
    r"([A-Za-z0-9_-]+)\s+(subscription|plan|model)",
    message,
    re.I
)

        if subscription_match:

            model_name = subscription_match.group(1)

            subscription = subscription_engine.search_subscription(model_name, role,
    user)

            if subscription:

                context["subscription_details"] = subscription
                context["active_module"] = "subscription_config_engine"
    # =====================================
    # DRIVER REPORT
    # =====================================

    try:

        driver_filter = get_rbac_filter(role,
    user,
    "drivers",
    db
)

        driver = db["drivers"].find_one({

    "$and": [

        driver_filter,

        {
            "username":
            user.get("username")
        }

    ]

})

        if driver:

            context["reports"] = (

                report_engine
                .get_driver_report(
                    driver, role,
    user
                )

            )

    except Exception as e:

        print(
            "Report Error",
            e
        )

    # =====================================
    # EXTRA CONTEXT
    # =====================================
    try:

        if driver:

            device_filter = get_rbac_filter(
    role,
    user,
    "devices",
    db
)

            device = db["devices"].find_one({

    "$and": [

        device_filter,

        {
            "_id":
            driver.get(
                "deviceObjId"
            )
        }

    ]

})

            context["extra"] = (

                extra_engine
                .build_extra_context(

                    driver,
                    device,   role,
    user
                )
            )
    except Exception as e:

        print(
            "Extra Error",
            e
        )


    km_data = None

    vehicle_keywords = [
        "km",
        "distance",
        "mileage",
        "vehicle report",
        "km report"
]
    is_vehicle_query = any(
        keyword in message.lower()
        for keyword in vehicle_keywords
)

    if is_vehicle_query:

        vehicle_number = None
    
        vehicle_match = re.search(
        r"\b[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}\b",
        message.upper()
)

    vehicle_number = vehicle_match.group() if vehicle_match else None

    if vehicle_number:

        km_data = vehicle_km_engine.get_km_report(
        vehicle_number,
        message, role,
    user
    )

    if km_data:
        context["vehicle_km_report"] = km_data
        context["active_module"] = "vehicle_km_engine"
    # =====================================
    # DEVICE SEARCH
    # =====================================

    try:

        device = device_engine.find_device(
            message, role,
    user
        )

        if device:

            unique_id = device.get(
                "uniqueId"
            )

            context[
                "device_details"
            ] = (

                device_engine
                .get_device_details(
                    device,  role,
        user
                )

            )

            context[
                "fleet_analytics"
            ] = (

                fleet_engine
                .get_vehicle_analytics(
                    unique_id,  role,
        user
                )

            )

    except Exception as e:

        print(
            "Device Error",
            e
        )



    school_match = re.search(





    r"([A-Za-z0-9\s]+)\s+school",
    message,
    re.I
)

    if school_match:

        school_name = school_match.group(1).strip()

        school_data = (
        school_device_engine
        .get_school_with_vehicles(
            school_name, role,
        user
        )
    )

        if school_data:

            context["school_vehicle_details"] = school_data 
    # =====================================
    # SCHOOL ENGINE
    # =====================================

    try:

        school_id = user.get("schoolId")

        if school_id:

            if (
                "school" in message.lower()
                or "dashboard" in message.lower()
                or "vehicle" in message.lower()
                or "driver" in message.lower()
            ):

                context["school_dashboard"] = (
                    school_engine.get_school_dashboard(
                        school_id,   role,
        user
                    )
                )

                context["school_profile"] = (
                    school_engine.get_school_profile(
                        school_id,   role,
        user
                    )
                )

    except Exception as e:

        print(
            "School Engine Error",
            e
        )
    try:

        group_id = None

    # ----------------------------
    # STEP 1: FROM USER OBJECT
    # ----------------------------
        group_id = (
        user.get("groupId")
        or user.get("branchGroupId")
    )

    # ----------------------------
    # STEP 2: FALLBACK DB LOOKUP
    # ----------------------------
        if not group_id and user.get("username"):

            user_doc = db["authorized_users"].find_one({
            "username": user.get("username")
        })

            if user_doc:
                group_id = (
                user_doc.get("groupId")
                or user_doc.get("branchGroupId")
            )

    # ----------------------------
    # STEP 3: VALIDATE group_id
    # ----------------------------
        if group_id and ObjectId.is_valid(str(group_id)):

            message_text = (message or "").lower()

        # cache engine calls (IMPORTANT OPTIMIZATION)
            engine = branch_group_engine

        # ---------------- DASHBOARD
            if "dashboard" in message_text:
                context["branch_group_dashboard"] = engine.get_group_dashboard(
                group_id, role, user
            )

        # ---------------- PROFILE
            elif "profile" in message_text:
                context["branch_group_profile"] = engine.get_group_profile(
                group_id, role, user
            )

        # ---------------- BRANCHES
            elif "branch" in message_text:
                context["branch_group_branches"] = engine.get_group_branches(
                group_id, role, user
            )

        # ---------------- VEHICLES
            elif "vehicle" in message_text:
                context["branch_group_vehicles"] = engine.get_group_vehicles(
                group_id, role, user
            )

        # ---------------- DRIVERS
            elif "driver" in message_text:
                context["branch_group_drivers"] = engine.get_group_drivers(
                group_id, role, user
            )

        # ---------------- ROUTES
            elif "route" in message_text:
                context["branch_group_routes"] = engine.get_group_routes(
                group_id, role, user
            )

        # ---------------- GEOFENCES
            elif "geofence" in message_text:
                context["branch_group_geofences"] = engine.get_group_geofences(
                group_id, role, user
            )

    except Exception as e:
        print("Branch Group Engine Error:", e)
    # =====================================
    # SCHOOL DEVICE ENGINE
    # =====================================
    try:
        school_id = user.get("schoolId")

        if school_id:

            msg = message.lower()

            if (
                "school" in msg and (
                    "vehicles" in msg  or
                    "vehicle" in msg  or
                    "device" in msg  or
                    "devices" in msg 
				)
            ):

                context["school_devices"] = (
                    school_device_engine.get_school_devices(
                        school_id,  role,
        user
                    )
                )
            elif "school device summary" in msg:
                context["school_device_summary"] = (
                    school_device_engine.get_school_device_summary(
                        school_id,  role,
        user
                    )
                )
    except Exception as e:
        print("School Device Engine Error:", e)
    # =====================================
    # UNIQUE ID SEARCH
    # =====================================

    uid_match = re.search(
        r"\b\d{15}\b",
        message
    )
    if uid_match:
        unique_id = uid_match.group()
        context[
            "fleet_analytics"
        ] = (
            fleet_engine
            .get_vehicle_analytics(
                unique_id, role,
        user
            )
        )
        



    branch_filter = get_rbac_filter(
    role,
    user,
    "branches",
    db
)
    for branch in db["branches"].find():

        branch_name = branch.get(
            "branchName",
        ""
    )

        if branch_name.lower() in message.lower():

            branch_id = branch["_id"]

            if "vehicle" in message.lower():

                context[
                "branch_vehicles"
            ] = (
                branch_engine
                .get_branch_vehicles(
                    branch_id, role,
    user
                )
            )

            elif "driver" in message.lower():

                context[
                "branch_drivers"
            ] = (
                branch_engine
                .get_branch_drivers(
                    branch_id, role,
    user
                )
            )

            elif "route" in message.lower():

                context[
                "branch_routes"
            ] = (
                branch_engine
                .get_branch_routes(
                    branch_id, role,
    user
                )
            )

        

            elif "geofence" in message.lower():

                context[
                "branch_geofences"
            ] = (
                branch_engine
                .get_branch_geofences(
                    branch_id, role,
    user
                )
            )

            else:

                context[
                "branch_details"
            ] = (
                branch_engine
                .get_branch_details(
                    branch_id,role,user
                )
            )

            context[
            "active_module"
        ] = "branch_engine"

            break    


    for branch in db["branches"].find():

        branch_name = branch.get(
        "branchName",
        ""
    )

        if branch_name.lower() in message.lower():

            context[
            "branch_with_vehicles"
        ] = (
            branch_device_engine
            .get_branch_with_vehicles(
                branch_name, role,
    user
            )
        )

            context[
            "active_module"
        ] = "branch_device_engine"

           
            collections.append("branches")
            collections.append("devices")

            break
# =====================================
# SCHOOL VEHICLE DETECTION (IMPORTANT)
# =====================================

    school_data = None

    words = message.split()

    for word in words:

        if len(word) < 3:
            continue
        school_filter = get_rbac_filter(
    role,
    user,
    "schools",
    db
)
        school_data = db["schools"].find_one({
        "schoolName": {
            "$regex": word,
            "$options": "i"
        }
    })

        if school_data:
            break

        if school_data:

            context["school_with_vehicles"] = (
            school_device_engine.get_school_with_vehicles(
            school_data["name"],
             role,
    user
        )
    )

        context["active_module"] = "school_device_engine"
    return context


# ==========================================
# PROMPT
# ==========================================
def build_prompt(
    role,
    user,
    message,
    context
):

    return f"""
You are an Enterprise Fleet AI Assistant.

ROLE:
{role}

USERNAME:
{user.get("username")}

IMPORTANT RULES:

1. Follow RBAC strictly.
2. Never reveal unauthorized data.
3. Use only the provided context.
4. Never assume missing values.
5. Never invent data.
6. If data is unavailable, say "Data not available".
7. Answer ONLY what the user asks.
8. Do NOT generate extra sections unless requested.
9. Keep responses concise and accurate.
10. For vehicle name queries, return only vehicle names.
11. For vehicle count queries, return only vehicle count.
12. For branch queries, return only branch information.
13. For school queries, return only school information.
14. For driver queries, return only driver information.
15. For distance questions, show exact values from data.
16.IF school_with_vehicles EXISTS:

17. If user asks "all vehicles / vehicle details"
- "vehicle details"
- "all vehicle details"
- "complete vehicle details"
- "school vehicle details"

→ return:
Vehicle Name
Unique ID
Status
phone number
KM Report
Category
Model
SchoolId
BranchId

Do NOT return only vehicle names.

18. DO NOT return single vehicle if ask any school, branch all

19. Always format like: vehicle

Vehicle List:
- vehicle1
- vehicle2
- vehicle3
20.


If driver_routes exists:
Return all routes assigned to driver.

If device_geofences exists:
Return:
- geofenceName1
- geofenceName2
- geofenceName3
Return ALL geofence names in list format.
If "school_with_vehicles" is present in context, you MUST use:
context["school_with_vehicles"]["vehicles"]

Do NOT summarize into a single value.
Do NOT return only one vehicle.
21.BRANCH RULES

If branch_details exists:
Return complete branch information.

If branch_vehicles exists:
Return all vehicles assigned to branch.

If branch_drivers exists:
Return all drivers assigned to branch.

If branch_routes exists:
Return all routes assigned to branch.

If branch_geofences exists:
Return:
- geofenceName1
- geofenceName2
- geofenceName3
Return ALL geofence names in list format.

If branch dashboard exists:
Return vehicle count, driver count, route count,
geofence count and ticket count.

If user asks event information → return event information only.
If all_events exists:
Return eventType,
uniqueId,
eventTime,
latitude,
longitude,
speed.
==============================
DEVICE SUBSCRIPTION HISTORY RULES
==============================

If device_subscription_history exists:

Return the complete subscription history.

For each record return:

- Device ID
- Previous Expiry Date
- New Expiry Date
- Changed By
- Changed By Model
- Changed By Role
- Remark
- Changed Date

Format:

Subscription History:

Record 1
Device ID:
Previous Expiry Date:
New Expiry Date:
Changed By:
Changed By Model:
Changed By Role:
Remark:
Changed Date:

Record 2
...

If there are multiple history records, return ALL records.

Do NOT summarize.
Do NOT skip any record.
Do NOT invent missing values.

If no subscription history exists, reply:
"Subscription history not available."
==============================
DEVICE SUBSCRIPTION RULES
==============================

If device_subscription exists:

Return:

- Device ID
- Unique ID
- Base Amount
- GST Amount
- GST Rate
- Total Amount
- Currency
- Payment Status
- Previous Expiry Date
- New Expiry Date
- Paid At
- Paid By
- Paid By Model
- Paid By Role
- Razorpay Order ID
- Razorpay Payment ID

If multiple subscriptions exist, return ALL records.

If no subscription exists, reply:
"Subscription details not available."

Do not summarize.
Do not invent values.

==============================
GEOFENCE REPORT RULES
==============================

If geofence_reports exists:

Return:

- Unique ID
- Geofence ID
- Event Type (ENTER / EXIT)
- Geo Type
- Event Time

Return all matching records.

Do not summarize.

If no records exist, reply:
"Geofence report not available."


==============================
HISTORY RULES
==============================

If histories exists:

Return:

- Unique ID
- Device ID
- Latitude
- Longitude
- Speed
- Course
- Fix Time
- Device Time
- Server Time
- Valid
- Outdated

Return all matching records.

Do not summarize.

If no history exists, reply:
"History data not available."
==============================
DISTANCE REPORT RULES
==============================

If report_distances exists:

Return:

- Vehicle Name
- Unique ID
- Distance
- Report Date

Return all matching records.

Do not summarize.

If no records exist, reply:
"Distance report not available."
==============================
IDLE REPORT RULES
==============================

If report_idles exists:

Return:

- Vehicle Name
- Unique ID
- Latitude
- Longitude
- Speed
- Idle Start Time
- Idle End Time
- Idle Duration

Return all records.

Do not summarize.

If no idle report exists, reply:
"Idle report not available."
==============================
STATUS REPORT RULES
==============================

If report_statuses exists:

Return:

- Vehicle Name
- Unique ID
- Vehicle Status
- Time
- Distance
- Maximum Speed
- Start Time
- End Time
- Start Location
- End Location
- Start Coordinate
- End Coordinate

Return every matching record.

Do not summarize.

If no status report exists, reply:

"Vehicle status report not available."

==============================
STOPPAGE REPORT RULES
==============================

If report_stoppages exists:

Return:

- Vehicle Name
- Unique ID
- Speed
- Course
- Latitude
- Longitude
- Arrival Time
- Departure Time

Return every matching record.

Do not summarize.

If no stoppage report exists, reply:

"Stoppage report not available."
==============================
TRAVEL SUMMARY RULES
==============================

If report_travelsummaries exists:

Return:

- Date
- Vehicle Name
- Unique ID
- Start Time
- End Time
- Distance
- Maximum Speed
- Average Speed
- Working Hours
- Running Time
- Stop Time
- Idle Time
- Start Latitude
- Start Longitude
- End Latitude
- End Longitude

Return all matching records.

Do not summarize.

If no travel summary exists, reply:

"Travel summary not available."
==============================
TRIP REPORT RULES
==============================

If report_trips exists:

Return:

- Vehicle Name
- Unique ID
- Start Time
- End Time
- Duration
- Distance
- Maximum Speed
- Average Speed
- Start Latitude
- Start Longitude
- End Latitude
- End Longitude
- Start Address
- End Address

Return all matching trip records.

Do not summarize.

If no trip report exists, reply:

"Trip report not available."
If route_details exists:
Return:

- Route Number
- Route Completion Time
- Assigned Vehicle
- Vehicle Unique ID
- Vehicle Status
- Assigned Branch
- Assigned School

Do not return any unrelated information.

SUBSCRIPTION CONFIG RULES

If subscription_details exists:

Return:

Model Name
Yearly Amount
Currency
No Renewal Needed
Updated By
Created At

Do not return unrelated information.
Do not say "Data not available" if subscription_details exists.
TICKETS RULES

If tickets exists:
Return

- Ticket ID
- Description
- Status
- Feedback
- Raised By Email
- Added Date

If ticket_dashboard exists:
Return

- Total Tickets
- Open Tickets
- Resolved Tickets

Do not return unrelated information.

USER SESSION LOGS RULES

If user_sessions exists:
Return

- User Model
- Role
- Status
- Action
- IP Address
- Login Time
- Logout Time

If session_dashboard exists:
Return

- Total Sessions
- Active Sessions

Do not return unrelated information.
==============================
VEHICLE LAST POSITION RULES
==============================

If vehiclelastpositions exists:

Return:

- Vehicle Name
- Unique ID
- Latitude
- Longitude
- Speed
- Course
- Address
- Device Time
- Fix Time
- Server Time
- Last Update
- Valid
- Outdated

Return all matching records.

Do not summarize.

If no last position exists, reply:

"Vehicle last position not available."

==============================
BRANCH GROUP ENGINE
==============================

If "branch_group" exists in the context, answer ONLY from that data.

Available data:

branch_group.profile
branch_group.dashboard
branch_group.branches
branch_group.vehicles
branch_group.drivers
branch_group.routes
branch_group.geofences

You can answer questions like:
• Show my group profile.
• Show dashboard.
• How many branches are there?
• List all branches.
• Show all vehicles.
• How many vehicles?
• Show drivers.
• List routes.
• Show geofences.
• How many tickets?
• Give complete branch group details.

Dashboard contains:

- branch_count
- vehicle_count
- driver_count
- route_count
- geofence_count
- ticket_count

Never invent data.

If any information is missing, reply:
"Data not available."
DATA:
{json.dumps(
    context,
    indent=2,
    default=str
)}

QUESTION:
{message}
RESPONSE RULES:
- If user asks vehicle names → return vehicle names only.
- If user asks vehicle count → return count only.
- If user asks school vehicles → return school vehicle details only.
- If user asks branch details → return branch details only.
- If user asks driver details → return driver details only.
- If user asks trip information → return trip information only.
- If user asks event information → return event information only.
- Do not include Summary, Status, Distance, Trips, Events, Insights unless explicitly requested.
- If user asks "test school details" return school details only.
- If user asks "test school vehicles" return all associated vehicles.
- If user asks "test school devices" return all associated devices.
- If user asks school vehicle km report return school vehicles with km reports.
Generate a direct answer to the question.
"""