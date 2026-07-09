class ChatbotRouter:


    def __init__(self,engines):

        self.engines=engines



    def execute(
        self,
        action,
        role,
        user
    ):


        engine=self.engines.get(action)


        if not engine:

            return {
                "message":"Engine not connected"
            }



        return engine(
            role,
            user
        )