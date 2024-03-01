# from fastapi import FastAPI

# # Create an instance of the FastAPI class
# app = FastAPI()

# # Define a route for the root endpoint


from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from models import * # Import the PersonalInfo model
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# adding cors urls
origins = ['http://localhost:3000']

# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)
# Register Tortoise

# API routes

@app.get("/")
def index():
    return {"message": "Hello, FastAPI!"}


@app.post('/personal_info/')
async def create_personal_info(payload: PersonalInfo_request):
    new_info = await PersonalInfo.create(**payload.dict())
    response  = await PersonalInfo_pydantic.from_tortoise_orm(new_info)
    return {"status": "success", "response": response}

@app.get('/personal-info/{personal_info_id}', response_model=PersonalInfo)
async def read_personal_info(personal_info_id: int):
    info = await PersonalInfo.get_or_none(id=personal_info_id)
    if info is None:
        raise HTTPException(status_code=404, detail="Personal Info not found")
    return {"response": info}

@app.get('/get_all_personal_info')
async def get_all_personal_info():
    response = await PersonalInfo_pydantic.from_queryset(PersonalInfo.all())
    return {"status": "success", "response": response}

register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},  # Update to point to the models module
    generate_schemas=True,
    add_exception_handlers=True
)
