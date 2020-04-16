from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from api.utils.database_connection import get_connection
from api.utils.helpers import calculate_acumulated_values, to_br_date

router = APIRouter()


class Data(BaseModel):
    region: str
    state: str
    date: str
    new_cases: int
    acumulated_cases: int
    new_deaths: int
    acumulated_deaths: int


class CountryModel(BaseModel):
    data: Data


class RegionData(BaseModel):
    separated: List[Data]
    accumulated: Data


class RegionModel(BaseModel):
    data: RegionData


class StateModel(BaseModel):
    data: List[Data]


class ResponseArray(BaseModel):
    data: List[Data] = []


class Dates(BaseModel):
    dates: List[str] = []


@router.get("/covid-19/", tags=["covid-19"], response_model=Dates)
async def get_available_dates():
    db = get_connection()
    names = db.collection_names()
    dates = [n[-8:] for n in names]

    return {"dates": dates}


@router.get("/covid-19/{date}", tags=["covid-19"], response_model=CountryModel)
async def read_general_data(date: str):
    db = get_connection()
    collection_name = f"situation_{date}"
    br_date = to_br_date(date)
    final_result = db[collection_name].find({"date": br_date})
    result = [r for r in final_result]

    acc = {
        "total_new_cases": 0,
        "total_acumulated_cases": 0,
        "total_new_deaths": 0,
        "total_acumulated_deaths": 0,
    }

    for res in result:
        del res["_id"]
        acc = calculate_acumulated_values(acc, res)

    return {
        "data": {
            "region": "Brasil",
            "state": "Brasil",
            "date": br_date,
            "new_cases": acc["total_new_cases"],
            "acumulated_cases": acc["total_acumulated_cases"],
            "new_deaths": acc["total_new_deaths"],
            "acumulated_deaths": acc["total_acumulated_deaths"],
        }
    }


@router.get("/covid-19/{date}/{region}", tags=["covid-19"], response_model=RegionModel)
async def read_region_data(date: str, region: str):
    db = get_connection()
    collection_name = f"situation_{date}"
    br_date = to_br_date(date)
    final_result = db[collection_name].find({"date": br_date, "region": region})
    result = [r for r in final_result]

    acc = {
        "total_new_cases": 0,
        "total_acumulated_cases": 0,
        "total_new_deaths": 0,
        "total_acumulated_deaths": 0,
    }

    for res in result:
        del res["_id"]
        res["new_cases"] = int(res["new_cases"])
        res["acumulated_cases"] = int(res["acumulated_cases"])
        res["new_deaths"] = int(res["new_deaths"])
        res["acumulated_deaths"] = int(res["acumulated_deaths"])

        acc = calculate_acumulated_values(acc, res)

    accumulated = {
        "region": region,
        "state": region,
        "date": br_date,
        "new_cases": acc["total_new_cases"],
        "acumulated_cases": acc["total_acumulated_cases"],
        "new_deaths": acc["total_new_deaths"],
        "acumulated_deaths": acc["total_acumulated_deaths"],
    }

    return {"data": {"separated": result, "accumulated": accumulated}}


@router.get(
    "/covid-19/{date}/{region}/{state}", tags=["covid-19"], response_model=StateModel
)
async def read_state_data(date: str, region: str, state: str):
    db = get_connection()
    collection_name = f"situation_{date}"
    br_date = to_br_date(date)
    final_result = db[collection_name].find(
        {"date": br_date, "region": region, "state": state}
    )
    result = [r for r in final_result]

    for res in result:
        del res["_id"]

    return {"data": result}
