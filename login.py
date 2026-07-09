from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from bson import ObjectId
from rbac import get_rbac_filter
from mongodb import db
from fastapi.middleware.cors import CORSMiddleware
from jwt_handler import (
    create_token,
    verify_token
)


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

class ChatRequest(BaseModel):
    token: str
    collection_name: str


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
        "success": True,
        "message": "FastAPI RBAC Server Running"
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

                {
                    "username": req.username
                },

                {
                    "email": req.username
                },

                {
                    "mobileNo": req.username
                }
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

    token = create_token({

        "_id": str(user["_id"]),

        "username": user.get("username", ""),

        "role": user.get("role", ""),

        "schoolId": str(
            user.get("schoolId", "")
        ),

        "branchId": str(
            user.get("branchId", "")
        ),

        "deviceObjId": str(
            user.get("deviceObjId", "")
        ),

        "routeObjId": str(
            user.get("routeObjId", "")
        )
    })

    return {

        "success": True,
        "token": token,
        "role": user.get("role"),
        "collection": found_collection,
        "user_id": str(user["_id"]),
        "username": user.get("username"),
        "email": user.get("email"),
        "mobileNo": user.get("mobileNo"),
        "schoolId": str(
            user.get("schoolId", "")
        ),
        "branchId": str(
            user.get("branchId", "")
        ),
        "deviceObjId": str(
            user.get("deviceObjId", "")
        ),
        "routeObjId": str(
            user.get("routeObjId", "")
        )
    }


# ==========================
# RBAC COLLECTION DATA
# ==========================

@app.post("/collection-data")
def collection_data(req: ChatRequest):

    decoded = verify_token(
        req.token
    )

    filter_query = get_rbac_filter(

        role=decoded["role"],

        user=decoded,

        collection_name=req.collection_name,

        db=db
    )

    data = list(

        db[req.collection_name]
        .find(filter_query)
        .limit(100)
    )

    data = serialize_document(data)

    return {

        "success": True,

        "role": decoded["role"],

        "user_id": decoded["_id"],

        "collection": req.collection_name,

        "filter": serialize_document(
            filter_query
        ),

        "count": len(data),

        "data": data
    }


# ==========================
# TOKEN INFO
# ==========================

@app.post("/me")
def me(req: ChatRequest):

    decoded = verify_token(
        req.token
    )

    return {

        "success": True,

        "user": decoded
    }