import tkinter as tk
from tkinter import ttk
from selenium import webdriver
import time
import pandas as pd
from vogueSnack import Sourcing, Uploading, Tool
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from tkinter import messagebox
from datetime import datetime, timedelta
import dateutil.relativedelta
import threading
import schedule
import queue
# After adding edge webdriver path to environment variable, you can execute below code.(ex. )

url = "https://sellha.kr/member/login"
url2 = "https://sellha.kr/discover"
url3 = "https://www.onch3.co.kr/login/login_web.php"
url4 = "https://www.onch3.co.kr/dbcenter_renewal/index.php"
smart_url = "https://accounts.commerce.naver.com/login?url=https%3A%2F%2Fsell.smartstore.naver.com%2F%23%2Flogin-callback"
coupang_url = 'https://xauth.coupang.com/auth/realms/seller/protocol/openid-connect/auth?response_type=code&client_id=wing&redirect_uri=https%3A%2F%2Fwing.coupang.com%2Fsso%2Flogin?returnUrl%3D%252F&state=456c3cf5-a6dd-4f52-abe4-cd3364bad4e4&login=true&scope=openid'
coupang_return_management_url = 'https://wing.coupang.com/tenants/sfl-portal/return-delivery/list'
naver_datalab_url = "https://datalab.naver.com/"
onchan_prd_stat_url = "https://www.onch3.co.kr/admin_mem_clo_list_2.php?ost=&sec=&ol=&npage="
onchan_order_stat_coupang_url = "https://www.onch3.co.kr/admin_api_order.html?api_name=coupang"
onchan_order_stat_smart_url = "https://www.onch3.co.kr/admin_api_order.html?api_name=smartstore"
onchan_prd_list_url = "https://www.onch3.co.kr/admin_mem_prd_list.html"
onchan_smart_prd_managenemt_url = "https://www.onch3.co.kr/admin_smart_manage.html#"
onchan_coupang_prd_managenemt_url = "https://www.onch3.co.kr/admin_coupang_manage.html"
onchan_my_prd_list_url = "https://www.onch3.co.kr/admin_mem_prd.html"
coupang_prd_list_url = "https://wing.coupang.com/vendor-inventory/list?searchIds=&startTime=2000-01-01&endTime=2099-12-31&productName=&brandName=&manufacturerName=&productType=&autoPricingStatus=ALL&dateType=productRegistrationDate&dateRangeShowStyle=true&dateRange=all&saleEndDatePeriodType=&includeUsedProduct=&deleteType=false&deliveryMethod=&shippingType=&shipping=&otherType=&productStatus=SAVED,WAIT_FOR_SALE,VALID,SOLD_OUT,INVALID,END_FOR_SALE,APPROVING,IN_REVIEW,DENIED,PARTIAL_APPROVED,APPROVED,ALL&advanceConditionShow=false&displayCategoryCodes=&currentMenuCode=&rocketMerchantVersion=&registrationType=&upBundling=ALL&hasUpBundlingItem=&hasBadImage=false&page=1&countPerPage=50&sortField=vendorInventoryId&desc=true&fromListV2=true&locale=ko_KR&vendorItemViolationType=&coupangAttributeOptimized=FALSE&autoPricingActive="
smart_prd_list_url = "https://sell.smartstore.naver.com/#/products/origin-list"

loginbtn1 = '.sc-iAEyYk.loQZmZ'
onchan_login_btn = '.btn.btn-lg.btn-primary.btn-block'
smart_login_btn = 'ul.panel_wrap li.panel_item .panel_inner .btn_login_wrap .btn_login'
coupang_loginbtn = '.cp-loginpage__form__submit'

base_path = '/Users/papag/OneDrive/src/Projects/vogueSnack'
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
    net_profit_ratio_entry.insert(0, "15")
    min_rating_entry.insert(0, "4.5")
    prd_max_num_entry.insert(0, "15")
    min_searched_num_entry.insert(0, "10000")
    sourcing_size_entry.insert(0, "150")

def initialize_webdriver():
    global driver, EdgeSourcing, EdgeUploading, EdgeTool

    # Set Edge options to disable pop-ups and use Chromium engine
    options = EdgeOptions()
    options.use_chromium = True  # Ensure we're using the Chromium version of Edge
    options.add_argument('--log-level=3')  # Set log level to suppress most logs

    driver = webdriver.Edge(options=options)
    driver.maximize_window()
    EdgeTool = Tool(driver, result_text)
    EdgeSourcing = Sourcing(driver, tool=EdgeTool)
    EdgeUploading = Uploading(driver, tool=EdgeTool)

    print("[+] WebDriver Initialized")
    return open_tabs()

def sourcing_action():
    global driver, EdgeSourcing, EdgeTool, isloggedin_sellha
    min_searched_num = int(min_searched_num_var.get())
    sourcing_size = int(sourcing_size_var.get())
    current_date = datetime.now()
    before_date = datetime.now() - dateutil.relativedelta.relativedelta(years=1) + dateutil.relativedelta.relativedelta(months=1)
    current_formatted_date = f"{current_date.year}-{current_date.month}"
    before_formatted_date = f"{before_date.year}-{before_date.month}"
    isDownloaded_sellha_df_current = EdgeSourcing.downloadChecker('/Users/papag/Downloads', f"셀하 아이템 발굴 EXCEL_전체_{current_formatted_date}", first_phase=True)
    # isDownloaded_sellha_df_before = EdgeSourcing.downloadChecker('/Users/papag/Downloads', f"셀하 아이템 발굴 EXCEL_전체_{before_formatted_date}", first_phase=False)
    isDownloaded_sourced = EdgeSourcing.downloadChecker('/Users/papag/OneDrive/src/Projects/vogueSnack', "sourced.csv", first_phase=True)
    print("[+] Sourcing phase start.")
    while True:
            try:
                driver.switch_to.window(window_sellha)
                if not isDownloaded_sellha_df_current:
                    sellha_id = id_var.get()
                    sellha_pw = password_var.get()
                    # isloggedin_sellha = EdgeSourcing.login('sellha',url,sellha_id,sellha_pw,'email', 'password',loginbtn1, False)
                    if not isloggedin_sellha:
                        EdgeSourcing.login('sellha',url,sellha_id,sellha_pw,'email', 'password',loginbtn1, False)
                        EdgeTool.popupHandler(5, 'sellha')
                    EdgeTool.popupHandler(5, 'sellha')
                    EdgeSourcing.pageNavigator(url2)
                    time.sleep(0.5)
                    EdgeSourcing.categoryButtonClicker(1)#All
                    time.sleep(0.5)
                    EdgeSourcing.csvButtonClicker(True)
                    time.sleep(0.5)
                    sellha_df_current = EdgeSourcing.downloadChecker('/Users/papag/Downloads', f"셀하 아이템 발굴 EXCEL_전체_{current_formatted_date}", first_phase=False)
                    sellha_df_before = EdgeSourcing.downloadChecker('/Users/papag/Downloads', f"셀하 아이템 발굴 EXCEL_전체_{before_formatted_date}", first_phase=False)
                    sellha_df_current_preProcessed = EdgeSourcing.preProcessor(sellha_df_current, min_searched_num, sourcing_size)
                    sellha_df_before_preProcessed = EdgeSourcing.preProcessor(sellha_df_before, min_searched_num, sourcing_size)
                    merged_df = pd.concat([sellha_df_current_preProcessed, sellha_df_before_preProcessed], axis=0)
                    merged_df.to_csv('sourced.csv', encoding='utf-8-sig', index = False)
                    EdgeSourcing.targetListMaker(pd.read_csv('sourced.csv', encoding='utf-8-sig'), False)
                    break
                if isDownloaded_sellha_df_current:
                    if isDownloaded_sourced:
                        EdgeSourcing.targetListMaker(pd.read_csv('sourced.csv', encoding='utf-8-sig'), isDaily=False)
                        break
                    if not isDownloaded_sourced:
                        sellha_df_current = EdgeSourcing.downloadChecker('/Users/papag/Downloads', f"셀하 아이템 발굴 EXCEL_전체_{current_formatted_date}", first_phase=False)
                        sellha_df_before = EdgeSourcing.downloadChecker('/Users/papag/Downloads', f"셀하 아이템 발굴 EXCEL_전체_{before_formatted_date}", first_phase=False)
                        sellha_df_current_preProcessed = EdgeSourcing.preProcessor(sellha_df_current, min_searched_num, sourcing_size)
                        sellha_df_before_preProcessed = EdgeSourcing.preProcessor(sellha_df_before, min_searched_num, sourcing_size)
                        merged_df = pd.concat([sellha_df_current_preProcessed, sellha_df_before_preProcessed], axis=0)
                        merged_df.to_csv('sourced.csv', encoding='utf-8-sig', index = False)
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
    global driver, EdgeSourcing, EdgeUploading, EdgeTool, isLoggedin_onchan
    min_rating = float(min_rating_var.get())
    prd_max_num = int(prd_max_num_var.get())
    net_profit_ratio = int(net_profit_ratio_var.get())
    onchan_id = id2_var.get()
    onchan_pw = password2_var.get()

    # login checking
    isLoggedin_onchan, isLoggedin_coupang = EdgeTool.login_checker(window_onchan, url3, window_coupang, coupang_url)

    driver.switch_to.window(window_onchan)
    while True:
            try:
                # Move to the data center hompage and compare keywords if there is in the center or not.
                if not isLoggedin_onchan:
                    EdgeSourcing.login('onchan',url3,onchan_id,onchan_pw,'username','password',onchan_login_btn, False)
                EdgeTool.popupHandler(3, 'onchan')
                preprocesedSourced_df = pd.read_csv('preprocesedSourced.csv', encoding='utf-8-sig')
                EdgeUploading.keywordCompare(preprocesedSourced_df, net_profit_ratio, min_rating, prd_max_num, isDaily=False, discount_rate_calculation=False, isDeliveryCharge_coupang=delivery_charge_var_coupang.get() == "True", isDeliveryCharge_smart=delivery_charge_var_smart.get() == "True", is_margin_descend=margin_descend_var.get() == "True")
                break
            except ElementClickInterceptedException:
                    message = "[!] Element intercepted while uploading.\n"
                    EdgeTool.append_to_text_widget(message, "red")
                    EdgeTool.scroll_downer(250)
                    message = "[*] Element intercepted fixed while uploading.\n"
                    EdgeTool.append_to_text_widget(message, "blue")
    print("[+] Uploading phase end.")

def monthly_sourcing_uploading_action():
    print("[+] Monthly phase start.")
    sourcing_action()
    uploading_action()
    # login checking
    isLoggedin_onchan, isLoggedin_coupang = EdgeTool.login_checker(window_onchan, url3, window_coupang, coupang_url)
    if not isLoggedin_coupang:
        coupang_id = coupang_id_var.get()
        coupang_pw = coupang_pw_var.get()
        driver.switch_to.window(window_coupang)
        EdgeSourcing.login('coupang',coupang_url, coupang_id, coupang_pw, 'username', 'password', coupang_loginbtn, authPhase=False)
    driver.switch_to.window(window_coupang)
    EdgeTool.delivery_charge_changer('coupang', coupang_prd_list_url, isDeliveryCharge=delivery_charge_var_coupang.get() == "True")
    print("[+] Monthly phase end.")

def daily_sourcing_uploading_action():
    print("[+] Daily sourcing & uploading start.")
    net_profit_ratio = int(net_profit_ratio_var.get())
    min_rating = float(min_rating_var.get())
    prd_max_num = int(prd_max_num_var.get())
    # login checking
    isLoggedin_onchan, isLoggedin_coupang = EdgeTool.login_checker(window_onchan, url3, window_coupang, coupang_url)
    if not isLoggedin_onchan:
        onchan_id = id2_var.get()
        onchan_pw = password2_var.get()
        driver.switch_to.window(window_onchan)
        EdgeSourcing.login('onchan',url3,onchan_id,onchan_pw,'username','password',onchan_login_btn, False)
    if not isLoggedin_coupang:
        coupang_id = coupang_id_var.get()
        coupang_pw = coupang_pw_var.get()
        driver.switch_to.window(window_coupang)
        EdgeSourcing.login('coupang',coupang_url, coupang_id, coupang_pw, 'username', 'password', coupang_loginbtn, authPhase=False)
    while True:
            try:
                driver.switch_to.window(window_empty)
                naver_sourced_df = EdgeSourcing.daily_sourcing()
                naver_sourced_isEdited_df = EdgeSourcing.targetListMaker(naver_sourced_df, isDaily=True)
                driver.switch_to.window(window_onchan)
                EdgeUploading.keywordCompare(naver_sourced_isEdited_df, net_profit_ratio, min_rating, prd_max_num, isDaily=True, discount_rate_calculation=False, isDeliveryCharge_coupang=delivery_charge_var_coupang.get() == "True", isDeliveryCharge_smart=delivery_charge_var_smart.get() == "True", is_margin_descend=margin_descend_var.get() == "True")
                driver.switch_to.window(window_coupang)
                EdgeTool.delivery_charge_changer('coupang', coupang_prd_list_url, isDeliveryCharge=delivery_charge_var_coupang.get() == "True")
                break
            except ElementClickInterceptedException:
                    message = "[!] Element intercepted while daily.\n"
                    EdgeTool.append_to_text_widget(message, "red")
                    EdgeTool.scroll_downer(250)
                    message = "[*] Element intercepted fixed while daily.\n"
                    EdgeTool.append_to_text_widget(message, "blue")
    print("[+] Daily sourcing & uploading successfully end.")
    EdgeTool.dummy_deleter(base_path, 'preprocesednaverSourcedUpdated')
    EdgeTool.dummy_deleter(base_path, 'naverSourced')
    EdgeTool.dummy_deleter(base_path, 'preprocessedNaverSourced')

def discount_rate_pricing_action():
    global driver, EdgeSourcing, EdgeUploading, EdgeTool
    isLoggedin = False
    smart_id = smart_id_var.get()
    smart_pw = smart_pw_var.get()
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
    global driver, EdgeSourcing, EdgeUploading, EdgeTool, isLoggedin_onchan, isLoggedin_coupang, isLoggedin_smart
    # isLoggedin_onchan = False
    # isLoggedin_coupang = False
    # isLoggedin_smart = False
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

    # login checking
    isLoggedin_onchan, isLoggedin_coupang = EdgeTool.login_checker(window_onchan, url3, window_coupang, coupang_url)
    if not isLoggedin_onchan:
        driver.switch_to.window(window_onchan)
        EdgeSourcing.login('onchan',url3,onchan_id,onchan_pw,'username','password',onchan_login_btn, False)
    if not isLoggedin_coupang:
        driver.switch_to.window(window_coupang)
        EdgeSourcing.login('coupang',coupang_url, coupang_id, coupang_pw, 'username', 'password', coupang_loginbtn, authPhase=False)
    
    while True:
        try:
            # Start the checking
            if not checking_phase_done:
                driver.switch_to.window(window_onchan)
                EdgeSourcing.pageNavigator(onchan_prd_stat_url)
                # Deleting or Suspending procedure.
                out_of_stock_prd_string, out_of_stock_prd_temp_string = EdgeTool.out_of_stock_checker()
                out_of_stock_prd_list = out_of_stock_prd_string.split(',')
                out_of_stock_prd_temp_list = out_of_stock_prd_temp_string.split(',')
                out_of_stock_prd_list.extend(out_of_stock_prd_temp_list)
                unique_prd_name_list = [i for i in out_of_stock_prd_list if i != 'Empty']
                message = f" [!] Stat Checking: {unique_prd_name_list}\n"
                EdgeTool.append_to_text_widget(message, "red")
                checking_phase_done = True
            if out_of_stock_prd_string == 'Empty' and out_of_stock_prd_temp_string == 'Empty':
                 coupang_phase_done = True
                 smart_phase_done = True
                 all_phase_done = True
            # Coupang
            if not coupang_phase_done:
                driver.switch_to.window(window_coupang)
                EdgeSourcing.pageNavigator(coupang_prd_list_url)
                EdgeTool.out_of_stock_product_deleter('coupang', out_of_stock_prd_string, out_of_stock_prd_temp_string)
                coupang_phase_done = True
            # Smart
            if not smart_phase_done:
                driver.switch_to.window(window_smart)
                EdgeSourcing.pageNavigator(smart_prd_list_url)
                EdgeTool.popupHandler(5, 'smart')
                EdgeTool.out_of_stock_product_deleter('smart', out_of_stock_prd_string, out_of_stock_prd_temp_string)
                smart_phase_done = True
            if checking_phase_done and coupang_phase_done and smart_phase_done:
                if not all_phase_done:
                    driver.switch_to.window(window_onchan)
                    EdgeSourcing.pageNavigator(onchan_prd_stat_url)
                    # EdgeTool.popupHandler(3, 'onchan')
                    EdgeTool.out_of_stock_finisher()
                    # Move to the product management page and delete the product.
                    '''
                    The process of deletion applies only to out-of-stock items. 
                    For temporarily out-of-stock or option-out-of-stock products, 
                    they are already marked as unavailable for sale(sale suspention), 
                    so the deletion process occurs within the filtering function.
                    '''
                    EdgeSourcing.pageNavigator(onchan_smart_prd_managenemt_url)
                    EdgeTool.onchan_prd_management_deleter('smart', unique_prd_name_list)
                    EdgeSourcing.pageNavigator(onchan_coupang_prd_managenemt_url)
                    EdgeTool.onchan_prd_management_deleter('coupang', unique_prd_name_list)
                    all_phase_done = True
            break
        except ElementClickInterceptedException:
                message = "[!] Element intercepted. \n"
                EdgeTool.append_to_text_widget(message, "red")
                print("[!] Element intercepted. Scroll down the page.")
                EdgeTool.scroll_downer(250)
    print("[+] Out of stock handling finish.")
    EdgeTool.dummy_deleter(download_path, 'excel_downdload')

def gathering_order_action():
    print("[+] Order gathering process start.")
    global driver, EdgeSourcing, EdgeUploading, EdgeTool, isLoggedin_onchan
    # isLoggedin_onchan = False
    onchan_id = id2_var.get()
    onchan_pw = password2_var.get()
    # login checking
    isLoggedin_onchan, isLoggedin_coupang = EdgeTool.login_checker(window_onchan, url3, window_coupang, coupang_url)
    if not isLoggedin_onchan:
        driver.switch_to.window(window_onchan)
        EdgeSourcing.login('onchan',url3,onchan_id,onchan_pw,'username','password',onchan_login_btn, False)

    driver.switch_to.window(window_onchan)
    while True:
        try:
            EdgeSourcing.pageNavigator(onchan_order_stat_coupang_url)
            EdgeTool.order_gathering_handler('coupang')
            EdgeSourcing.pageNavigator(onchan_order_stat_smart_url)
            EdgeTool.order_gathering_handler('smart')
            print("[+] Order gathering process end.")
            break
        except ElementClickInterceptedException:
                message = "[!] Element intercepted. \n"
                EdgeTool.append_to_text_widget(message, "red")
                print("[!] Element intercepted. Scroll down the page.")
                EdgeTool.scroll_downer(250)

def prd_filtering_action():
    onchan_filtering_done = False
    coupang_filtering_done = False
    coupang_again_filtering_done = False
    smart_filtering_done = False
    coupang_id = coupang_id_var.get()
    coupang_pw = coupang_pw_var.get()
    onchan_id = id2_var.get()
    onchan_pw = password2_var.get()

    # login checking
    isLoggedin_onchan, isLoggedin_coupang = EdgeTool.login_checker(window_onchan, url3, window_coupang, coupang_url)
    if not isLoggedin_onchan:
        driver.switch_to.window(window_onchan)
        EdgeSourcing.login('onchan',url3,onchan_id,onchan_pw,'username','password',onchan_login_btn, False)
    if not isLoggedin_coupang:
        driver.switch_to.window(window_coupang)
        EdgeSourcing.login('coupang',coupang_url, coupang_id, coupang_pw, 'username', 'password', coupang_loginbtn, authPhase=False)

    while True:
        try:
            if not coupang_filtering_done:
                driver.switch_to.window(window_coupang)
                EdgeSourcing.pageNavigator(coupang_prd_list_url)
                prd_name_list = EdgeTool.filtered_prd_deleter('coupang', [])
                coupang_filtering_done = True
                df = pd.DataFrame(prd_name_list, columns=['prd_code'])
                df.to_csv('suspended_prd_coupang.csv', index=False)
            # Smart
            if not smart_filtering_done:
                driver.switch_to.window(window_smart)
                time.sleep(0.5)
                EdgeSourcing.pageNavigator(smart_prd_list_url)
                
                EdgeTool.popupHandler(5, 'smart')
                prd_name_list_updated = EdgeTool.filtered_prd_deleter('smart', prd_name_list)
                unique_prd_name_list = list(set(prd_name_list_updated))
                smart_filtering_done = True
                df = pd.DataFrame(unique_prd_name_list, columns=['prd_code'])
                df.to_csv('suspended_prd_smartcoupang.csv', index=False)
                if len(prd_name_list_updated) == 0:
                    coupang_again_filtering_done = True
                    onchan_filtering_done = True
                if len(prd_name_list_updated) == len(prd_name_list):
                    coupang_again_filtering_done = True
            # Coupang again(with smart suspended product list)
            if not coupang_again_filtering_done:
                driver.switch_to.window(window_coupang)
                EdgeSourcing.pageNavigator(coupang_prd_list_url)
                EdgeTool.filtered_prd_deleter('coupang', unique_prd_name_list)
                coupang_again_filtering_done = True
            # Onchan
            if not onchan_filtering_done:
                driver.switch_to.window(window_onchan)
                EdgeSourcing.pageNavigator(onchan_prd_list_url)
                EdgeTool.filtered_prd_deleter('onchan', unique_prd_name_list)
                # Move to the product management page and delete the product.
                time.sleep(0.5)
                EdgeSourcing.pageNavigator(onchan_smart_prd_managenemt_url)
                EdgeTool.onchan_prd_management_deleter('smart', unique_prd_name_list)
                time.sleep(0.5)
                EdgeSourcing.pageNavigator(onchan_coupang_prd_managenemt_url)
                EdgeTool.onchan_prd_management_deleter('coupang', unique_prd_name_list)
                onchan_filtering_done = True
            print("[+] Filtering end.")
            EdgeTool.dummy_deleter(base_path, 'suspended_prd')
            break
        except ElementClickInterceptedException:
                message = "[!] Element intercepted. \n"
                EdgeTool.append_to_text_widget(message, "red")
                print("[!] Element intercepted. Scroll down the page.")
                EdgeTool.scroll_downer(250)

def open_tabs():
    print("[+] Open tab start.")
    global driver, EdgeSourcing, EdgeUploading, EdgeTool, isLoggedin_smart, isLoggedin_coupang, isLoggedin_onchan, isloggedin_sellha, windows, window_smart, window_coupang, window_onchan, window_sellha, window_empty
    # Open smart, coupang, onchan, sellha tab with logged in.
    isLoggedin_smart = False
    isLoggedin_coupang = False
    isLoggedin_onchan = False
    isloggedin_sellha = False
    smart_id = smart_id_var.get()
    smart_pw = smart_pw_var.get()
    coupang_id = coupang_id_var.get()
    coupang_pw = coupang_pw_var.get()
    onchan_id = id2_var.get()
    onchan_pw = password2_var.get()
    sellha_id = id_var.get()
    sellha_pw = password_var.get()
        # smart
    isLoggedin_smart = EdgeSourcing.login('smart',smart_url,smart_id,smart_pw,'id','pw',smart_login_btn, authPhase=True)
        # Open tabs
    for _ in range(4):
        driver.execute_script("window.open('about:blank', '_blank');")
        time.sleep(1)
    windows = driver.window_handles
    window_smart = windows[0]
    window_coupang = windows[1]
    window_onchan = windows[2]
    window_sellha = windows[3]
    window_empty = windows[4]
        # coupang
    driver.switch_to.window(window_coupang)
    isLoggedin_coupang = EdgeSourcing.login('coupang',coupang_url, coupang_id, coupang_pw, 'username', 'password', coupang_loginbtn, authPhase=False)
        # onchan
    driver.switch_to.window(window_onchan)
    isLoggedin_onchan = EdgeSourcing.login('onchan',url3,onchan_id,onchan_pw,'username','password',onchan_login_btn, False)
        # sellha
    driver.switch_to.window(window_sellha)
    isloggedin_sellha = EdgeSourcing.login('sellha',url,sellha_id,sellha_pw,'email', 'password',loginbtn1, False)
    print("[+] Open tab successful.")

def prd_exsition_comparing_action():
    onchan_checking_done = False
    coupang_checking_done = False
    smart_checking_done = False
    while True:
        try:
            if not coupang_checking_done:
                driver.switch_to.window(window_coupang)
                EdgeSourcing.pageNavigator(coupang_prd_list_url)
                EdgeTool.prd_exsition_comparer('coupang')
                coupang_checking_done = True
            # Smart
            if not smart_checking_done:
                driver.switch_to.window(window_smart)
                EdgeSourcing.pageNavigator(smart_prd_list_url)
                EdgeTool.popupHandler(5, 'smart')
                EdgeTool.prd_exsition_comparer('smart')
                smart_checking_done = True
            # Onchan
            if not onchan_checking_done:
                driver.switch_to.window(window_onchan)
                EdgeSourcing.pageNavigator(onchan_prd_list_url)
                EdgeTool.prd_exsition_comparer('onchan')
                onchan_checking_done = True
            print("[+] Checking end.")
            break
        except ElementClickInterceptedException:
                message = "[!] Element intercepted. \n"
                EdgeTool.append_to_text_widget(message, "red")
                print("[!] Element intercepted. Scroll down the page.")
                EdgeTool.scroll_downer(250)

def return_manager_action():
    coupang_id = coupang_id_var.get()
    coupang_pw = coupang_pw_var.get()
    onchan_id = id2_var.get()
    onchan_pw = password2_var.get()

    # login checking
    isLoggedin_onchan, isLoggedin_coupang = EdgeTool.login_checker(window_onchan, url3, window_coupang, coupang_url)
    if not isLoggedin_onchan:
        driver.switch_to.window(window_onchan)
        EdgeSourcing.login('onchan',url3,onchan_id,onchan_pw,'username','password',onchan_login_btn, False)
    if not isLoggedin_coupang:
        driver.switch_to.window(window_coupang)
        EdgeSourcing.login('coupang',coupang_url, coupang_id, coupang_pw, 'username', 'password', coupang_loginbtn, authPhase=False)

    while True:
        try:
            driver.switch_to.window(window_coupang)
            EdgeSourcing.pageNavigator(coupang_return_management_url)
            cust_name_list,delivery_code_list = EdgeTool.return_manager('coupang')
            driver.switch_to.window(window_onchan)
            EdgeSourcing.pageNavigator(onchan_my_prd_list_url)
            EdgeTool.return_manager_onchan(cust_name_list, delivery_code_list)
            print("[+] Return managing end.")
            break
        except ElementClickInterceptedException:
                message = "[!] Element intercepted. \n"
                EdgeTool.append_to_text_widget(message, "red")
                print("[!] Element intercepted. Scroll down the page.")
                EdgeTool.scroll_downer(250)

# Initialize the main window
root = tk.Tk()
root.title("Automation Tool")
root.geometry("500x800")

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
min_rating_var = tk.StringVar()
prd_max_num_var = tk.StringVar()
min_searched_num_var = tk.StringVar()
sourcing_size_var = tk.StringVar()
delivery_charge_var_coupang = tk.StringVar(value="False")
delivery_charge_var_smart = tk.StringVar(value="True")
margin_descend_var = tk.StringVar(value="False")

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
frame10 = tk.Frame(root)
frame11 = tk.Frame(root)
frame12 = tk.Frame(root)
frame13 = tk.Frame(root)
frame14 = tk.Frame(root)
frame15 = tk.Frame(root)
frame16 = tk.Frame(root)

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
label_min_rating = tk.Label(frame10, text="Minimum rating(1~5)")
label_prd_max_num = tk.Label(frame11, text="Maximum number of products uploading per keyword")
label_delivery_charge_dropdown_coupang = tk.Label(frame12, text="Coupang Delivery charge")
label_delivery_charge_dropdown_smart = tk.Label(frame13, text="Smart Delivery charge")
label_margin_descend_dropdown = tk.Label(frame14, text="Sort by highest margin")
label_min_searched_num = tk.Label(frame15, text="Minimum searched number")
label_sourcing_size = tk.Label(frame16, text="Sourcing size")

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
min_rating_entry = tk.Entry(frame10, textvariable=min_rating_var)
prd_max_num_entry = tk.Entry(frame11, textvariable=prd_max_num_var)
min_searched_num_entry = tk.Entry(frame15, textvariable=min_searched_num_var)
sourcing_size_entry = tk.Entry(frame16, textvariable=sourcing_size_var)

# Create Drop downs
delivery_charge_dropdown_coupang = ttk.Combobox(frame12, textvariable=delivery_charge_var_coupang, values=["True", "False"])
delivery_charge_dropdown_smart = ttk.Combobox(frame13, textvariable=delivery_charge_var_smart, values=["True", "False"])
margin_descend_dropdown = ttk.Combobox(frame14, textvariable=margin_descend_var, values=["True", "False"])

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
label_min_rating.pack(side=tk.LEFT)
min_rating_entry.pack(side=tk.RIGHT)
label_prd_max_num.pack(side=tk.LEFT)
prd_max_num_entry.pack(side=tk.RIGHT)
label_min_searched_num.pack(side=tk.LEFT)
min_searched_num_entry.pack(side=tk.RIGHT)
label_sourcing_size.pack(side=tk.LEFT)
sourcing_size_entry.pack(side=tk.RIGHT)
label_delivery_charge_dropdown_coupang.pack(side=tk.LEFT)
delivery_charge_dropdown_coupang.pack(side=tk.RIGHT)
label_delivery_charge_dropdown_smart.pack(side=tk.LEFT)
delivery_charge_dropdown_smart.pack(side=tk.RIGHT)
label_margin_descend_dropdown.pack(side=tk.LEFT)
margin_descend_dropdown.pack(side=tk.RIGHT)

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
frame10.pack()
frame11.pack()
frame12.pack()
frame13.pack()
frame14.pack()
frame15.pack()
frame16.pack()

# Create buttons for Sourcing and Uploading
sourcing_btn = tk.Button(root, text="Monthly Sourcing", command=sourcing_action)
uploading_btn = tk.Button(root, text="Monthly Uploading", command=uploading_action)
monthly_btn = tk.Button(root, text="Monthly Sourcing & Uploading", command=monthly_sourcing_uploading_action)
webdriver_btn = tk.Button(root, text="Initialize WebDriver", command=initialize_webdriver)
daily_btn = tk.Button(root, text="Daily Sourcing & Uploading", command=daily_sourcing_uploading_action)
pricing_btn = tk.Button(root, text="Pricing", command=discount_rate_pricing_action)
prd_stat_checking_btn = tk.Button(root, text="Product stat checking", command=prd_stat_checking_action)
prd_filtering_btn = tk.Button(root, text="Product filtering", command=prd_filtering_action)
gathering_order_btn = tk.Button(root, text="Order gathering", command=gathering_order_action)
prd_exsition_comparing_btn = tk.Button(root, text="Product existion checking", command=prd_exsition_comparing_action)
return_manager_btn = tk.Button(root, text="Return management", command=return_manager_action)

webdriver_btn.pack()
# sourcing_btn.pack()
# uploading_btn.pack()
monthly_btn.pack()
daily_btn.pack()
# pricing_btn.pack()
prd_stat_checking_btn.pack()
prd_filtering_btn.pack()
gathering_order_btn.pack()
return_manager_btn.pack()

# Creating and placing the result Text widget
result_text = tk.Text(root, height=25, width=60)
result_text.pack()

# Configure the tag for red text
result_text.tag_configure("red", foreground="red")

# Button activate scheduling: activate one after the other when the schediule is overlapped.
task_queue = queue.Queue()  # Global queue for tasks

def run_scheduled_jobs():
    while True:
        schedule.run_pending()
        time.sleep(1)

def task_worker():
    """Worker thread that processes tasks in the queue."""
    while True:
        task = task_queue.get()  # Wait for a task from the queue
        try:
            task()  # Execute the task
        except Exception as e:
            message = f" [!] Task worker: {e}\n"
            EdgeTool.append_to_text_widget(message, "red")
        finally:
            task_queue.task_done()  # Mark the task as done, regardless of success or failure

def enqueue_task(task):
    """Function to add a task to the queue."""
    task_queue.put(task)

def schedule_actions():
    # Schedule Monthly Button to enqueue task
    def check_and_enqueue_monthly_task():
        current_date = datetime.now()
        # Check if today is the first day of the month
        if current_date.day == 1:
            enqueue_task(lambda: monthly_btn.invoke())
    schedule.every().day.at("17:00").do(check_and_enqueue_monthly_task)

    # Schedule Daily Button to enqueue task
    schedule.every().day.at("10:00").do(lambda: enqueue_task(lambda: daily_btn.invoke()))

    # Schedule Product Status Checking Button every 30 minutes to enqueue task
    def enqueue_prd_stat_checking_if_within_time():
        current_time = datetime.now()
        current_hour = current_time.hour
        if 9 <= current_hour <= 20:# 9am~8pm
            enqueue_task(lambda: prd_stat_checking_btn.invoke())
    schedule.every(30).minutes.do(enqueue_prd_stat_checking_if_within_time)

    def enqueue_prd_filtering_if_within_time():
        current_time = datetime.now()
        current_hour = current_time.hour
        if 11 <= current_hour <= 20: #11am~8pm
            enqueue_task(lambda: prd_filtering_btn.invoke())
    # Schedule Product Filtering Button every 6 hours to enqueue task
    schedule.every(3).hours.do(enqueue_prd_filtering_if_within_time)

    # Schedule Gathering Order Button every 3 hours to enqueue task
    schedule.every(3).hours.do(lambda: enqueue_task(lambda: gathering_order_btn.invoke()))

if __name__ == "__main__":
    set_default_text()
    initialize_webdriver()
    schedule_actions()
    
    # Start the scheduler thread
    scheduler_thread = threading.Thread(target=run_scheduled_jobs, daemon=True)
    scheduler_thread.start()
    
    # Start the task worker thread
    worker_thread = threading.Thread(target=task_worker, daemon=True)
    worker_thread.start()

    root.mainloop()

# Start the main event loop
# set_default_text()
# initialize_webdriver()
# root.mainloop()