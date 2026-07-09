# intent_detector.py


INTENT_MAP = {

"allevents": [

    "event",
    "events",
    "all events",
    "show events",
    "recent events",
    "latest events",
    "alerts",
    "ignition",
    "ignition on",
    "ignition off",
    "overspeed",
    "sos",
    "alarm",
    "panic",
    "last event",
    "vehicle event",
    "branch events",
    "school events"

],
"geofences":[

    "geofence",
    "geofences",
    "geofence details",
    "geofence list",
    "fence",
    "fences",
    "location fence",
    "geo fence"

],
"geofencereports":[
    "geofence report",
    "geofence reports",
    "geofence event",
    "geofence events",
    "enter geofence",
    "exit geofence",
    "entered geofence",
    "left geofence",
    "geo report",
    "geo events"
],
"school_vehicles": [

    "all vehicle",
    "all vehicles",
    "vehicle name",
    "vehicle names",
    "vehcile",
    "vehicke",
    "vehicle list",
    "bus list"

],


    "attendances": [

        "attendance",
        "present",
        "absent"

    ],



    "branches": [

    "branch",
    "branch details",
    "branch info",
    "branch vehicle",
    "branch vehicles",
    "branch all vehicle"

],
"devicesubscriptions":[
    "subscription",
    "subscriptions",
    "payment",
    "renewal",
    "expiry",
    "paid",
    "subscription status",
    "subscription details"
],

    "categories": [

        "category",
        "vehicle category"
        "device category"

    ],
    "branch_groups": [
    "branch group",
    "branch groups",
    "group",
    "groups",
    "group details",
    "group info",
    "group dashboard",
    "group vehicles",
    "group drivers",
    "group routes",
    "group geofences",
    "group tickets",
    "branch group details",
    "branch group vehicles",
    "branch group drivers",
    "branchgroup",
    "branchgroups",
    "branch group dashboard",
    "branch group summary"
    "branchgroup summary"

],
"devicesubscriptionhistories":[

    "subscription history",
    "subscription",
    "renewal",
    "renew",
    "expiry history",
    "subscription logs",
    "subscription details",
    "history"

],
    "chats": [

        "chat",
        "conversation"

    ],



    "messages": [

        "message",
        "messages"

    ],



    "children": [

        "child",
        "student",
        "children"

    ],



    "contacts": [

        "contact",
        "phone",
        "mobile",
        "email"

    ],



    "daily_vehicle_distance_caches": [

        "total km",
        "distance",
        "odometer",
        "overall km",
        "running km"

    ],



    "devices": [

    "vehicle",
    "vehicles",

    "vehcile",
    "vehciles",
    "vehical",
    "vehicals",
    "vechile",

    "device",
    "devices",

    "gps",
    "tracker",

    "car",
    "bus",
    "truck",
    "bike",
    "van",

    "vehicle name",
    "vehicle names",
    "vehicle list",

    "all vehicle",
    "all vehicles",

    "vehicle details",

    "sim",
    "model",

    "unique id",
    "uniqueid"

],
"device_location":[

    "location",
    "live location",
    "current location",
    "where is vehicle",
    "last position"

],

"device_trip":[

    "trip",
    "trip report"

],

"device_idle":[

    "idle",
    "idle report"

],

"device_distance":[

    "distance",
    "today km",
    "daily km"

],

"device_summary":[

    "summary",
    "travel summary",
    "analytics"

],



    "school_vehicles": [

        "school vehicle",
        "school vehicles",
        "school bus",
        "school buses",

        "school all vehicle",
        "all school vehicle",
        "all school vehicles",

        "vehicle under school",
        "vehicles under school",

        "school vehicle name",
        "school vehicle list"

    ],



    "devicesubscriptions": [

        "subscription",
        "expiry",
        "renew",
        "payment"

    ],



    "devicesubscriptionhistories": [

        "subscription history",
        "renewal history"

    ],



    "drivers": [

        "driver",
        "drivers",
        "driver details",
        "driver info"

    ],



    "geofencereports": [

        "geofence report",
        "enter geofence",
        "exit geofence"

    ],



    "geofences": [

        "geofence",
        "zone",
        "fence"

    ],



    "histories": [

        "history",
        "travel history",
        "vehicle history"

    ],
    


    "models": [

        "model",
        "device model"

    ],



    "report_distances": [

        "distance",
        "today km",
        "daily km",
        "monthly km"

    ],



    "report_idles": [

        "idle",
        "idle time"

    ],



    "report_statuses": [

        "status",
        "vehicle status",
        "ignition status"

    ],



    "report_stopages": [

        "stop",
        "stoppage",
        "parking"

    ],



    "report_travelsummaries": [

        "travel summary",
        "avg speed",
        "max speed",
        "working hours"

    ],



    "report_trips": [

        "trip",
        "trip report",
        "journey"

    ],
"BRANCH_KEYWORDS" : [

    "branch",

    "branch details",

    "branch profile",

    "branch dashboard",

    "branch vehicles",

    "branch drivers",

    "branch routes",

    "branch geofences",

    "branch tickets"
],


    "routes": [

        "route",
        "route number"

    ],
    "school_devices": [
    "school devices",
    "school vehicles",
    "test school devices",
    "all school vehicles"
],



    "schools": [

        "school",
        "schools",
        "school name",
        "school details",
        "school info"

    ],



    "tickets": [

        "ticket",
        "complaint",
        "issue"

    ],



    "users": [

        "user",
        "account"

    ],
"histories":[
    "history",
    "vehicle history",
    "tracking history",
    "location history",
    "travel history",
    "gps history",
    "position history",
    "movement history"
],


    "usersessionlogs": [

        "login",
        "logout",
        "session"

    ],
    "school_dashboard":[
    "school dashboard",
    "dashboard"
],

"school_details":[
    "school details",
    "school info",
    "my school"
],
"report_idles": [

    "idle report",
    "idle",
    "idling",
    "idle vehicle",
    "vehicle idle",
    "idle time",
    "engine idle",
    "idle duration",
    "stopped engine"

],
"report_statuses": [

    "status report",
    "vehicle status",
    "ignition status",
    "running status",
    "vehicle report",
    "status history",
    "engine status",
    "ignition on",
    "ignition off",
    "status"

],
"report_travelsummaries": [

    "travel summary",
    "travel summaries",
    "travel report",
    "trip summary",
    "journey summary",
    "daily travel",
    "daily summary",
    "vehicle summary",
    "running summary",
    "travel details"

],
"report_trips":[

    "trip",
    "trips",
    "trip report",
    "journey",
    "journeys",
    "travel trip",
    "trip history",
    "vehicle trip",
    "trip details",
    "trip summary"

],
"report_stoppages": [

    "stoppage report",
    "stoppage",
    "stop report",
    "vehicle stop",
    "stopped vehicle",
    "parking report",
    "halt report",
    "arrival report",
    "departure report"

],
"school_vehicles":[
    "school vehicles",
    "school buses",
    "all vehicles"
],

    "school_drivers":[
    "school drivers",
    "all drivers"
],
"report_distances":[
    "distance report",
    "distance",
    "travel distance",
    "km report",
    "kilometer report",
    "vehicle distance",
    "distance travelled",
    "distance summary"
],


"vehiclelastpositions": [

    "last position",
    "current location",
    "vehicle location",
    "live location",
    "latest location",
    "last known location",
    "current position",
    "vehicle position",
    "last gps",
    "track vehicle"

],

}
     





# spelling correction

SPELL_CORRECTIONS = {


    "vehcile":"vehicle",
    "vehciles":"vehicles",

    "vehical":"vehicle",
    "vehicals":"vehicles",

    "vechile":"vehicle",

    "scholl":"school",
    "schoool":"school",

    "anme":"name",
    "nmae":"name"

}





def normalize_text(text):


    words = text.lower().split()


    fixed=[]


    for word in words:


        if word in SPELL_CORRECTIONS:

            fixed.append(
                SPELL_CORRECTIONS[word]
            )

        else:

            fixed.append(word)



    return " ".join(fixed)







def detect_intent(message):


    msg = normalize_text(message)


    matched=set()



    for collection, keywords in INTENT_MAP.items():


        for keyword in keywords:


            if keyword in msg:

                matched.add(collection)

                break





    # default

    if not matched:


        matched.update([

            "schools",
            "branches",
            "drivers",
            "devices"

        ])




    return list(matched)