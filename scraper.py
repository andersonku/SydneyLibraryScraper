from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium

from pprint import pprint


def get_subjects(tr_element):
    result = dict()
    try:
        head = tr_element.find_element_by_css_selector("div.divItems")
        result['id'] = head.get_attribute("id")

        tr_elements = tr_element.find_elements_by_css_selector("table.tblLinks > tbody > tr.InnerItemStyle")
        result['subjects'] = list()
        for tr in tr_elements:
            key = tr.find_element_by_css_selector("td:nth-child(2)").text
            value = tr.find_element_by_css_selector("td:nth-child(3)").text
            if key == "Subject": result['subjects'].append(value)

    except selenium.common.exceptions.NoSuchElementException:
        return None
    return result


def get_book_info(tr_element):
    id = tr_element.get_attribute("id");
    if not id: return get_subjects(tr_element)
    result = dict()
    result['id'] = id
    span_element = tr_element.find_element_by_css_selector("span.WorkTitle")
    result['title'] = span_element.text
    work_details = tr_element.find_element_by_css_selector("div.divWorkDetails")
    result['detail'] = work_details.text
    return result


def get_more_detail(tr_element):
    try:
        more_detail = tr_element.find_element_by_css_selector("td:nth-child(2) > div > span.BlueLinks > u")
        if more_detail: more_detail.click()
    except selenium.common.exceptions.NoSuchElementException:
        pass
    finally:
        pass


def main():
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 10)
    driver.get("https://library.cityofsydney.nsw.gov.au/opac/Default.aspx")
    driver.find_element_by_xpath("//*[@id=\"ctl00_BodyPlaceHolder_SearchTabStrip\"]/div/ul/li[3]/a").click()
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[@id=\"ctl00_BodyPlaceHolder_coNumberOfDays_Input\"]"))
    )

    # Set time in the past 84 Days
    driver.find_element_by_xpath("//*[@id=\"ctl00_BodyPlaceHolder_coNumberOfDays_Input\"]").send_keys(Keys.BACKSPACE * 10 + "1" + Keys.ENTER)

    # Search
    driver.find_element_by_xpath("//*[@id=\"ctl00_BodyPlaceHolder_ButtonNewlyAcquired\"]").click()

    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#ctl00_BodyPlaceHolder_divSearchResults > table > tbody"))
    )

    # ctl00_BodyPlaceHolder_lblTotalPagesDDS
    total_pages = int(driver.find_element_by_css_selector("#ctl00_BodyPlaceHolder_lblTotalPagesDDS").text)
    current_page = 1;

    while current_page <= total_pages:
        if current_page > 1:
            driver.find_element_by_css_selector("#ctl00_BodyPlaceHolder_coPagesDDS_Input").clear()
            driver.find_element_by_css_selector("#ctl00_BodyPlaceHolder_coPagesDDS_Input").send_keys(str(current_page) + Keys.ENTER)



        wait.until(
            #ctl00_BodyPlaceHolder_lblInfoDDS2
            EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "#ctl00_BodyPlaceHolder_lblInfoDDS2"), str((current_page-1)*25 + 1)))(
        )
        tr_elements = driver.find_elements_by_css_selector("#ctl00_BodyPlaceHolder_divSearchResults > table > tbody > tr")
        current_page += 1
        continue
        count = 0
        for tr_element in tr_elements:
            get_more_detail(tr_element)
        #
        # tr_elements = driver.find_elements_by_css_selector("#ctl00_BodyPlaceHolder_divSearchResults > table > tbody > tr")
        # for tr_element in tr_elements:
            book = get_book_info(tr_element)
            pprint(book)

            count += 1
            if count > 1: break;
main()
