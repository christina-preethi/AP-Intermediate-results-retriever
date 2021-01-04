from selenium import webdriver
import csv
import os
import logging
import time

logging.basicConfig(
    filename='logs/inter_results.log',
    filemode='a', format='%(asctime)s %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def init(webdriver_path, website_url, workspace):
    logging.info("Creating web driver")
    driver = webdriver.Chrome(executable_path=webdriver_path)

    logging.info("Setting script timeout to 2s")
    driver.set_script_timeout(2)

    logging.info("Getting website URL")
    driver.get(website_url)

    logging.info("Setting workspace")
    os.chdir(workspace)

    return driver

def fetch_result_info(driver, rollno):
    logging.info("Fetching input element")
    inputElement = driver.find_element_by_id("txtHTNo")
    inputElement.send_keys(rollno)

    logging.info("Fetching submit button")
    submit_button = driver.find_element_by_id("btnSubmit")
    submit_button.click() 
    time.sleep(1)

    result_info = []
    logging.info("Fetching all the required fields and appending to list")
    hallticket_no = driver.find_element_by_xpath("//span[@id='lblHTNo']").text
    result_info.append(hallticket_no)

    name = driver.find_element_by_xpath("//span[@id='lblName']").text
    result_info.append(name)
    
    grade = driver.find_element_by_xpath("//span[@id='lblTotal']").text
    result_info.append(grade)
    
    result = driver.find_element_by_xpath("//span[@id='lblResultGrade']").text
    result_info.append(result)
    
    english_paper1 = driver.find_element_by_xpath("//span[@id='lblSubMarks1']").text
    result_info.append(english_paper1)

    sanskrit_paper1 = driver.find_element_by_xpath("//span[@id='lblSubMarks2']").text
    result_info.append(sanskrit_paper1)

    mathematics_paper1a = driver.find_element_by_xpath("//span[@id='lblSubMarks3']").text
    result_info.append(mathematics_paper1a)

    mathematics_paper1b = driver.find_element_by_xpath("//span[@id='lblSubMarks4']").text
    result_info.append(mathematics_paper1b)

    physcis_paper_1 = driver.find_element_by_xpath("//span[@id='lblSubMarks5']").text
    result_info.append(physcis_paper_1)

    chemistry_paper_1 = driver.find_element_by_xpath("//span[@id='lblSubMarks6']").text
    result_info.append(chemistry_paper_1)
    
    return result_info

if __name__ == '__main__':
    WEBDRIVER_PATH = "C:/Users/hp/Downloads/chromedriver_win32/chromedriver.exe"
    WEBSITE_URL = "http://results.eenadu.net/inter-2020/ap-inter-1st-year-results-2020-general.aspx"
    WORKSPACE = "D:\AP inter results\Results"
    driver = init(WEBDRIVER_PATH, WEBSITE_URL, WORKSPACE)

    fields = ['HallTicket_No', 'Name', 'Grade', 'Result', 'ENGLISH', 'SANSKRIT', '1A', '1B', 'Physics', 'Chemistry']
    filename = "inter_results.csv"
    with open(filename, 'w', newline='') as csvfile:  
        csvwriter = csv.writer(csvfile)  
        csvwriter.writerow(fields)  
    
        with open('inter_halltickets.csv') as f:
            csv_f = csv.reader(f)
            for record in csv_f:
                info = fetch_result_info(driver, record[0])
                csvwriter.writerow(info) 
               
    driver.close()

