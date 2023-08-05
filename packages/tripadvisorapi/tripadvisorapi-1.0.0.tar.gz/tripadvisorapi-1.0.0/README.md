# Tripadvisor Content API

This is a simple python wrapper for the [Tripadvisor Content API](https://tripadvisor-content-api.readme.io/reference/overview).

## Content API
- [Location Details](https://tripadvisor-content-api.readme.io/reference/getlocationdetails)
    - A Location Details request returns comprehensive information about a location (hotel, restaurant, or an attraction) such as name, address, rating, and URLs for the listing on Tripadvisor.
- [Location Photos ](https://tripadvisor-content-api.readme.io/reference/getlocationphotos)
    - The Location Photos request returns up to 5 high-quality photos for a specific location. The photos are ordered by recency.
- [Location Reviews](https://tripadvisor-content-api.readme.io/reference/getlocationreviews)
    - The Location Reviews request returns up to 5 of the most recent reviews for a specific location.
- [Location Search](https://tripadvisor-content-api.readme.io/reference/searchforlocations)
    - The Location Search request returns up to 10 locations found by the given search query. You can use category ("hotels", "attractions", "restaurants", "geos"), phone number, address, and latitude/longtitude to search with more accuracy.
- [Nearby Location Search](https://tripadvisor-content-api.readme.io/reference/searchfornearbylocations)
    - The Nearby Location Search request returns up to 10 locations found near the given latitude/longtitude.


## Example Code
Creating new API
```python
from tripadvisorapi import TripadvisorApi

# Initialize API with your API key

key = "YOUR_KEY"

api = TripadvisorApi(key)

```

Location Search
```python
api = TripadvisorApi(key)

res = api.location_search("Los Angeles")

res_json = json.loads(res.text)

print(res_json)
```