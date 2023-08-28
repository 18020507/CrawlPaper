from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import By
from selenium.webdriver.support.wait import WebDriverWait


def start_chrome():
    # 크롬 구동 - Control chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    driver.maximize_window()
    # driver.set_page_load_timeout(300)
    return driver


def search_keyword_blog_naver_by_date():
    driver = start_chrome()
    driver.get("https://www.mckinsey.com/?fbclid=IwAR1aDLmyz_4iDcKi7ArpuJEjZvzth2nCLpHP5ecUM0GSXGWFThMlv5CP7Hg")
    windows_before = driver.current_window_handle
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
    element.click()
    # accecpt_all_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    # accecpt_all_button.click()
    element = driver.find_element(By.CLASS_NAME,
                                  'mck-o-container-universal-header').find_elements(By.TAG_NAME, "a")
    for element in element:
        a = element.text
        b = ""
        link_address = element.get_attribute("href")
        driver.execute_script("window.open('{}');".format(link_address))
        driver.switch_to.window(driver.window_handles[1])
        content = driver.find_elements(By.TAG_NAME, "p")
        for i in content:
            b += i.text + "\n"
        if len(driver.window_handles) > 1:
            driver.close()
        with open("1/{}.txt".format(a), "w", encoding="utf-8") as file:
            file.write(b)
        driver.switch_to.window(windows_before)

    elements = driver.find_element(By.CLASS_NAME, "mck-o-container").find_elements(By.TAG_NAME, "a")
    print(elements)
    for element in elements:
        a = element.text
        b = ""
        link_address = element.get_attribute("href")
        print(link_address)
        driver.execute_script("window.open('{}');".format(link_address))
        driver.switch_to.window(driver.window_handles[1])
        content = driver.find_elements(By.TAG_NAME, "p")
        for i in content:
            b += i.text + "\n"
        if len(driver.window_handles) > 1:
            driver.close()
        with open("2/{}.txt".format(a), "w", encoding="utf-8") as file:
            file.write(str(b))
        driver.switch_to.window(windows_before)


search_keyword_blog_naver_by_date()
