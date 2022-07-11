#!/usr/bin/env python3
import errno
import logging
import datetime

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

api = RecGovApi()
api.get_campground_availability(233723, first_day_of_month.strftime("%Y-%m-%d"))