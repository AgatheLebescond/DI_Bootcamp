Exercises XP
Last Updated: May 9th, 2025

Tutorial Overview: Building a Sales Prediction Web App from End to End
In this tutorial, you’ll go through a complete, hands-on project that takes you from zero to a working, interactive machine-learning application. By the end, you will have:

A clean Python development environment

Learn how to create and activate virtual environments (Windows and macOS)
Install all necessary dependencies in one place
The core libraries loaded and ready

Streamlit for UI
Pandas and NumPy for data handling
A trained Random Forest model (pickle) and scikit-learn preprocessing tools
Your trained ML model integrated into code

Unpack the saved model file (rf_model.pkl) to retrieve imputers, encoders, and the forest itself
Wrap standard scaling and categorical encoding exactly as during training
An interactive Streamlit interface

A polished layout with title, caption, and optional image
A sidebar that explains every input field—so users know exactly what to enter
Three-column input grid for all numerical and categorical features
A “Predict” button wired to your model pipeline

Convert user inputs into a DataFrame
Apply grouping of product families and all preprocessing steps
Feed the cleaned, encoded, and scaled data into the Random Forest
Display the resulting sales prediction immediately on screen
Local testing and deployment

Run streamlit run app.py to launch the app in your browser
Verify end-to-end functionality: from input sliders and dropdowns to live model output


What You’re Achieving
Reproducible Environment: Master environment management so your app runs anywhere.
Model Operationalization: Take a model off the shelf and embed it in a real-world tool.
User-Friendly UI: Turn raw code into an intuitive dashboard that non-technical users can operate.
Data Processing Best Practices: Apply the same imputers, encoders, and scalers you used in training—ensuring consistency and accuracy.
Rapid Prototyping with Streamlit: Learn how quickly you can go from a Python script to a shareable web app.


👩‍🏫 👩🏿‍🏫 What You’ll learn
How to set up and configure a Python environment for ML apps.
How to build an interactive ML web application using Streamlit.
How to load and use a trained machine learning model.
How to process user inputs, apply preprocessing, and make predictions.


🛠️ What you will create
You will create a sales prediction web app using a trained Random Forest model. Users can input various features related to a store and get predicted sales values displayed instantly.



🌟 Part I : Create Your Project Environment
Open your terminal.
Create a new directory for your project.
Navigate into the directory.
Create and activate a virtual environment:
if windows :



python -m venv venv; venv\Scripts\activate; python -m pip install -q --upgrade pip; python -m pip install -qr requirements.txt


if mac :



python3 -m venv venv; source venv/bin/activate; python -m pip install -q --upgrade pip; python -m pip install -qr requirements.txt


🌟 Part II : Install and Import Required Libraries
Ensure your environment has all the required libraries installed from requirements.txt
Then, in a new file called app.py, import the required libraries:


import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler


🌟 Part III : Load the Trained ML Model
Load the components from your saved model (rf_model.pkl):



with open("rf_model.pkl", "rb") as f:
    components = pickle.load(f)

num_imputer = components["..."]
cat_imputer = components["..."]
encoder = components["..."]
model = components["..."]
scaler = StandardScaler()


Make sure this file (rf_model.pkl) includes your trained model and any preprocessing objects like imputers or encoders.



🌟 Part IV : Build the Streamlit App Interface
Provide a title and introductory caption for your app. You can also add an image.
Create a sidebar to display input field descriptions for users for them to understand what is required for each input field.
Create input fields for users to enter data.


st.image("...")
st.title("...")
st.caption("...")

# Sidebar with input field descriptions
st.sidebar.header("Description of The Required Input Fields")
st.sidebar.markdown("**Store Number**: The number of the store.")
st.sidebar.markdown("**Product Family**: Product Family such as 'AUTOMOTIVE', 'BEAUTY', etc. "
                    "Details:\n"
                    " - **AUTOMOTIVE**: Products related to the automotive industry.\n"
                    " - **BEAUTY**: Beauty and personal care products.\n"
                   ...
                    " - **STATIONERY**: Stationery and office supplies.")
st.sidebar.markdown("**Number of Items on Promotion**: Number of items on promotion within a particular shop.")
st.sidebar.markdown("**City**: ...")
st.sidebar.markdown("**Cluster**: ...")
st.sidebar.markdown("**Transactions**: ...")
st.sidebar.markdown("**Crude Oil Price**: ...")


# Create the input fields
input_data = {}
col1,col2,col3 = st.columns(3)
with col1:
    input_data['store_nbr'] = st.slider("Store Number",0,54)
    input_data['family'] = st.selectbox("Product Family", ['AUTOMOTIVE', ...'])
    # Number of items on promotions
    input_data['onpromotion'] =...
    input_data['state'] = st.selectbox("State Where The Store Is Located", ['Pichincha', 'Cotopaxi', 'Chimborazo', 'Imbabura',
       'Santo Domingo de los Tsachilas', 'Bolivar', 'Pastaza', 'Tungurahua', 'Guayas', 'Santa Elena', 'Los Rios', 'Azuay', 'Loja',
       'El Oro', 'Esmeraldas', 'Manabi'])
    input_data['transactions'] = ...

with col2:
    input_data['store_type'] = 
    input_data['cluster'] = 
    # Add more fields in col2

with col3:
    input_data['month'] = 
    input_data['day'] =
    input_data['dayofweek'] = 


🌟 Part V : Create a button to trigger predictions
Complete this section of the code that takes the user input, applies the necessary preprocessing steps including categorical encoding and scaling, and then uses the trained model to predict the sales. The predicted sales value is then displayed to the user.



# Create a button to make a prediction
if st.button("Predict"):
  # Convert the input data to a pandas DataFrame
    input_df = pd.DataFrame([input_data])    # Product Categorization Based on Families
    food_families = ['BEVERAGES', ...']
    home_families = ['HOME AND KITCHEN I', ...]
    clothing_families = ['...]
    grocery_families = [...]
    stationery_families = [...]
    cleaning_families = [...]
    hardware_families = [...]    # Apply the same preprocessing steps as done during training
    input_df['family'] = np.where(input_df['family'].isin(food_families), 'FOODS', input_df['family'])
    input_df['family'] = ...
    input_df['family'] =...
    input_df['family'] = ...
    input_df['family'] = ...
    input_df['family'] = ...
    input_df['family'] = ...
    input_df_cat = input_df[categorical_columns].copy()
    input_df_num = ...
    input_df_cat_imputed = cat_imputer.transform(input_df_cat)
    input_df_num_imputed = ...    # Encode categorical features
    input_df_cat_encoded = pd.DataFrame(encoder.transform(input_df_cat_imputed).toarray(),
                                        columns=encoder.get_feature_names_out(categorical_columns))    # Scale numerical features
    input_df_num_scaled = scaler.transform(input_df_num_imputed)
    input_df_num_sc = ...    # Combine encoded categorical features and scaled numerical features
    input_df_processed = ...  # Make predictions using the trained model
    predictions = ...   # Display the predicted sales value to the user:
    st.write("The predicted sales are:", predictions[0])


🌟 Part VI : Run the Streamlit App
To launch your app, use this command in the terminal:



streamlit run app.py
# This will start a local server and open the app in your default web browser.