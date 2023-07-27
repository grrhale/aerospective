# Aerospective



## How to run:

It may be easiest to run Aerospective in a python virtual environment so you do not have to install all dependencies in your primary environment. Here are the steps to do that:

1) Navigated to the directory you have cloned this repository to in your CLI.
2) Run 'python -m venv venv' in that directory.
3) Activate the virtual environment by running
'./venv/Scripts/activate'
4) Run 'pip install -r requirements.txt'
5) Now, run Aerospective with: 
'python aerospective_main.py'

The 'requirements.txt' file contains all dependencies necessary to run this program, and the above instructions will ensure you have them. If you do not wish to set up a venv, the following dependencies are required to be installed through 'pip':
- pgeocode
- urllib
- requests
- json
- pandas
- datetime
- dateutil

Once these are installed, running 'python aerospective_main.py' in the cloned/downloaded repo directory should function as expected.


## Using Aerospective

Aerospective only requires one input from you, which it will ask for: the zip code you would like an aerospective for. 

At the prompt: 'Please enter your zipcode (#####):'
simply provide the five digit zipcode (aerospective currently relies on the American EPA API and does not work outside of the US). You will be presented three bar charts depicting:

1) The worst days over the past three months to have been outside, considering an overall high mean AQI (in PM2.5) and overall high mean temperature (in Fahrenheit).

2) The best days over the past three months to have been outside, considering an overall low mean AQI (in PM2.5) and overall low mean temperature (in Fahrenheit).

3) A ranking of the previous three months, divided into 30 day periods, of the lowest mean AQI/lowest mean temperature to the highest of each. 
