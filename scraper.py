import time
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

    # Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "{your_email}"
EMAIL_PASSWORD = "{your_app_password}"

def send_email(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Set up Selenium options
options = Options()
options.add_argument("--headless")  # Run browser in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Set up the WebDriver
service = Service("./chromedriver")  # Use chromedriver from the same path as this script

driver = webdriver.Chrome(service=service, options=options)

# Target URL
url = "{kleinanzeigen_url}"

# Function to fetch the current listings
def fetch_listings():
    driver.get(url)
    time.sleep(5)  # Allow time for the page to load completely
    try:
        # Locate the main container for the listings
        main_container = driver.find_element(By.CSS_SELECTOR, "#srchrslt-adtable")  # Replace with the correct ID or class

        # Extract listings within the main container
        results = main_container.find_elements(By.CSS_SELECTOR, ".aditem-main")  # Adjust selector for ads inside the main container
        titles = [result.text for result in results]
    except Exception as e:
        print(f"Error fetching listings: {e}")
        titles = []  # Return an empty list if no results are found
    return titles


# Monitor the website
try:
    print("Starting the bot...")
    old_results = fetch_listings()
    print(f"Initial results: {len(old_results)} items found.")

    while True:
        time.sleep(60)  # Wait 1 minute before checking again
        new_results = fetch_listings()
        if len(new_results) > len(old_results):
            print("New items detected!")
            for item in new_results:
                if item not in old_results:
                    print(item)
                    send_email("New Listing Alert", f"New listing: {item}")
            old_results = new_results
        else:
            print("No new items.")

except KeyboardInterrupt:
    print("Stopping the bot...")
finally:
    driver.quit()
