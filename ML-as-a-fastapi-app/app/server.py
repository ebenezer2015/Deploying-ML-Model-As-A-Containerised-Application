# 1. Library imports
import uvicorn
import pickle
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeatureAttributes(BaseModel):
    """
    FeatureAttributes model which describes the input features for predictions.

    Attributes:
        longitude (float): Longitude of the location.
        latitude (float): Latitude of the location.
        housing_median_age (float): Median age of the housing.
        total_rooms (float): Total number of rooms.
        total_bedrooms (float): Total number of bedrooms.
        population (float): Population of the area.
        households (float): Number of households.
        median_income (float): Median income of the households.
        ocean_proximity (str): Proximity to the ocean (categorical).
    """
    longitude: float
    latitude: float
    housing_median_age: float
    total_rooms: float
    total_bedrooms: float
    population: float
    households: float
    median_income: float
    ocean_proximity: str

# 2. Load the saved model object
def load_model():
    """
    Loads the best model from the specified pickle file.

    Returns:
        object: The loaded model.
    """
    with open('../best_model.pkl', 'rb') as f:
        loaded_model = pickle.load(f)
    return loaded_model

# Load the model outside the app
loaded_model = load_model()

# 3. Create the app object
app = FastAPI()

# 4. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    """
    Index route that opens automatically at the base URL.

    Returns:
        dict: A welcome message.
    """
    return {'message': 'Median House Price model API'}

# 5. Route with a single parameter, returns the parameter within a message
# Located at: http://127.0.0.1:8000/AnyNameHere# 
@app.get('/{name}')
def get_name(name: str):
    """
    Greets the user by name.

    Args:
        name (str): The name of the user.

    Returns:
        dict: A welcome message with the user's name.
    """
    return {'Welcome To Median House Price Prediction Task': f'{name}'}

@app.post('/predict')
async def predict(request: Request, data: FeatureAttributes):
    """
    Predicts the median house price based on the input features.

    Args:
        request (Request): The HTTP request.
        data (FeatureAttributes): A dictionary containing the features for prediction.

    Returns:
        dict: A dictionary containing the predicted median house price.

    Raises:
        HTTPException: If there is an error in processing the input data or prediction.
    """
    try:
        logger.info("Received request: %s", await request.json())
        data = data.dict()
        df = pd.DataFrame(data, index=[0])

        # Create dummy variables for the categorical feature
        df = pd.get_dummies(df, columns=['ocean_proximity'])

        # Ensure the DataFrame has the same columns as the training data
        model_columns = loaded_model.feature_names_in_
        df = df.reindex(columns=model_columns, fill_value=0)

        # Predict the outcome
        prediction = loaded_model.predict(df)[0]
        logger.info("Prediction: %s", prediction)
        return {'prediction': prediction}
    except Exception as e:
        logger.error("Error: %s", str(e))
        # Handle errors
        raise HTTPException(status_code=400, detail=str(e))

# 5. Run the API with uvicorn. It will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
