from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv

with open('courses.csv', 'w') as f:
    writer = csv.writer(f)

    header = ['number', 'name', 'description']

    writer.writerow(header)

    # create a new Firefox browser and navigate to the webpage

    DRIVER_PATH = '/path/to/chromedriver'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    NUM_PAGES = 185

    for i in range(NUM_PAGES):
        driver.get('https://explorecourses.stanford.edu/search?view=catalog&filter-coursestatus-Active=on&page=' + str(i) + '&catalog=&academicYear=&q=all&collapse')

        # wait for the elements with class 'courseInfo' to be present on the page
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "courseInfo"))
        )

        # find all elements with class 'courseInfo' and store them in a list
        elements = driver.find_elements(By.CLASS_NAME, 'courseInfo')

        for element in elements:
            number_element = element.find_element(By.CLASS_NAME, "courseNumber")
            title_element = element.find_element(By.CLASS_NAME, "courseTitle")
            description_element = element.find_element(By.CLASS_NAME, "courseDescription")

            print(number_element.text)
            print(title_element.text)
            print(description_element.text)

            row = [number_element.text, title_element.text, description_element.text]
            writer.writerow(row)

        # print the number of elements found
        print(f'Number of elements found: {len(elements)}')

driver.quit()
