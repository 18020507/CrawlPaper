import os

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def start_chrome():
    # 크롬 구동 - Control chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    # driver.set_page_load_timeout(300)
    return driver


def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    else:
        print(f"Directory '{directory_path}' already exists.")


def remove_special_characters(input_string):
    special_characters = "!@#$%^&*()_+{}[]|\\;:'\"<>,.?/~`"

    cleaned_string = ''.join([char for char in input_string if char not in special_characters])

    return cleaned_string


def crawl_data_home():
    driver = start_chrome()
    driver.get("https://www.mckinsey.com/")
    windows_before = driver.current_window_handle
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
    element.click()
    accecpt_all_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    accecpt_all_button.click()
    list_ele_home = []
    element = driver.find_element(By.CLASS_NAME,
                                  'mck-o-container-universal-header').find_elements(By.TAG_NAME, "a")
    element1 = driver.find_element(By.CLASS_NAME, "mck-o-container").find_elements(By.TAG_NAME, "a")
    list_ele_home.append(element)
    list_ele_home.append(element1)
    for element in list_ele_home:
        for e in element:
            a = e.text.replace("\n", "")
            b = ""
            link_address = e.get_attribute("href")
            driver.execute_script("window.open('{}');".format(link_address))
            driver.switch_to.window(driver.window_handles[1])
            content = driver.find_elements(By.TAG_NAME, "p")
            for i in content:
                b += i.text + "\n"
            if len(driver.window_handles) > 1:
                driver.close()
            with open("Home/{}.txt".format(str(a)), "w", encoding="utf-8") as file:
                file.write(b)
            driver.switch_to.window(windows_before)
    # driver.close()
    # driver.quit()


def crawl_industries(url= None, folder= None):
    driver = start_chrome()
    driver.get("https://www.mckinsey.com/industries/education/our-insights")
    windows_before = driver.current_window_handle
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
    element.click()
    accecpt_all_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    accecpt_all_button.click()
    last_height = driver.execute_script("return document.body.scrollHeight")
    folder_name = remove_special_characters(driver.find_element(By.TAG_NAME, 'h1').text).replace(" ", "")

    create_directory(folder_name)
    elements = driver.find_elements(By.TAG_NAME, "body")
    print(elements)
    for element in elements:
        for e in range(0, len(element.find_elements(By.TAG_NAME, "a")), 2):
            link = element.find_elements(By.TAG_NAME, "a")[e]

            b = ""
            link_address = link.get_attribute("href")
            print(link_address)
            if "https://www.mckinsey.com/industries/" in link_address:
                driver.execute_script("window.open('{}');".format(link_address))
                driver.switch_to.window(driver.window_handles[1])

                content = driver.find_elements(By.CLASS_NAME, "mdc-o-content-body")
                try:
                    file_name = remove_special_characters(driver.find_element(By.TAG_NAME, 'h1').text)
                except:
                    file_name = remove_special_characters(driver.find_element(By.TAG_NAME, 'h2').text)
                # print(file_name)
                for i in content:
                    i.find_elements(By.TAG_NAME, "p")
                    for p in i.find_elements(By.TAG_NAME, "p"):
                        b += p.text + "\n"
                with open("{}/{}.txt".format(folder_name,str(file_name)), "w", encoding="utf-8") as file:
                    file.write(b)
                if len(driver.window_handles) > 1:
                    driver.close()
                driver.switch_to.window(windows_before)
            else:
                print("URL không thỏa mãn điều kiện:", link_address)


# driver = start_chrome()
# driver.get('https://www.mckinsey.com/industries')
# windows_before = driver.current_window_handle
# wait = WebDriverWait(driver, 10)
# element = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
# element.click()
# accecpt_all_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
# accecpt_all_button.click()
# elements = driver.find_elements(By.CLASS_NAME, "mck-o-container")[1]
# for i in elements.find_elements(By.TAG_NAME, "a"):
#     if "https://www.mckinsey.com/industries/" in i.get_attribute("href"):
#         crawl_industries(i.get_attribute("href"), "Industries")

crawl_industries()