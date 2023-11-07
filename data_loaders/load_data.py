import io

import pandas as pd
import requests

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    url = "https://api.covid19india.org/state_district_wise.json"
    response = requests.get(url)
    js = response.json()
    return js


@test
def test_data(js, *args) -> None:
    assert js is not None, "The output is undefined"
