from selenium import webdriver
import csv
from PIL import Image 
import os
import logging
import time
from Screenshot import Screenshot_Clipping

logging.basicConfig(
    filename='logs/inter_results.log',
    filemode='a', format='%(asctime)s %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def init(webdriver_path, website_url, workspace):
    logging.info("Creating web driver")
    driver = webdriver.Chrome(executable_path=webdriver_path)
    # driver.get(website_url)
    logging.info("Setting script timeout to 2s")
    driver.set_script_timeout(2)

    logging.info("Maximxing and zooming to 75%")
    driver.maximize_window()
    
    logging.info("Getting website URL")
    driver.get(website_url)

    return driver

def fetch_result_as_image(driver, rollno):
    # marks_div = driver.find_element_by_xpath("//div[@id='cnct']") 
    # marks_div = driver.find_element_by_tag_name('body')
    logging.info("Fetching input element")
    inputElement = driver.find_element_by_id("txtHTNo")
    inputElement.send_keys(rollno)

    logging.info("Fetching submit button")
    submit_button = driver.find_element_by_id("btnSubmit")
    submit_button.click() 
    driver.execute_script("document.body.style.zoom='75%'")
    time.sleep(2)

    logging.info("Creating image name and saving screenshot")
    image_name = rollno + ".png"
   
    driver.save_screenshot(image_name)

    return image_name

def convert_image_to_pdf(image_name):
    logging.info("Creating pdf name")
    pdf_name = image_name.replace(".png", ".pdf")

    logging.info("converting image to pdf and saving pdf")
    png = Image.open(image_name)
    im = png.convert('RGB')
    im.save(pdf_name)
    png.close()

    return pdf_name

if __name__ == '__main__':
    WEBDRIVER_PATH = "C:/Users/hp/Downloads/chromedriver_win32/chromedriver.exe"
    WEBSITE_URL = "http://results.eenadu.net/inter-2020/ap-inter-1st-year-results-2020-general.aspx"
    WORKSPACE = "D:\AP inter results\Results"
    # driver = init(WEBDRIVER_PATH, WEBSITE_URL, WORKSPACE)
    os.chdir(WORKSPACE)

    with open('inter_halltickets.csv') as f:
        csv_f = csv.reader(f)
        for record in csv_f:
            driver = init(WEBDRIVER_PATH, WEBSITE_URL, WORKSPACE)
            image_name = fetch_result_as_image(driver, record[0])
            pdf_name = convert_image_to_pdf(image_name)
            os.remove(image_name)
            driver.close()

    # driver.close()

    