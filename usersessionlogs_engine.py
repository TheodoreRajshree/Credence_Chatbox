from bson import ObjectId
from rbac import get_rbac_filter


class UserSessionLogsEngine:

    def __init__(self, db):
        self.db = db


    def _convert_id(self, value):

        try:
            return ObjectId(value)

        except:
            return value



    # ====================================
    # RBAC FILTER
    # ====================================

    def get_session_filter(
        self,
        role,
        user
    ):

        return get_rbac_filter(

            role,

            user,

            "usersessionlogs",

            self.db

        )



    # ====================================
    # FORMAT SESSION
    # ====================================

    def format_session(self, s):

        return {

            "userId":
            str(s.get("userId")),

            "userModel":
            s.get("userModel"),

            "role":
            s.get("role"),

            "status":
            s.get("status"),

            "action":
            s.get("action"),

            "ip":
            s.get("ip"),

            "userAgent":
            s.get("userAgent"),

            "loginAt":
            s.get("loginAt"),

            "logoutAt":
            s.get("logoutAt")

        }



    # ====================================
    # SINGLE SESSION
    # ====================================

    def get_session(
        self,
        session_id,
        role,
        user
    ):


        session = self.db["usersessionlogs"].find_one({

            "$and":[

                self.get_session_filter(

                    role,

                    user

                ),

                {

                    "_id":
                    self._convert_id(
                        session_id
                    )

                }

            ]

        })


        if not session:
            return None


        return self.format_session(session)



    # ====================================
    # ALL SESSIONS
    # ====================================

    def get_all_sessions(
        self,
        role,
        user
    ):


        sessions = list(

            self.db["usersessionlogs"].find(

                self.get_session_filter(

                    role,

                    user

                )

            )

        )


        return [

            self.format_session(s)

            for s in sessions

        ]



    # ====================================
    # USER SESSIONS
    # ====================================

    def get_user_sessions(
        self,
        user_id,
        role,
        user
    ):


        sessions = list(

            self.db["usersessionlogs"].find({

                "$and":[

                    self.get_session_filter(

                        role,

                        user

                    ),

                    {

                        "userId":
                        self._convert_id(
                            user_id
                        )

                    }

                ]

            })

        )


        return [

            {

                "status":
                s.get("status"),

                "action":
                s.get("action"),

                "ip":
                s.get("ip"),

                "loginAt":
                s.get("loginAt"),

                "logoutAt":
                s.get("logoutAt")

            }

            for s in sessions

        ]



    # ====================================
    # ACTIVE SESSIONS
    # ====================================

    def get_active_sessions(
        self,
        role,
        user
    ):


        sessions = list(

            self.db["usersessionlogs"].find({

                "$and":[

                    self.get_session_filter(

                        role,

                        user

                    ),

                    {

                        "status":
                        "ACTIVE"

                    }

                ]

            })

        )


        return [

            {

                "userId":
                str(s.get("userId")),

                "userModel":
                s.get("userModel"),

                "role":
                s.get("role"),

                "ip":
                s.get("ip"),

                "loginAt":
                s.get("loginAt")

            }

            for s in sessions

        ]



    # ====================================
    # ROLE FILTER
    # ====================================

    def get_role_sessions(
        self,
        search_role,
        role,
        user
    ):


        sessions = list(

            self.db["usersessionlogs"].find({

                "$and":[

                    self.get_session_filter(

                        role,

                        user

                    ),

                    {

                        "role":{

                            "$regex":
                            search_role,

                            "$options":
                            "i"

                        }

                    }

                ]

            })

        )


        return [

            {

                "userId":
                str(s.get("userId")),

                "status":
                s.get("status"),

                "action":
                s.get("action"),

                "ip":
                s.get("ip"),

                "loginAt":
                s.get("loginAt")

            }

            for s in sessions

        ]



    # ====================================
    # COUNTS
    # ====================================

    def get_total_session_count(
        self,
        role,
        user
    ):


        return self.db["usersessionlogs"].count_documents(

            self.get_session_filter(

                role,

                user

            )

        )



    def get_active_session_count(
        self,
        role,
        user
    ):


        return self.db["usersessionlogs"].count_documents({

            "$and":[

                self.get_session_filter(

                    role,

                    user

                ),

                {

                    "status":
                    "ACTIVE"

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

            "totalSessions":

            self.get_total_session_count(

                role,

                user

            ),


            "activeSessions":

            self.get_active_session_count(

                role,

                user

            )

        }