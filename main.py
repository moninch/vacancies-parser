from multiprocessing import Process
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from multiprocessing import Pool


def scrape_city(city):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск в фоновом режиме

    service = Service(
        "C:\\Users\\Даниил\\Desktop\\chromedriver-win64\\chromedriver.exe"
    )  # Укажи путь к chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = f"https://www.tbank.ru/career/vacancies/service/{city}/?utm_medium=sn_tg&utm_source=mgm_mb_android&short_link=9CqkvjrwMuV&_deep_link_sub1=9CqkvjrwMuV&httpMethod=GET"
    driver.get(url)

    # Нажатие на кнопку "Показать еще" до тех пор, пока кнопка доступна
    while True:
        try:
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button[data-qa-type="vc:show-more-btn"]')
                )
            )
            show_more_button.click()
            time.sleep(2)  # Небольшая задержка для подгрузки новых данных
        except:
            print(f"Кнопка 'Показать еще' больше недоступна для {city}.")
            break

    # Получение HTML и парсинг вакансий
    soup = BeautifulSoup(driver.page_source, "html.parser")
    vacancies = soup.find_all("div", class_="VacancyCard__title-desktop_eq6NiZ")

    # Сохранение вакансий в отдельный файл для каждого города, НЕОБХОДИМО СОЗДАТЬ ПАПКУ parsing_town
    with open(f"parsing_town/{city}_vacancies.txt", "w", encoding="utf-8") as f:
        for vacancy in vacancies:
            title = vacancy.text.strip()
            f.write(title + "\n")

    print(f"Сбор данных для города {city} завершен.")
    driver.quit()


def main():
    towns = [
        "nizhny-novgorod",
        "moscow",
        "saint-petersburg",
        "krasnodar",
        "novosibirsk",
        "yekaterinburg",
        "rostov-on-don",
        "kazan",
        "volgograd",
        "ufa",
        "samara",
        "saratov",
        "seversk",
        "perm",
        "chelyabinsk",
        "kaliningrad",
        "vladivostok",
    ]

    with Pool(4) as pool:
        pool.map(scrape_city, towns)

    print("Сбор данных завершен для всех городов.")


if __name__ == "__main__":
    main()
