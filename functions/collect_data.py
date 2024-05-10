import requests
import base64
import json


def generate_auth_key(username: str, password: str):
    '''
    Input: Username and password
    Output: Auth Key
    Function to encode username and password
    '''
    # Encode username and password
    auth_key = base64.b64encode(bytes(f'{username}:{password}', 'utf-8'))

    return auth_key


def collect_service_metric_data(from_loc: str, to_loc: str, from_time: str,
                                to_time: str, from_date: str, to_date: str,
                                auth_key: str, days: str = 'WEEKDAY'):
    '''
    Input: Auth key and request parameters
    Output: List of train journey ids
    Function to collect unique train journey ids
    '''

    # Define service metric endpoint address
    url = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"

    # Define request payload
    payload = json.dumps({
        "from_loc": from_loc,
        "to_loc": to_loc,
        "from_time": from_time,
        "to_time": to_time,
        "from_date": from_date,
        "to_date": to_date,
        "days": days
    })

    # Define request headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {auth_key.decode("utf-8")}'
    }

    # Execute post request
    response = requests.request("POST", url, headers=headers, data=payload) \
        .json()

    # Collect list of specific train journey ids
    trains = []
    for i in range(len(response['Services'])):
        trains.append(response['Services'][i]
                      ['serviceAttributesMetrics']['rids'])

    # Flatten list of train ids
    trains = [x for xs in trains for x in xs]

    return trains


def collect_service_detail_data(rid: str, auth_key: str):
    '''
    Input: Train journey id and api auth key
    Output: Service detail endpoint response
    Function to collect service detail data from endpoint
    '''
    # Define endpoint url
    url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"

    # Define request payload
    payload = json.dumps({
        "rid": rid
    })

    # Define request header
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {auth_key.decode("utf-8")}',
    }

    # Execute service detail request
    response = requests.request("POST", url, headers=headers, data=payload)
    rid_response = response.json()['serviceAttributesDetails']

    return rid_response


def calculate_delay(rid_details: list, start_station: str,
                    end_station: str, logger):
    '''
    Input: Start and end station and train journey data
    Output: Train journey data with delay appended to dictionary object
    Function to calculate the delay of a specific train journey
    '''
    # Retrieve train journey departure time
    departure_time = [rid_detail for rid_detail in rid_details['locations']
                      if rid_detail['location'] ==
                      start_station][0]['gbtt_ptd']

    # Filter out data not associated with the final station
    arrival_data = [rid_detail for rid_detail in rid_details['locations']
                    if rid_detail['location'] == end_station][0]

    # Calculate delay at final station
    rid_details['delay'] = int(arrival_data['actual_ta']) \
        - int(arrival_data['gbtt_pta'])

    # Append departure time to dictionary
    rid_details['departure_time'] = departure_time

    # Log data
    log_message = f'Data collected for {rid_details["date_of_service"]}' + \
                  f' - {departure_time} from {start_station}'
    logger.info(log_message)

    return rid_details
