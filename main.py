from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from os import system
from termcolor import colored
from datetime import datetime
from progress.bar import Bar

options = webdriver.FirefoxOptions()
options.set_preference("general.useragent.override", "Mozilla/5.0 (Linux; U; Android 5.1.1; Nexus 5 Build/LMY48B) AppleWebKit/534.4 (KHTML, like Gecko)  Chrome/52.0.3088.298 Mobile Safari/535.1")
options.add_argument('--headless')
options.page_load_strategy = 'none'

eur_usd = "https://ru.investing.com/currencies/eur-usd-technical"

def ticker(url :str) -> dict :

    try:

        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(5)
        driver.get(url)
        five_min_bt = '*[data-test=\"5m\"]'
        min_bt = '*[data-test=\"1m\"]'

        try:

            accept = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
            accept.click()

        except Exception as e:
            pass
            #print("[INFO] Cookie accept button missed")
            #print(f"\n{e}")
        
        button1 = driver.find_element(By.CSS_SELECTOR, min_bt)
        button5 = driver.find_element(By.CSS_SELECTOR, five_min_bt)
        #print('[INFO] Buttons finded')

        def scrape_data() -> list: 

            tech_info = driver.find_element(By.CSS_SELECTOR, '.order-1:nth-child(2) .mb-6')
            try:
                total = driver.find_element(By.CSS_SELECTOR, '.bg-negative-main')
            except Exception as e:
                try:
                    total = driver.find_element(By.CSS_SELECTOR, '.bg-\[\#5B616E\]')
                except Exception as e:
                    total = driver.find_element(By.CSS_SELECTOR, '.bg-positive-main')

            average = driver.find_element(By.CSS_SELECTOR, '.order-3 .mb-6')

            #print('[INFO] Complete find elements\n')
            tech = tech_info.text
            average = average.text
            total = total.text
        
            return {
                "tech" : tech,
                "average" : average,
                "total" : total
            }
        
        driver.execute_script('arguments[0].click()', button1)
        #print('[INFO] Scrape 1 min')
        one = scrape_data()
        #print('[INFO] Complete')
        driver.execute_script('arguments[0].click()', button5)
        #print('[INFO] Scrape 5 min')
        five = scrape_data()
        #print('[INFO] Complete!')
        
        return [one, five]

    except Exception as e:
        print(e)
        return None

    finally:
        driver.close()
        driver.quit()

def colorize (str :str) -> str :
    match str:
        case "Активно продавать":
            return colored(str, 'light_red')
        case "Продавать":
            return colored(str, 'red')
        case "Активно покупать":
            return colored(str, 'light_green')
        case "Покупать":
            return colored(str, 'green')
        case "Нейтрально":
            return colored(str, 'yellow')
        case _:
            return "Ошибка"

def printResponse(money_pair :str, clear_cls :bool = False) -> str : 

    begin = datetime.now()
    res = ticker(money_pair)
    system('cls')

    print(f"[INFO] Текущее время : {begin.strftime('%H:%M:%S')}\n")
    print(f" --- Минутный прогноз ---\n"
            f"Тех.анализ  : {colorize(res[0]['tech'])}\n"
            f"Скл. ср.    : {colorize(res[0]['average'])}\n"
            f"Резюме      : {colorize(res[0]['total'])}\n"
            f"----------------------------------------------\n"
            f" --- Пятиминутный прогноз ---\n"
            f"Тех.анализ  : {colorize(res[1]['tech'])}\n"
            f"Скл. ср.    : {colorize(res[1]['average'])}\n"
            f"Резюме      : {colorize(res[1]['total'])}\n"
            f"----------------------------------------------\n")

    end = datetime.now() - begin
    
    print(f'[INFO] Выполнение скрипта заняло {end.seconds} секунд\n')
    print("[INFO] Ожидаем 5 секунд на повтор..\n"
          f"[INFO Для выхода из программы нажмите Ctrl+C]")
    
    with Bar('Ожидание : ', max = 5) as bar:
        for i in range(5):
            sleep(1)
            bar.next()

    if clear_cls:
        system('cls')

def main():
    
    system('cls')
    print("[INFO] Запуск скрипта ... ")

    while True:
        printResponse(eur_usd)
        
if __name__ == '__main__':
    main()
