import streamlit as st
import http.client
import json
from datetime import datetime

def get_trains_between_stations(from_station, to_station, date_of_journey):
    conn = http.client.HTTPSConnection("irctc1.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "675713ba0dmshe4d2b0991f5f10dp10f5c5jsn1ab79e2b5f4e",  # Replace with your actual API key
        'x-rapidapi-host': "irctc1.p.rapidapi.com"
    }
    
    journey_date = date_of_journey.strftime("%Y-%m-%d")
    
    conn.request("GET", f"/api/v3/trainBetweenStations?fromStationCode={from_station}&toStationCode={to_station}&dateOfJourney={journey_date}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    
    return json.loads(data.decode("utf-8"))

def check_seat_availability(train_no, class_type, from_station, to_station, journey_date):
    conn = http.client.HTTPSConnection("irctc1.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "eb00fc7232msh56b6731540c6937p1937aajsnfdba7b3702f2", 
        'x-rapidapi-host': "irctc1.p.rapidapi.com"
    }
    
    conn.request("GET", f"/api/v1/checkSeatAvailability?classType={class_type}&fromStationCode={from_station}&quota=GN&toStationCode={to_station}&trainNo={train_no}&date={journey_date}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    
    return json.loads(data.decode("utf-8"))

st.title("Train Schedule Finder")

from_station = st.text_input("Enter From Station Code (e.g., PUNE):", "PUNE")
to_station = st.text_input("Enter To Station Code (e.g., AMI):", "AMI")

date_of_journey = st.date_input("Select Date of Journey:", datetime.now())

busy_hours_pune = {
    "Monday": [("00:00", "02:00"), ("09:00", "13:00"), ("15:00", "19:00"), ("23:00", "23:59")],
    "Tuesday": [("00:00", "00:00"), ("04:00", "05:00"), ("10:00", "20:00")],
    "Wednesday": [("03:00", "03:00"), ("09:00", "09:00"), ("12:00", "14:00"), ("22:00", "22:00")],
    "Thursday": [("09:00", "09:00"), ("11:00", "17:00")],
    "Friday": [("03:00", "04:00"), ("08:00", "08:00"), ("10:00", "10:00"), ("12:00", "18:00")],
    "Saturday": [("00:00", "03:00"), ("10:00", "13:00"), ("16:00", "20:00")],
    "Sunday": [("16:00", "16:00")]
}
busy_hours_dinagaon = {
    "Monday": [("14:00", "15:00"), ("20:00", "23:59")],
    "Tuesday": [("08:00", "09:00"), ("19:00", "23:00")],
    "Wednesday": [],
    "Thursday": [("19:00", "23:00")],
    "Friday": [("18:00", "20:00")],
    "Saturday": [("18:00", "23:00")],
    "Sunday": [("20:00", "23:00")]
}

busy_hours_jalamb = {
    "Monday": [("14:00", "16:00"), ("20:00", "23:00")],
    "Tuesday": [("15:00", "17:00"), ("22:00", "22:00")],
    "Wednesday": [("20:00", "23:00")],
    "Thursday": [("09:00", "10:00"), ("21:00", "22:00")],
    "Friday": [("20:00", "23:00")],
    "Saturday": [("08:00", "09:00"), ("21:00", "22:00")],
    "Sunday": [("15:00", "16:00"), ("20:00", "23:00")]
}

busy_hours_shivajinagar =  {
    "Monday": [("09:00", "10:00"), ("16:00", "20:00")],
    "Tuesday": [("09:00", "10:00"), ("17:00", "20:00")],
    "Wednesday": [("09:00", "10:00"), ("16:00", "21:00")],
    "Thursday": [("09:00", "10:00"), ("17:00", "20:00")],
    "Friday": [("17:00", "21:00")],
    "Saturday": [("09:00", "10:00"), ("16:00", "21:00")],
    "Sunday": [("18:00", "20:00")]
}

busy_hours_hingoli = {
    "Monday": [("16:00", "18:00"), ("21:00", "23:00")],
    "Tuesday": [("16:00", "17:00"), ("21:00", "23:00")],
    "Wednesday": [("16:00", "18:00"), ("22:00", "23:00")],
    "Thursday": [("09:00", "10:00"), ("16:00", "18:00")],
    "Friday": [("16:00", "17:00"), ("21:00", "23:00")],
    "Saturday": [("16:00", "18:00"), ("21:00", "23:00")],
    "Sunday": [("10:00", "11:00"), ("16:00", "17:00"), ("21:00", "23:00")]
}
def is_within_busy_hours(departure_time, busy_hours):
    """Check if the departure time is within any of the busy hour ranges."""
    departure_time = datetime.strptime(departure_time, "%H:%M").time()
    
    for start, end in busy_hours:
        start_time = datetime.strptime(start, "%H:%M").time()
        end_time = datetime.strptime(end, "%H:%M").time()
        
        # Check if departure time is within the range
        if start_time <= departure_time <= end_time:
            return True
    return False

def parse_date(date_str):
    """Convert date string from 'dd-mm-yyyy' to datetime object."""
    return datetime.strptime(date_str, "%d-%m-%Y")

senior_citizen = st.checkbox("Senior Citizen")

if 'page' not in st.session_state:
    st.session_state.page = 'main'

if st.session_state.page == 'main':
    if st.button("Find Trains"):
        with st.spinner('Fetching train data...'):
            try:
                train_data = get_trains_between_stations(from_station, to_station, date_of_journey)
                if train_data and "data" in train_data:
                    for train in train_data["data"]:
                        train_departure_time = train['from_std']  
                        train_date = parse_date(train['train_date'])  
                        train_day_of_week = train_date.strftime('%A')

                        if senior_citizen:
                            if from_station == 'PUNE':
                                busy_hours = busy_hours_pune
                            if from_station == 'DIQ':
                                busy_hours = busy_hours_dinagaon
                            if from_station == 'HNL':
                                busy_hours = busy_hours_hingoli
                            if from_station == 'JM':
                                busy_hours = busy_hours_jalamb
                            if from_station == 'SVJR':
                                busy_hours = busy_hours_shivajinagar
                            if is_within_busy_hours(train_departure_time, busy_hours[train_day_of_week]):
                                continue  

                        st.header(f"{train['train_number']} {train['train_name']}")
                        run_days = " ".join(train['run_days'])
                        st.write(f"Runs on: {run_days}")
                        st.write(f"{train['train_type']} ({train['train_number']} Running Status)")

                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.write(f"{train['from_station_name']} {train['from_std']} | {train_date.strftime('%Y-%m-%d')}")
                        with col2:
                            st.write(f"{train['duration']} hr")
                        with col3:
                            st.write(f"{train['to_station_name']} {train['to_std']} | Next Day")

                        # with st.expander(f"Show Availability for {train['train_name']}", expanded=False):
                        #     availability_data = check_seat_availability(
                        #         train['train_number'],
                        #         "2A",  
                        #         from_station,
                        #         to_station,
                        #         date_of_journey.strftime("%Y-%m-%d")
                        #     )
                            
                        #     if availability_data and "data" in availability_data:
                        #         for avail in availability_data["data"]:
                        #             st.write(f"Date: {avail['date']} - Status: {avail['current_status']} - Fare: ₹{avail['total_fare']}")
                        #     else:
                        #         st.error("No availability data found.")
                else:
                    st.error("No data found for the given inputs.")
            except Exception as e:
                st.error(f"Error fetching train data: {e}")
