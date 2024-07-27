from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import re, time


def select_date(driver, date_field_xpath, month, year, day):
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, date_field_xpath))).click()
        datePickMonth = Select(driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div[1]/div/select[1]'))
        datePickMonth.select_by_visible_text(month)
        datePickYear = Select(driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div[1]/div/select[2]'))
        datePickYear.select_by_visible_text(year)
        all_dates = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="ui-datepicker-div"]/table/tbody/tr/td/a')))
        for date in all_dates:
            if date.text == day:
                date.click()
                break
    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        print(f"Error while selecting date: {e}")

def fill_text_field(driver, xpath, text):
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath))).send_keys(text)


def click_element(driver, xpath):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()



driver_path = "C:/Drivers/edgedriver_win64/msedgedriver.exe"
service = Service(driver_path)
driver = webdriver.Edge(service=service)

try:
    driver.get("https://www.dummyticket.com/dummy-ticket-for-visa-application/")
    driver.maximize_window()

    # Selecting a product
    click_element(driver, '//*[@id="product_7441"]')

    # Entering passenger details
    fill_text_field(driver, '//*[@id="travname"]', "mohammed")
    fill_text_field(driver, '//*[@id="travlastname"]', "saif")
    fill_text_field(driver, '//*[@id="order_comments"]', "this is the ticket for holiday")

    # Date of Birth
    select_date(driver, '//*[@id="dob"]', "May", "2000", "18")

    click_element(driver, '//*[@id="sex_field"]/span/label[1]')
    click_element(driver, '//*[@id="addmorepax_field"]/span/label')

    # Additional passenger
    click_element(driver, '//*[@id="addpaxno_field"]/span/span/span[1]')
    click_element(driver, '//li[contains(text(), "add 1 more passenger (100%)")]')

    fill_text_field(driver, '//*[@id="travname2"]', "shahbaz")
    fill_text_field(driver, '//*[@id="travlastname2"]', "khan")

    # Second passenger date of birth
    select_date(driver, '//*[@id="dob2"]', "Jun", "1988", "1")

    click_element(driver, '//*[@id="sex2_1"]')
    click_element(driver, '//*[@id="select2-paxtype2-container"]')
    click_element(driver, '//li[contains(text(), "Child")]')

    click_element(driver, '//*[@id="traveltype_2"]')
    fill_text_field(driver, '//*[@id="fromcity"]', "Hyderabad")
    fill_text_field(driver, '//*[@id="tocity"]', "Sydney")

    # Departure date
    select_date(driver, '//*[@id="departon"]', "Jul", "2024", "29")

    # Return date
    select_date(driver, '//*[@id="returndate"]', "Aug", "2024", "29")

    fill_text_field(driver, '//*[@id="notes"]', "only 2 days are left for our trip !!")

    # Delivery option
    click_element(driver, '//*[@id="select2-reasondummy-container"]')
    click_element(driver, '//li[contains(text(), "Prank a friend")]')
    click_element(driver, '// *[ @ id = "deliverymethod_3"]')

    fill_text_field(driver, '//*[@id="billname"]', "XYZ......!")
    fill_text_field(driver, '//*[@id="billing_phone"]', "7887878787")
    fill_text_field(driver, '//*[@id="billing_email"]', "mohds@gmail.com")

    click_element(driver, '//*[@id="select2-billing_country-container"]')
    click_element(driver, '//li[contains(text(), "India")]')

    fill_text_field(driver, '//*[@id="billing_address_1"]', "near natraj nagar hyd")
    fill_text_field(driver, '//*[@id="billing_address_2"]', "asif nagar hyd")
    fill_text_field(driver, '//*[@id="billing_city"]', "Hyderabad")
    fill_text_field(driver, '//*[@id="billing_postcode"]', "560998")

    quantities = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="order_review"]/div[1]/table/tbody/tr/td[1]/div[3]'))
    )

    # Printing the quantity text
    for q in quantities:
        print('Quantity of your order is:', q.text.strip())

    rows = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="order_review"]/div[1]/table/tbody//td'))
    )
    #printing the price of order
    for price in rows:
        price_text = price.text.strip()
        if re.match(r'^[₹\d,]+$', price_text):
            print('Your Order Total is :', price_text)
            break
    time.sleep(5)
finally:
    driver.quit()

