import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

CHROMEDRIVER_PATH = r"C:\chromedriver\chromedriver-win64\chromedriver.exe"
OUTPUT_FILE = "hotel_prices.csv"

HOTELS = [
    {
        "name": "Taipei Marriott",
        "base_url": "https://www.booking.com/hotel/tw/taipei-marriott.en-gb.html?checkin={checkin}&checkout={checkout}"
    },
    {
        "name": "Holiday Inn Express Taoyuan",
        "base_url": "https://www.booking.com/hotel/tw/new-continental.en-gb.html?checkin={checkin}&checkout={checkout}"
    },
    {
        "name": "Hilton Taipei Sinban",
        "base_url": "https://www.booking.com/hotel/tw/hilton-taipei-sinban.en-gb.html?checkin={checkin}&checkout={checkout}"
    },
    {
        "name": "Humble House Taipei, Curio Collection by Hilton",
        "base_url": "https://www.booking.com/hotel/tw/humble-house-taipei-curio-collection-by-hilton.en-gb.html?checkin={checkin}&checkout={checkout}"
    },

    {
        "name": "Holiday Inn Express Taipei Main Station",
        "base_url": "https://www.booking.com/hotel/tw/new-continental.en-gb.html?checkin={checkin}&checkout={checkout}"
    },
    {
        "name": "Four Points by Sheraton Linkou",
        "base_url": "https://www.booking.com/hotel/tw/four-points-by-sheraton-linkou.en-gb.html?checkin={checkin}&checkout={checkout}"
    }
]

DATES = [
    ("2025-08-06", "2025-08-07"),
    ("2025-08-07", "2025-08-08"),
    ("2025-09-02", "2025-09-03"),
    ("2025-09-03", "2025-09-04"),
    ("2025-10-02", "2025-10-03"),
    ("2025-10-15", "2025-10-16"),
    ("2025-11-02", "2025-11-03"),
    ("2025-11-15", "2025-11-16"),
    ("2025-12-02", "2025-12-03"),
    ("2025-12-15", "2025-12-16"),
]


def get_driver():
    service = Service(CHROMEDRIVER_PATH)
    options = Options()
    # REMOVE headless so possible to see the window
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def accept_cookies(driver):
    try:
        time.sleep(3)  # time to load
        button = driver.find_element(
            By.XPATH, "//button[contains(text(),'Accept')]")
        button.click()
        print("Cookie banner accepted")
    except Exception:
        print("No cookie banner found or clickable")


def extract_prices(driver):
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    price_spans = soup.find_all('span', class_='prco-valign-middle-helper')
    prices = sorted(set(span.get_text(strip=True) for span in price_spans))
    return prices


if __name__ == "__main__":
    driver = get_driver()
    all_data = []

    for hotel in HOTELS:
        for checkin, checkout in DATES:
            url = hotel["base_url"].format(checkin=checkin, checkout=checkout)
            print(f"Loading URL: {url}")

            driver.get(url)
            time.sleep(5)  # initial load

            accept_cookies(driver)

            prices = extract_prices(driver)
            if prices:
                for price in prices:
                    all_data.append([hotel["name"], checkin, checkout, price])
                print(
                    f"Prices found for {hotel['name']} on {checkin} - {checkout}")
            else:
                print(
                    f"No prices found for {hotel['name']} on {checkin} - {checkout}")

    driver.quit()

    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Hotel Name', 'Check-in', 'Check-out', 'Price'])
        writer.writerows(all_data)

    print(f"\n Data saved to {OUTPUT_FILE}")
