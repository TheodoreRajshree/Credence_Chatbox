from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from bson import ObjectId
from rbac import get_rbac_filter
from mongodb import db
from fastapi.middleware.cors import CORSMiddleware
# from chatbot_engine import build_context, build_prompt
# from gemini_engine import GeminiEngine
from chatbot_engine import execute_predefined_question
import jwt
import os
import uvicorn
from dotenv import load_dotenv
from pymongo import MongoClient
from predefined_questions import QUESTIONS
from jwt_handler import (
    create_token,
    verify_token
)

# ==========================
# ENV
# ==========================

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
JWT_SECRET = os.getenv("JWT_SECRET")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DB_NAME = "credence3_0"
app = FastAPI()
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ==========================
# REQUEST MODELS
# ==========================

class LoginRequest(BaseModel):
    username: str
    password: str
class QuestionRequest(BaseModel):
    token: str
class PredefinedChatRequest(BaseModel):
    token: str
    message: str | None = None 
    question_id: int
    branch_name: str | None = None
    vehicle_input: str | None = None
    function: str | None = None

# ==========================
# DB CONNECTION
# ==========================

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
# ==========================
# GEMINI
# ==========================

# gemini = GeminiEngine(GEMINI_API_KEY)

# ==========================
# BSON SERIALIZER
# ==========================

def serialize_document(doc):

    if isinstance(doc, list):
        return [serialize_document(x) for x in doc]

    if isinstance(doc, dict):

        result = {}

        for k, v in doc.items():

            if isinstance(v, ObjectId):
                result[k] = str(v)

            elif isinstance(v, dict):
                result[k] = serialize_document(v)

            elif isinstance(v, list):
                result[k] = serialize_document(v)

            else:
                result[k] = v

        return result

    return doc

# ==========================
# HOME
# ==========================

@app.get("/")
def home():

    return {
        "status": "running",
        "database": DB_NAME
    }

# ==========================
# LOGIN
# ==========================

@app.post("/validate-user")
def validate_user(req: LoginRequest):

    collections = [
        "superadmins",
        "schools",
        "branches",
        "drivers",
        "branchgroups"
    ]

    user = None
    found_collection = None


    for collection in collections:

        user = db[collection].find_one({

            "$or": [
                {"username": req.username},
                {"email": req.username},
                {"mobileNo": req.username}
            ],

            "password": req.password

        })
        
        
        if user:

            found_collection = collection
            break
    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )
    # ==========================
    # CREATE IDS
    # ==========================

    school_id = str(

        user.get("schoolId")

        or

        (
            user["_id"]
            if found_collection == "schools"
            else ""
        )

    )
    group_id = (
    user.get("groupId")
    or user.get("branchGroupId")
    or (
        user["_id"]
        if found_collection == "branchgroups"
        else None
    )
)
    branch_id = str(

        user.get("branchId")

        or

        (
            user["_id"]
            if found_collection == "branches"
            else ""
        )

    )



    # ==========================
    # CREATE TOKEN
    # ==========================

    token = create_token({

        "_id": str(
            user["_id"]
        ),

        "username": user.get(
            "username",
            ""
        ),

        # "role": user.get(
            # "role",
            # ""
        # ),
        "role": (user.get("role") or "").strip().lower(),

        "schoolId": school_id,

        "branchId": branch_id,
        "groupId": str(group_id) if group_id else None, 

        "deviceObjId": str(
            user.get(
                "deviceObjId",
                ""
            )
        ),

        "routeObjId": str(
            user.get(
                "routeObjId",
                ""
            )
        )

    })



    return {

        "success": True,

        "token": token,

        "role": user.get(
            "role"
        ),

        "collection": found_collection,

        "user_id": str(
            user["_id"]
        ),

        "username": user.get(
            "username"
        ),

        "email": user.get(
            "email"
        ),

        "mobileNo": user.get(
            "mobileNo"
        ),

        "schoolId": school_id,

        "branchId": branch_id,

        "deviceObjId": str(
            user.get(
                "deviceObjId",
                ""
            )
        ),

        "routeObjId": str(
            user.get(
                "routeObjId",
                ""
            )
        )
    }
@app.post("/questions")
def get_questions(req: QuestionRequest):

    try:

        user = verify_token(req.token)

        role = (user.get("role") or "").lower()
        # role = (user.get("role") or "").strip().lower()
        print("ROLE:", role)
        print("AVAILABLE KEYS:", QUESTIONS.keys())
        return {

            "success": True,

            "role": role,

            "questions": QUESTIONS.get(role, [])

        }
    

    except Exception as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
# ==========================
# CHAT
# ==========================

@app.post("/predefined-chat")
def predefined_chat(req: PredefinedChatRequest):

    try:

        user = verify_token(req.token)
        print("TOKEN USER =================")
        print(user)
        print(user)
        print("ID =", user.get("_id"))
        print("GROUP ID =", user.get("groupId"))
        print("ROLE =", user.get("role"))
        user["groupId"] = (
    user.get("groupId")
    or user.get("branchGroupId")
    or user.get("_id")
)
        # role = user.get("role", "").lower()
        role = (user.get("role") or "").strip().lower()

        print("ROLE:", role)
        print("QUESTION ID:", req.question_id)

        input_value = {
    "branch_name": req.branch_name,
    "vehicle_input": req.vehicle_input
}

        response = execute_predefined_question(
    role,
    user,
    req.question_id,
    input_value
)
        print("RESPONSE =", response)
        return {
    "success": True,
    "ui_type": "auto",   # we will improve later
    "data": response
}

    except Exception as e:

        return {
            "reply": str(e)
        }
# ==========================
# START SERVER
# ==========================
def detect_intent(text: str):
    text = text.lower()

    if "vehicle" in text and "status" in text:
        return "vehicle_status"

    if "branch" in text and "vehicles" in text:
        return "branch_devices"

    if "distance" in text:
        return "distance_report"

    return "unknown"
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
