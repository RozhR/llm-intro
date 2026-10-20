import pytest
from pydantic import ValidationError

from models.travel_model import TravelInfoRequest, TravelInfoResponse

# TODO: Add tests for TravelInfoRequest and TravelInfoResponse

def test_travel_info_request_requires_all_fields():
    with pytest.raises(ValidationError):
        TravelInfoRequest(country_from="France")