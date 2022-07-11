# Campsite Finder 
Uses the Recreation.gov API to search for campground and campsite availability. 

## Installation
For local development:
	
	python3 -m venv ./env
    source ./env/bin/activate

When you're done:

	deactivate

## Running
The `run.py` script provides a few examples how to search for campgrounds and campsites.

	run.py

It's a fairly simple wrapper around the API providing a basic mechanism to do lookups

	from campsitefinder import (
    	RecGovApi
	)
	
	# Note: The recreation.gov API accepts date formates as yyyy-mm-dd and requires
	# the day to be the first of the month. Ex: 2022-07-01
	today = datetime.date.today()
	first_day_of_month = today.replace(day=1)

	api = RecGovApi()
	api.get_campground_availability(233723, first_day_of_month.strftime("%Y-%m-%d"))

## Testing
To run the suite of tests you can either

	make test

or 

	pytest tests/