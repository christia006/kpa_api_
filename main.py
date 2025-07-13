from fastapi import FastAPI
from routers import bogie_checksheet, wheel_specifications

app = FastAPI(title="KPA Form API")

app.include_router(bogie_checksheet.router)
app.include_router(wheel_specifications.router)
