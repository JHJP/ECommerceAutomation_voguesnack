import tkinter as tk
from selenium import webdriver
import time
import pandas as pd
from vogueSnack import Sourcing, Uploading, Tool
from selenium.common.exceptions import ElementClickInterceptedException
# After adding edge webdriver path to environment variable, you can execute below code.(ex. )

url = "https://sellha.kr/member/login"
url2 = "https://sellha.kr/discover"
url3 = "https://www.onch3.co.kr/login/login_web.php"
url4 = "https://www.onch3.co.kr/dbcenter_renewal/index.php"
smart_url = "https://accounts.commerce.naver.com/login?url=https%3A%2F%2Fsell.smartstore.naver.com%2F%23%2Flogin-callback"
naver_datalab_url = "https://datalab.naver.com/"
# id = "papagogo041@gmail.com"
# password = "9Hy:Snc9nqH8.9F"
# id2 = "onchan"
# password2 = "T-vtXPDK6qBerh!"
loginbtn1 = '.sc-iAEyYk.loQZmZ'
loginbtn2 = '.btn.btn-lg.btn-primary.btn-block'
smart_login_btn = 'ul.panel_wrap li.panel_item .panel_inner .btn_login_wrap .btn_login'
download_path = '/Users/papag/Downloads'
file_prefix_all = "셀하 아이템 발굴 EXCEL_전체"
closeBtnXPath = '//*[@id="ch-shadow-root-wrapper"]/article/div/div/div[2]/button'

# Initialize the WebDriver
def set_default_text():
    # Set default text
    id_entry.insert(0, "papagogo041@gmail.com")
    password_entry.insert(0, "9Hy:Snc9nqH8.9F")
    id2_entry.insert(0, "onchan")
    password2_entry.insert(0, "T-vtXPDK6qBerh!")
    smart_id_entry.insert(0,"voguesnack")
    smart_pw_entry.insert(0,"rq3.XW.NzXuaCc8")
    margin_entry.insert(0, "10")

def initialize_webdriver():
    global driver, EdgeSourcing, EdgeUploading, EdgeTool
    driver = webdriver.Edge()
    EdgeTool = Tool(driver, result_text)
    EdgeSourcing = Sourcing(driver, tool=EdgeTool)
    EdgeUploading = Uploading(driver, tool=EdgeTool)
    print("WebDriver Initialized")

def sourcing_action():
    while True:
            try:
                sellha_id = id_var.get()
                sellha_pw = password_var.get()
                global driver, EdgeSourcing, EdgeTool
                EdgeSourcing.login(url,sellha_id,sellha_pw,'email', 'password',loginbtn1, False)
                # time.sleep(1)
                EdgeTool.popupHandler(5)
                EdgeSourcing.pageNavigator(url2)
                time.sleep(5)
                EdgeSourcing.categoryButtonClicker(1)#All
                time.sleep(5)
                EdgeSourcing.csvButtonClicker(True)
                time.sleep(5)
                sellha_df = EdgeSourcing.downloadChecker(download_path, file_prefix_all)
                EdgeSourcing.preProcessor(sellha_df, 10000)
                EdgeSourcing.targetListMaker(pd.read_csv('sourced.csv', encoding='utf-8-sig'), False)
                break
            except ElementClickInterceptedException:
                    message = "[!] Element intercpeted. Move the page and press enter.\n"
                    EdgeTool.append_to_text_widget(message, "red")
                    input("[!] Element intercpeted. Move the page and press enter.")
def uploading_action():
    while True:
            try:
                margin = int(margin_var.get())
                onchan_id = id2_var.get()
                onchan_pw = password2_var.get()
                smart_id = smart_id_var.get()
                smart_pw = smart_pw_var.get()
                global driver, EdgeSourcing, EdgeUploading, EdgeTool
                # Move to the data center hompage and compare keywords if there is in the center or not.
                # time.sleep(5)
                EdgeSourcing.login(url3,onchan_id,onchan_pw,'username','password',loginbtn2, False)
                EdgeTool.popupHandler(3)
                EdgeUploading.keywordCompare(pd.read_csv('preprocesedSourced.csv', encoding='utf-8-sig'), False, margin)
                # Start the pricing
                EdgeTool.priceSetting(smart_url, smart_id, smart_pw, 'smart', smart_login_btn)
                break
            except ElementClickInterceptedException:
                    message = "[!] Element intercpeted. Move the page and press enter.\n"
                    EdgeTool.append_to_text_widget(message, "red")
                    input("[!] Element intercpeted. Move the page and press enter.")

def daily_sourcing_uploading_action():
    while True:
            try:
                margin = int(margin_var.get())
                onchan_id = id2_var.get()
                onchan_pw = password2_var.get()
                smart_id = smart_id_var.get()
                smart_pw = smart_pw_var.get()
                global driver, EdgeSourcing, EdgeUploading, EdgeTool
                naver_sourced_df = EdgeSourcing.daily_sourcing()
                naver_sourced_isEdited_df = EdgeSourcing.targetListMaker(naver_sourced_df, True)
                EdgeSourcing.login(url3,onchan_id,onchan_pw,'username','password',loginbtn2, False)
                EdgeTool.popupHandler(3)
                EdgeUploading.keywordCompare(naver_sourced_isEdited_df, True, margin)
                # Start the pricing
                EdgeTool.priceSetting(smart_url, smart_id, smart_pw, 'smart', smart_login_btn)
                break
            except ElementClickInterceptedException:
                    message = "[!] Element intercpeted. Move the page and press enter.\n"
                    EdgeTool.append_to_text_widget(message, "red")
                    input("[!] Element intercpeted. Move the page and press enter.")

def discount_rate_pricing_action():
    while True:
            try:
                smart_id = smart_id_var.get()
                smart_pw = smart_pw_var.get()
                global driver, EdgeSourcing, EdgeUploading, EdgeTool
                # Start the pricing
                EdgeTool.priceSetting(smart_url, smart_id, smart_pw, 'smart', smart_login_btn)
                break
            except ElementClickInterceptedException:
                    message = "[!] Element intercpeted. Move the page and press enter.\n"
                    EdgeTool.append_to_text_widget(message, "red")
                    input("[!] Element intercpeted. Move the page and press enter.")

# Initialize the main window
root = tk.Tk()
root.title("Automation Tool")
root.geometry("400x400")

# Create StringVars for entries
id_var = tk.StringVar()
password_var = tk.StringVar()
id2_var = tk.StringVar()
password2_var = tk.StringVar()
smart_id_var = tk.StringVar()
smart_pw_var = tk.StringVar()
margin_var = tk.StringVar()

# Creating Frames for each set of label and entry for better alignment
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)
frame3 = tk.Frame(root)
frame4 = tk.Frame(root)
frame5 = tk.Frame(root)
frame6 = tk.Frame(root)
frame7 = tk.Frame(root)

# Create Labels
label_id = tk.Label(frame1, text="Sellha ID")
label_password = tk.Label(frame2, text="Sellha PW")
label_id2 = tk.Label(frame3, text="Onchan ID")
label_password2 = tk.Label(frame4, text="Onchan PW")
label_smart_id = tk.Label(frame5, text="Smart ID")
label_smart_pw = tk.Label(frame6, text="Smart PW")
label_margin = tk.Label(frame7, text="Margin(%)")

# Create Entries
id_entry = tk.Entry(frame1, textvariable=id_var)
password_entry = tk.Entry(frame2, textvariable=password_var, show="*")
id2_entry = tk.Entry(frame3, textvariable=id2_var)
password2_entry = tk.Entry(frame4, textvariable=password2_var, show="*")
smart_id_entry = tk.Entry(frame5, textvariable=smart_id_var)
smart_pw_entry = tk.Entry(frame6, textvariable=smart_pw_var, show="*")
margin_entry = tk.Entry(frame7, textvariable=margin_var)

# Packing Labels and Entries in their respective frames
label_id.pack(side=tk.LEFT)
id_entry.pack(side=tk.RIGHT)
label_password.pack(side=tk.LEFT)
password_entry.pack(side=tk.RIGHT)
label_id2.pack(side=tk.LEFT)
id2_entry.pack(side=tk.RIGHT)
label_password2.pack(side=tk.LEFT)
password2_entry.pack(side=tk.RIGHT)
label_smart_id.pack(side=tk.LEFT)
smart_id_entry.pack(side=tk.RIGHT)
label_smart_pw.pack(side=tk.LEFT)
smart_pw_entry.pack(side=tk.RIGHT)
label_margin.pack(side=tk.LEFT)
margin_entry.pack(side=tk.RIGHT)

# Packing Frames
frame1.pack()
frame2.pack()
frame3.pack()
frame4.pack()
frame5.pack()
frame6.pack()
frame7.pack()

# Create buttons for Sourcing and Uploading
sourcing_btn = tk.Button(root, text="Monthly Sourcing", command=sourcing_action)
uploading_btn = tk.Button(root, text="Monthly Uploading", command=uploading_action)
webdriver_btn = tk.Button(root, text="Initialize WebDriver", command=initialize_webdriver)
daily_btn = tk.Button(root, text="Daily Sourcing & Uploading", command=daily_sourcing_uploading_action)
pricing_btn = tk.Button(root, text="Pricing", command=discount_rate_pricing_action)

webdriver_btn.pack()
sourcing_btn.pack()
uploading_btn.pack()
daily_btn.pack()
pricing_btn.pack()

# Creating and placing the result Text widget
result_text = tk.Text(root, height=10, width=50)
result_text.pack()

# Configure the tag for red text
result_text.tag_configure("red", foreground="red")

# Start the main event loop
set_default_text()
initialize_webdriver()
root.mainloop()