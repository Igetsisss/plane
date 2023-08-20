from FlightRadar24 import FlightRadar24API
import re
import webbrowser
import time
import pyautogui

# Replace with your actual API key
api_key = "your_api_key_here"
fr_api = FlightRadar24API(api_key)

# Set your bounds or zone as needed
bounds = "33.892658,33.7993677,-84.5913579,-84.1958444"

previous_tail_number = None

while True:
    data = fr_api.get_flights(bounds=bounds)

    if data == []:
        print("NO PLANES")
        pyautogui.hotkey('ctrl', 'w')
    else:
        print(data)

    input_string = data

    pattern = r'<\((.*?)\) (N[0-9A-Z]+) - Altitude: (\d+) - Ground Speed: (\d+) - Heading: (\d+)>'

    matches = re.finditer(pattern, str(input_string))
    data_list = []

    for match in matches:
        model = match.group(1)
        tail_number = match.group(2)
        altitude = int(match.group(3))
        ground_speed = int(match.group(4))
        heading = int(match.group(5))
        
        data_list.append({
            'model': model,
            'tail_number': tail_number,
            'altitude': altitude,
            'ground_speed': ground_speed,
            'heading': heading
        })
        
        if tail_number != previous_tail_number:
            url = f"https://www.flightradar24.com/{tail_number}/3d"
            webbrowser.open(url)
            previous_tail_number = tail_number

    print(data_list)
    
    # Add a delay before the next iteration to avoid excessive API requests
    time.sleep(3)  # Sleep for 5 minutes
