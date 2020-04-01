from fastapi import APIRouter
from api.utils.database_connection import get_connection
from api.utils.helpers import to_br_date
from pydantic import BaseModel

router = APIRouter()


class Data(BaseModel):
    region: str
    state: str
    date: str
    new_cases: int
    acumulated_cases: int
    new_deaths: int
    acumulated_deaths: int

class Response(BaseModel):
    data: Data


@router.get("/covid-19/{date}", tags=["covid-19"], response_model=Response)
async def read_general_data(date: str):
    db = get_connection()
    collection_name = f"situation_{date}"
    br_date = to_br_date(date)
    final_result = db[collection_name].find({"date": br_date})
    result = [r for r in final_result]

    total_new_cases = 0
    total_acumulated_cases = 0
    total_new_deaths = 0
    total_acumulated_deaths = 0

    for res in result:
        del res['_id']
        total_new_cases = total_new_cases + int(res['new_cases'])
        total_acumulated_cases = total_acumulated_cases + int(res['acumulated_cases'])
        total_new_deaths = total_new_deaths + int(res['new_deaths'])
        total_acumulated_deaths = total_acumulated_deaths + int(res['acumulated_deaths'])

    return {"data": {
        'region': 'Brasil',
        'state': None,
        'date': br_date,
        'new_cases': total_new_cases,
        'acumulated_cases': total_acumulated_cases,
        'new_deaths': total_new_deaths,
        'acumulated_deaths': total_acumulated_deaths
    }}

