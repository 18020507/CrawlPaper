import os
import time
import uuid

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
    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    # driver.maximize_window()
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


def crawl_industries(url=None, folder=None):
    driver = start_chrome()
    driver.get("https://www.mckinsey.com/alumni/")
    windows_before = driver.current_window_handle
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
    element.click()
    accecpt_all_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    accecpt_all_button.click()
    #  xử lý Viewmore
    # for i in range(6):
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     driver.implicitly_wait(1)
    #     button = driver.find_element(By.ID, "viewMore")
    #     time.sleep(1)
    #     button.click()
    #     time.sleep(3)
    #     print(button)
    folder_name = remove_special_characters(driver.find_element(By.TAG_NAME, 'h1').text).replace(" ", "")
    # folder_name = folder
    create_directory("industries/{}".format(folder_name))
    elements = driver.find_elements(By.TAG_NAME, "body")
    print(elements)
    for element in elements:
        try:
            for e in range(0, len(element.find_elements(By.TAG_NAME, "a")), 2):
                link = element.find_elements(By.TAG_NAME, "a")[e]
                link_address = link.get_attribute("href")
                print(link_address)
                if "https://www.mckinsey.com/industries/" or "https://www.mckinsey.com/capabilities/" or "https://www.mckinsey.com/featured-insights/" or 'https://www.mckinsey.com/alumni' in link_address:
                    b = ""
                    b += link_address + "\n"

                    try:
                        driver.execute_script("window.open('{}');".format(link_address))
                        driver.switch_to.window(driver.window_handles[1])

                        content = driver.find_elements(By.CLASS_NAME, "mdc-o-content-body")
                        try:
                            file_name = remove_special_characters(driver.find_element(By.TAG_NAME, 'h1').text).replace(
                                " ", "")
                        except:
                            file_name = str(uuid.uuid4())
                        print(file_name)
                        # print(file_name)
                        for i in content:
                            data = i.find_elements(By.TAG_NAME, "p")
                            for p in data:
                                b += p.text + "\n"
                            if len(data) == 0:
                                data = driver.find_element(By.TAG_NAME, "body")
                                b += data.text
                            print(b)
                        with open("about-us/alumni/{}.txt".format(str(file_name)), "w", encoding="utf-8") as file:
                            file.write(b)
                        if len(driver.window_handles) > 1:
                            driver.close()
                        driver.switch_to.window(windows_before)
                    except Exception as e:
                        print("Looix", e)
                        pass

            else:
                print("URL không thỏa mãn điều kiện:", link_address)
        except:
            print("URL lỗi", link)
            pass


def crawl_one_tab(url):
    driver = start_chrome()
    driver.get(url)
    windows_before = driver.current_window_handle
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
    element.click()
    accecpt_all_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    accecpt_all_button.click()
    file_name = remove_special_characters(driver.find_element(By.TAG_NAME, 'h1').text).replace(
        " ", "-")
    content = driver.find_elements(By.CLASS_NAME, "mdc-o-content-body")
    b = ""
    print(file_name)
    for i in content:
        data = i.find_elements(By.TAG_NAME, "p")
        if len(data) != 0:
            for p in data:
                b += p.text + "\n"
            print('lay the b')
        if len(data) == 0:
            data = driver.find_element(By.TAG_NAME, "body")
            b += data.text
            print('lay all')
    with open("featured-insights/business-resilience/{}.txt".format((file_name)), "w", encoding="utf-8") as file:
        file.write(b)


url = []
url_loi = []


def crawl_featured_insights(url=None, folder=None):
    url_loi = []
    driver = start_chrome()
    driver.get(url)
    windows_before = driver.current_window_handle
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
    element.click()
    accecpt_all_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    accecpt_all_button.click()
    #  xử lý Viewmore
    # for i in range(6):
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     driver.implicitly_wait(1)
    #     button = driver.find_element(By.ID, "viewMore")
    #     time.sleep(1)
    #     button.click()
    #     time.sleep(3)
    #     print(button)
    elements = driver.find_element(By.TAG_NAME, "body").find_elements(By.TAG_NAME, "a")
    try:
        for e in range(0, len(elements), 2):
            link_address = elements[e].get_attribute("href")
            if link_address is None:
                continue
            if ("https://www.mckinsey.com/industries/" in link_address
                    or "https://www.mckinsey.com/capabilities/" in link_address
                    or "https://www.mckinsey.com/mhi/our-insights/" in link_address):
                print(link_address)
                if link_address not in url:
                    print("true")
                    try:
                        b = ""
                        b += link_address + "\n"
                        driver.execute_script("window.open('{}');".format(link_address))
                        driver.switch_to.window(driver.window_handles[1])
                        try:
                            # content = wait.until(EC.element_to_be_selected((By.CLASS_NAME, "mdc-o-content-body")))
                            content = driver.find_elements(By.CLASS_NAME, "mdc-o-content-body")
                        except:
                            print("Lỗi")
                            if len(driver.window_handles) > 1:
                                driver.close()
                            driver.switch_to.window(windows_before)
                            continue
                        try:
                            file_name = remove_special_characters(driver.find_element(By.TAG_NAME, 'h1').text).replace(
                                " ", "-")
                        except:
                            file_name = str(uuid.uuid4())
                        file_name = file_name + (str(e))
                        print(file_name)
                        if file_name is None:
                            file_name = str(uuid.uuid4())
                        try:
                            for i in content:
                                data = i.find_elements(By.TAG_NAME, "p")
                                if len(data) != 0:
                                    for p in data:
                                        b += p.text + "\n"
                                    print('lay the b')
                                if len(data) == 0:
                                    data = driver.find_element(By.TAG_NAME, "body")
                                    b += data.text
                                    print('lay all')
                            with open("featured-insights/bem/{}.txt".format(str(file_name)),
                                      "w", encoding="utf-8") as file:
                                file.write(b)
                            print('Success')
                        except:
                            print("Lỗi")
                            if len(driver.window_handles) > 1:
                                driver.close()
                            driver.switch_to.window(windows_before)
                            continue
                        if len(driver.window_handles) > 1:
                            driver.close()
                        driver.switch_to.window(windows_before)
                    except Exception as e:
                        print(e)
                        url_loi.append(link_address)
                        continue
        print(url_loi)
    except Exception as e:
        print(e)


# crawl_one_tab('https://www.mckinsey.com/industries/healthcare/our-insights/preparing-healthcare-leaders-for-the-next-economic-downturn')
# crawl_featured_insights('https://www.mckinsey.com/bem/our-insights')

def crawl_careers(url=None):
    driver = start_chrome()
    driver.get(url)
    windows_before = driver.current_window_handle
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
    element.click()
    accecpt_all_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    accecpt_all_button.click()
    #  xử lý Viewmore
    # for i in range(6):
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     driver.implicitly_wait(1)
    #     # button = driver.find_element(By.ID, "viewMore")
    #     time.sleep(2)
    #     # button.click()
    #     # time.sleep(3)
    #     # print(button)
    elements = driver.find_element(By.TAG_NAME, "body").find_elements(By.TAG_NAME, "a")
    for e in range(0, len(elements), 2):
        link_address = elements[e].get_attribute("href")
        if link_address is None:
            continue
        # if ("https://www.mckinsey.com/industries/" in link_address
        #         or "https://www.mckinsey.com/capabilities/" in link_address
        #         or "https://www.mckinsey.com/careers/internal-roles/capabilities-and-roles/" in link_address):
        if ("https://www.mckinsey.com/" in link_address):
            print(link_address)
            try:
                b = ""
                b += link_address + "\n"
                driver.execute_script("window.open('{}');".format(link_address))
                driver.switch_to.window(driver.window_handles[1])
                data = driver.find_element(By.TAG_NAME, "body")
                b += data.text
                file_name = remove_special_characters(driver.find_element(By.TAG_NAME, 'h1').text).replace(
                    " ", "-")
                print(file_name)
                with open("careers/home/{}.txt".format(str(file_name)),
                          "w", encoding="utf-8") as file:
                    file.write(b)
                print('Success')
                if len(driver.window_handles) > 1:
                    driver.close()
                driver.switch_to.window(windows_before)
            except Exception as e:
                print("loi")
                if len(driver.window_handles) > 1:
                    driver.close()
                driver.switch_to.window(windows_before)
                continue



crawl_careers("https://www.mckinsey.com/home")
