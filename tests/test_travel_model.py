import pytest
from pydantic import ValidationError

from models.travel_model import TravelInfoRequest, TravelInfoResponse


def test_travel_info_request_requires_all_fields():
    with pytest.raises(ValidationError):
        TravelInfoRequest(country_from="France")


def test_travel_info_request_valid():
    request = TravelInfoRequest(
        country_from="Ukraine",
        country_to="Germany",
        is_capital=True,
        is_weather=False,
        is_currency=True,
    )

    assert request.country_to == "Germany"


def test_travel_info_response_optional_fields_default_none():
    response = TravelInfoResponse(country_from="Ukraine", country_to="Germany")

    assert response.capital_to is None
    assert response.weather is None
    assert response.currency_code_from is None
    assert response.exchange_rate is None


def test_travel_info_response_currency_code_length_enforced():
    with pytest.raises(ValidationError):
        TravelInfoResponse(
            country_from="Ukraine",
            country_to="Germany",
            currency_code_from="TOOLONG",
        )
