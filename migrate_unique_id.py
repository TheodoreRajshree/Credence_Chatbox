from mongodb import db


collections = [
    "report_stopages",
    "report_distances",
    "report_trips",
    "report_idles",
    "report_statuses",
    "report_travelsummaries",
    "vehiclelastpositions"
]


for collection_name in collections:

    collection = db[collection_name]

    print("Migrating:", collection_name)

    for doc in collection.find():

        uid = doc.get("uniqueId")

        if uid is not None:

            collection.update_one(
                {
                    "_id": doc["_id"]
                },
                {
                    "$set": {
                        "uniqueId": str(uid)
                    }
                }
            )

print("Migration completed")