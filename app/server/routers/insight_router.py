from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from server.services.insighs.financial_summary_service import get_financial_summary
from server.services.insighs.trip_analysis_service import get_trip_analysis
from server.services.insighs.user_behavior_service import get_user_behavior_insights
from server.services.insighs.driver_performance_service import get_driver_performance

insight_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

@insight_router.get("/insights/driver-performance")
async def driver_performance(token: str = Depends(oauth2_scheme)):
    try:
        get_driver_perf = await get_driver_performance(token)
        return get_driver_perf
    except HTTPException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)


@insight_router.get("/insights/user-behavior")
async def user_behavior(token: str = Depends(oauth2_scheme)):
    try:
        get_user_behavior = await get_user_behavior_insights(token)
        return get_user_behavior
    except HTTPException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
    

@insight_router.get("/insights/trip-analysis")
async def trip_analysis(token: str = Depends(oauth2_scheme)):
    try:
        get_trip_analys = await get_trip_analysis(token)
        return get_trip_analys
    except HTTPException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)


@insight_router.get("/insights/financial-summary")
async def financial_summary(token: str = Depends(oauth2_scheme)):
    try:
        get_financial_summ = await get_financial_summary(token)
        return get_financial_summ
    except HTTPException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)