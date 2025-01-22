import geocoder
from openai import OpenAI
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def get_current_location():
    """
    Fetches the current latitude and longitude of the machine using geocoder.

    :return: A dictionary with latitude and longitude or None if failed
    """
    try:
        # Use geocoder to fetch the current location
        location = geocoder.ip('me')  # Fetches location using IP

        if location and location.latlng:
            return location.latlng[0], location.latlng[1]
        else:
            print("Unable to fetch location. Ensure location services are enabled.")
            return None
    except Exception as e:
        print(f"An error occurred while fetching location: {e}")
        return None

from geopy.geocoders import Nominatim
import overpy
def find_places_nearby(latitude, longitude, radius_km=5, keyword="restaurant"):
    """
    Search for nearby places using Overpass API.

    :param latitude: Latitude of the location
    :param longitude: Longitude of the location
    :param radius_km: Search radius in kilometers
    :param keyword: Keyword to search for (e.g., "restaurant")
    :return: List of places with names and locations
    """
    try:
        # Initialize Overpass API
        api = overpy.Overpass()

        # Overpass query to search for Points of Interest (POI) with the keyword
        query = f"""
        [out:json];
        (
          node["amenity"="{keyword}"](around:{radius_km * 1000},{latitude},{longitude});
        );
        out center;
        """

        result = api.query(query)

        # Extract place names and locations
        places = [
            {"name": node.tags.get("name", "Unnamed"), "lat": node.lat, "lon": node.lon}
            for node in result.nodes
        ]

        return places
    except Exception as e:
        print(f"Error fetching places: {e}")
        return []
    

# def extract_conditions_with_ai(query: str) -> dict:
    
#     messages = {"user": query}
#     """
#     Extract conditions like ingredients to include/exclude and price limits from the query using OpenAI.
#     """
#     prompt = f"""
#     You are a helpful assistant, you have to politely say hello, and if user provides information about the food, you have to extract information from the query. Extract the following information from this query, if there is anything mentioned about an allergy or sickness, exclude the ingredients which are bad for the user:
#     - Main food category
#     - Ingredients to include(if mentioned).
#     - Ingredients to exclude(if mentioned, create based on your knowledge if any types of allergy or sickness mentioned).
#     - Price limit (in dollars, if mentioned).
#     if you need further information you need to ask.
#     Query: "{query}"

#     Return the information as a JSON object with keys: "food","include", "exclude", and "price_limit".
#     If an element is missing, return it as an empty list or "none".
#     """


#     client = OpenAI()
#     response = client.chat.completions.create(
#         model="gpt-4",
#         messages=[{"role": "system", "content": "You are a helpful assistant for parsing user queries."},
#                   {"role": "user", "content": prompt}],
#         temperature=0
#     )
#     extracted_conditions = response.choices[0].message.content
#     messages["system"] = extracted_conditions
#     print(extracted_conditions)
#     return eval(extracted_conditions)
def extract_conditions_with_ai(query: str) -> dict:
    messages = [
        {"role": "system", "content": "You are a helpful assistant for parsing user queries."},
        {"role": "user", "content": query}
    ]
    """
    Extract conditions like ingredients to include/exclude and price limits from the query using OpenAI.
    """
    prompt = """
    You are a helpful assistant, you have to politely say hello, and if user provides information about the food, you have to extract information from the query. Extract the following information from this query, if there is anything mentioned about an allergy or sickness, exclude the ingredients which are bad for the user:
    - Main food category
    - Ingredients to include(if mentioned).
    - Ingredients to exclude(if mentioned, create based on your knowledge if any types of allergy or sickness mentioned).
    - Price limit (in dollars, if mentioned).
    if you need further information you need to ask.
    Query: "{query}"

    Return the information as a JSON object with keys: "food","include", "exclude", and "price_limit".
    If an element is missing, return it as an empty list or "none".
    """

    client = OpenAI()
    while True:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0
        )
        extracted_conditions = response.choices[0].message.content
        messages.append({"role": "system", "content": extracted_conditions})
        print(extracted_conditions)

        # Check if the response contains all needed information
        extracted_dict = eval(extracted_conditions)
        if all(key in extracted_dict and extracted_dict[key] for key in ["food", "include", "exclude", "price_limit"]):
            break
        else:
            # Ask the user for more information if needed
            user_input = input("Please provide more details: ")
            messages.append({"role": "user", "content": user_input})

    return extracted_dict








def search_vectorstore(conditions, vectorstore, top_k=10):
    """
    Perform similarity search in FAISS vector store with main food category and other conditions.
    """
    query = f"{conditions['food']} containing {', '.join(conditions['include'])}"
    results = vectorstore.similarity_search(query, k=top_k)
    return results

def filter_results_with_ai(results, conditions):
    """
    Use OpenAI to filter results based on the food category and other conditions.
    """
    items = [
        {
            "text": res.page_content,
            "restaurant_name": res.metadata.get("restaurant_name", "Unknown"),
            "url": res.metadata.get("url", "N/A")
        }
        for res in results
    ]

    prompt = f"""
    You are a helpful assistant. Filter the following menu items based on these conditions:
    - Food category: {conditions['food']}
    - Include ingredients: {conditions['include']}
    - Exclude ingredients: {conditions['exclude']}
    - Price limit: {conditions['price_limit']} dollars

    Menu items to filter (each includes restaurant name and URL):
    {items}

    Return only the items that match all the conditions as a JSON array.
    Each item in the array should include:
    - "food_name": name of the item in the restaurant.
    - "price": price of the item.
    - "text": The menu item ingredients.
    - "restaurant_name": The name of the restaurant.
    - "url": The URL of the restaurant.
    if there is not any relevant item in the menu, say: sorry, this item is not available in our menu
    """
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a helpful assistant for filtering menu items."},
                  {"role": "user", "content": prompt}],
        temperature=0
    )
    filtered_results = response.choices[0].message.content
    if not "sorry" in filtered_results:
        return eval(filtered_results)
    else:
        return filtered_results




def search_restaurant_google(restaurant_name):
    # Configure ChromeDriver options to disable GPU acceleration

    # Initialize WebDriver
    driver = webdriver.Chrome()
    
    try:
        # Open Google
        driver.get("https://www.google.com")
        time.sleep(2)  # Wait for the page to load

        # Find the search box and input the query
        search_box = driver.find_element(By.NAME, "q")
        query = f"{restaurant_name} UberEats Montreal"
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        
        time.sleep(1.5)  # Wait for search results to load

        # Get the first search result link
        search_results = driver.find_elements(By.CSS_SELECTOR, "a")
        for result in search_results:
            href = result.get_attribute("href")
            if href and "ubereats" in href:  # Check for None and "ubereats" in href
                result.click()  # Click the link
                time.sleep(1.5)  # Wait for the page to load completely
                return driver.current_url  # Return the URL of the loaded page
        
        return f"No UberEats page found for '{restaurant_name}'."
    finally:
        # Close the WebDriver
        driver.quit()
