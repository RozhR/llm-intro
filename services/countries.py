import os
from dataclasses import dataclass

import httpx
from fastapi import HTTPException
from loggers.logger_req import logger

COUNTRIES_URL = "https://api.restcountries.com/countries/v5"
API_KEY = os.environ.get("COUNTRY_API_KEY")

if not API_KEY:
    raise ValueError("COUNTRY_API_KEY environment variable is not set")


@dataclass
class CountryInfo:
    capital: str
    currency_code: str
    currency_name: str


async def get_country_info(country_name: str) -> CountryInfo:
    logger.debug(f"Fetching country info for {country_name}")
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(COUNTRIES_URL, params={"q": country_name, "limit": 10},
                                    headers={"Authorization": f"Bearer {API_KEY}"})
    except httpx.RequestError as exc:
        logger.error(f"Countries service unreachable: {exc}")
        raise HTTPException(status_code=502, detail="Countries service unreachable") from exc

    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        logger.error(f"Error fetch country info: {exc}")
        raise HTTPException(status_code=502, detail="Error fetch country info") from exc
    data = resp.json()
    objects = data.get("data", {}).get("objects", [])
    if not objects:
        logger.warning(f"Country {country_name} not found")
        raise HTTPException(status_code=400, detail=f"Country info not found: {country_name}")
    item = objects[0]
    try:
        capital = item["capitals"][0]["name"]
        currency_code = item["currencies"][0]["code"]
        currency_name = item["currencies"][0]["name"]
    except (KeyError, TypeError) as exc:
        logger.error(f"Unexpected country response for {country_name}: {exc}")
        raise HTTPException(status_code=502, detail=f"Unexpected country response for {country_name}") from exc
    return CountryInfo(capital=capital, currency_code=currency_code, currency_name=currency_name)
