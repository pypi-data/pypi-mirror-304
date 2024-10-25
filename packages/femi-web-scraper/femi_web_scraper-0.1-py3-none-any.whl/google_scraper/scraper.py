import csv
import os
import requests
from bs4 import BeautifulSoup
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

class GoogleScraper:
    def __init__(self, proxies=None):
        self.proxies = proxies or {}
        self.search_results = []

    def save_data_to_csv(self, filename='output.csv'):
        file_exists = os.path.isfile(filename)
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Title', 'Content', 'Link', 'Media'])  # CSV header
            writer.writerows([(result['title'], result['content'], result['link'], "") for result in self.search_results])  # Adding empty media

    def scrape(self, query: str) -> list:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        try:
            response = requests.get(search_url, proxies=self.proxies, headers=headers)
            response.raise_for_status()  # Raises an error for 4xx and 5xx status codes

            soup = BeautifulSoup(response.text, 'html.parser')

            for g in soup.find_all('div', class_='g'):
                title_tag = g.find('h3', class_='LC20lb')
                link_tag = g.find('a')
                content_tag = g.find('div', class_='VwiC3b')

                if title_tag and link_tag:
                    title = title_tag.text
                    link = link_tag['href']
                    content = content_tag.text if content_tag else "No content available"

                    logging.info(f"Extracted Title: {title}, Link: {link}, Content: {content}")

                    self.search_results.append({
                        'title': title,
                        'link': link,
                        'content': content
                    })

            if self.search_results:
                self.save_data_to_csv()  # Save to CSV if results are found
                logging.info(f"Successfully scraped {len(self.search_results)} results for query: {query}")
                return self.search_results
            else:
                logging.info(f"No search results found for query: {query}")
                return "No search results found for query: " + query  # Return a string message

        except requests.RequestException as e:
            logging.error(f"Failed to retrieve search results: {e}")
            return f"Failed to retrieve search results: {e}"
