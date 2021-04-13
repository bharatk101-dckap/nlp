import datetime
from fastapi import APIRouter, Depends, Header
from app.auth import verify_token
from app.module.graphs.common import SearchFilter, CheckFilter, SuggestionFilter
from typing import Optional
from app.page.nlp.output import sda
from  app.page.nlp.autosuggestion import autosuggestion
import pandas as pd
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

nlp = APIRouter()
now = datetime.datetime.now()


@nlp.post('/nlp/search', dependencies=[Depends(verify_token)])
async def get_query(filters: Optional[SearchFilter] = None, company_Id: str = Header(None)):
    try:
        if filters is not None:
            data = sda(company_Id, query=filters.query, type_=filters.data_type)
        else:
            data = JSONResponse(content=jsonable_encoder({"data": [], "title": "NLP"}), status_code=203)
    except Exception:
        data = JSONResponse(content=jsonable_encoder({"data": [], "title": "NLP"}), status_code=203)
    return data


@nlp.post('/nlp/result', dependencies=[Depends(verify_token)])
async def get_result(filters: Optional[CheckFilter] = None, company_Id: str = Header(None)):
    try:
        if filters is not None:
            if filters.result is not None:
                # df = pd.DataFrame(columns=["company_Id", "queries"])
                # df.to_csv("app/ln2sql/queries.csv", index=False)
                df = pd.read_csv("app/ln2sql/queries.csv")
                df = df.append({'company_Id': company_Id, 'queries': filters.query}, ignore_index=True)
                df.to_csv("app/ln2sql/queries.csv", index=False)
        else:
            pass
    except Exception:
        pass


@nlp.post('/nlp/autosuggestion', dependencies=[Depends(verify_token)])
async def get_suggestion(filters: Optional[SuggestionFilter] = None, company_Id: str = Header(None)):
    try:
        if filters is not None:
            data = autosuggestion(input_=filters.query)
        else:
            data = JSONResponse(content=jsonable_encoder({"word_suggestions": []}), status_code=203)
    except Exception:
        data = JSONResponse(content=jsonable_encoder({"word_suggestions": []}), status_code=203)
    return data
