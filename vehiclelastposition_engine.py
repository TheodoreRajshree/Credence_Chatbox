from rbac import get_rbac_filter
import requests
import re
from geopy.geocoders import Nominatim
class VehicleLastPositionEngine:

    def __init__(self, db):
        self.db = db
        self.geolocator = Nominatim(
        user_agent="vehicle_tracking_system",
        timeout=10
    )

    # ====================================
    # RBAC FILTER
    # ====================================
    def get_address(self, latitude, longitude):

        try:

            location = self.geolocator.reverse(
            f"{latitude}, {longitude}",
            language="en",
            exactly_one=True,
            timeout=10
        )

            if location:
                return location.address

        except Exception as e:

            print("Reverse Geocoding Error:", e)

        return "Address Not Available"
    def get_position_filter(
        self,
        role,
        user
    ):

        return get_rbac_filter(

            role,

            user,

            "vehiclelastpositions",

            self.db

        )



    # ====================================
    # SINGLE VEHICLE LAST POSITION
    # ====================================

    def get_vehicle_last_position(
        self,
        unique_id,
        role,
        user
    ):


        position_filter = self.get_position_filter(

            role,

            user

        )


        vehicle = self.db["vehiclelastpositions"].find_one({

            "$and":[

                position_filter,

                {

                    "uniqueId":
                    str(unique_id)

                }

            ]

        })
        print("ENGINE = VehicleLastPositionEngine")
        print("MONGO ADDRESS =", vehicle.get("address"))


        if not vehicle:
            return None

        address = self.get_address(
    vehicle.get("latitude"),
    vehicle.get("longitude")
)
        
        return {

            "vehicleName":
            vehicle.get("name"),

            "uniqueId":
            vehicle.get("uniqueId"),

            "latitude":
            vehicle.get("latitude"),

            "longitude":
            vehicle.get("longitude"),

            "speed":
            vehicle.get("speed"),

            "course":
            vehicle.get("course"),

            "accuracy":
            vehicle.get("accuracy"),

            "altitude":
            vehicle.get("altitude"),

            "address": address,

            "protocol":
            vehicle.get("protocol"),

            "deviceTime":
            vehicle.get("deviceTime"),

            "fixTime":
            vehicle.get("fixTime"),

            "serverTime":
            vehicle.get("serverTime"),

            "lastUpdate":
            vehicle.get("lastUpdate"),

            "valid":
            vehicle.get("valid"),

            "outdated":
            vehicle.get("outdated")

        }



    # ====================================
    # ALL VEHICLE POSITIONS
    # ====================================

    def get_all_last_positions(
        self,
        role,
        user
    ):


        vehicles = list(

            self.db["vehiclelastpositions"].find(

                self.get_position_filter(

                    role,

                    user

                )

            )

        )


        return [

            {

                "vehicleName":
                v.get("name"),

                "uniqueId":
                v.get("uniqueId"),

                "latitude":
                v.get("latitude"),

                "longitude":
                v.get("longitude"),

                "speed":
                v.get("speed"),

                "lastUpdate":
                v.get("lastUpdate")

            }

            for v in vehicles

        ]
    # ====================================
    # ACTIVE VEHICLES
    # ====================================

    def get_active_vehicles(
        self,
        role,
        user
    ):


        vehicles = list(

            self.db["vehiclelastpositions"].find({

                "$and":[

                    self.get_position_filter(

                        role,

                        user

                    ),

                    {

                        "speed":
                        {
                            "$gt":0
                        }

                    }

                ]

            })

        )


        return [

            {

                "vehicleName":
                v.get("name"),

                "uniqueId":
                v.get("uniqueId"),

                "speed":
                v.get("speed"),

                "latitude":
                v.get("latitude"),

                "longitude":
                v.get("longitude")

            }

            for v in vehicles

        ]



    # ====================================
    # STOPPED VEHICLES
    # ====================================

    def get_stopped_vehicles(
        self,
        role,
        user
    ):


        vehicles = list(

            self.db["vehiclelastpositions"].find({

                "$and":[

                    self.get_position_filter(

                        role,

                        user

                    ),

                    {

                        "speed":
                        0

                    }

                ]

            })

        )


        return [

            {

                "vehicleName":
                v.get("name"),

                "uniqueId":
                v.get("uniqueId"),

                "latitude":
                v.get("latitude"),

                "longitude":
                v.get("longitude"),

                "lastUpdate":
                v.get("lastUpdate")

            }

            for v in vehicles

        ]



    # ====================================
    # COUNTS
    # ====================================

    def get_total_vehicle_count(
        self,
        role,
        user
    ):


        return self.db["vehiclelastpositions"].count_documents(

            self.get_position_filter(

                role,

                user

            )

        )



    def get_active_vehicle_count(
        self,
        role,
        user
    ):


        return self.db["vehiclelastpositions"].count_documents({

            "$and":[

                self.get_position_filter(

                    role,

                    user

                ),

                {

                    "speed":
                    {
                        "$gt":0
                    }

                }

            ]

        })



    def get_stopped_vehicle_count(
        self,
        role,
        user
    ):


        return self.db["vehiclelastpositions"].count_documents({

            "$and":[

                self.get_position_filter(

                    role,

                    user

                ),

                {

                    "speed":
                    0

                }

            ]

        })



    # ====================================
    # DASHBOARD
    # ====================================

    def get_dashboard(
        self,
        role,
        user
    ):


        return {

            "totalVehicles":

            self.get_total_vehicle_count(

                role,

                user

            ),


            "activeVehicles":

            self.get_active_vehicle_count(

                role,

                user

            ),


            "stoppedVehicles":

            self.get_stopped_vehicle_count(

                role,

                user

            )

        }
    def get_specific_vehicle_last_position(
    self,
    role,
    user,
    vehicle_input=None
):


    # ====================================
    # STEP 1: VEHICLE INPUT
    # ====================================

        vehicle_name = str(vehicle_input or "").strip()


        if not vehicle_name:

            return {

            "success": False,

            "message": "Please enter vehicle name or unique ID"

        }



    # ====================================
    # STEP 2: POSITION FILTER
    # ====================================

        base_filter = self.get_position_filter(

        role,

        user

    )



    # ====================================
    # STEP 3: VEHICLE SEARCH
    # ====================================

        regex = re.compile(

        re.escape(vehicle_name),

        re.IGNORECASE

    )


        query = {

        "$and": [

            base_filter,

            {

                "$or": [

                    {
                        "name": regex
                    },

                    {
                        "uniqueId": regex
                    }

                ]

            }

        ]

    }



        vehicle = self.db["vehiclelastpositions"].find_one(

        query

    )



        if not vehicle:

            return {

            "success": False,

            "message": "Vehicle not found"

        }



    # ====================================
    # STEP 4: RESPONSE
    # ====================================

        return {

        "success": True,

        "vehicle": {

            "vehicleName":
                vehicle.get("name"),


            "uniqueId":
                vehicle.get("uniqueId"),


            "latitude":
                vehicle.get("latitude"),


            "longitude":
                vehicle.get("longitude"),


            "speed":
                vehicle.get("speed"),


            "lastUpdate":
                vehicle.get("lastUpdate")

        }

    }   
        