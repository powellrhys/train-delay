# train-delay

## Overview

Train train-delay application is a Python application designed to provide users with information about the most delayed train times based on their journey parameters. The application utilizes the National Rail API to collect real-time train data and presents it through a user-friendly interface built with Streamlit.

## Features

- User-friendly Interface: The application offers a simple and intuitive interface created with Streamlit, allowing users to easily input their journey parameters.
- Real-time Data: Train Delay Finder fetches real-time train data from the National Rail API, ensuring that users receive up-to-date information about train delays.
- Customizable Parameters: Users can specify various parameters such as departure station, destination station, date, and time to tailor the search for delayed trains according to their specific journey requirements.

## Requirements
Python 3.9.1
Streamlit 1.34.0

## Installation

1. Clone the repository:

`git clone https://github.com/powellrhys/train-delay.git`

2. Install the required dependencies:

`pip install -r requirements.txt`

## Usage

1. Navigate to the project directory:

`cd train-delay`

2. Run the Streamlit application:

`streamlit run Home.py`

3. Access the application in your web browser by visiting the provided URL.

4. Enter your journey parameters, including departure station, destination station, date, and time.
Click on the "Collect Data" button to retrieve a list of the most delayed train times that meet the specified parameters.

5. View the results

## Deployed Version

The application itself can be found here: [train-delay](https://train-delay.azurewebsites.net/)
