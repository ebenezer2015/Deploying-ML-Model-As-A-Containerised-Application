import pickle
import pandas as pd
from flask import Flask, render_template, request, jsonify

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

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract input features from the form
        inputs = {
            'longitude': float(request.form['longitude']),
            'latitude': float(request.form['latitude']),
            'housing_median_age': float(request.form['housing_median_age']),
            'total_rooms': float(request.form['total_rooms']),
            'total_bedrooms': float(request.form['total_bedrooms']),
            'population': float(request.form['population']),
            'households': float(request.form['households']),
            'median_income': float(request.form['median_income']),
            'ocean_proximity': request.form['ocean_proximity']
        }

        # Create a DataFrame with the input features
        df = pd.DataFrame(inputs, index=[0])
        
        # Create dummy variables for the categorical feature
        df = pd.get_dummies(df, columns=['ocean_proximity'])
        
        # Ensure that the input DataFrame has the same columns as the training data
        model_columns = loaded_model.feature_names_in_
        df = df.reindex(columns=model_columns, fill_value=0)
        
        # Make predictions
        predictions = loaded_model.predict(df)
        
        # Return predictions in the HTML template
        result = predictions[0]
        return render_template('index.html', **locals())
    
    except Exception as e:
        # Handle errors (e.g., invalid data format)
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
