from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.chrome.options import Options
import warnings
import time
import chromedriver_autoinstaller
import getpass

chromedriver_autoinstaller.install()

warnings.filterwarnings("ignore", category=DeprecationWarning)
def get_attendance_record(username, password, year, season):
    data = {
        "logonuidfield": username,
        "logonpassfield": password
    }

    options = Options()
    options.add_argument('--log-level-3')
    options.add_argument('--headless')
    web = webdriver.Chrome(executable_path="chromedriver.exe", options=options)

    def click_by_class_name(ele):
        while True:
            if web.find_elements_by_class_name(ele):
                return web.find_element_by_class_name(ele).click()
            else:
        
                time.sleep(1)

    def click_by_xpath(ele):
        while True:
            if web.find_elements(by=By.XPATH, value=ele):
                return web.find_element_by_xpath(ele).click()
            else:
                print(True)
                time.sleep(1)

    def click_by_id(ele):
        while True:
            if web.find_elements(by=By.ID, value=ele):
                return web.find_element_by_id(ele).click()
            else:
                print(True)
                time.sleep(1)

    web.get("https://kiitportal.kiituniversity.net/irj/portal/")

    for i in data:
        web.find_element_by_id(i).send_keys(data[i])

    web.find_element_by_id(i).send_keys(Keys.ENTER)
    time.sleep(2)
    if "User authentication failed" in web.find_elements_by_tag_name("html")[0].text:
        return "Failed to pass credentials"
        web.quit()
    else:
        click_by_class_name("prtlTopNav1stLvl-i")

        web.switch_to.frame("Desktop Inner Page    ")

        web.find_elements_by_css_selector("span[class='urTxtStd']")[0].click()

        for i in web.find_elements_by_css_selector("span[class='urTxtStd']"):
            if i.text == "Student Attendance Details":
                i.click()
                break

        web.switch_to.frame("isolatedWorkArea")

        while True:
            if web.find_elements_by_id("WD5C"):
                break
            else:
                time.sleep(0.3)

        web.find_element_by_id("WD5C").send_keys(year)

        web.find_element_by_id("WD74").send_keys(season)

        web.find_element_by_id("WD81").click()

        time.sleep(3)

        tg1, tg2, tg3, tg4 = -1, -1, -1, -1

        for i in range(len(web.find_elements_by_tag_name('td'))):
            if tg1 == -1 or tg2 == -1 or tg3 == -1 or tg4 == -1:
                if web.find_elements_by_tag_name('td')[i].text == "Subject":
                    tg1 = i+10
                if web.find_elements_by_tag_name('td')[i].text == "No.of Present":
                    tg2 = i+10
                if web.find_elements_by_tag_name('td')[i].text == "No.of Absent":
                    tg3 = i+10
                if web.find_elements_by_tag_name('td')[i].text == "Total No. of Days":
                    tg4 = i+10
            else:
                break
        
        if tg1 == -1 or tg2 == -1 or tg3 == -1 or tg4 == -1:
            return "Column in Attendance Table is hidden"

        data = {
            "Subject": [], 
            "No. of Present": [], 
            "No. of Absent": [], 
            "Total No. of days": [],
        }
                
        sub = []

        while True:
            try:
                if web.find_elements_by_tag_name('td')[tg1].text.strip() != "":
                    data['Subject'].append(web.find_elements_by_tag_name('td')[tg1].text)
                else:
                    break
                
                if web.find_elements_by_tag_name('td')[tg2].text.strip() != "":
                    data['No. of Present'].append(web.find_elements_by_tag_name('td')[tg2].text)
                else:
                    break
                
                if web.find_elements_by_tag_name('td')[tg3].text.strip() != "":
                    data['No. of Absent'].append(web.find_elements_by_tag_name('td')[tg3].text)
                else:
                    break
                
                if web.find_elements_by_tag_name('td')[tg4].text.strip() != "":
                    data['Total No. of days'].append(web.find_elements_by_tag_name('td')[tg4].text)
                else:
                    break

                tg1+=10
                tg2+=10
                tg3+=10
                tg4+=10

            except:
                break
        
        for i in range(len(data["Subject"])):
            if int(data["No. of Present"][i].split(".")[0])/int(data["Total No. of days"][i].split(".")[0])>=0.75:
                sub.append([data["Subject"][i], int(data["No. of Present"][i].split(".")[0]),int(data["No. of Absent"][i].split(".")[0]), int(data["Total No. of days"][i].split(".")[0])])
            else:
                a, b = int(data["No. of Present"][i].split(".")[0]), int(data["Total No. of days"][i].split(".")[0])
                while a/b<0.75:
                    a+=1
                    b+=1
                sub.append([data["Subject"][i], int(data["No. of Present"][i].split(".")[0]),int(data["No. of Absent"][i].split(".")[0]), int(data["Total No. of days"][i].split(".")[0]), a-int(data["No. of Present"][i].split(".")[0])])
        
        web.quit()
        return sub
