from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

class LinkedInCrawler:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def extract(self, user_profile_link):
        driver = None  # Initialize driver to ensure scope
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        posts_content = []  # List to store the posts

        try:
            # Initialize the WebDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            # Log in to LinkedIn
            driver.get("https://www.linkedin.com/login")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            driver.find_element(By.ID, "username").send_keys(self.email)
            driver.find_element(By.ID, "password").send_keys(self.password)
            driver.find_element(By.XPATH, '//button[@type="submit"]').click()

            # Navigate to the user's recent activity feed
            activity_feed_link = f"{user_profile_link.rstrip('/')}/recent-activity/all/"
            driver.get(activity_feed_link)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "feed-shared-update-v2__description"))
            )

            # Parse the page with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")
            posts = soup.find_all("div", {"class": "feed-shared-update-v2__description"})

            # Collect the text content of each post
            for post in posts:
                posts_content.append(post.get_text(strip=True))

        except Exception as e:
            return {"error": f"An error occurred: {e}"}

        finally:
            if driver:
                driver.quit()  # Ensure driver is quit properly

        return posts_content  # Return the list of posts


