import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class ParseBayonneBay:
    def __init__(self, config) -> None:
        """
        Initialize the ParseBayonneBay class.

        Args:
            config (dict): A dictionary containing parsing setup details.
                It should include the path to the Chrome WebDriver executable.

        Attributes:
            chrome_driver (str): The path to the Chrome WebDriver executable. For Linux user.

        Usage:
            Initialize an instance of ParseBayonneBay with the configuration.
        """
        self.chrome_driver = config["parse_setup"]["chrome_driver"]
        self.chrome_driver = config["parse_setup"]["chrome_driver"]

    def parse_apt_link(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        # Sending a GET request to the webpage with the added headers
        response = requests.get(url, headers=headers)

        # Sending a GET request to the webpage
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="listings")
        apartments = {}
        for row in table.find_all("tr")[1:]:  # Skipping the header row
            columns = row.find_all(["th", "td"])
            title = (
                columns[0]
                .get_text(strip=True)
                .split("This link")[0]
                .split(" ")[-1]
            )
            if title == "":
                continue
            for column in columns:
                links = column.find_all(
                    "a", href=lambda href: href and "availableunits" in href
                )
                for link in links:
                    link_tmp = link["href"]
            apartments[title] = link_tmp
        return apartments

    def parse_apt_detail(self, url_dict):
        content = []
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Enables headless mode
        # Initialize the WebDriver with Chrome options
        for title, link in url_dict.items():
            tmp_result = {}
            tmp_result["Type"] = title
            driver = webdriver.Chrome(
                self.chrome_driver,
            )
            driver.get(link)
            html_content = driver.page_source
            time.sleep(random.uniform(5, 10))
            # Remember to close the browser when you're done
            driver.quit()
            soup = BeautifulSoup(html_content, "html.parser")
            table = soup.find("table", class_="availableUnits")
            for row in table.find("tbody").find_all("tr"):
                cells = row.find_all("td")
                tmp_result["Apartment"] = cells[0].get_text(strip=True)
                tmp_result["Size"] = cells[1].get_text(strip=True)
                tmp_result["Price"] = cells[2].get_text(strip=True)
                tmp_result["Avail Date"] = cells[3].get_text(strip=True)
                content.append(tmp_result)

        return content
