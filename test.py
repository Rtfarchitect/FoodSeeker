from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
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
restaurant_url = search_restaurant_google("domino")
print("heereeeee", restaurant_url)