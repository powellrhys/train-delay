from functions.collect_data import generate_auth_key, \
    collect_service_metric_data, collect_service_detail_data, \
    calculate_delay

from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import datetime
import logging
import os

# Configure Logger
logger = logging.getLogger('BASIC')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler = logging.StreamHandler()
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

# Load Environment Variables
load_dotenv()
username = os.getenv('account_username')
password = os.getenv('account_password')

# Generate Base64 auth key
auth_key = generate_auth_key(username, password)

# Define start up config
data_present = False

# Configure page config
st.set_page_config(
    page_title="Home",
    page_icon=":light_rail:",
    layout='wide'
)

# Define page title and columns
st.title('Train Delay Dashboard')
col1, col2, col3 = st.columns([1, 1, 3])

# Generate column 1 components
with col1:
    start_date = str(st.date_input("Start Date", datetime.datetime.today()))
    start_time = str(st.time_input("Start Time", datetime.time(19, 00)))
    start_time = str(start_time[:2]) + start_time[3:5]
    start_station = str(st.text_input("Starting Station", "PAD"))
    button = st.button('Collect Data')

# Generate column 2 components
with col2:
    end_date = str(st.date_input("End Date", datetime.datetime.today()))
    end_time = str(st.time_input("End Time", datetime.time(23, 30)))
    end_time = str(end_time[:2]) + end_time[3:5]
    end_station = str(st.text_input("Destination Station", "CDF"))

    # Logic to execute if button is clicked
    if button:
        button = False

        # Generate spinner on page
        with st.spinner('Collecting Data...'):

            # Collect metric data from criteria specified on page
            logger.info('Collecting service metric data...')
            trains = collect_service_metric_data(start_station, end_station,
                                                 start_time, end_time,
                                                 start_date, end_date,
                                                 auth_key)
            logger.info('Service Metric Data Collected')

            # Iterate through each journey to collect specific journey data
            journey_details = []
            for rid in trains:

                try:
                    # Collect specific train journey data
                    rid_details = collect_service_detail_data(rid, auth_key)
                    rid_details = calculate_delay(rid_details, start_station,
                                                  end_station, logger)
                    journey_details.append(rid_details)

                except BaseException as error:
                    # Display error if we have failures
                    error_message = 'Unable to fetch data for rid: ' + \
                        f'{rid} - {error}'
                    logger.error(error_message)

            data_present = True

# Define column 3 components
with col3:

    # If we have collected data - display data in dataframe
    if data_present:
        df = pd.DataFrame(journey_details)
        df = df[['date_of_service', 'departure_time', 'delay']]
        df = df.rename(columns={"date_of_service": "Date",
                                "departure_time": "Depature Time",
                                "delay": "Delay (mins)"})
        df = df.sort_values(by='Delay (mins)', ascending=False)
        st.table(df.head(10))
