from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def check_element_exists(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
        return True
    except Exception:
        return False

chrome_options = Options()
chrome_options.add_argument("--start-maximized")  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--no-sandbox")  

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.commencis.com/thoughts/")

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='isotope-container grid-container isotope-layout style-masonry isotope-pagination grid-pagination un-isotope-init']"))
)
populars = driver.find_elements(By.XPATH, "//div[@class='isotope-container grid-container isotope-layout style-masonry isotope-pagination grid-pagination un-isotope-init']")

anchor_links = set()

for popular in populars:
    popular_anchors = popular.find_elements(By.TAG_NAME, "a")
    
    for anchor in popular_anchors:
        href = anchor.get_attribute('href') 
        target = anchor.get_attribute('target')  

        if href and target == "_self":
            anchor_links.add(href)  

driver.quit()


expected_name = "Commencis"
expected_src = "https://cdn-www.commencis.com/wp-content/uploads/2018/03/favicon_commencis.png"
expected_alt = "commencis logo"

for link in anchor_links:
    driver2 = webdriver.Chrome(service=service, options=chrome_options)
    
    driver2.get(str(link))  
    time.sleep(2)

    try:
        info_div = driver2.find_element(By.XPATH, "//div[@class='icon-box icon-box-left  icon-media-image']")
        name = info_div.find_elements(By.TAG_NAME, "h3")[0].text
        logo_alt = info_div.find_elements(By.TAG_NAME, "img")[0].get_attribute('alt')
        logo_src = info_div.find_elements(By.TAG_NAME, "img")[0].get_attribute('src')

        date = driver2.find_element(By.XPATH, "//span[@class='date-info']").text
        email = check_element_exists(driver2, "//input[@type='email']")
        tune = check_element_exists(driver2, "//input[@value='Stay Tuned']") 
        blog_title = check_element_exists(driver2, "//div[@id='blog-title']") or check_element_exists(driver2, "//div[@class='heading-text el-text']")
        #blog_title_helper = driver2.find_element(By.XPATH, "//div[@id='blog-title']")
        #blog_title = blog_title_helper.find_elements(By.TAG_NAME, "h1")[0].text

        # Print extracted information
        print(50*"*")
        print(f"Name: {name}")
        print(f"Date: {date}")
        print(f"Blog Title Exist: {blog_title}")
        print(f"Email Exists: {email}")
        print(f"Tune Exists: {tune}")

        if name == expected_name or logo_src == expected_src or logo_alt == expected_alt:
            if name == expected_name and logo_src == expected_src and logo_alt == expected_alt:
                print(f"Commencis and true : {link}")
            else:
                print(f"Commencis but false : {link}")
        else:
            print(f"No Commencis : {link}")
    except Exception as e:
        print(f"An error occurred while processing the link {link}: {e}")

    #driver2.quit()
