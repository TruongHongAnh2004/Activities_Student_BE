from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from app.controllers import extract_controllers
from app.controllers.postgres_controllers import postgres
from app.controllers.management_controllers import metadata 
from app.controllers.admin_controllers import admin 
from app.controllers.user_controllers import users 
from app.controllers.extract_controllers import extract
app = FastAPI()
    
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Allows specific origins
    allow_credentials=True,       # Allows cookies to be included in cross-origin requests
    allow_methods=["*"],          # Allows all standard methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],          # Allows all standard and custom headers
)

app.include_router(metadata)
app.include_router(postgres)
app.include_router(admin)
app.include_router(users)
app.include_router(extract)
