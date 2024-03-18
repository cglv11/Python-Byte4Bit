import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from ..graphql_service import execute_graphql_query

async def get_trip_data(token: str):
    trip_query = """
    query {
        trips {
            trips {
                distance
                duration
                fare
                origin
                startDateTime
            }
        }
    }
    """
    response = await execute_graphql_query(trip_query, token=token)
    trip_data = response.get("data", {}).get("trips", {}).get("trips", [])
    return trip_data

async def get_financial_summary(token: str):
    trip_data = await get_trip_data(token)

    # Convertir a DataFrame de Pandas
    df = pd.DataFrame(trip_data)
    df['distance'] = pd.to_numeric(df['distance'], errors='coerce')
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
    df['fare'] = pd.to_numeric(df['fare'], errors='coerce')
    df.dropna(inplace=True)  # Descartar filas con valores nulos

    # Análisis de la relación entre distancia, duración y tarifa
    X = df[['distance', 'duration']]
    y = df['fare']
    model = LinearRegression().fit(X, y)
    relationship_summary = {
        'coefficient_distance': model.coef_[0],
        'coefficient_duration': model.coef_[1],
        'intercept': model.intercept_
    }

    # Predicción de ingresos (esto es un ejemplo muy simplificado)
    df['startDateTime'] = pd.to_datetime(df['startDateTime'])
    df['month'] = df['startDateTime'].dt.month
    monthly_income = df.groupby('month')['fare'].sum()
    income_trend = LinearRegression().fit(monthly_income.index.values.reshape(-1, 1), monthly_income.values)
    predicted_next_month_income = income_trend.predict(np.array([[monthly_income.index.max() + 1]]))[0]

    # Rentabilidad por zona geográfica
    profitability_by_area = df.groupby('origin')['fare'].sum().sort_values(ascending=False).to_dict()

    return {
        'Relationship summary': relationship_summary,
        'Predicted next month income': predicted_next_month_income,
        'Profitability by area': profitability_by_area
    }
