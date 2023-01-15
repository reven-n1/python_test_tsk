from fastapi import FastAPI
from src import statistics


app = FastAPI()
app.include_router(statistics.router)
