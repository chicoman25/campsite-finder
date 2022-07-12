from email.mime import base
import pytest
import requests_mock
import logging
import json

from pathlib import Path
from campsitefinder import (
    ApiClient,
    RecGovApi,
    RecGovConnectionError
)

class TestApiClient:

    def setup_method(self):
        logging.basicConfig(level=logging.INFO)        
       
    # Tests building and appending of URL for API calls
    def test_url(self):
        base_url = "www.recreation.gov/api"
        self.api_client = ApiClient(base_url)
        expected = f"https://{base_url}/camps/campgrounds/250005"
        actual = self.api_client.url("camps/campgrounds/250005")
        assert actual == expected


class TestRecGovApi:
    def setup_method(self):
        self.api = RecGovApi()
        logging.basicConfig(level=logging.INFO)        
    
    # Recreation.gov uses CloudFront to serve content and will error with a 403 when a user-agent isn't present
    def test_should_fail_on_missing_user_agent(self):
        with requests_mock.Mocker() as mock:
            mock.get(
                "https://www.recreation.gov/api/camps/availability/campground/232368/month?start_date=2022-07-01T00%3A00%3A00.000Z",
                json={}, 
                status_code=403
            )
            with pytest.raises(RecGovConnectionError):
                # wipe out the default_headers which contain a real user-agent
                self.api.api_client.default_headers = {}
                self.api.get_campground_availability(232368, "2022-07-01")
    

    def test_get_campground_availability(self):
        response_value = self.read_json_data_file("campground-availability.json")
        with requests_mock.Mocker() as mock:
            mock.get(
                "https://www.recreation.gov/api/camps/availability/campground/232368/month?start_date=2022-07-01T00%3A00%3A00.000Z",
                json=response_value, 
                status_code=200
            )
            response = self.api.get_campground_availability(232368, "2022-07-01")
            assert response['count'] == len(response['campsites'])

    def test_get_campground(self):
        response_value = self.read_json_data_file("campground.json")
        with requests_mock.Mocker() as mock:
            mock.get(
                "https://www.recreation.gov/api/camps/campgrounds/232368",
                json=response_value, 
                status_code=200
            )
            campground_id = 232368
            response = self.api.get_campground(campground_id)
            assert response['campground']['facility_id'] == str(campground_id)

    def test_get_campsite(self):
        response_value = self.read_json_data_file("campsite.json")
        with requests_mock.Mocker() as mock:
            mock.get(
                "https://www.recreation.gov/api/camps/campsites/22956",
                json=response_value, 
                status_code=200
            )
            response = self.api.get_campsite(22956)
            assert "22956" == response['campsite']['campsite_id']
            
    
    def read_json_data_file(self, file_name):
        this_dir = Path(__file__).parent
        data_file = f"{this_dir.parent}/data/{file_name}"
        with open(data_file) as f:
            contents = json.load(f)
        return contents