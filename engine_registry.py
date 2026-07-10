# engine_registry.py


from all_events_engine import AllEventsEngine
from branch_device_engine import BranchDeviceEngine
from branch_engine import BranchEngine
from branch_group_engine import BranchGroupEngine
from device_engine import DeviceEngine
from Device_Subscription_Engine import DeviceSubscriptionEngine
from Device_SubscriptionHistory_Engine import DeviceSubscriptionHistoryEngine
from geofence_report_engine import GeofenceReportEngine
from geofences_engine import GeofencesEngine
from histories_engine import HistoriesEngine
from report_distance_engine import ReportDistanceEngine
from report_engine import ReportEngine
from report_idle_engine import ReportIdleEngine
from report_status_engine import ReportStatusEngine
from report_stoppage_engine import ReportStoppageEngine
from report_travel_summary_engine import ReportTravelSummaryEngine
from report_trip_engine import ReportTripEngine
from route_engine import RouteEngine
from school_device_engine import SchoolDeviceEngine
from school_engine import SchoolEngine
from subscription_config_engine import SubscriptionConfigEngine
from tickets_engine import TicketsEngine
from usersessionlogs_engine import UserSessionLogsEngine
from vehicle_km_engine import VehicleKmEngine
from vehiclelastposition_engine import VehicleLastPositionEngine
from rbac import get_rbac_filter
from mongodb import db
import functools
from daily_distance_cache_engine import DailyDistanceCacheEngine
import superadmin
# ==========================
# ENGINE OBJECTS
# ==========================

all_events_engine = AllEventsEngine(db)

branch_device_engine = BranchDeviceEngine(db)

branch_engine = BranchEngine(db)

branch_group_engine = BranchGroupEngine(db)

device_engine = DeviceEngine(db)

subscription_engine = DeviceSubscriptionEngine(db)

subscription_history_engine = DeviceSubscriptionHistoryEngine(db)

geofence_report_engine = GeofenceReportEngine(db)
geofences_engine = GeofencesEngine(db)
histories_engine = HistoriesEngine(db)
report_distance_engine = ReportDistanceEngine(db)
report_engine = ReportEngine(db)
report_idle_engine = ReportIdleEngine(db)
report_status_engine = ReportStatusEngine(db)
report_stoppage_engine = ReportStoppageEngine(db)
report_travel_summary_engine = ReportTravelSummaryEngine(db)
report_trip_engine = ReportTripEngine(db)
route_engine = RouteEngine(db)
school_device_engine = SchoolDeviceEngine(db)
school_engine = SchoolEngine(db)
subscription_config_engine = SubscriptionConfigEngine(db)
tickets_engine = TicketsEngine(db)
user_session_logs_engine = UserSessionLogsEngine(db)
vehicle_km_engine = VehicleKmEngine(db)
vehicle_last_position_engine = VehicleLastPositionEngine(db)
daily_distance_cache_engine = DailyDistanceCacheEngine(db)

# ==========================
# FUNCTION MAP
# ==========================



def wrap_engine(method):

    @functools.wraps(method)
    def wrapper(*args, **kwargs):

        return method(*args, **kwargs)

    return wrapper
ENGINE_REGISTRY = {



# =====================
# ALL EVENTS
# =====================

"get_vehicle_events":
    all_events_engine.get_vehicle_events,


"get_school_events":
    all_events_engine.get_school_events,


"get_branch_events":
    all_events_engine.get_branch_events,


"get_driver_events":
    all_events_engine.get_driver_events,


"get_all_events":
    all_events_engine.get_all_events,


"get_event_count_by_vehicle":
    all_events_engine.get_event_count_by_vehicle,


"get_event_summary":
    all_events_engine.get_event_summary,





# =====================
# BRANCH DEVICE
# =====================

"find_branch":
    branch_device_engine.find_branch,


"get_branch_with_vehicles":
    branch_device_engine.get_branch_with_vehicles,


"get_branch_dashboard_by_name":
    branch_device_engine.get_branch_dashboard,


"get_branch_devices":
    branch_device_engine.get_branch_devices,

"get_branch_single_vehicle":
    branch_device_engine.get_branch_single_vehicle,

"get_single_branch_vehicle_status":
    branch_device_engine.get_single_branch_vehicle_status,

"get_specific_vehicle_distance_report":
branch_device_engine.get_specific_vehicle_distance_report,
"get_specific_vehicle_travel_summary":
branch_device_engine.get_specific_vehicle_travel_summary,
"get_specific_vehicle_idle_report":
branch_device_engine.get_specific_vehicle_idle_report,
"get_specific_vehicle_last_position":
branch_device_engine.get_specific_vehicle_last_position,
"get_specific_branch_geofence":
branch_device_engine.get_specific_branch_geofence,
"get_branch_daily_distance":
daily_distance_cache_engine.get_branch_daily_distance,
"get_specific_vehicle_daily_distance":
branch_device_engine.get_specific_vehicle_daily_distance,
# "get_branch_vehicle_km_report":
# branch_engine.get_branch_vehicle_km_report,


"get_school_single_vehicle":
school_engine.get_school_single_vehicle,
"get_single_school_vehicle_status":
school_engine.get_single_school_vehicle_status,
"get_specific_school_vehicle_distance_report":
school_engine.get_specific_school_vehicle_distance_report,
"get_driver_daily_distance":
daily_distance_cache_engine.get_driver_daily_distance,
"get_branch_single_vehicle_km_report":
branch_device_engine.get_branch_single_vehicle_km_report,
# "get_branch_vehicle_km_report":
# branch_engine.get_branch_vehicle_km_report,
"get_branch_distance_report_per_day":
branch_engine.get_branch_distance_report_per_day,
"get_branch_vehicle_km_report":
branch_engine.get_branch_vehicle_km_report,
"calculate_week_month_distance":
branch_device_engine.calculate_week_month_distance,
"get_branch_today_accurate_distance":
branch_device_engine.get_branch_today_accurate_distance,
"get_school_single_vehicle_km_report":
school_engine.get_school_single_vehicle_km_report,
"get_school_today_accurate_distance":
school_engine.get_school_today_accurate_distance,
"get_school_with_vehicles_final_for_devices":
school_engine.get_school_with_vehicles_final_for_devices,

"get_school_single_branch":
school_device_engine.get_school_single_branch,
"get_device_details":
device_engine.get_device_details,
"get_superadmin_vehicle_details":
device_engine.get_superadmin_vehicle_details,
"find_school_superadmin":
school_engine.find_school_superadmin,
"find_specific_school_superadmin":
school_engine.find_specific_school_superadmin,
"find_specific_branch_superadmin":
branch_engine.find_specific_branch_superadmin,
"find_branch_superadmin":
branch_engine.find_branch_superadmin,
"get_superadmin_single_vehicle_km_report":
branch_device_engine.get_superadmin_single_vehicle_km_report,
"get_assigned_branches":
branch_group_engine.get_assigned_branches,
"get_specific_branch_by_name":
branch_group_engine.get_specific_branch_by_name,
"get_assigned_school_super":
branch_group_engine.get_assigned_school_super,
"get_branchgroup_devices":
branch_group_engine.get_branchgroup_devices,
"get_branchgroup_vehicle_school_branch":
branch_group_engine.get_branchgroup_vehicle_school_branch,
"get_branchgroup_vehicle_today_distance":
branch_group_engine.get_branchgroup_vehicle_today_distance,
"get_branchgroup_geofences":
    branch_group_engine.get_branchgroup_geofences,
    "get_branchgroup_travel_summary":
    branch_group_engine.get_branchgroup_travel_summary,
    "get_branchgroup_vehicle_status_report":
    branch_group_engine.get_branchgroup_vehicle_status_report,
    
        "get_branchgroup_vehicle_last_positions":
    branch_group_engine.get_branchgroup_vehicle_last_positions,
    "get_branchgroup_routes":
    branch_group_engine.get_branchgroup_routes,
    "get_device_geofence_superadmin":
    geofences_engine.get_device_geofence_superadmin,
    "get_specific_vehicle_branch_geofences":
    geofences_engine.get_specific_vehicle_branch_geofences,
    "get_school_user_branch_geofences":
    geofences_engine.get_school_user_branch_geofences,
    "get_specific_vehicle_branch_of_school_geofences":
    geofences_engine.get_specific_vehicle_branch_of_school_geofences,
    "get_branchgroup_specific_branch_geofences":
    branch_group_engine.get_branchgroup_specific_branch_geofences,
    "get_branch_group_profile_only":
    branch_group_engine.get_branch_group_profile_only,
    "get_branchgroup_specific_branch":
    branch_group_engine.get_branchgroup_specific_branch,
    "get_assigned_school_branchgroup":
    branch_group_engine.get_assigned_school_branchgroup,
    "get_branchgroup_specific_branch_vehicles":
    branch_group_engine.get_branchgroup_specific_branch_vehicles,
    "get_branchgroup_school_vehicle":
    branch_group_engine.get_branchgroup_school_vehicle,
    "get_branchgroup_specific_vehicle":
    branch_group_engine.get_branchgroup_specific_vehicle,
    "get_branchgroup_specific_vehicle_geofence":
    branch_group_engine.get_branchgroup_specific_vehicle_geofence,
    "get_branchgroup_specific_branch_vehicle_geofence":
    branch_group_engine.get_branchgroup_specific_branch_vehicle_geofence,
    "get_branchgroup_school_vehicle_geofence":
    branch_group_engine.get_branchgroup_school_vehicle_geofence,
    "get_branchgroup_specific_branch_vehicle_today_distance":
    branch_group_engine.get_branchgroup_specific_branch_vehicle_today_distance,
    "get_branchgroup_vehicle_today_distance":
branch_group_engine.get_branchgroup_vehicle_today_distance,
"get_branchgroup_specific_branch_vehicle_km_report":
    branch_group_engine.get_branchgroup_specific_branch_vehicle_km_report,
     "get_branchgroup_vehicle_km_report":
    branch_group_engine.get_branchgroup_vehicle_km_report,
    "get_branchgroup_specific_branch_vehicle_distance_report":
branch_group_engine.get_branchgroup_specific_branch_vehicle_distance_report,
"get_branchgroup_specific_branch_vehicles_g":
branch_group_engine.get_branchgroup_specific_branch_vehicles_g,
"get_branchgroup_specific_branch_vehicle_status":
    branch_group_engine.get_branchgroup_specific_branch_vehicle_status,
    "get_branchgroup_specific_branch_vehicle_distance_report":
    branch_group_engine.get_branchgroup_specific_branch_vehicle_distance_report,
    "get_branchgroup_specific_branch_vehicle_last_position":
    branch_group_engine.get_branchgroup_specific_branch_vehicle_last_position,
# =====================
# BRANCH
# =====================

"get_branch_profile":
    branch_engine.get_branch_profile,


"get_branch_vehicles":
    branch_engine.get_branch_vehicles,


"get_branch_vehicle_count":
    branch_engine.get_branch_vehicle_count,


"get_branch_drivers":
    branch_engine.get_branch_drivers,


"get_branch_driver_count":
    branch_engine.get_branch_driver_count,


"get_branch_routes":
    branch_device_engine.get_route_branch,


"get_branch_geofences":
    branch_engine.get_branch_geofences,


"get_branch_tickets":
    branch_engine.get_branch_tickets,


"get_branch_dashboard":
    branch_engine.get_branch_dashboard,


"get_branch_details":
    branch_engine.get_branch_details,

"get_branch_status_report":
branch_device_engine.get_branch_status_report,
"get_school_single_vehicle_km_report":
school_engine.get_school_single_vehicle_km_report,
# "get_vehicle_km_custom_report":
# branch_device_engine.get_vehicle_km_custom_report,
"get_branch_distance_report_per_day":
branch_engine.get_branch_distance_report_per_day,


# =====================
# BRANCH GROUP
# =====================


"get_branch_group_profile":
branch_group_engine.get_branch_group_profile,

# "get_group_branches":
#     branch_group_engine.get_group_branches,


# "get_group_branch_count":
#     branch_group_engine.get_group_branch_count,


# "get_group_vehicles":
#     branch_group_engine.get_group_vehicles,


# "get_group_vehicle_count":
#     branch_group_engine.get_group_vehicle_count,


# "get_group_drivers":
#     branch_group_engine.get_group_drivers,


# "get_group_driver_count":
#     branch_group_engine.get_group_driver_count,


# "get_group_routes":
#     branch_group_engine.get_group_routes,


# "get_group_geofences":
#     branch_group_engine.get_group_geofences,


# "get_group_tickets":
#     branch_group_engine.get_group_tickets,


# "get_group_dashboard":
#     branch_group_engine.get_group_dashboard,


# "get_group_details":
#     branch_group_engine.get_group_details,





# =====================
# DEVICE
# =====================

"find_device":
    device_engine.find_device,


"get_device_details":
    device_engine.get_device_details,


"get_all_devices":
    device_engine.get_all_devices,


"get_school_devices":
    device_engine.get_school_devices,


"get_branch_devices":
    device_engine.get_branch_devices,


"get_driver_device":
    device_engine.get_driver_device,


"get_last_position":
    device_engine.get_last_position,


"get_device_summary":
    device_engine.get_device_summary,





# =====================
# DEVICE SUBSCRIPTION
# =====================

"get_device_subscription":
    subscription_engine.get_device_subscription,


"get_allowed_devices":
    subscription_engine.get_allowed_devices,


"get_school_subscriptions":
    subscription_engine.get_school_subscriptions,


"get_branch_subscriptions":
    subscription_engine.get_branch_subscriptions,


"get_driver_subscription":
    subscription_engine.get_driver_subscription,


"get_all_subscriptions":
    subscription_engine.get_all_subscriptions,


"get_subscription_count":
    subscription_engine.get_subscription_count,


"get_paid_subscriptions":
    subscription_engine.get_paid_subscriptions,


"get_expired_subscriptions":
    subscription_engine.get_expired_subscriptions,





# =====================
# DEVICE SUBSCRIPTION HISTORY
# =====================

"get_device_subscription_history":
    subscription_history_engine.get_device_subscription_history,


"get_school_subscription_history":
    subscription_history_engine.get_school_subscription_history,


"get_branch_subscription_history":
    subscription_history_engine.get_branch_subscription_history,


"get_driver_subscription_history":
    subscription_history_engine.get_driver_subscription_history,


"get_all_subscription_history":
    subscription_history_engine.get_all_subscription_history,


"get_history_count":
    subscription_history_engine.get_history_count,


"get_latest_subscription":
    subscription_history_engine.get_latest_subscription,

# =====================
# GEOFENCE REPORT
# =====================

"get_vehicle_geofence_reports":

    geofence_report_engine.get_vehicle_geofence_reports,


"get_school_geofence_reports":

    geofence_report_engine.get_school_geofence_reports,


"get_branch_geofence_reports":

    geofence_report_engine.get_branch_geofence_reports,


"get_driver_geofence_reports":

    geofence_report_engine.get_driver_geofence_report,


"get_all_geofence_reports":

    geofence_report_engine.get_all_geofence_reports,





# "get_geofence_event_summary":

#     geofence_report_engine.get_event_summary,


# =====================
# GEOFENCES
# =====================

"get_geofence":

    geofences_engine.get_geofence,


"get_school_geofences":

    geofences_engine.get_school_geofences,


"get_branch_geofences":

    geofences_engine.get_branch_geofences,


"get_driver_geofences":

    geofences_engine.get_driver_geofences,


"get_all_geofences":

    geofences_engine.get_all_geofences,


"get_geofence_count":

    geofences_engine.get_geofence_count,


"search_geofence":

    geofences_engine.search_geofence,


"get_route_geofences":

    geofences_engine.get_route_geofences,

    # =====================
# HISTORIES
# =====================

"get_vehicle_history":

    histories_engine.get_vehicle_history,


"get_school_history":

    histories_engine.get_school_history,


"get_branch_history":

    histories_engine.get_branch_history,


"get_driver_history":

    histories_engine.get_driver_history,


"get_all_history":

    histories_engine.get_all_history,


"get_history_count":

    histories_engine.get_history_count,


"get_latest_history":

    histories_engine.get_latest_history,
    # =====================
# REPORT DISTANCE
# =====================

"get_vehicle_distance_report":

    report_distance_engine.get_vehicle_distance_report,


"get_school_distance_report":

    report_distance_engine.get_school_distance_report,


"get_branch_distance_report":

    report_distance_engine.get_branch_distance_report,


"get_driver_distance_report":

    report_distance_engine.get_driver_distance_report,


"get_all_distance_reports":

    report_distance_engine.get_all_distance_reports,


"get_distance_report_count":

    report_distance_engine.get_report_count,


"get_total_distance":

    report_distance_engine.get_total_distance,

    # =====================
# REPORT ENGINE
# =====================

"report_latest":

    report_engine.latest,


"get_device_report":

    report_engine.get_device,


"get_last_position_report":

    report_engine.get_last_position,


"get_distance_report":

    report_engine.get_distance_report,


"get_trip_report":

    report_engine.get_trip_report,


"get_idle_report":

    report_engine.get_idle_report,


"get_stoppage_report":

    report_engine.get_stoppage_report,


"get_travel_summary":

    report_engine.get_travel_summary,


"get_subscription_report":

    report_engine.get_subscription,


"get_daily_distance":

    report_engine.get_daily_distance,


"get_driver_report":

    report_engine.get_driver_report,
    # =====================
# REPORT IDLE
# =====================

"get_vehicle_idle_report":
    report_idle_engine.get_vehicle_idle_report,


"get_school_idle_report":
    report_idle_engine.get_school_idle_report,


"get_branch_idle_report":
    report_idle_engine.get_branch_idle_report,


"get_driver_idle_report":
    report_idle_engine.get_driver_idle_report,


"get_all_idle_reports":
    report_idle_engine.get_all_idle_reports,


"get_idle_count":
    report_idle_engine.get_idle_count,
    # =====================
# REPORT STATUS
# =====================

"get_vehicle_status_report":
    report_status_engine.get_vehicle_status_report,


"get_school_status_report":
    report_status_engine.get_school_status_report,


"get_branch_status_report":
    branch_engine.get_branch_status_report,


"get_driver_status_report":
    report_status_engine.get_driver_status_report,


"get_all_status_reports":
    report_status_engine.get_all_status_reports,


"get_status_count":
    report_status_engine.get_status_count,
    # =====================
# REPORT STOPPAGE
# =====================

"get_vehicle_stoppage_report":
    report_stoppage_engine.get_vehicle_stoppage_report,


"get_school_stoppage_report":
    report_stoppage_engine.get_school_stoppage_report,


"get_branch_stoppage_report":
    report_stoppage_engine.get_branch_stoppage_report,


"get_driver_stoppage_report":
    report_stoppage_engine.get_driver_stoppage_report,


"get_all_stoppage_reports":
    report_stoppage_engine.get_all_stoppage_reports,


"get_stoppage_count":
    report_stoppage_engine.get_stoppage_count,


    # =====================
# REPORT TRAVEL SUMMARY
# =====================

"get_vehicle_travel_summary":
    report_travel_summary_engine.get_vehicle_travel_summary,


"get_school_travel_summary":
    report_travel_summary_engine.get_school_travel_summary,


"get_branch_travel_summary":
    report_travel_summary_engine.get_branch_travel_summary,


"get_driver_travel_summary":
    report_travel_summary_engine.get_driver_travel_summary,


"get_all_travel_summaries":
    report_travel_summary_engine.get_all_travel_summaries,


"get_summary_count":
    report_travel_summary_engine.get_summary_count,

    # =====================
# REPORT TRIP
# =====================

"get_vehicle_trips":
    report_trip_engine.get_vehicle_trips,


"get_school_trips":
    report_trip_engine.get_school_trips,


"get_branch_trips":
    report_trip_engine.get_branch_trips,


"get_driver_trips":
    report_trip_engine.get_driver_trips,


"get_all_trips":
    report_trip_engine.get_all_trips,


"get_trip_count":
    report_trip_engine.get_trip_count,
    # =====================
# ROUTE
# =====================

"get_route":

    route_engine.get_route,


"get_route_profile":

    route_engine.get_route_profile,


"get_route_device":

    route_engine.get_route_device,


"get_route_branch":

    branch_device_engine.get_route_branch,

"get_route_branch_specific_vehicle":
branch_device_engine.get_route_branch_specific_vehicle,
"get_route_school_specific_vehicle":
school_engine.get_route_school_specific_vehicle,
"get_route_school":

    route_engine.get_route_school,
    


" get_route_school":

    route_engine.get_route_school,


"find_route":

    route_engine.find_route,


"get_route_count":

    route_engine.get_route_count,
    # =====================
# SCHOOL DEVICE
# =====================

"find_school":

    school_device_engine.find_school,


"get_school_with_vehicles":

    school_device_engine.get_school_with_vehicles,


"get_school_devices":

    school_device_engine.get_school_devices,


"get_school_device_summary":

    school_device_engine.get_school_device_summary,


"get_school_dashboard":

    school_device_engine.get_school_dashboard,

    # =====================
# SCHOOL
# =====================

"get_school_profile":

    school_engine.get_school_profile,


"get_school_vehicles":

    school_engine.get_school_vehicles,


"get_school_vehicle_count":

    school_engine.get_school_vehicle_count,


"get_school_drivers":

    school_engine.get_school_drivers,


"get_school_driver_count":

    school_engine.get_school_driver_count,


"get_school_route":

    route_engine.get_route_school,


"get_school_geofences":

    geofences_engine.get_school_geofences,

"get_school_geofence_report":
geofence_report_engine.get_school_geofence_reports,
     
"get_school_tickets":

    school_engine.get_school_tickets,


"get_school_subscriptions":

    school_engine.get_school_subscriptions,


"get_school_dashboard":

    school_engine.get_school_dashboard,
    "get_school_km_report":
    school_engine.get_school_km_report,
    "get_school_distance_report":
    report_distance_engine.get_school_distance_report,
    "get_school_daily_distance":
    daily_distance_cache_engine.get_school_daily_distance,
    "get_specific_school_vehicle_distance_report":
    school_engine.get_specific_school_vehicle_distance_report,
    "get_specific_vehicle_travel_summary":
    school_engine.get_specific_vehicle_travel_summary,
    "get_specific_vehicle_idle_report":
    school_engine.get_specific_vehicle_idle_report,
    "get_specific_vehicle_last_position":
    school_engine.get_specific_vehicle_last_position,
    "get_school_specific_geofence":
    school_engine.get_school_specific_geofence,
    "get_specific_vehicle_daily_distance":
    school_engine.get_specific_vehicle_daily_distance,
    # =====================
# SUBSCRIPTION CONFIG
# =====================

"get_subscription_by_model":

    subscription_config_engine.get_subscription_by_model,


"get_all_subscription_configs":

    subscription_config_engine.get_all_subscription_configs,


"get_subscription_count":

    subscription_config_engine.get_subscription_count,


"get_subscription_dashboard":

    subscription_config_engine.get_dashboard,


"search_subscription":

    subscription_config_engine.search_subscription,
# =====================
# TICKETS
# =====================


"get_ticket":
    tickets_engine.get_ticket,


"get_all_tickets":
    tickets_engine.get_all_tickets,


"get_school_tickets":
    tickets_engine.get_school_tickets,


"get_branch_tickets":
    tickets_engine.get_branch_tickets,


"get_tickets_by_status":
    tickets_engine.get_tickets_by_status,


"get_total_ticket_count":
    tickets_engine.get_total_ticket_count,


"get_open_ticket_count":
    tickets_engine.get_open_ticket_count,


"get_resolved_ticket_count":
    tickets_engine.get_resolved_ticket_count,


"get_ticket_dashboard":
    tickets_engine.get_ticket_dashboard,
    # =====================
# USER SESSION LOGS
# =====================


"get_session":
    user_session_logs_engine.get_session,


"get_all_sessions":
    user_session_logs_engine.get_all_sessions,


"get_user_sessions":
    user_session_logs_engine.get_user_sessions,


"get_active_sessions":
    user_session_logs_engine.get_active_sessions,


"get_role_sessions":
    user_session_logs_engine.get_role_sessions,


"get_total_session_count":
    user_session_logs_engine.get_total_session_count,


"get_active_session_count":
    user_session_logs_engine.get_active_session_count,


"get_session_dashboard":
    user_session_logs_engine.get_dashboard,
# =====================
# VEHICLE KM
# =====================


"get_allowed_device":
    vehicle_km_engine.get_allowed_device,


"resolve_date":
    vehicle_km_engine.resolve_date,


"get_km_report":
    vehicle_km_engine.get_km_report,
    # =====================
# VEHICLE LAST POSITION
# =====================


"get_position_filter":
    vehicle_last_position_engine.get_position_filter,


"get_vehicle_last_position":
    vehicle_last_position_engine.get_vehicle_last_position,


"get_all_last_positions":
    vehicle_last_position_engine.get_all_last_positions,


"get_active_vehicles":
    vehicle_last_position_engine.get_active_vehicles,


"get_stopped_vehicles":
    vehicle_last_position_engine.get_stopped_vehicles,


"get_total_vehicle_count":
    vehicle_last_position_engine.get_total_vehicle_count,


"get_active_vehicle_count":
    vehicle_last_position_engine.get_active_vehicle_count,


"get_stopped_vehicle_count":
    vehicle_last_position_engine.get_stopped_vehicle_count,


"get_dashboard":
    vehicle_last_position_engine.get_dashboard,
    
}




# ==========================
# AUTO WRAP ALL ENGINES
# ==========================

for name, method in ENGINE_REGISTRY.items():

    ENGINE_REGISTRY[name] = wrap_engine(method)



print("ENGINE LOAD SUCCESS")
print(len(ENGINE_REGISTRY))