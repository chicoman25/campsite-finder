#!/usr/bin/env python3
import errno
import logging
import datetime
from unicodedata import name

from campsitefinder import (
    RecGovApi
)

# Configure debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Example Dates
# Note: The recreation.gov API accepts date formates as yyyy-mm-dd and requires
# the day to be the first of the month. Ex: 2022-07-01
today = datetime.date.today()
first_day_of_month = today.replace(day=1)

class Campsite(object):
    def __init__(self, campsite_id, campground):
        self.campsite_id = campsite_id
        self.campground = campground #the campground this site belongs to

class Campground(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name


class AvailableSite:
    def __init__(self, campsite, date):
        self.campsite = campsite
        self.date = date

    def __str__(self):
        return "f{campsite} : {date}"


api = RecGovApi()
# api.get_campground_availability(233723, first_day_of_month.strftime("%Y-%m-%d"))

Campgrounds = dict[int, str]
campgrounds = {
    232152: "Dinner Station",
    10165480: "Mosca"
    # 10165500: "North Bank",
    # 10165576: "Rivers End",
    # 232154: "Lakeview Gunnison",
    # 232157: "Rosy Lane"
}


available_sites = []
for campground in campgrounds:
    logger.info(f"Processing campground {campground}")
    response = api.get_campground_availability(campground, first_day_of_month.strftime("%Y-%m-%d"))
    campsites = response['campsites']
    for site_id, site_details in campsites.items():
        availabilities = site_details['availabilities']
        if availabilities:
            for date_key,status in availabilities.items():
                if status == "Available":
                    logger.debug(f"Found available site at {campgrounds[campground]}: {site_details['campsite_id']}, {site_details['site']}, {date_key}" )
                    available_date = datetime.datetime.strptime(date_key, "%Y-%m-%dT%H:%M:%SZ")
                    available_site = AvailableSite(site_details['campsite_id'], available_date)
                    available_sites.append(available_site)
    

print(available_sites)
