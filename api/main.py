from fastapi import Depends, FastAPI, Header, HTTPException

from routers import covid_19

app = FastAPI()

app.include_router(covid_19.router)

