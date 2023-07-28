# Aerospective

## How to run:

It may be easiest to run Aerospective in a python virtual environment so you do not have to install all dependencies in your primary environment. Here are the steps to do that:

1) Navigated to the directory you have cloned this repository to in your CLI.
2) Run 'python -m venv venv' in that directory.
3) Activate the virtual environment by running
'./venv/Scripts/activate' on Mac or Linux, or by running 'venv\scripts\activate.bat' on Windows.
4) Run 'pip install -r requirements.txt'
5) Now, if you possess a 'config.py' file with a valid AirNow API key, run Aerospective with: 
'python aerospective_main.py'

The 'requirements.txt' file contains all dependencies necessary to run this program, and the above instructions will ensure you have them. If you do not wish to set up a venv, the following dependencies are required to be installed through 'pip':
- pgeocode
- urllib
- requests
- json
- pandas
- datetime
- dateutil

Once these are installed, there is one final step to run aerospective. An API key is required to interface with the EPA's API. You either will have already received the 'config.py' file from me, or you may create your own key. To create your own key, visit the EPA's AirNow website here: https://docs.airnowapi.org/login?index= 
1) Create an account. You will be provided a key upon account creation. 
2) Place that key in a file named 'config.py' using the following format:
'API_key = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
3) Ensure 'config.py' is located in the same directory as aerospective_main.py and the module .py files, then run aerospective_main.py per step 5 above.


## Using Aerospective

Aerospective only requires one input from you, which it will ask for: the zip code you would like data for. 

At the prompt: 'Please enter your zipcode (#####):'
simply provide the five digit zipcode (aerospective currently relies on the American EPA API and does not work outside of the US). You will be presented three bar charts depicting:

1) The worst days over the past three months to have been outside, considering an overall high mean AQI (in PM2.5) and overall high mean temperature (in Fahrenheit) represented as a bar graph. The worst date is shown on the right side of the graph.
![alt_text](https://i.imgur.com/Fsm9C2M.png)

2) The best days over the past three months to have been outside, considering an overall low mean AQI (in PM2.5) and overall low mean temperature (in Fahrenheit) represented as a bar graph. The best date is shown on the right side of the graph.
![alt_text](https://i.imgur.com/OlX2ksn.png)

3) A ranking of the previous 90 days, divided into 30 day periods, of which period had the overall highest and overall lowest AQI, with mean temperature shown, represented as a bar graph. The 30 day periods are ranked from left to right, best to worst.
![alt_text](https://i.imgur.com/lOXqhO4.png)

Should you present an area code without any reasonably close air monitoring stations, Aerospective will recognize this and advise you to run the program again with another zipcode. Most reasonably sized towns have at least one monitoring station.
