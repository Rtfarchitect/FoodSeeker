from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options

from functions import find_places_nearby, get_current_location
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

# Example usage
# restaurant_url = search_restaurant_google("poulet rouge")
# print("heereeeee", restaurant_url)

# latitude, longitude = get_current_location()
# places = find_places_nearby(latitude, longitude, radius_km=1.5, keyword="restaurant")
# print(len(places))
# urls = []
# for i in places[:10]:
#     urls.append(search_restaurant_google(i["name"]))

output_file = "urls.txt"

# # Write URLs to the file
# with open(output_file, "w") as file:
#     for url in urls:
#         file.write(url + "\n")

# print(f"URLs saved to {output_file}")

# output_file1 = "locs&names.txt"
# with open(output_file1, "w") as file1:
#     for place in places:
#         file.write(url + "\n")

