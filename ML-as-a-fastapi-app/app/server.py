# 1. Library imports
from fastapi import FastAPI
import uvicorn
import pickle
from base_model_ import FeatureAttributes
import numpy as np

# 2. Create the app object
def load_model():
    """Loads the best model from the specified pickle file."""
    with open('../best_model.pkl', 'rb') as f:
        loaded_model = pickle.load(f)
    return loaded_model

# Load the model outside the app
loaded_model = load_model()

app = FastAPI()

# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'Median House Price model API'}

# 4. Route with a single parameter, returns the parameter within a message
#    Located at: http://127.0.0.1:8000/AnyNameHere
@app.get('/{name}')
def get_name(name: str):
    return {'Welcome To Krish Youtube Channel': f'{name}'}

#@app.get('/')
#def read_root():
 #   return {'message': 'Median House Price model API'}

@app.post('/predict')
def predict(data:FeatureAttributes):
    """
    Predicts the class of a given set of features.

    Args:
        data (dict): A dictionary containing the features to predict.
        e.g. {"features": [1, 2, 3, 4]}

    Returns:
        dict: A dictionary containing the predicted class.
    """   
    
    data = data.dict()
    
    df = pd.DataFrame(data, index=[0])
        
    # Preprocess data if needed
    df = df.dropna(subset=df.columns)
    # Create dummy variables for the categorical feature
    df = pd.get_dummies(df, columns=['ocean_proximity'])

    # Ensure that the input DataFrame has the same columns as the training data
    model_columns = loaded_model.feature_names_in_
    df = df.reindex(columns=model_columns, fill_value=0)
    
    # Predict the outcome using the saved model
    prediction = loaded_model.predict(df)[0]
    
    return {'prediction': prediction} 

# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
#uvicorn app:app --reload