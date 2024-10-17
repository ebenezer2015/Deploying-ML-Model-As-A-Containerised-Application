from pydantic import BaseModel

# 2. Class which describes Model's features
class FeatureAttributes(BaseModel):
    longitude: float 
    latitude: float 
    housing_median_age: float 
    total_rooms: float 
    total_bedrooms: float 
    population: float 
    households: float 
    median_income: float 
    ocean_proximity: str
   