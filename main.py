

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

from fastapi import FastAPI, HTTPException, Header
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
    "http://localhost:5500",
    "http://localhost:3000",
    "http://127.0.0.1:8000 "
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
    pass
class PredefinedChatRequest(BaseModel):

    message: str | None = None

    question_id: int

    branch_name: str | None = None

    school_name: str | None = None
    school_id: str | None = None

    vehicle_input: str | None = None

    function: str | None = None

    branchgroup_input: str | None = None

    report_date: str | None = None
    from_date: str | None = None       # ADD
    to_date: str | None = None  
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
def convert_objectids_to_strings(value):

    if isinstance(value, ObjectId):

        return str(value)


    if isinstance(value, list):

        return [

            convert_objectids_to_strings(item)

            for item in value

        ]


    if isinstance(value, dict):

        return {

            key: convert_objectids_to_strings(val)

            for key, val in value.items()

        }


    return value
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

        or

        user.get("branchGroupId")

        or

        (

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

    # if found_collection == "branches":

    #     # Branch user gets only:
    #     # _id
    #     # username
    #     # role
    #     # schoolId

    #     token_payload = {

    #         "id": str(
    #             user["_id"]
    #         ),

    #         "username": user.get(
    #             "username",
    #             ""
    #         ),

    #         "role": (
    #             user.get("role") or ""
    #         ).strip().lower(),

    #         "schoolId": school_id

    #     }

    # else:

    #     # School and other users
    #     # keep the existing token structure

    #     token_payload = {

    #         "_id": str(
    #             user["_id"]
    #         ),

    #         "username": user.get(
    #             "username",
    #             ""
    #         ),

    #         "role": (
    #             user.get("role") or ""
    #         ).strip().lower(),

    #         "schoolId": school_id,

    #         "branchId": branch_id,

    #         "groupId": (
    #             str(group_id)
    #             if group_id
    #             else None
    #         )

    #     }
     # ==========================
# CREATE TOKEN
# ==========================

     # ==========================
# CREATE TOKEN
# ==========================

    if found_collection == "branches":

    # ==========================
    # BRANCH TOKEN
    # ==========================

        token_payload = {

        "id": str(
            user["_id"]
        ),

        "username": user.get(
            "username",
            ""
        ),

        "role": (
            user.get("role") or ""
        ).strip().lower(),

        "schoolId": school_id

    }


    elif found_collection == "branchgroups":

    # ==========================
    # BRANCHGROUP TOKEN
    # ==========================

        assigned_branches = (

        user.get(
            "AssignedBranch",
            []
        )

        or []

    )


        assigned_branches = (

        convert_objectids_to_strings(

            assigned_branches

        )

    )


        token_payload = {

        "id": str(
            user["_id"]
        ),

        "username": user.get(
            "username",
            ""
        ),

        "role": (
            user.get("role") or ""
        ).strip().lower(),

        "schoolId": school_id,

        "AssignedBranch": assigned_branches

    }

    elif found_collection == "schools":

    # ==========================================
    # SCHOOL TOKEN
    # ==========================================

       # ==========================================
# SCHOOL ID
# ==========================================

        school_object_id = user["_id"]

        school_id = str(
    school_object_id
)


# ==========================================
# FIND ALL BRANCHES OF THIS SCHOOL
# ==========================================

        school_branches = list(

    db["branches"].find(

        {
            "$or": [

                # If branches.schoolId is ObjectId
                {
                    "schoolId": school_object_id
                },

                # If branches.schoolId is string
                {
                    "schoolId": school_id
                }

            ]
        },

        {
            "_id": 1
        }

    )

)


# ==========================================
# CONVERT BRANCH IDS TO STRINGS
# ==========================================

        assigned_branches = [

    str(branch["_id"])

    for branch in school_branches

]


        print(
    "SCHOOL ID:",
    school_id
)

        print(
    "FOUND SCHOOL BRANCHES:",
    assigned_branches
)


    # ==========================================
    # CONVERT BRANCH IDS TO STRINGS
    # ==========================================

        assigned_branches = [

        str(
            branch["_id"]
        )

        for branch in school_branches

    ]


        token_payload = {

        "id": school_id,

        "username": user.get(

            "username",

            ""

        ),

        "role": (

            user.get(

                "role"

            )

            or "school"

        ).strip().lower(),

        "AssignedBranch": assigned_branches,

        "loginAccess": user.get(

            "loginAccess",

            True

        )

    }
    


    else:

    # ==========================
    # OTHER USERS
    # OLD TOKEN STRUCTURE
    # ==========================

        token_payload = {

        "_id": str(
            user["_id"]
        ),

        "username": user.get(
            "username",
            ""
        ),

        "role": (
            user.get("role") or ""
        ).strip().lower(),

        "schoolId": school_id,

        "branchId": branch_id,

        "groupId": (

            str(group_id)

            if group_id

            else None

        )

    }

    # ==========================
    # CREATE JWT TOKEN
    # ==========================

    token = create_token(
        token_payload
    )


    # ==========================
    # RETURN RESPONSE
    # ==========================

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
def get_questions(authorization: str = Header(...)):

    try:
        # Check header format
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Invalid Authorization header"
            )

        # Extract token
        token = authorization.replace("Bearer ", "").strip()

        # Verify JWT
        user = verify_token(token)

        # Get role
        role = (user.get("role") or "").strip().lower()

        print("ROLE:", role)
        print("AVAILABLE KEYS:", QUESTIONS.keys())

        return {
            "success": True,
            "role": role,
            "questions": QUESTIONS.get(role, [])
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
# ==========================
# CHAT
# ==========================

# @app.post("/predefined-chat")
# def predefined_chat(req: PredefinedChatRequest):

#     try:

#         user = verify_token(req.token)
@app.post("/predefined-chat")
def predefined_chat(
    req: PredefinedChatRequest,
    authorization: str = Header(...)
):

    try:

        # ==========================================
        # 1. CHECK AUTHORIZATION HEADER
        # ==========================================

        if not authorization.startswith("Bearer "):

            raise HTTPException(
                status_code=401,
                detail="Invalid Authorization header"
            )


        # ==========================================
        # 2. EXTRACT TOKEN
        # ==========================================

        token = authorization.replace(
            "Bearer ",
            "",
            1
        ).strip()


        if not token:

            raise HTTPException(
                status_code=401,
                detail="Token is missing"
            )


        # ==========================================
        # 3. VERIFY JWT TOKEN
        # ==========================================

        user = verify_token(token)


        if not user:

            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )


        print(
            "TOKEN USER ================="
        )

        print(user)


        # ==========================================
        # 4. GET ROLE
        # ==========================================

        role = (

            user.get("role")

            or ""

        ).strip().lower()


        if not role:

            raise HTTPException(
                status_code=401,
                detail="Role missing in token"
            )


        # ==========================================
        # 5. NORMALIZE USER ID
        # ==========================================

        if role == "branch":

            # Branch token:
            #
            # {
            #     "id": "BRANCH_ID",
            #     "role": "branch"
            # }
            #
            # Existing backend expects:
            #
            # user["branchId"]
            # user["_id"]

            branch_id = user.get("id")


            if not branch_id:

                raise HTTPException(
                    status_code=401,
                    detail="Branch ID missing in token"
                )


            user["branchId"] = branch_id

            user["_id"] = branch_id


        elif role == "branchgroup":

            # BranchGroup token:
            #
            # {
            #     "id": "GROUP_ID",
            #     "role": "branchgroup",
            #     "AssignedBranch": [...]
            # }

            group_id = user.get("id")


            if not group_id:

                raise HTTPException(
                    status_code=401,
                    detail="BranchGroup ID missing in token"
                )


            user["groupId"] = group_id

            user["_id"] = group_id


        elif role == "school":

            # School token:
            #
            # {
            #     "id": "SCHOOL_ID",
            #     "username": "gpswale",
            #     "role": "school",
            #     "AssignedBranch": [],
            #     "loginAccess": true
            # }

            school_id = user.get("id")


            if not school_id:

                raise HTTPException(
                    status_code=401,
                    detail="School ID missing in token"
                )


            # Existing school code can use _id

            user["_id"] = school_id


            # Also provide schoolId
            # for compatibility with old functions

            user["schoolId"] = school_id


        else:

            # ==========================================
            # OLD USERS
            # ==========================================

            user["_id"] = (

                user.get("_id")

                or user.get("id")

            )


            user["schoolId"] = (

                user.get("schoolId")

            )


            user["branchId"] = (

                user.get("branchId")

            )


            user["groupId"] = (

                user.get("groupId")

                or user.get("branchGroupId")

            )


        # ==========================================
        # 6. DEBUG
        # ==========================================

        print(
            "================ NORMALIZED USER ================"
        )

        print(
            "ID =",
            user.get("_id")
        )

        print(
            "SCHOOL ID =",
            user.get("schoolId")
        )

        print(
            "BRANCH ID =",
            user.get("branchId")
        )

        print(
            "GROUP ID =",
            user.get("groupId")
        )

        print(
            "ROLE =",
            role
        )

        print(
            "QUESTION ID =",
            req.question_id
        )


        # ==========================================
        # 7. REQUEST INPUT VALUES
        # ==========================================

        input_value = {

            "branch_name":
                req.branch_name,

            "school_name":
                req.school_name,

            "school_id": (
        req.school_id
        or req.school_name
    ),

            "vehicle_input":
                req.vehicle_input,

            "branchgroup_input":
                req.branchgroup_input,

            "report_date":
                req.report_date,

            "from_date":
                req.from_date,

            "to_date":
                req.to_date

        }


        print(
            "REQUEST DATA ================="
        )

        print(
            req.model_dump()
        )


        # ==========================================
        # 8. EXECUTE QUESTION
        # ==========================================

        response = execute_predefined_question(

            role,

            user,

            req.question_id,

            input_value

        )


        print(
            "RESPONSE ================="
        )

        print(response)


        # ==========================================
        # 9. HANDLE NO DATA
        # ==========================================

        if (

            isinstance(
                response,
                dict
            )

            and response.get(
                "success"
            ) is False

        ):

            raise HTTPException(

                status_code=404,

                detail=response.get(

                    "message",

                    "Data not found"

                )

            )


        # ==========================================
        # 10. SUCCESS RESPONSE
        # ==========================================
        response.pop("success", None)
        return {

            "success": True,
            
            "ui_type": "auto",
            "data": response

            

        }
        # response["ui_type"] = "auto"
        # return response


    except HTTPException:

        raise


    except ValueError as e:

        raise HTTPException(

            status_code=404,

            detail=str(e)

        )


    except Exception as e:

        print(
            "PREDEFINED CHAT ERROR ================="
        )

        print(e)


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )
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