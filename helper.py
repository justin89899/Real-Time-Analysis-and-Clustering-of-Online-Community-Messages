from selenium import webdriver
from bs4 import BeautifulSoup
import time
#from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.firefox.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scrape_ieee(url):
    #driver_path = '/usr/bin/chromedriver'

    #options = webdriver.ChromeOptions()
    #options.add_experimental_option('detach', True)
    #service = webdriver.ChromeService(executable_path=driver_path)
    #driver = webdriver.Chrome(service=service, options=options)
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.PhantomJS()
    driver.get(url)
    time.sleep(0.5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    raw = soup.find('div', {'class':'body-description'}).find_all('p')
    full_text = ""
    for i in raw:
        full_text += i.text

    driver.quit()
    return full_text

def scrape_reuters(url):
    #driver_path = '/home/vboxuser/Downloads/chromedriver-linux64/chromedriver'

    #options = Options()
    #options.add_argument("--headless")
    #options.add_experimental_option('detach', True)
    #service = webdriver.ChromeService(executable_path=driver_path)
    #driver = webdriver.Chrome(service=service, options=options)
    
    #service = Service(executable_path="/snap/bin/geckodriver")

    #driver = webdriver.Firefox(service=service, options=options)

    #driver_path = '/usr/bin/chromedriver'

    #options = webdriver.ChromeOptions()
    #options.add_experimental_option('detach', True)
    #service = webdriver.ChromeService(executable_path=driver_path)
    #driver = webdriver.Chrome(service=service, options=options)
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.PhantomJS()

    driver.get(url)
    time.sleep(0.5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    raw = soup.select('div[data-testid*="paragraph"]')
    full_text = ""
    for i in raw:
        full_text += i.text

    driver.quit()
    return full_text
