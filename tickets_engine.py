from bson import ObjectId
from rbac import get_rbac_filter


class TicketsEngine:

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

    def get_ticket_filter(
        self,
        role,
        user
    ):

        return get_rbac_filter(

            role,

            user,

            "tickets",

            self.db

        )



    # ====================================
    # FORMAT RESPONSE
    # ====================================

    def format_ticket(self, t):

        return {

            "ticketId":
            t.get("ticket_id"),

            "description":
            t.get("description"),

            "status":
            t.get("status"),

            "feedback":
            t.get("feedback"),

            "role":
            t.get("role"),

            "email":
            t.get("raised_by", {}).get("email"),

            "addedDate":
            t.get("added_date")

        }



    # ====================================
    # SINGLE TICKET
    # ====================================

    def get_ticket(
        self,
        ticket_id,
        role,
        user
    ):


        ticket = self.db["tickets"].find_one({

            "$and":[

                self.get_ticket_filter(

                    role,

                    user

                ),

                {

                    "_id":
                    self._convert_id(
                        ticket_id
                    )

                }

            ]

        })


        if not ticket:
            return None


        return self.format_ticket(ticket)



    # ====================================
    # ALL TICKETS
    # ====================================

    def get_all_tickets(
        self,
        role,
        user
    ):


        tickets = list(

            self.db["tickets"].find(

                self.get_ticket_filter(

                    role,

                    user

                )

            )

        )


        return [

            self.format_ticket(t)

            for t in tickets

        ]



    # ====================================
    # SCHOOL TICKETS
    # ====================================

    def get_school_tickets(
        self,
        school_id,
        role,
        user
    ):


        tickets = list(

            self.db["tickets"].find({

                "$and":[

                    self.get_ticket_filter(

                        role,

                        user

                    ),

                    {

                        "schoolId":
                        self._convert_id(
                            school_id
                        )

                    }

                ]

            })

        )


        return [

            self.format_ticket(t)

            for t in tickets

        ]



    # ====================================
    # BRANCH TICKETS
    # ====================================

    def get_branch_tickets(
        self,
        branch_id,
        role,
        user
    ):


        tickets = list(

            self.db["tickets"].find({

                "$and":[

                    self.get_ticket_filter(

                        role,

                        user

                    ),

                    {

                        "branchId":
                        self._convert_id(
                            branch_id
                        )

                    }

                ]

            })

        )


        return [

            self.format_ticket(t)

            for t in tickets

        ]



    # ====================================
    # STATUS FILTER
    # ====================================

    def get_tickets_by_status(
        self,
        status,
        role,
        user
    ):


        tickets = list(

            self.db["tickets"].find({

                "$and":[

                    self.get_ticket_filter(

                        role,

                        user

                    ),

                    {

                        "status":{

                            "$regex":
                            status,

                            "$options":
                            "i"

                        }

                    }

                ]

            })

        )


        return [

            self.format_ticket(t)

            for t in tickets

        ]



    # ====================================
    # COUNTS
    # ====================================

    def get_total_ticket_count(
        self,
        role,
        user
    ):


        return self.db["tickets"].count_documents(

            self.get_ticket_filter(

                role,

                user

            )

        )



    def get_open_ticket_count(
        self,
        role,
        user
    ):


        return self.db["tickets"].count_documents({

            "$and":[

                self.get_ticket_filter(

                    role,

                    user

                ),

                {

                    "status":{

                        "$regex":
                        "open|pending",

                        "$options":
                        "i"

                    }

                }

            ]

        })



    def get_resolved_ticket_count(
        self,
        role,
        user
    ):


        return self.db["tickets"].count_documents({

            "$and":[

                self.get_ticket_filter(

                    role,

                    user

                ),

                {

                    "status":{

                        "$regex":
                        "resolved",

                        "$options":
                        "i"

                    }

                }

            ]

        })



    # ====================================
    # DASHBOARD
    # ====================================

    def get_ticket_dashboard(
        self,
        role,
        user
    ):


        return {

            "totalTickets":

            self.get_total_ticket_count(

                role,

                user

            ),


            "openTickets":

            self.get_open_ticket_count(

                role,

                user

            ),


            "resolvedTickets":

            self.get_resolved_ticket_count(

                role,

                user

            )

        }