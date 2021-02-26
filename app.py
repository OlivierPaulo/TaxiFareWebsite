import streamlit as st
import requests
import datetime
from Tools.utils import geocoder_here
from PIL import Image


title1, title2 = st.beta_columns([1,5])
image = Image.open('images/lewagon.png')
with title1:
    st.image(image, caption='Le Wagon', width=64, use_column_width=None)
with title2:
    st.title("TaxiFare - Batch #555 Lisbon")


st.markdown("## Datetime")
date_col1, date_col2 = st.beta_columns(2)
### Request Date of the course ###
with date_col1:
    d = st.date_input(
        "Please choose the the *pickup date* of the course",
        datetime.date(2021, 2, 26))

with date_col2:
    ### Request Time of the course ###
    t = st.time_input('Please choose the the *pickup time* of the course', datetime.time(11, 30, 00))

### Format the datetime for our API ###
pickup_datetime = f"{d} {t} UTC"

### Display the Pickup Datetime ###
st.success(f'Pickup datetime : {pickup_datetime}')

### Request the Pickup location ###
st.markdown("## Locations")


loc_col1, loc_col2 = st.beta_columns([20,20])
with loc_col1:
    st.markdown("### Pickup Location")
    pickup_adress = st.text_input("Please enter the pickup address", "251 Church St, New York, NY 10013")

    ### Getting Coordinates from Address locations ###
    error1 = ""

    try:
        pickup_coords = geocoder_here(pickup_adress)
    except IndexError:
        error1 = "Pickup Address invalide, default coordinates : "
        pickup_coords = {
            "longitude": -73.9798156,
            "latitude": 40.7614327
        }
    
    pickup_longitude = pickup_coords['longitude']
    pickup_latitude = pickup_coords['latitude']

    ### Displaying the Pickup Coordinates ###
    if error1 == "":
        st.success(f'Lat: {pickup_latitude}, Lon : {pickup_longitude}')
    else:
        st.error(f'"{pickup_adress}" {error1} \n Lat : {pickup_latitude}, Lon : {pickup_longitude}')


with loc_col2:
    ### Request the Dropoff location ###
    st.markdown("### Dropoff Location")
    dropoff_address = st.text_input("Please enter the dropoff address", "434 6th Ave, New York, NY 10011")

    ### Getting Coordinates from Address locations ###
    error2 = ""
    try:
        dropoff_coords = geocoder_here(dropoff_address)
    except IndexError:
        error2 = "Dropoff Address invalide, default coordinates : "
        dropoff_coords = {
            "longitude": -73.9797156,
            "latitude": 40.6413111
        }
    
    dropoff_longitude = dropoff_coords['longitude']
    dropoff_latitude = dropoff_coords['latitude']

    ### Displaying the Pickup Coordinates ###
    if error2 == "":
        st.success(f'Lat : {dropoff_latitude}, Lon : {dropoff_longitude}')
    else:
        st.error(f'"{dropoff_address}" {error2} Lat: {dropoff_latitude}, Lon: {dropoff_longitude}')

### Request the Passenger Count ###
st.markdown("## Number of Passengers")
passenger_count = st.slider('Number of passengers', 1, 9, 1)

### Display the numer of passenger ###
st.success(f'Number of passengers : {passenger_count}')




### Launch Fare Prediction ###
st.markdown("## Prediction")
if st.button('Get Fare Prediction'):

    params = {
        "key" : str(pickup_datetime),
        "pickup_datetime" : str(pickup_datetime),
        "pickup_longitude": float(pickup_longitude),
        "pickup_latitude": float(pickup_latitude),
        "dropoff_longitude" : float(dropoff_longitude),
        "dropoff_latitude": float(dropoff_latitude),
        "passenger_count": int(passenger_count)
    }   
    local_api_url = f"http://127.0.0.1:8000/predict_fare"
    cloud_url = "https://predict-api-vwdzl6iuoa-ew.a.run.app/predict_fare"
    response = requests.get(
    url=cloud_url, params=params
    ).json()

    st.info(f"Taxi Fare Predication 🎉 : {round(response['prediction'], 2)}$")

