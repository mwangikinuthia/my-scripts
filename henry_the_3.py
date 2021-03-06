from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import argparse
import io
import re
import time


def init_dr():
    driver = webdriver.Chrome('/home/sammy/Desktop/scraping/chromedriver')
    #Please change this to your location of the chrome driver.exe
    return driver
global premium_apps
global freeapps


urls = ['BOOKS_AND_REFERENCE', 'BUSINESS', 'COMICS', 'COMMUNICATION', 'EDUCATION', 'ENTERTAINMENT', 'FINANCE',
        'HEALTH_AND_FITNESS', 'LIBRARIES_AND_DEMOS', 'LIFESTYLE', 'MEDIA_AND_VIDEO', 'MEDICAL', 'MUSIC_AND_AUDIO',
        'NEWS_AND_MAGAZINES', 'PERSONALIZATION', 'PHOTOGRAPHY', 'PRODUCTIVITY', 'SHOPPING', 'SOCIAL', 'SPORTS',
        'TOOLS', 'TRANSPORTATION', 'TRAVEL_AND_LOCAL', 'WEATHER', 'GAME_ACTION', 'GAME_ADVENTURE', 'GAME_ARCADE',
        'GAME_BOARD', 'GAME_CARD', 'GAME_CASINO', 'GAME_CASUAL', 'GAME_EDUCATIONAL', 'GAME_MUSIC', 'GAME_PUZZLE',
        'GAME_RACING', 'GAME_ROLE_PLAYING'
    , 'GAME_SIMULATION', 'GAME_SPORTS', 'GAME_STRATEGY', 'GAME_TRIVIA', 'GAME_WORD', 'FAMILY_BRAINGAMES',
        'FAMILY_CREATE', 'FAMILY_EDUCATION', 'FAMILY_MUSICVIDEO',
        'FAMILY_PRETEND',  # 'FAMILY?age=AGE_RANGE1','FAMILY?age=AGE_RANGE2','FAMILY?age=AGE_RANGE3',
        ]
free_paid = ['free', 'paid']


def generateStartUrls():
    free_urls = []
    i = 0
    while i < len(urls):
        free_urls.append(
            'https://play.google.com/store/apps/category/' + urls[i] + '/collection/topselling_' + free_paid[0]+'?hl=en')
        i += 1
    return free_urls

def mainFree():
    driver = init_dr()
    for category in generateStartUrls():
        driver.get(category)
        print '[*] Generating all free apps in ' + category + ' category'
        # wait = WebDriverWait(driver,1000)
        for i in range(6):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(2)
        a=driver.find_elements(By.CLASS_NAME,'title')
        app_urls = []
        for c in a:
            y=c.get_attribute('href')
            app_urls.append(y)
        app_urls = app_urls[3:]
        for ur in app_urls:
            ur = str(ur)
            try:
                driver.get(ur)
                print '[*]Fetching individual apps detail'
                wait = WebDriverWait(driver, 10)

                if True:
                    app_name = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#body-content > div > div > div.main-content > div:nth-child(1) > div > div.details-info > div > div.info-box-top > h1 > div')))
                    app_name = app_name.text
                    app_name = re.sub('\xe2\x80\x93', ' ', app_name)
                    app_name = re.sub('\u2013',' ', app_name)
                    appurl = ur
                    rating = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#body-content > div.outer-container > div > div.main-content > div.details-wrapper.apps > div.details-section.reviews > div.details-section-contents > div.rating-box > div.score-container > div.score')))
                    rating = rating.text
                    installs = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#body-content > div.outer-container > div > div.main-content > div.details-wrapper.apps-secondary-color > div > div.details-section-contents > div:nth-child(3) > div.content')))
                    installs = installs.text
                    installs = installs.replace(',', ' ')
                    dateUpdated = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#body-content > div.outer-container > div > div.main-content > div.details-wrapper.apps-secondary-color > div > div.details-section-contents > div:nth-child(1) > div.content')))
                    dateUpdated =dateUpdated.text
                    print app_name
                    this_app =[ur, app_name, rating, installs,dateUpdated]
                    export = ', '.join(this_app)
                    freeapps = io.open(args.freeapps, 'a+', encoding='utf8')
                    freeapps.write(export)
                    freeapps.write(u'\n')
                    print '-+ ' + app_name + ' '
                else:

                    'Internal Err'
            except StaleElementReferenceException:
                continue
    freeapps.close()
    driver.close()
def generateStartUrls_paid():
    free_urls = []
    i = 0
    while i < len(urls):
        free_urls.append(
            'https://play.google.com/store/apps/category/' + urls[i] + '/collection/topselling_' + free_paid[1] + '?hl=en')
        i += 1
    return free_urls


def mainPaid():
    driver = init_dr()
    for category in generateStartUrls_paid():
        driver.get(category)
        print '[*] Generating all free apps in ' + category + ' category'
        # wait = WebDriverWait(driver,1000)
        for i in range(5):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(1)
        a = driver.find_elements(By.CLASS_NAME, 'title')
        app_urls = []
        for c in a:
            y = c.get_attribute('href')
            app_urls.append(y)
        app_urls = app_urls[3:]
        for ur in app_urls:
            ur = str(ur)
            try:
                driver.get(ur)
                wait = WebDriverWait(driver, 10)
                print '[*]Fetching individual apps detail'
                if True:
                    app_name = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                            '#body-content > div > div > div.main-content > div:nth-child(1) > div > div.details-info > div > div.info-box-top > h1 > div')))
                    app_name = app_name.text
                    app_name = re.sub('\xe2\x80\x93', ' ', app_name)
                    app_name = re.sub('\u2013',' ', app_name)
                    rating = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                          '#body-content > div.outer-container > div > div.main-content > div.details-wrapper.apps > div.details-section.reviews > div.details-section-contents > div.rating-box > div.score-container > div.score')))
                    rating = rating.text
                    installs = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                            '#body-content > div.outer-container > div > div.main-content > div.details-wrapper.apps-secondary-color > div > div.details-section-contents > div:nth-child(3) > div.content')))
                    installs = installs.text
                    installs = installs.replace(',', ' ')
                    dateUpdated = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                               '#body-content > div.outer-container > div > div.main-content > div.details-wrapper.apps-secondary-color > div > div.details-section-contents > div:nth-child(1) > div.content')))
                    dateUpdated = dateUpdated.text
                    price = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                         '#body-content > div.outer-container > div > div.main-content > div:nth-child(1) > div > div.details-info > div > div.info-box-bottom > div > div.details-actions-right > span > span > button > span:nth-child(3)')))
                    price = price.text
                    this_app = [ur, app_name, rating, installs, dateUpdated, price]
                    export = ', '.join(this_app)
                    premium_apps = io.open(args.paidapps,'a+', encoding='utf8')
                    premium_apps.write(export)
                    premium_apps.write(u'\n')
                    print '+- '+app_name+ ' '
                else:

                    'Internal Err'
            except StaleElementReferenceException:
                'Bot timed out'
                continue
    premium_apps.close()
    driver.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('freeapps',help='Enter the csv to output all free apps')
    parser.add_argument('paidapps',help='Enter the csv to output all paid apps')
    args = parser.parse_args()
    print '[*] Bot starting'
    print '[*]---------Free apps------------'
    mainFree()
    print '[*]--------Paid apps------------'
    mainPaid()


