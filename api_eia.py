"""Module for API calls to the Energy Information Administration (EIA)"""

# imports
import pandas as pd
import requests

from keys import eia_api_key

api_url = "https://api.eia.gov/v2/electricity/electric-power-operational-data/data/"


def api_test():
    """Test the API call"""
    print("Testing the API call")
    url = api_url + "?api_key=" + eia_api_key()

    response = requests.get(url)

    # turn the response into a dataframe
    print(response.json())

    print(response.status_code)


if __name__ == "__main__":
    api_test()
