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
def get_attendance_record(username, password):
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

        web.find_element_by_id("WD5C").send_keys('2021-2022')

        web.find_element_by_id("WD74").send_keys('Spring')

        web.find_element_by_id("WD81").click()

        time.sleep(3)

        data_ = web.find_element_by_tag_name("html").text.split("\n")

        data = {
            "Subject": [], 
            "No. of Present": [], 
            "No. of Absent": [], 
            "Total No. of days": [],
            "Total Precentage": [],
            "Total precentage of excuses": [], 
            "Faculty Code": [], 
            "Faculty Name": [], 
            "No. of Execuses": []
        }

        for i in data_:
            if i.startswith("  ") and len(i.split(" "))>=9:
                subject = ""
                np = -1
                na = -1
                tnd = -1
                tp = -1
                tpe = -1
                fc = -1
                fn = ""
                ne = -1
                for j in i.split():
                    if j.isalpha() or j == 'Mathematics-II':
                        if np == -1:
                            subject += j + " "
                        else:
                            fn += j + " "
                    else:
                        if np == -1:
                            np = j
                        elif na == -1:
                            na = j
                        elif tnd == -1:
                            tnd = j
                        elif tp  ==  -1:
                            tp = j
                        elif tpe == -1:
                            tpe = j
                        elif fc == -1:
                            fc = j
                        elif ne == -1:
                            ne = j
                data["Subject"].append(subject)
                data["No. of Present"].append(np)
                data["No. of Absent"].append(na)
                data["Total No. of days"].append(tnd)
                data["Total Precentage"].append(tp)
                data["Total precentage of excuses"].append(tpe)
                data["Faculty Code"].append(fc)
                data["Faculty Name"].append(fn)
                data["No. of Execuses"].append(ne)

        sub = []

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
