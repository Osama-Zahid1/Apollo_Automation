from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
import time

APOLLO_LOGIN_URL = "https://app.apollo.io/#/people"
EMAIL = "@gmail.com"  # Replace with your actual email
PASSWORD = "xyz"  # Replace with your actual password

# WebDriver setup (outside the loop)
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
#options.add_argument("--headless=new") #for running in background

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

def login_to_apollo(driver, wait):
    try:
        driver.get(APOLLO_LOGIN_URL)
        wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(EMAIL)
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.RETURN)
        print("Logged in successfully.")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".zp_T7Mub"))) #wait until dashboard loads
        time.sleep(5)
    except Exception as e:
        print(f"Login failed: {e}")
        raise

def process_list(driver, wait, list_url):
    try:
        driver.get(list_url)
        print(f"Processing list: {list_url}")
        current_url = driver.current_url
        first_page = True

        while True:
            try:
                if not first_page:
                    # Unselect "25 selected" if it's there
                    try:
                        parent_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".zp_TO5Gi")))
                        selected_button = parent_div.find_element(By.CSS_SELECTOR, "button:nth-child(1)")
                        selected_button.click()
                        print("'25 selected' button clicked - contacts unselected.")
                        time.sleep(2)
                    except (TimeoutException, NoSuchElementException):
                        print("No '25 selected' button found or timed out.")
                        pass # if it doesn't exist, it is not an issue

                # Select checkboxes
                checkboxes = wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.zp_wMhzv input[type='checkbox']")
                ))
                for checkbox in checkboxes:
                    try:
                        checkbox.click()
                    except ElementClickInterceptedException:
                        actions = ActionChains(driver)
                        actions.move_to_element(checkbox).click().perform()
                        print("Checkbox clicked using ActionChains.")
                print("Rows selected.")

                # Click 'Apply' button
                apply_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//span[text()='Apply']]")))
                apply_button.click()
                print("Apply button clicked.")
                time.sleep(2)

                # Click 'Enrich' button
                enrich_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//span[text()='Enrich']]")))
                enrich_button.click()
                print("Enrich button clicked.")

                # Click 'Enrich emails' option
                enrich_emails_option = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, ".//span[text()='Enrich emails']")))
                enrich_emails_option.click()
                print("Enrich emails option selected.")
                time.sleep(2)

                # Click the 'Enrich emails' button
                enrich_emails_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, ".//button[.//div[text()='Enrich emails']]")))
                enrich_emails_button.click()
                print("Emails enriched.")
                time.sleep(5)

                # Navigate to the next page
                try:
                    next_button = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//button[@aria-label='Next']")))
                    next_button.click()
                    print("Next button clicked.")

                    wait.until(lambda driver: driver.current_url != current_url)
                    current_url = driver.current_url
                    print("Navigated to the next page.")

                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.zp_wMhzv"))) #wait for rows to load
                    time.sleep(5)
                    first_page = False

                except TimeoutException:
                    print("No more pages to process. Reached the last page.")
                    break

            except (TimeoutException, StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException) as e:
                print(f"Error interacting with elements: {e}. Retrying after short delay...")
                time.sleep(5)
                continue

    except Exception as e:
        print(f"Error processing list: {e}")
        raise

def main():
    try:
        login_to_apollo(driver, wait)
        list_urls = [
            "xyz url"
        ]
        for url in list_urls:
            process_list(driver, wait, url)
    except Exception as e:
        print(f"Script error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
