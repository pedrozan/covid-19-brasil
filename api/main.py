from fastapi import Depends, FastAPI, Header, HTTPException

from .routers import covid_19

app = FastAPI(
    title="Covid-19 in Brazil",
    description="An API with the oficial data from the Health Ministry",
    version="0.1.0",
)

app.include_router(covid_19.router)
