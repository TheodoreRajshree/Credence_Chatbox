from bson import ObjectId
from rbac import get_rbac_filter
from vehicle_km_engine import VehicleKmEngine

class SubscriptionConfigEngine:

    def __init__(self, db):
        self.db = db


    # ====================================
    # SAFE OBJECT ID
    # ====================================

    def _convert_id(self, value):

        try:
            return ObjectId(value)

        except:
            return value



    # ====================================
    # GET ALLOWED FILTER
    # ====================================

    def get_allowed_filter(
        self,
        role,
        user
    ):

        return get_rbac_filter(

            role,

            user,

            "subscriptionconfigs",

            self.db

        )



    # ====================================
    # GET SUBSCRIPTION BY MODEL
    # ====================================

    def get_subscription_by_model(
        self,
        model_name,
        role,
        user
    ):


        config_filter = self.get_allowed_filter(

            role,

            user

        )


        config = self.db["subscriptionconfigs"].find_one({

            "$and":[

                config_filter,

                {
                    "modelName": {

                        "$regex":
                        f"^{model_name}$",

                        "$options":
                        "i"

                    }
                }

            ]

        })


        if not config:
            return None


        return {

            "modelName":
            config.get("modelName"),

            "yearlyAmount":
            config.get("yearlyAmount"),

            "currency":
            config.get("currency"),

            "noRenewalNeeded":
            config.get("noRenewalNeeded"),

            "updatedBy":
            str(
                config.get("updatedBy")
            ),

            "createdAt":
            str(
                config.get("createdAt")
            )

        }



    # ====================================
    # GET ALL SUBSCRIPTIONS
    # ====================================

    def get_all_subscription_configs(
        self,
        role,
        user
    ):


        configs = list(

            self.db["subscriptionconfigs"].find(

                self.get_allowed_filter(

                    role,

                    user

                )

            )

        )


        return [

            {

                "modelName":
                c.get("modelName"),

                "yearlyAmount":
                c.get("yearlyAmount"),

                "currency":
                c.get("currency"),

                "noRenewalNeeded":
                c.get("noRenewalNeeded")

            }

            for c in configs

        ]



    # ====================================
    # TOTAL CONFIG COUNT
    # ====================================

    def get_subscription_count(
        self,
        role,
        user
    ):


        return self.db["subscriptionconfigs"].count_documents(

            self.get_allowed_filter(

                role,

                user

            )

        )



    # ====================================
    # DASHBOARD
    # ====================================

    def get_dashboard(
        self,
        role,
        user
    ):


        return {

            "subscription_models":

            self.get_subscription_count(

                role,

                user

            )

        }



    # ====================================
    # SEARCH
    # ====================================

    def search_subscription(
        self,
        model_name,
        role,
        user
    ):


        config = self.db["subscriptionconfigs"].find_one({

            "$and":[

                self.get_allowed_filter(

                    role,

                    user

                ),

                {

                    "modelName": {

                        "$regex":
                        f"^{model_name}$",

                        "$options":
                        "i"

                    }

                }

            ]

        })


        if not config:
            return None


        return self.get_subscription_by_model(

            model_name,

            role,

            user

        )