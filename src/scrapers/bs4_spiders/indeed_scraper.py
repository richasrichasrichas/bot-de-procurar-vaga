# src/scrapers/bs4_spiders/indeed_scraper.py
import requests
from bs4 import BeautifulSoup
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import random

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
BASE_URL = 'https://br.indeed.com/'
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/88.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/88.0.705.63",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240"
]

def fetch_page(url, browser='chrome'):
    """Fetches the content of a webpage and returns the response.
    
    Args:
        url (str): The URL to fetch.
        browser (str): The browser to use ('chrome', 'firefox', 'edge'). Default is 'chrome'.
    
    Returns:
        requests.Response or None: The response object if successful, None otherwise.
    """
    try:
        logging.info(f"Fetching page: {url}")
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logging.error(f"Failed to retrieve the webpage using requests. URL: {url}. Error: {e}")
        try:
            # Fallback to Selenium
            logging.info(f"Falling back to Selenium for URL: {url}")
            user_agent = random.choice(USER_AGENTS)
            headers = {'User-Agent': user_agent}

            if browser == 'chrome':
                service = Service(ChromeDriverManager().install())
                options = webdriver.ChromeOptions()
                options.add_argument(f'user-agent={user_agent}')
                driver = webdriver.Chrome(service=service, options=options)
            elif browser == 'firefox':
                service = FirefoxService(GeckoDriverManager().install())
                options = webdriver.FirefoxOptions()
                options.set_preference("general.useragent.override", user_agent)
                driver = webdriver.Firefox(service=service, options=options)
            elif browser == 'edge':
                service = EdgeService(EdgeChromiumDriverManager().install())
                options = webdriver.EdgeOptions()
                options.add_argument(f'user-agent={user_agent}')
                driver = webdriver.Edge(service=service, options=options)
            else:
                logging.error("Unsupported browser specified.")
                return None

            driver.get(url)
            response = driver.page_source
            driver.quit()
            return response
        except Exception as e:
            logging.error(f"Failed to retrieve the webpage using Selenium. URL: {url}. Error: {e}")
            return None

def parse_page(soup):
    """Parses the HTML content and extracts links.
    
    Args:
        soup (BeautifulSoup): The BeautifulSoup object representing the HTML content.
    
    Returns:
        list: A list of links extracted from the page.
    """
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            links.append(href)
    return links

def print_links(links):
    """Prints the list of links.
    
    Args:
        links (list): The list of links to print.
    """
    for link in links:
        print(link)

def main():
    """Main function to execute the scraping process."""
    logging.info("Starting the Indeed scraper.")
    response = fetch_page(BASE_URL, browser='chrome')  # You can change the browser here
    if response:
        soup = BeautifulSoup(response, 'html.parser')
        links = parse_page(soup)
        print_links(links)
        logging.info("Scraping completed successfully.")
    else:
        logging.error("Failed to scrape the page.")

if __name__ == "__main__":
    main()
