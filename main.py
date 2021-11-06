# main.py

from logging import debug
import uvicorn
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mftool import Mftool
from pydantic import BaseModel

import services.holdingService as holdingservice
import services.investmentService as investmentservice
import services.watchlistService as watchlistService
import exception.apiError as error

import utils.newsfeedUtil as newsfeed
import utils.stockUtil as stockutil

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HoldingList(BaseModel):
    holdingList: list

@app.exception_handler(error.APIError)
async def unicorn_exception_handler(request: Request, exc: error.APIError):
    return JSONResponse(
        status_code=exc.statusCode,
        content={"error": exc.message},
    )

@app.get("/ping")
def ping():
    return {'status' : 'service is up and running!'}

@app.get("/v1/api/user/{email}/portfolio/{portfolio_id}/holding")
def getUserHolding(email,portfolio_id):
    return holdingservice.getHolding(email,portfolio_id)

@app.post("/v1/api/user/{email}/portfolio/{portfolio_id}/holding")
def createUserHolding(email,portfolio_id,holdingList:HoldingList):
    return holdingservice.createHolding(email,portfolio_id,holdingList)

@app.get("/v1/api/user/{email}/portfolio/{portfolio_id}/investment")
def getUserInvestment(email,portfolio_id):
    return investmentservice.getInvestment(email,portfolio_id)

@app.post("/v1/api/user/{email}/portfolio/{portfolio_id}/investment")
def createUserInvestment(email,portfolio_id):
    return investmentservice.createInvestment(email,portfolio_id)

@app.get("/v1/api/user/{email}/watchlist")
def getUserWatchlist(email):
    return watchlistService.getUserWatchList(email)

@app.get("/v1/api/user/{email}/portfolio")
def getUserPortfolio(email):
     return holdingservice.getUserPortfolio(email)

@app.get("/current/feeds/site/{site}/")
def getCurrentFeeds(site):
    return newsfeed.get_current_feeds(site)

@app.get("/mf/nav/")
def getCurrentNAV():
    mf = Mftool()
    #return mf.get_scheme_codes()
    return mf.get_scheme_quote('135781')

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True)

