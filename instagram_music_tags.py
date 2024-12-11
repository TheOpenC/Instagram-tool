from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
import chromedriver_autoinstaller

# Automatically download and install the correct version of ChromeDriver
chromedriver_autoinstaller.install()

# Configure WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')

def initialize_driver():
    print("Initializing ChromeDriver...")
    try:
        return webdriver.Chrome(options=options)
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        print("Reinstalling ChromeDriver with chromedriver_autoinstaller...")
        chromedriver_autoinstaller.install()
        return webdriver.Chrome(options=options)

driver = initialize_driver()

# Instagram credentials (replace with your own)
USERNAME = 'ddpromospam'
PASSWORD = '&MYV6VxyF3@,9*u'

# Function to log in to Instagram
def login_to_instagram():
    print("Navigating to Instagram login page...")
    driver.get('https://www.instagram.com/')
    time.sleep(3)  # Allow time for the page to load

    try:
        # Look for the "Open Instagram" button and click it if present
        try:
            print("Looking for 'Open Instagram' button...")
            open_instagram_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Open Instagram')]")
            open_instagram_button.click()
            print("Clicked 'Open Instagram' button.")
            time.sleep(2)
        except Exception as e:
            print(f"'Open Instagram' button not found: {e}. Proceeding to 'Log in' link...")

        # Look for and click the "Log in" link
        print("Looking for 'Log in' link...")
        try:
            login_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Log in')]")
            login_link.click()
            print("Clicked 'Log in' link.")
            time.sleep(2)  # Wait for login form to appear
        except Exception as e:
            print(f"'Log in' link not found: {e}")
            driver.save_screenshot("login_error_link.png")
            raise

        # Check for login inputs
        print("Looking for username input field...")
        username_input = driver.find_element(By.NAME, 'username')
        print("Username input field found.")

        print("Looking for password input field...")
        password_input = driver.find_element(By.NAME, 'password')
        print("Password input field found.")

        print("Looking for submit button...")
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        print("Submit button found.")

        # Enter credentials
        print("Entering credentials...")
        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
        print("Submitting login form...")
        submit_button.click()

        print("Waiting for login to complete...")
        time.sleep(5)  # Wait for login to complete

        # Post-login check
        if "wrong password" in driver.page_source.lower():
            raise Exception("Incorrect credentials detected.")

        # Capture screenshot after login
        driver.save_screenshot("post_login.png")
        print("Screenshot saved as 'post_login.png'")
    except Exception as e:
        print(f"Error during login: {e}")
        driver.save_screenshot("login_error.png")
        print("Screenshot saved as 'login_error.png'")
        driver.quit()
        raise

# Function to scrape music tags from posts
def scrape_music_tags(account_username):
    driver.get(f'https://www.instagram.com/{account_username}/')
    time.sleep(3)

    # Scroll through the account's posts and collect music tags
    post_links = []  # Use a list to maintain order
    music_tags = []

    for _ in range(5):  # Adjust the range for the number of scrolls you want
        posts = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
        for post in posts:
            link = post.get_attribute('href')
            if link not in post_links:  # Avoid duplicates
                post_links.append(link)
        
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)

    # Reverse the list to start from the oldest post
    post_links.reverse()

    # Visit each post and collect the music tags
    for link in post_links:
        driver.get(link)
        time.sleep(2)
        try:
            music_tag = driver.find_element(By.XPATH, "//div[@aria-label='Tagged music']/descendant::span").text
            # Check if the music tag matches "beyondvaudeville - Original audio"
            if music_tag == 'beyondvaudeville - Original audio':
                pass  # Skip this specific tag
            else:
                music_tags.append(music_tag)
        except:
            pass  # If no music tag is found, skip

    return music_tags

# Main execution
try:
    print("Starting Instagram login...")
    login_to_instagram()
    print("Login successful. Starting music tag scraping...")
    account_username = 'beyondvaudeville'  # Replace with the target account's username
    music_tags = scrape_music_tags(account_username)
    print("Collected music tags:", music_tags)

except Exception as e:
    print(f"An error occurred: {e}")
    driver.save_screenshot("critical_error.png")
    print("Screenshot saved as 'critical_error.png' for debugging.")

finally:
    print("Closing the browser.")
    driver.quit()
