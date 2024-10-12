import streamlit as st
import pandas as pd
import pickle

# Load necessary data and models
df = pd.read_csv("cleaned_data.csv")

with open("encoded_ocean_proximity.pkl", 'rb') as f:
    encoder = pickle.load(f)

with open("scaler.pkl", 'rb') as f:
    scaler = pickle.load(f)

with open("best_model.pkl", 'rb') as f:
    model_ = pickle.load(f)

def pred_page():
    with st.expander("Dataframe"):
        st.info("This is a cleaned dataframe")
        st.dataframe(df)
    
    st.write("""### Please provide the details of the house:""")

    with st.sidebar:
        st.subheader("Input Features")
        
        # Collecting input values from sliders
        longitude = st.slider('Longitude', min_value=-125.0, max_value=-114.0, value=-120.0, step=0.1)
        latitude = st.slider('Latitude', min_value=32.0, max_value=42.0, value=37.0, step=0.1)
        housing_median_age = st.slider('Housing Median Age', min_value=1, max_value=100, value=30)
        total_rooms = st.slider('Total Rooms', min_value=1, max_value=10000, value=2000, step=50)
        total_bedrooms = st.slider('Total Bedrooms', min_value=1, max_value=5000, value=500, step=10)
        population = st.slider('Population', min_value=1, max_value=50000, value=1000, step=100)
        households = st.slider('Households', min_value=1, max_value=5000, value=300, step=10)
        median_income = st.slider('Median Income', min_value=0.0, max_value=15.0, value=3.5)
        ocean_proximity = st.selectbox('Ocean Proximity', ['<1H OCEAN', 'INLAND', 'NEAR BAY', 'NEAR OCEAN', 'ISLAND'])
    
    # Create a DataFrame from the input values
    input_data = pd.DataFrame({
        'longitude': [longitude],
        'latitude': [latitude],
        'housing_median_age': [housing_median_age],
        'total_rooms': [total_rooms],
        'total_bedrooms': [total_bedrooms],
        'population': [population],
        'households': [households],
        'median_income': [median_income],
        'ocean_proximity': [ocean_proximity]  # Original ocean_proximity input
    })
    
    # Apply OneHotEncoding to 'ocean_proximity' and concatenate the result
    ocean_proximity_encoded = encoder.transform(input_data[['ocean_proximity']]).toarray()
    ocean_proximity_df = pd.DataFrame(ocean_proximity_encoded, columns=encoder.get_feature_names_out(['ocean_proximity']))
    
    # Drop the original 'ocean_proximity' and add the encoded columns
    input_data = input_data.drop('ocean_proximity', axis=1)
    input_data = pd.concat([input_data, ocean_proximity_df], axis=1)

    st.write("Input Data for Prediction")
    st.dataframe(input_data)

    # Scale the data using the pre-fitted scaler (transform, not fit_transform)
    scaled_data = scaler.transform(input_data)
    
    # Make prediction using the pre-trained model
    prediction = model_.predict(scaled_data)[0]

    # Show predictions
    st.success(f"Predicted house price: ${prediction:,.2f}")

