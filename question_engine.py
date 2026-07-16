from predefined_questions import QUESTIONS
from engine_registry import ENGINE_REGISTRY
class QuestionEngine:
    def find_function(
        self,
        role,
        user_question
    ):
        user_question = user_question.lower()
        questions = QUESTIONS.get(
            role,
            []
        )
        for q in questions:
            text = q["question"].lower()
            if text in user_question:
                return q["function"]
        return None                
    def execute(
        self,
        role,
        user_question,
        user,
        **params
    ):
        function_name = self.find_function(
            role,
            user_question
        )
        if not function_name:
            return {
                "message":
                "Question not supported !!! WHHHHHHHHyyyyyyy?"
            } 
        engine_function = ENGINE_REGISTRY.get(
            function_name
        )
        if not engine_function:
            return {
                "message":
                "Engine function missing",
                "function":
                function_name
            }
        return engine_function(
            role,
            user,
            **params
        )   