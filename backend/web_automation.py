from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def order_food(query):
    driver = setup_driver()
    try:
        # Open Swiggy
        driver.get("https://www.swiggy.com")
        
        # Wait for search box and enter query
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Search for restaurants']"))
        )
        search_box.clear()
        search_box.send_keys(query)
        
        # Wait for search button and click it
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        search_button.click()
        
        # Wait for results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".RestaurantList"))
        )
        
        # Get the current URL after search
        current_url = driver.current_url
        
        # Close the browser
        driver.quit()
        
        return {
            "status": "success",
            "url": current_url,
            "message": "Search completed on Swiggy"
        }
    except Exception as e:
        driver.quit()
        return {
            "status": "error",
            "message": f"Error in food order: {str(e)}"
        }

def order_cab(query):
    driver = setup_driver()
    try:
        # Open Uber
        driver.get("https://www.uber.com")
        
        # Wait for destination input and enter query
        destination = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Where to?']"))
        )
        destination.send_keys(query)
        destination.submit()
        
        # Wait for results and get the URL
        time.sleep(3)
        current_url = driver.current_url
        
        # Close the browser
        driver.quit()
        
        return {
            "status": "success",
            "url": current_url,
            "message": "Redirecting to Uber search results"
        }
    except Exception as e:
        driver.quit()
        return {
            "status": "error",
            "message": f"Error in cab order: {str(e)}"
        }

def order_accessories(query):
    driver = setup_driver()
    try:
        # Open Amazon
        driver.get("https://www.amazon.com")
        
        # Wait for search box and enter query
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Search Amazon']"))
        )
        search_box.clear()
        search_box.send_keys(query)
        
        # Wait for search button and click it
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))
        )
        search_button.click()
        
        # Wait for results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-component-type='s-search-result']"))
        )
        
        # Get the current URL after search
        current_url = driver.current_url
        
        # Close the browser
        driver.quit()
        
        return {
            "status": "success",
            "url": current_url,
            "message": "Search completed on Amazon"
        }
    except Exception as e:
        driver.quit()
        return {
            "status": "error",
            "message": f"Error in accessories order: {str(e)}"
        } 