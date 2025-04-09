# # # popular.py
# # from flask import Blueprint, render_template
# # import requests
# # from app import save_locations_to_db

# # popular_bp = Blueprint('popular', __name__)

# # def fetch_osm_tourist_spots(city_name="Jaipur"):
# #     overpass_url = "http://overpass-api.de/api/interpreter"
# #     query = f"""
# #     [out:json][timeout:25];
# #     area[name="{city_name}"]->.searchArea;
# #     (
# #       node["tourism"="attraction"](area.searchArea);
# #       way["tourism"="attraction"](area.searchArea);
# #       relation["tourism"="attraction"](area.searchArea);
# #     );
# #     out center;
# #     """
# #     response = requests.post(overpass_url, data={'data': query})
# #     results = []

# #     if response.status_code == 200:
# #         data = response.json()
# #         for element in data['elements']:
# #             name = element['tags'].get('name')
# #             lat = element.get('lat') or element.get('center', {}).get('lat')
# #             lon = element.get('lon') or element.get('center', {}).get('lon')
# #             if name and lat and lon:
# #                 results.append({'name': name, 'lat': lat, 'lon': lon})
# #     return results



# # @popular_bp.route('/popular-tourism')
# # def popular_tourism():
# #     locations = fetch_osm_tourist_spots("Jaipur")

# #     # Save the results into your MySQL database
# #     save_locations_to_db(locations)

# #     return render_template("popular_tourism.html", locations=locations)



# from flask import Blueprint, render_template
# import requests
# from utils import save_locations_to_db


# popular_bp = Blueprint('popular', __name__)

# def fetch_osm_tourist_spots(city_name="Jaipur"):
#     overpass_url = "http://overpass-api.de/api/interpreter"
#     query = f"""
#     [out:json][timeout:25];
#     area[name="{city_name}"]->.searchArea;
#     (
#       node["tourism"="attraction"](area.searchArea);
#       way["tourism"="attraction"](area.searchArea);
#       relation["tourism"="attraction"](area.searchArea);
#     );
#     out center;
#     """
#     response = requests.post(overpass_url, data={'data': query})
#     results = []

#     if response.status_code == 200:
#         data = response.json()
#         for element in data['elements']:
#             name = element['tags'].get('name')
#             lat = element.get('lat') or element.get('center', {}).get('lat')
#             lon = element.get('lon') or element.get('center', {}).get('lon')
#             if name and lat and lon:
#                 results.append({'name': name, 'lat': lat, 'lon': lon})
#     return results


# @popular_bp.route('/popular_tourism')
# def popular_tourism():
#     locations = fetch_osm_tourist_spots("Jaipur")
#     save_locations_to_db(locations)  # Save to DB (optional)
#     return render_template("popular_tourism.html", locations=locations)



# popular.py
from flask import Blueprint, render_template
import requests
from utils.save_popular_locations import save_locations_to_db

popular_bp = Blueprint('popular', __name__)

# def fetch_osm_tourist_spots(city_name="Jaipur"):
#     overpass_url = "http://overpass-api.de/api/interpreter"
#     query = f"""
#     [out:json][timeout:25];
#     area[name="{city_name}"]->.searchArea;
#     (
#       node["tourism"="attraction"](area.searchArea);
#       way["tourism"="attraction"](area.searchArea);
#       relation["tourism"="attraction"](area.searchArea);
#     );
#     out center;
#     """
#     response = requests.post(overpass_url, data={'data': query})
#     locations = []

#     if response.status_code == 200:
#         data = response.json()
#         for element in data['elements']:
#             name = element['tags'].get('name')
#             lat = element.get('lat') or element.get('center', {}).get('lat')
#             lon = element.get('lon') or element.get('center', {}).get('lon')

#             if name and lat and lon:
#                 description = ""
#                 image_url = ""

#                 # Wikipedia search
#                 wiki_response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{name}")
#                 if wiki_response.status_code == 200:
#                     wiki_data = wiki_response.json()
#                     description = wiki_data.get('extract', "")
#                     image_url = wiki_data.get('thumbnail', {}).get('source', "")

#                 locations.append({
#                     'name': name,
#                     'lat': lat,
#                     'lon': lon,
#                     'description': description,
#                     'image_url': image_url
#                 })

#     return locations



def fetch_osm_tourist_spots(cities):
    overpass_url = "http://overpass-api.de/api/interpreter"
    all_locations = []

    for city_name in cities:
        print(f"Fetching for city: {city_name}")
        query = f"""
        [out:json][timeout:25];
        area[name="{city_name}"]->.searchArea;
        (
          node["tourism"="attraction"](area.searchArea);
          way["tourism"="attraction"](area.searchArea);
          relation["tourism"="attraction"](area.searchArea);
        );
        out center;
        """
        response = requests.post(overpass_url, data={'data': query})
        if response.status_code == 200:
            data = response.json()
            for index, element in enumerate(data['elements']):
                name = element['tags'].get('name')
                lat = element.get('lat') or element.get('center', {}).get('lat')
                lon = element.get('lon') or element.get('center', {}).get('lon')

                if name and lat and lon:
                    description = ""
                    image_url = ""
                    rating = 0
                    review_count = 0

                    # Wikipedia Info
                    wiki_response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{name}")
                    if wiki_response.status_code == 200:
                        wiki_data = wiki_response.json()
                        description = wiki_data.get('extract', "")
                        image_url = wiki_data.get('thumbnail', {}).get('source', "")

                    # Placeholder review & rating (replace with real API later)
                    rating = round(3 + (index % 3) + 0.5, 1)  # dummy
                    review_count = 50 + index * 3  # dummy

                    all_locations.append({
                        'name': name,
                        'lat': lat,
                        'lon': lon,
                        'description': description,
                        'image_url': image_url,
                        'rating': rating,
                        'review_count': review_count
                    })

    return all_locations







@popular_bp.route('/popular_tourism')
def popular_tourism():
    cities = ["Jaipur", "Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
    locations = fetch_osm_tourist_spots(cities)

    # Sort using data mining concept: based on reviews + rating
    sorted_locations = sorted(locations, key=lambda x: (x['review_count'], x['rating']), reverse=True)

    top_locations = sorted_locations[:10]  # You can increase this as needed

    save_locations_to_db(top_locations)  # Optional
    return render_template("popular_tourism.html", locations=top_locations)

