import pwinput
from bs4 import BeautifulSoup
import mechanicalsoup
from time import sleep
import os
from tabulate import tabulate


def is_float_digit(n: str) -> bool:
    try:
        float(n)
        return True
    except ValueError:
        return False


def display_welcome_msg():
    pagex = browser.get("https://webkiosk.thapar.edu/CommonFiles/TopTitle.jsp")
    html = pagex.soup
    with open("myResult_fetcher_html.html", "w", encoding="utf-8") as f:
        f.write(str(html))

    with open("myResult_fetcher_html.html", "r") as f:
        html_doc = f.read()

    soup = BeautifulSoup(html_doc, "html.parser")
    my_list = soup.get_text().split()
    my_list = list(filter('Â'.__ne__, my_list))
    print(f"\n\t\t\t{my_list[len(my_list) - 2]}")


def fetch_cg():
    cg_page = browser.get("https://webkiosk.thapar.edu/StudentFiles/Exam/StudCGPAReport.jsp")
    cg_html = cg_page.soup
    with open("myResult_fetcher_html.html", "w", encoding="utf-8") as f:
        f.write(str(cg_html))

    with open("myResult_fetcher_html.html", "r") as f:
        html_doc = f.read()

    soup = BeautifulSoup(html_doc, "html.parser")
    index = len(soup.findAll("td")) - 2
    print("\nThe current CGPA extracted: ", soup.findAll("td")[index].get_text())


def fetch_grades():
    grades_page = browser.get("https://webkiosk.thapar.edu/StudentFiles/Exam/StudentEventGradesView.jsp")
    grades_html = grades_page.soup
    with open("myResult_fetcher_html.html", "w", encoding="utf-8") as f:
        f.write(str(grades_html))

    with open("myResult_fetcher_html.html", "r") as f:
        html_doc = f.read()

    soup = BeautifulSoup(html_doc, "html.parser")
    my_list = soup.find(id="table-1").get_text().split()
    my_list = list(filter('Â'.__ne__, my_list))
    my_list = list(filter('2223EVESEM'.__ne__, my_list))
    my_list = list(filter('2223ODDSEM'.__ne__, my_list))
    my_list = list(filter('Awarded'.__ne__, my_list))

    my_list1, temp = [], []
    i = 8

    print("\nThe Exam Grades are as follows -\n")

    while i < len(my_list):
        #i += 1
        if my_list[i - 1] in {'A+', 'A', 'A-', 'B', 'B-', 'C', 'C-', 'E', 'F', 'RA', 'I', 'X'}:
            my_list1.append(temp)
            temp = []
        temp.append(my_list[i])
        i += 1
    my_list1.append(temp)
    for i in my_list1:
        temp_str = ""
        count = 0
        for j in i:
            if j.strip().isdecimal() or j.strip().isnumeric() or is_float_digit(j):
                break
            temp_str += j + " "
            count += 1
        i[0] = temp_str

        for k in range(count, len(i)):
            i[k - count + 1] = i[k]
        for l in range(count - 1):
            i.pop()
    # my_list1.insert(0, ['Course Name(Course Code)', 'Obtained Marks', 'Maximum Marks', 'Grade Awarded'])
    print(tabulate(my_list1))


def tableDataText(table):
    def rowgetDataText(tr, coltag='td'):
        return [td.get_text(strip=True) for td in tr.find_all(coltag)]
    try:
        rows = []
        trs = table.find_all('tr')
        headerow = rowgetDataText(trs[0], 'th')
        if headerow:  # if there is a header row include first
            rows.append(headerow)
            trs = trs[1:]
        for tr in trs:  # for every table row
            rows.append(rowgetDataText(tr, 'td'))  # data row
        return rows
    except:
        print("\t\t----No DateSheet Available----")


def fetch_info():
    grades_page = browser.get("https://webkiosk.thapar.edu/StudentFiles/PersonalFiles/StudPersonalInfo.jsp")
    grades_html = grades_page.soup
    with open("myResult_fetcher_html.html", "w", encoding="utf-8") as f:
        f.write(str(grades_html))

    with open("myResult_fetcher_html.html", "r") as f:
        html_doc = f.read()
    print("\n")
    htmltable = grades_html.find('table')
    list_table = tableDataText(htmltable)
    print(tabulate(list_table))


def fetch_datesheet():
    datesheet_page = browser.get("https://webkiosk.thapar.edu/StudentFiles/Exam/StudViewDateSheet.jsp")
    datesheet_html = datesheet_page.soup
    with open("myResult_fetcher_html.html", "w", encoding="utf-8") as f:
        f.write(str(datesheet_html))

    with open("myResult_fetcher_html.html", "r") as f:
        html_doc = f.read()
    print("\n")
    htmltable = datesheet_html.find(id="table-1")
    list_table = tableDataText(htmltable)
    print(tabulate(list_table))

'''--------------------------------------------------------------------__main__----------------------------------------------------------------------'''

browser = mechanicalsoup.Browser()
url = "https://webkiosk.thapar.edu/"
page = browser.get(url)
login_html = page.soup

os.system('cls')

while True:
    print("\t\t\tWELCOME TO MyResultFetcher\nPls enter your credentials-\n")
    eno = input("Enrollment Number: ")
    password = pwinput.pwinput()

    form = login_html.select("form")[0]
    form.select("input")[2]["value"] = "102217202"
    form.select("input")[4]["value"] = "singh123"

    home_page = browser.submit(form, page.url)

    if home_page.url == "https://webkiosk.thapar.edu/StudentFiles/StudentPage.jsp":
        display_welcome_msg()
        print(
            "\npress 1 for CGPA\npress 2 for Exam Grades\npress 3 for Date Sheet\npress 4 for Personal Information\npress 9 to LogOut\n")
        try:
            choice = int(input("enter choice: "))
            while True:
                if choice == 1:
                    fetch_cg()
                    choice = int(input("\nenter choice: "))

                elif choice == 2:
                    fetch_grades()
                    choice = int(input("\nenter choice: "))

                elif choice == 3:
                    fetch_datesheet()
                    choice = int(input("\nenter choice: "))

                elif choice == 4:
                    fetch_info()
                    choice = int(input("\nenter choice: "))

                elif choice == 9:
                    print("\t\t\tLoging Out !!")
                    sleep(1)
                    os.system('cls')
                    break
                else:
                    print("\t\t\t----invalid choice----")
                    choice = int(input("\nenter choice: "))
        except ValueError:
            print("\t\t\t----invalid choice----")
            choice = int(input("\nenter choice: "))

    else:
        print("\n\t\t\tError loging in !!\n")
        sleep(2)
        os.system('cls')
