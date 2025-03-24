from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import pandas as pd

def extract_names_and_emails(url):
    # Set up Selenium WebDriver (using Chrome)
    options = Options()
    options.headless = True  # Run in headless mode (no browser window)
    driver = webdriver.Chrome(options=options)
    
    driver.get(url)

    # Explicit wait to ensure the page is fully loaded
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))  # Wait for body to load
        )
    except:
        print("Timeout waiting for page to load")
        driver.quit()
        return []

    # Simulate scrolling to the bottom of the page to load dynamic content
    for _ in range(5):  # Scroll 5 times to allow content to load
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for the page to load more content

    # Get the page source after JavaScript rendering and scrolling
    page_source = driver.page_source
    driver.quit()

    # Parse the page with BeautifulSoup (for better structured extraction)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Assuming names are in <h3> or <p> tags and emails in 'mailto' links
    names = []
    emails = []

    # Example of extracting names and emails
    for person in soup.find_all('div', class_='person-info'):  # Adjust based on actual HTML structure
        name = person.find('h3')  # Adjust tag based on actual HTML
        email = person.find('a', href=re.compile(r'mailto:'))
        
        if name and email:
            names.append(name.get_text(strip=True))
            emails.append(email.get('href').replace('mailto:', '').strip())

    # Create a DataFrame for tabular display
    data = {
        'Name': names,
        'Email': emails
    }
    df = pd.DataFrame(data)

    return df

# Example usage
url = 'https://www.iiitnr.ac.in/faculty'
df = extract_names_and_emails(url)

# Display the table of extracted names and emails
print(df)
