"""
Recreation.gov provides a programatic way to look up campsite availability by month. 
Example Recreation.gov availability endpoint (with start date specifier):
  https://www.recreation.gov/api/camps/availability/campground/232487/month?start_date=2020-08-01T00%3A00%3A00.000Z
  Sample campground endpoint:
    https://www.recreation.gov/api/camps/campgrounds/250005
  Sample campsites endpoint:
     https://www.recreation.gov/api/camps/campsites/4522
  Sample campground website link:
    https://www.recreation.gov/camping/campgrounds/250005
"""
import json
import logging
import string
import requests

logger = logging.getLogger(__name__)

class ApiClient:
  default_headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
  }

  def __init__(self, baseurl, headers = None):
    """Return a new Client instance."""
    self.baseurl = baseurl
    if headers:
        self.headers = headers
    else:
        self.headers = self.default_headers.copy()

  def url(self, addurl=None):
    """Return the url for the API endpoint."""
    path = f"https://{self.baseurl}"
    if addurl is not None:
        path += f"/{addurl}"
    return path

  def get(self, addurl, params = None):
    """Make an API call using the GET method."""
    url = self.url(addurl)

    try:
      logger.debug("Making GET request to URL: %s", url)
      response = requests.get(
        url, 
        params = params,
        headers = self.headers
      )
      json_response = response.json()
      logger.debug("HTTP Response: %s", json_response)
      return json_response

    except Exception as err:
        logger.debug("Exception in HTTP Response: %s - %s", response.status_code, response.content)


class RecGovApi:
  """Class for fetching data from Recreation.gov"""
  def __init__(self):
    self.base_url = "www.recreation.gov/api"
    self.campground_availability_url = "camps/availability/campground"
    self.campsite_url = "camps/campsites"
    self.api_client = ApiClient(self.base_url)

  def get_campground_availability(self, campground_id: int, start_month: string):
    url = f"{self.campground_availability_url}/{campground_id}/month?start_date={start_month}T00%3A00%3A00.000Z"
    return self.api_client.get(url)

  def get_campsite(self, campsite_id):
    url = f"{self.campsite_url}/{campsite_id}"
    return self.api_client.get(url)