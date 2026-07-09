# config/device_relationship_map.py

DEVICE_RELATIONSHIP_MAP = {

    # Primary Key of devices collection
    "devicePrimaryKey": "_id",

    # Device Unique Identifier
    "uniqueIdField": "uniqueId",

    # Collections linked using Device.uniqueId
    "uniqueIdCollections": {

        "allevents": "uniqueId",

        "histories": "uniqueId",

        "vehiclelastpositions": "uniqueId",

        "daily_vehicle_distance_caches": "uniqueId",

        "geofencereports": "uniqueId",

        "report_distances": "uniqueId",

        "report_idles": "uniqueId",

        "report_statuses": "uniqueId",

        "report_stopages": "uniqueId",
        

        "report_travelsummaries": "uniqueId",

        "report_trips": "uniqueId"
    },

    # Collections linked using devices.deviceId
    "deviceIdCollections": {

        "devicesubscriptions": "deviceId"
    },

    # Collections linked using devices._id
    "deviceObjIdCollections": {

        "devicesubscriptionhistories": "deviceObjId"
    }
}