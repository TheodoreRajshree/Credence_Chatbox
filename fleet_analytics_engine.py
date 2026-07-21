from bson import ObjectId
class FleetAnalyticsEngine:
    def __init__(self, db):
        self.db = db
    def get_vehicle_analytics(self, unique_id):
        analytics = {
            "uniqueId": unique_id
        }
        try:
            # ==========================
            # DEVICE INFO
            # ==========================
            device = self.db["devices"].find_one(
                {"uniqueId": str(unique_id)}
            )
            if device:
                analytics["device"] = {
                    "vehicleName": device.get("name"),
                    "status": device.get("status"),
                    "model": device.get("model"),
                    "category": device.get("category"),
                    "sim": device.get("sim"),
                    "installationDate": str(
                        device.get("installationdate")
                    ),
                    "expiryDate": str(
                        device.get("expirationdate")
                    ),
                    "totalKmOfDevice": device.get(
                        "TotalKmOfDevice"
                    )
                }
            # ==========================
            # LAST POSITION
            # ==========================
            position = self.db[
                "vehiclelastpositions"
            ].find_one(
                {"uniqueId": str(unique_id)}
            )
            if position:
                analytics["last_position"] = {
                    "latitude": position.get("latitude"),
                    "longitude": position.get("longitude"),
                    "speed": position.get("speed"),
                    "deviceTime": str(
                        position.get("deviceTime")
                    ),
                    "lastUpdate": str(
                        position.get("lastUpdate")
                    )
                }
            # ==========================
            # DISTANCE CACHE
            # ==========================

            distance = self.db[
                "daily_vehicle_distance_caches"
            ].find_one(
                {"uniqueId": str(unique_id)}
            )
            if distance:
                analytics["distance"] = {
                    "startOdo": distance.get(
                        "startOdo"
                    ),
                    "totalKm": distance.get(
                        "totalKm"
                    )
                }
            # ==========================
            # TRAVEL SUMMARY
            # ==========================
            travel = self.db[
                "report_travelsummaries"
            ].find_one(
                {"uniqueId": str(unique_id)},
                sort=[("createdAt", -1)]
            )
            if travel:
                analytics["travel_summary"] = {
                    "distance": travel.get(
                        "distance"
                    ),
                    "avgSpeed": travel.get(
                        "avgSpeed"
                    ),
                    "maxSpeed": travel.get(
                        "maxSpeed"
                    ),
                    "workingHours": travel.get(
                        "workingHours"
                    ),
                    "runningTime": travel.get(
                        "runningTime"
                    ),
                    "stopTime": travel.get(
                        "stopTime"
                    )
                }
            # ==========================
            # LATEST TRIP
            # ==========================
            trip = self.db[
                "report_trips"
            ].find_one(
                {"uniqueId": str(unique_id)},
                sort=[("startTime", -1)]
            )
            if trip:
                analytics["latest_trip"] = {
                    "distance": trip.get(
                        "distance"
                    ),
                    "duration": trip.get(
                        "duration"
                    ),
                    "startLatitude": trip.get(
                        "startLatitude"
                    ),
                    "startLongitude": trip.get(
                        "startLongitude"
                    ),
                    "endLatitude": trip.get(
                        "endLatitude"
                    ),
                    "endLongitude": trip.get(
                        "endLongitude"
                    )
                }
            # ==========================
            # VEHICLE STATUS
            # ==========================
            status = self.db[
                "report_statuses"
            ].find_one(
                {"uniqueId": str(unique_id)},
                sort=[("endDateTime", -1)]
            )
            if status:
                analytics["status"] = {
                    "vehicleStatus":
                        status.get(
                            "vehicleStatus"
                        ),
                    "time":
                        status.get("time")
                }
            # ==========================
            # IDLE REPORT
            # ==========================
            idle = self.db[
                "report_idles"
            ].find_one(
                {"uniqueId": str(unique_id)},
                sort=[("idleEndTime", -1)]
            )
            if idle:
                analytics["idle"] = {
                    "duration":
                        idle.get(
                            "duration"
                        )
                }
            # ==========================
            # STOPPAGE REPORT
            # ==========================
            stop = self.db[
                "report_stopages"
            ].find_one(
                {"uniqueId": str(unique_id)},
                sort=[("departureTime", -1)]
            )
            if stop:
                analytics["stoppage"] = {
                    "arrivalTime":
                        str(
                            stop.get(
                                "arrivalTime"
                            )
                        ),
                    "departureTime":
                        str(
                            stop.get(
                                "departureTime"
                            )
                        )
                }
            # ==========================
            # SUBSCRIPTION
            # ==========================
            subscription = self.db[
                "devicesubscriptions"
            ].find_one(
                {"uniqueId": str(unique_id)}
            )
            if subscription:
                analytics["subscription"] = {
                    "status":
                        subscription.get(
                            "status"
                        ),
                    "amount":
                        subscription.get(
                            "amount"
                        ),
                    "expiry":
                        str(
                            subscription.get(
                                "newExpirationDate"
                            )
                        ),
                    "paidByRole":
                        subscription.get(
                            "paidByRole"
                        )
                }
            # ==========================
            # GEOFENCE EVENTS
            # ==========================
            geo = self.db[
                "geofencereports"
            ].find_one(
                {"uniqueId": str(unique_id)},
                sort=[("timestamp", -1)]
            )
            if geo:
                analytics["geofence"] = {
                    "eventType":
                        geo.get(
                            "eventType"
                        ),
                    "timestamp":
                        str(
                            geo.get(
                                "timestamp"
                            )
                        )
                }    
            # ==========================
            # HISTORY
            # ==========================
            history = self.db[
                "histories"
            ].find_one(
                {"uniqueId": str(unique_id)},
                sort=[("serverTime", -1)]
            )
            if history:
                analytics["history"] = {
                    "latitude":
                        history.get(
                            "latitude"
                        ),
                    "longitude":
                        history.get(
                            "longitude"
                        ),
                    "speed":
                        history.get(
                            "speed"
                        )
                }
        except Exception as e:
            analytics["error"] = str(e)
        return analytics
    
    
    
    
    
    
    
    
    
    
    
    
    