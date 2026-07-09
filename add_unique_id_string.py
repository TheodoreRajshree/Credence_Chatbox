from mongodb import db


collections = [
    "report_stopages",
    "report_distances",
    "report_trips",
    "report_idles",
    "report_statuses",
    "report_travelsummaries",
    "geofencereports",
    "vehiclelastpositions"
]
for collection_name in collections:

    collection = db[collection_name]

    print("Updating:", collection_name)

    cursor = collection.find({
        "uniqueId": {
            "$exists": True
        }
    })


    for doc in cursor:

        uid = doc.get("uniqueId")

        if uid is not None:

            collection.update_one(
                {
                    "_id": doc["_id"]
                },
                {
                    "$set":{
                        "uniqueIdString": str(uid)
                    }
                }
            )


print("Completed")