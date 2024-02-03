import tkinter as tk
from selenium import webdriver
import time
import pandas as pd
from vogueSnack import Sourcing, Uploading, Tool
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.edge.options import Options as EdgeOptions
from tkinter import messagebox
# After adding edge webdriver path to environment variable, you can execute below code.(ex. )

url = "https://sellha.kr/member/login"
url2 = "https://sellha.kr/discover"
url3 = "https://www.onch3.co.kr/login/login_web.php"
url4 = "https://www.onch3.co.kr/dbcenter_renewal/index.php"
smart_url = "https://accounts.commerce.naver.com/login?url=https%3A%2F%2Fsell.smartstore.naver.com%2F%23%2Flogin-callback"
coupang_url = 'https://xauth.coupang.com/auth/realms/seller/protocol/openid-connect/auth?response_type=code&client_id=wing&redirect_uri=https%3A%2F%2Fwing.coupang.com%2Fsso%2Flogin?returnUrl%3D%252F&state=456c3cf5-a6dd-4f52-abe4-cd3364bad4e4&login=true&scope=openid'
naver_datalab_url = "https://datalab.naver.com/"
onchan_prd_stat_url = "https://www.onch3.co.kr/admin_mem_clo_list_2.php?ost=&sec=&ol=&npage="
onchan_order_stat_coupang_url = "https://www.onch3.co.kr/admin_api_order.html?api_name=coupang"
onchan_order_stat_smart_url = "https://www.onch3.co.kr/admin_api_order.html?api_name=smartstore"
coupang_prd_list_url = "https://wing.coupang.com/vendor-inventory/list?searchIds=&startTime=2000-01-01&endTime=2099-12-31&productName=&brandName=&manufacturerName=&productType=&autoPricingStatus=ALL&dateType=productRegistrationDate&dateRangeShowStyle=true&dateRange=all&saleEndDatePeriodType=&includeUsedProduct=&deleteType=false&deliveryMethod=&shippingType=&shipping=&otherType=&productStatus=SAVED,WAIT_FOR_SALE,VALID,SOLD_OUT,INVALID,END_FOR_SALE,APPROVING,IN_REVIEW,DENIED,PARTIAL_APPROVED,APPROVED,ALL&advanceConditionShow=false&displayCategoryCodes=&currentMenuCode=&rocketMerchantVersion=&registrationType=&upBundling=ALL&hasUpBundlingItem=&hasBadImage=false&page=1&countPerPage=50&sortField=vendorInventoryId&desc=true&fromListV2=true&locale=ko_KR&vendorItemViolationType=&coupangAttributeOptimized=FALSE&autoPricingActive="
smart_prd_list_url = "https://sell.smartstore.naver.com/#/products/origin-list"

loginbtn1 = '.sc-iAEyYk.loQZmZ'
onchan_login_btn = '.btn.btn-lg.btn-primary.btn-block'
smart_login_btn = 'ul.panel_wrap li.panel_item .panel_inner .btn_login_wrap .btn_login'
coupang_loginbtn = '.cp-loginpage__form__submit'

download_path = '/Users/papag/Downloads'
file_prefix_all = "셀하 아이템 발굴 EXCEL_전체"
file_prefix_editable = "스마트스토어상품"
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
    coupang_id_entry.insert(0,"voguesnack")
    coupang_pw_entry.insert(0,"9w_kPvtu8Qcj93u")
    net_profit_ratio_entry.insert(0, "5")

def initialize_webdriver():
    global driver, EdgeSourcing, EdgeUploading, EdgeTool

    # Set Edge options to disable pop-ups and use Chromium engine
    options = EdgeOptions()
    options.use_chromium = True  # Ensure we're using the Chromium version of Edge
    options.add_argument("--disable-popup-blocking")  # Disable pop-up blocking
    options.add_argument("--disable-notifications")  # Disable notifications which might include the alert

    driver = webdriver.Edge(options=options)
    driver.maximize_window()
    EdgeTool = Tool(driver, result_text)
    EdgeSourcing = Sourcing(driver, tool=EdgeTool)
    EdgeUploading = Uploading(driver, tool=EdgeTool)
    print("[+] WebDriver Initialized")

def sourcing_action():
    global driver, EdgeSourcing, EdgeTool
    isloggedin_sellha = False
    isDownloaded_sellha_df = EdgeSourcing.downloadChecker('/Users/papag/Downloads', "셀하 아이템 발굴 EXCEL_전체", first_phase=True)
    isDownloaded_sourced = EdgeSourcing.downloadChecker('/Users/papag/OneDrive/src/Projects/vogueSnack', "sourced.csv", first_phase=True)
    print("[+] Sourcing phase start.")
    while True:
            try:
                if not isDownloaded_sellha_df:
                    sellha_id = id_var.get()
                    sellha_pw = password_var.get()
                    isloggedin_sellha = EdgeSourcing.login('sellha',url,sellha_id,sellha_pw,'email', 'password',loginbtn1, False)
                    if not isloggedin_sellha:
                        EdgeSourcing.login('sellha',url,sellha_id,sellha_pw,'email', 'password',loginbtn1, False)
                        EdgeTool.popupHandler(5, 'sellha')
                    EdgeTool.popupHandler(5, 'sellha')
                    EdgeSourcing.pageNavigator(url2)
                    time.sleep(5)
                    EdgeSourcing.categoryButtonClicker(1)#All
                    time.sleep(5)
                    EdgeSourcing.csvButtonClicker(True)
                    time.sleep(5)
                    sellha_df = EdgeSourcing.downloadChecker('/Users/papag/Downloads', "셀하 아이템 발굴 EXCEL_전체", first_phase=False)
                    EdgeSourcing.preProcessor(sellha_df, 10000)
                    EdgeSourcing.targetListMaker(pd.read_csv('sourced.csv', encoding='utf-8-sig'), False)
                    break
                if isDownloaded_sellha_df:
                    if isDownloaded_sourced:
                        EdgeSourcing.targetListMaker(pd.read_csv('sourced.csv', encoding='utf-8-sig'), isDaily=False)
                        break
                    if not isDownloaded_sourced:
                        sellha_df = EdgeSourcing.downloadChecker('/Users/papag/Downloads', "셀하 아이템 발굴 EXCEL_전체", first_phase=False)
                        EdgeSourcing.preProcessor(sellha_df, 10000)
                        EdgeSourcing.targetListMaker(pd.read_csv('sourced.csv', encoding='utf-8-sig'), isDaily=False)
                        break
            except ElementClickInterceptedException:
                    message = "[!] Element intercepted while sourcing.\n"
                    EdgeTool.append_to_text_widget(message, "red")
                    print("[!] Element intercepted. Scroll down the page.")
                    EdgeTool.scroll_downer(250)
                    message = "[*] Element intercepted fixed while sourcing.\n"
                    EdgeTool.append_to_text_widget(message, "blue")
    print("[+] Sourcing phase end.")

def uploading_action():
    print("[+] Uploading phase start.")
    global driver, EdgeSourcing, EdgeUploading, EdgeTool
    while True:
            try:
                net_profit_ratio = int(net_profit_ratio_var.get())
                onchan_id = id2_var.get()
                onchan_pw = password2_var.get()
                smart_id = smart_id_var.get()
                smart_pw = smart_pw_var.get()
                # Move to the data center hompage and compare keywords if there is in the center or not.
                EdgeSourcing.login('onchan',url3,onchan_id,onchan_pw,'username','password',onchan_login_btn, False)
                EdgeTool.popupHandler(3, 'onchan')
                preprocesedSourced_df = pd.read_csv('preprocesedSourced.csv', encoding='utf-8-sig')
                EdgeUploading.keywordCompare(preprocesedSourced_df, net_profit_ratio, isDaily=False, discount_rate_calculation=False, isDeliveryCharge_coupang=False, isDeliveryCharge_smart=True, is_margin_descend=False)
                break
            except ElementClickInterceptedException:
                    message = "[!] Element intercepted while uploading.\n"
                    EdgeTool.append_to_text_widget(message, "red")
                    EdgeTool.scroll_downer(250)
                    message = "[*] Element intercepted fixed while uploading.\n"
                    EdgeTool.append_to_text_widget(message, "blue")
    print("[+] Uploading phase end.")

def monthly_sourcing_uploading_action():
    sourcing_action()
    uploading_action()
    delivery_charge_changing_action()
    input("[+] press enter to finish monthly.")
    initialize_webdriver()

def daily_sourcing_uploading_action():
    net_profit_ratio = int(net_profit_ratio_var.get())
    onchan_id = id2_var.get()
    onchan_pw = password2_var.get()
    smart_id = smart_id_var.get()
    smart_pw = smart_pw_var.get()
    isloggedin = False
    global driver, EdgeSourcing, EdgeUploading, EdgeTool
    while True:
            try:
                naver_sourced_df = EdgeSourcing.daily_sourcing()
                naver_sourced_isEdited_df = EdgeSourcing.targetListMaker(naver_sourced_df, isDaily=True)
                if not isloggedin:
                    isloggedin = EdgeSourcing.login('onchan',url3,onchan_id,onchan_pw,'username','password',onchan_login_btn, False)
                    EdgeTool.popupHandler(3, 'onchan')
                EdgeUploading.keywordCompare(naver_sourced_isEdited_df, net_profit_ratio, isDaily=True, discount_rate_calculation=False, isDeliveryCharge_coupang=False, isDeliveryCharge_smart=True, is_margin_descend=False)
                delivery_charge_changing_action()
                input("press enter to close the program.")
                # return discount_rate_pricing_action() # If you want to use automize discount rate setting, turn on the line.
                break
            except ElementClickInterceptedException:
                    message = "[!] Element intercepted while daily.\n"
                    EdgeTool.append_to_text_widget(message, "red")
                    EdgeTool.scroll_downer(250)
                    message = "[*] Element intercepted fixed while daily.\n"
                    EdgeTool.append_to_text_widget(message, "blue")
    input("press enter to close the program.")

def delivery_charge_changing_action():
    isLoggedin = False
    coupang_id = coupang_id_var.get()
    coupang_pw = coupang_pw_var.get()
    global driver, EdgeSourcing, EdgeUploading, EdgeTool
    while True:
            try:
                if not isLoggedin:
                    isLoggedin = EdgeSourcing.login('coupang',coupang_url, coupang_id, coupang_pw, 'username', 'password', coupang_loginbtn, authPhase=True)
                EdgeTool.delivery_charge_changer('coupang',isDeliveryCharge=False)
                break
            except ElementClickInterceptedException:
                    message = "[!] Element intercepted. \n"
                    EdgeTool.append_to_text_widget(message, "red")
                    print("[!] Element intercepted. Scroll down the page.")
                    EdgeTool.scroll_downer(250)

def discount_rate_pricing_action():
    isLoggedin = False
    coupang_url = 'https://xauth.coupang.com/auth/realms/seller/protocol/openid-connect/auth?response_type=code&client_id=wing&redirect_uri=https%3A%2F%2Fwing.coupang.com%2Fsso%2Flogin?returnUrl%3D%252F&state=456c3cf5-a6dd-4f52-abe4-cd3364bad4e4&login=true&scope=openid'
    usernameBox = 'username'
    passwordBox = 'password'
    loginbtn = '.cp-loginpage__form__submit'
    smart_id = smart_id_var.get()
    smart_pw = smart_pw_var.get()
    coupang_id = coupang_id_var.get()
    coupang_pw = coupang_pw_var.get()
    global driver, EdgeSourcing, EdgeUploading, EdgeTool
    while True:
            try:
                # Start the pricing
                if not isLoggedin:
                    isLoggedin = EdgeSourcing.login('smart',url,smart_id,smart_pw,'id','pw',smart_login_btn, authPhase=True)
                    # isLoggedin = EdgeSourcing.login('coupang',url, coupang_id, coupang_pw, usernameBox, passwordBox, loginbtn, authPhase=True)
                EdgeTool.discountRateSetting('smart')
                # EdgeTool.delivery_charge_changer('coupang',isDeliveryCharge=False)
                break
            except ElementClickInterceptedException:
                    message = "[!] Element intercepted. \n"
                    EdgeTool.append_to_text_widget(message, "red")
                    print("[!] Element intercepted. Scroll down the page.")
                    EdgeTool.scroll_downer(250)

    # Function to show a confirmation dialog and return True if the user clicks 'Yes'
    root = tk.Tk()

    # Show a messagebox asking for confirmation
    response = messagebox.askquestion("Confirm", "Do you want to proceed?")

    root.destroy()  # Ensure the root window is destroyed after getting the response

    return response == 'yes'

def prd_stat_checking_action():
    isLoggedin_onchan = False
    isLoggedin_coupang = False
    isLoggedin_smart = False
    checking_phase_done = False
    coupang_phase_done = False
    smart_phase_done = False
    all_phase_done = False
    smart_id = smart_id_var.get()
    smart_pw = smart_pw_var.get()
    coupang_id = coupang_id_var.get()
    coupang_pw = coupang_pw_var.get()
    onchan_id = id2_var.get()
    onchan_pw = password2_var.get()
    global driver, EdgeSourcing, EdgeUploading, EdgeTool
    while True:
        try:
            if not checking_phase_done:
                # Start the checking
                if not isLoggedin_onchan:
                    # Move to the prodcut status page in onchan.
                    isLoggedin_onchan = EdgeSourcing.login('onchan',url3,onchan_id,onchan_pw,'username','password',onchan_login_btn, False)
                    EdgeTool.popupHandler(3, 'onchan')
                    EdgeSourcing.pageNavigator(onchan_prd_stat_url)
                    # Deleting or Suspending procedure.
                    out_of_stock_prd_string, out_of_stock_prd_temp_string = EdgeTool.out_of_stock_checker()
                    checking_phase_done = True
                elif isLoggedin_onchan:
                    # Deleting or Suspending procedure.
                    out_of_stock_prd_string, out_of_stock_prd_temp_string = EdgeTool.out_of_stock_checker()
                    checking_phase_done = True
            # Coupang
            if not coupang_phase_done:
                if not isLoggedin_coupang:
                    isLoggedin_coupang = EdgeSourcing.login('coupang',coupang_url, coupang_id, coupang_pw, 'username', 'password', coupang_loginbtn, authPhase=True)
                    EdgeSourcing.pageNavigator(coupang_prd_list_url)
                    EdgeTool.out_of_stock_product_deleter('coupang', out_of_stock_prd_string, out_of_stock_prd_temp_string)
                    coupang_phase_done = True
                elif isLoggedin_coupang:
                    EdgeTool.out_of_stock_product_deleter('coupang', out_of_stock_prd_string, out_of_stock_prd_temp_string)
                    coupang_phase_done = True
            # Smart
            if not smart_phase_done:
                if not isLoggedin_smart:
                    isLoggedin_smart = EdgeSourcing.login('smart',smart_url,smart_id,smart_pw,'id','pw',smart_login_btn, True)
                    EdgeTool.popupHandler(5, 'smart')
                    EdgeSourcing.pageNavigator(smart_prd_list_url)
                    EdgeTool.popupHandler(5, 'smart')
                    EdgeTool.out_of_stock_product_deleter('smart', out_of_stock_prd_string, out_of_stock_prd_temp_string)
                    smart_phase_done = True
                elif isLoggedin_smart:
                    EdgeTool.popupHandler(5, 'smart')
                    EdgeTool.out_of_stock_product_deleter('smart', out_of_stock_prd_string, out_of_stock_prd_temp_string)
                    smart_phase_done = True
            if checking_phase_done and coupang_phase_done and smart_phase_done:
                if not all_phase_done:
                    if not isLoggedin_onchan:
                    # Move to the prodcut status page in onchan.
                        isLoggedin_onchan = EdgeSourcing.login('onchan',url3,onchan_id,onchan_pw,'username','password',onchan_login_btn, False)
                        EdgeTool.popupHandler(3, 'onchan')
                        EdgeSourcing.pageNavigator(onchan_prd_stat_url)
                        # Deleting or Suspending procedure.
                        EdgeTool.out_of_stock_finisher()
                        all_phase_done = True
                    elif isLoggedin_onchan:
                        EdgeSourcing.pageNavigator(onchan_prd_stat_url)
                        EdgeTool.popupHandler(3, 'onchan')
                        EdgeTool.out_of_stock_finisher()
                        all_phase_done = True
            break
        except ElementClickInterceptedException:
                message = "[!] Element intercepted. \n"
                EdgeTool.append_to_text_widget(message, "red")
                print("[!] Element intercepted. Scroll down the page.")
                EdgeTool.scroll_downer(250)

def gathering_order_action():
    isLoggedin_onchan = False
    onchan_id = id2_var.get()
    onchan_pw = password2_var.get()
    global driver, EdgeSourcing, EdgeUploading, EdgeTool
    while True:
        try:
            if not isLoggedin_onchan:
                # Move to the prodcut status page in onchan.
                isLoggedin_onchan = EdgeSourcing.login('onchan',url3,onchan_id,onchan_pw,'username','password',onchan_login_btn, False)
                EdgeTool.popupHandler(3, 'onchan')
                EdgeSourcing.pageNavigator(onchan_order_stat_coupang_url)
                EdgeTool.order_gathering_handler('coupang')
                EdgeSourcing.pageNavigator(onchan_order_stat_smart_url)
                EdgeTool.order_gathering_handler('smart')
            elif isLoggedin_onchan:
                EdgeSourcing.pageNavigator(onchan_order_stat_coupang_url)
                EdgeTool.order_gathering_handler('coupang')
                EdgeSourcing.pageNavigator(onchan_order_stat_smart_url)
                EdgeTool.order_gathering_handler('smart')
            break
        except ElementClickInterceptedException:
                message = "[!] Element intercepted. \n"
                EdgeTool.append_to_text_widget(message, "red")
                print("[!] Element intercepted. Scroll down the page.")
                EdgeTool.scroll_downer(250)

# Initialize the main window
root = tk.Tk()
root.title("Automation Tool")
root.geometry("500x400")

# Create StringVars for entries
id_var = tk.StringVar()
password_var = tk.StringVar()
id2_var = tk.StringVar()
password2_var = tk.StringVar()
smart_id_var = tk.StringVar()
smart_pw_var = tk.StringVar()
coupang_id_var = tk.StringVar()
coupang_pw_var = tk.StringVar()
net_profit_ratio_var = tk.StringVar()

# Creating Frames for each set of label and entry for better alignment
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)
frame3 = tk.Frame(root)
frame4 = tk.Frame(root)
frame5 = tk.Frame(root)
frame6 = tk.Frame(root)
frame7 = tk.Frame(root)
frame8 = tk.Frame(root)
frame9 = tk.Frame(root)

# Create Labels
label_id = tk.Label(frame1, text="Sellha ID")
label_password = tk.Label(frame2, text="Sellha PW")
label_id2 = tk.Label(frame3, text="Onchan ID")
label_password2 = tk.Label(frame4, text="Onchan PW")
label_smart_id = tk.Label(frame5, text="Smart ID")
label_smart_pw = tk.Label(frame6, text="Smart PW")
label_coupang_id = tk.Label(frame7, text="Smart ID")
label_coupang_pw = tk.Label(frame8, text="Smart PW")
label_net_profit_ratio = tk.Label(frame9, text="Net profit ratio(%)")

# Create Entries
id_entry = tk.Entry(frame1, textvariable=id_var)
password_entry = tk.Entry(frame2, textvariable=password_var, show="*")
id2_entry = tk.Entry(frame3, textvariable=id2_var)
password2_entry = tk.Entry(frame4, textvariable=password2_var, show="*")
smart_id_entry = tk.Entry(frame5, textvariable=smart_id_var)
smart_pw_entry = tk.Entry(frame6, textvariable=smart_pw_var, show="*")
coupang_id_entry = tk.Entry(frame7, textvariable=coupang_id_var)
coupang_pw_entry = tk.Entry(frame8, textvariable=coupang_pw_var, show="*")
net_profit_ratio_entry = tk.Entry(frame9, textvariable=net_profit_ratio_var)

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
label_coupang_id.pack(side=tk.LEFT)
coupang_id_entry.pack(side=tk.RIGHT)
label_coupang_pw.pack(side=tk.LEFT)
coupang_pw_entry.pack(side=tk.RIGHT)
label_net_profit_ratio.pack(side=tk.LEFT)
net_profit_ratio_entry.pack(side=tk.RIGHT)

# Packing Frames
frame1.pack()
frame2.pack()
frame3.pack()
frame4.pack()
frame5.pack()
frame6.pack()
frame7.pack()
frame8.pack()
frame9.pack()

# Create buttons for Sourcing and Uploading
sourcing_btn = tk.Button(root, text="Monthly Sourcing", command=sourcing_action)
uploading_btn = tk.Button(root, text="Monthly Uploading", command=uploading_action)
monthly_btn = tk.Button(root, text="Monthly Sourcing & Uploading", command=monthly_sourcing_uploading_action)
webdriver_btn = tk.Button(root, text="Initialize WebDriver", command=initialize_webdriver)
daily_btn = tk.Button(root, text="Daily Sourcing & Uploading", command=daily_sourcing_uploading_action)
pricing_btn = tk.Button(root, text="Pricing", command=discount_rate_pricing_action)
delivery_charge_changing_btn = tk.Button(root, text="DC Changing", command=delivery_charge_changing_action)
prd_stat_checking_btn = tk.Button(root, text="Product stat checking", command=prd_stat_checking_action)
gathering_order_btn = tk.Button(root, text="Product stat checking", command=gathering_order_action)

webdriver_btn.pack()
# sourcing_btn.pack()
# uploading_btn.pack()
monthly_btn.pack()
daily_btn.pack()
# pricing_btn.pack()
delivery_charge_changing_btn.pack()
prd_stat_checking_btn.pack()

# Creating and placing the result Text widget
result_text = tk.Text(root, height=10, width=50)
result_text.pack()

# Configure the tag for red text
result_text.tag_configure("red", foreground="red")

# Start the main event loop
set_default_text()
initialize_webdriver()
root.mainloop()