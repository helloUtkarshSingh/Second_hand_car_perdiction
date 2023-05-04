import streamlit as st
import pickle 
import numpy as np
from PIL import Image
import base64

model = pickle.load(open("Car_price_prediction.pkl",'rb'))
df = pickle.load(open('df.pkl','rb'))

def perdict_car_price(year,brand,Model,km_driven,fuel_type,seller_Type,transmission,owner):

    #predict_data = np.array([2007,70000,'Petrol','Individual','Manual','First Owner','Maruti','800 AC']).reshape(1,-1)
    predict_data = np.array([year,km_driven,fuel_type,seller_Type,transmission,owner,brand,Model]).reshape(1,-1)
    
    prediction = model.predict(predict_data)

    prediction = np.round(prediction[0],0)

    return prediction

def main(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    html_template ="""
    <h1 style='color: linear-gradient;'>CarPriceWizard</h1>
    <p>Magically Predicting Your Car's Price.</p>
    <style>
        .stApp {
             background-image: url("Background.png");
             background-attachment: fixed;
             background-size: cover
         }
       footer {visibility: hidden;}
       </style>
    """
    im = Image.open('download.png')
    st.set_page_config(layout="centered",page_title="CarPriceWizard", page_icon = im)
   
    st.write(html_template, unsafe_allow_html=True,_class='my-text')

    left,middel,right,= st.columns(3)   
    with left:     
        year = st.text_input("Year of manufacture: ")  
        transmission = st.selectbox("Select Transmission Type",df['Transmission'].unique())
        fuel_type = st.radio('Select a fuel type',df['Fuel Type'].unique())
        owner = st.selectbox("Type of Owner",df['Owner'].unique())   
     
    with right:     
        brand = st.selectbox("Select your favorite brand:",df['Brand Name'].unique())
        brand_model = df[df['Brand Name']==brand]['Model Name'].unique()
        Model = st.selectbox("Select your favorite model:",brand_model)
        km_driven  =st.slider('Kilometer Drive', min_value=1, max_value=2360457, step=1000, value=500)
        seller_Type	= st.selectbox("Select Seller Type",df['Seller Type'].unique())
    
    result = ""
    if (st.button('Predict',help="Click to know the price of your car.")):
        result = perdict_car_price(year,brand,Model,km_driven,fuel_type,seller_Type,transmission,owner)

    st.success("The price of the car is: {} ".format(result))

    
    
    #print(year,brand,Model,km_driven,fuel_type,seller_Type,transmission,owner)

if __name__ == '__main__':
    main('Background2.jpg')