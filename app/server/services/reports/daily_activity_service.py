import pandas as pd
from typing import Dict, Any
from datetime import datetime
from fastapi import HTTPException

from server.services.graphql_service import execute_graphql_query


async def get_total_activity(token: str) -> Dict[str, Any]:
    query = """
    query {
        trips {
            trips {
                startDateTime
            }
        }
    }
    """
    
    try:
        # Ejecutas la consulta para obtener las fechas de inicio de los viajes
        response = await execute_graphql_query(query, token=token)
        trips_data = response.get("data", {}).get("trips", {}).get("trips", [])
        
        # Convertir la lista de viajes a un DataFrame de Pandas
        df = pd.DataFrame(trips_data)
        
        # Asegurarse de que startDateTime es del tipo datetime para su procesamiento
        df['startDateTime'] = pd.to_datetime(df['startDateTime'])
        
        # Agregar columnas para agrupar por día, semana y mes
        df['day'] = df['startDateTime'].dt.date
        df['week'] = df['startDateTime'].dt.isocalendar().week
        df['month'] = df['startDateTime'].dt.month
        
        # Contar el número de viajes por día, semana y mes
        daily_activity = df.groupby('day').size().to_dict()
        weekly_activity = df.groupby('week').size().to_dict()
        monthly_activity = df.groupby('month').size().to_dict()
        
        return {
            "Daily activity": {f"day {str(key)}": int(value) for key, value in daily_activity.items()},
            "Weekly activity": {f"week {str(key)}": int(value) for key, value in weekly_activity.items()},
            "Monthly activity": {f"month {str(key)}": int(value) for key, value in monthly_activity.items()},
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
