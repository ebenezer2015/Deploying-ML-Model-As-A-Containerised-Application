import pickle
import pandas as pd
from flask import Flask, render_template, request

def load_model():
    """Loads the best model from the specified pickle file."""
    with open('best_model.pkl', 'rb') as f:
        loaded_model = pickle.load(f)
    return loaded_model

app = Flask(__name__)

@app.route('/')
def home():
    result = ''
    return render_template('index.html', **locals())

# Load the model outside the Flask app
loaded_model = load_model()

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    try:
        longitude = float(request.form['longitude'])
        latitude = float(request.form['latitude'])
        housing_median_age = float(request.form['housing_median_age'])
        total_rooms = float(request.form['total_rooms'])
        total_bedrooms = float(request.form['total_bedrooms'])
        population = float(request.form['population'])
        households = float(request.form['households'])
        median_income = float(request.form['median_income'])
        ocean_proximity = request.form['ocean_proximity']
        
        data = {
        'longitude': longitude,
        'latitude': latitude,
        'housing_median_age': housing_median_age,
        'total_rooms': total_rooms,
        'total_bedrooms': total_bedrooms,
        'population': population,
        'households': households,
        'median_income': median_income,
        'ocean_proximity': ocean_proximity
        }
    
        df = pd.DataFrame(data, index=[0])
        
        # Preprocess data if needed
        df = df.dropna(subset=df.columns)
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        # Create dummy variables for the categorical feature
        df = pd.get_dummies(df, columns=categorical_columns)
    
        # Ensure that the input DataFrame has the same columns as the training data
        model_columns = loaded_model.feature_names_in_
        df = df.reindex(columns=model_columns, fill_value=False)
        
        # Make predictions
        predictions = loaded_model.predict(df)
    
        # Return predictions in JSON format
        return render_template('index.html', **locals())
    
    except Exception as e:
        # Handle errors (e.g., invalid data format)
        return jsonify({'error': str(e)}), 400  # Return error responseexcept Exception as e:

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)