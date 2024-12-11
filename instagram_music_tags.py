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
driver = webdriver.Chrome(options=options)

# Instagram credentials (replace with your own)
USERNAME = 'ddpromospam'
PASSWORD = '&MYV6VxyF3@,9*u'

# Function to log in to Instagram
def login_to_instagram():
    driver.get('https://www.instagram.com/')
    time.sleep(3)  # Allow time for the page to load

    try:
        # Update element locators for mobile layout
        username_input = driver.find_element(By.XPATH, "//input[@aria-label='Phone number, username, or email']")
        password_input = driver.find_element(By.XPATH, "//input[@aria-label='Password']")
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Log In')]")

        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
        login_button.click()

        time.sleep(5)  # Wait for login to complete
    except Exception as e:
        print(f"Error during login: {e}")
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
    login_to_instagram()
    account_username = 'beyondvaudeville'  # Replace with the target account's username
    music_tags = scrape_music_tags(account_username)
    print("Collected music tags:", music_tags)

finally:
    driver.quit()
