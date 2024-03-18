from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from server.services.reports.rates_service import get_rates_info
from server.services.reports.distances_durations import get_distance_duration_averages
from server.services.reports.earnings_service import get_earnings
from server.services.reports.distribution_ratings_service import get_rating_distribution
from server.services.reports.daily_activity_service import get_total_activity

report_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

@report_router.get("/reports/activity", status_code=200)
async def activity_report(token: str = Depends(oauth2_scheme)):
    try:
        activity_data = await get_total_activity(token)
        return activity_data
    except HTTPException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)

@report_router.get("/reports/ratings-distribution", status_code=200)
async def ratings_distribution(token: str = Depends(oauth2_scheme)):
    try:
        get_rating = await get_rating_distribution(token)
        return get_rating
    except HTTPException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
    
@report_router.get("/reports/earnings", status_code=200)
async def earnings_report(token: str = Depends(oauth2_scheme)):
    try:
        get_total_earnings = await get_earnings(token)
        return get_total_earnings
    except HTTPException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
    
@report_router.get("/reports/distance-duration-averages", status_code=200)
async def distance_duration_averages(token: str = Depends(oauth2_scheme)):
    try:
        get_distance_duration = await get_distance_duration_averages(token)
        return get_distance_duration
    except HTTPException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)

@report_router.get("/reports/rates-info", status_code=200)
async def rates_info(token: str = Depends(oauth2_scheme)):
    try:
        get_rates = await get_rates_info(token)
        return get_rates
    except HTTPException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
