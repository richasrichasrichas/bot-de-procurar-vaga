# bot-de-procurar-vaga/src/scrapers/bs4_spiders/indeed_scraper.py
import requests
from bs4 import BeautifulSoup
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
BASE_URL = 'https://br.indeed.com/'

def fetch_page(url):
    """Fetches the content of a webpage and returns the response.
    
    Args:
        url (str): The URL to fetch.
    
    Returns:
        requests.Response or None: The response object if successful, None otherwise.
    """
    try:
        logging.info(f"Fetching page: {url}")
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logging.error(f"Failed to retrieve the webpage. URL: {url}. Error: {e}")
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
    response = fetch_page(BASE_URL)
    if response:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = parse_page(soup)
        print_links(links)
        logging.info("Scraping completed successfully.")
    else:
        logging.error("Failed to scrape the page.")

if __name__ == "__main__":
    main()
