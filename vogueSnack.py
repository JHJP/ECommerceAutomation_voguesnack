from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
import os.path
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, StaleElementReferenceException, ElementClickInterceptedException, TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
import tkinter as tk
import re
import tkinter.messagebox as messagebox   # Import the function from shared.py

class Sourcing:
    def __init__(self, driver, tool=None):
        self.driver = driver
        self.tool = tool

    def login(self, store_name, url, id, password, usernameBox, passwordBox, loginbtn, authPhase):
        isLoggedin = False
        if not authPhase:
            self.driver.get(url)
        else:
            if store_name == 'smart':
                print("[+] Move to the opend tab.")
                self.driver.get(url)
                time.sleep(2)
                self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div/div[4]/div[1]/ul/li[2]/button').click()
                time.sleep(2)
                # move to the opend window
                windows = self.driver.window_handles
                smart_login_windows = windows[1]
                self.driver.switch_to.window(smart_login_windows)
                print("[+] Move to the opened tab successful.")
            if store_name == 'coupang':
                self.driver.get(url)
        self.driver.find_element(By.NAME, usernameBox).send_keys(id)
        self.driver.find_element(By.NAME, passwordBox).send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, loginbtn).click() # use CSS_SELECTOR to change class name format. Because there are spaces on class name, which means not a single class.
        while True:
            try:# wait the ready state to be complete
                WebDriverWait(driver=self.driver, timeout=10).until(
                    lambda x: x.execute_script("return document.readyState === 'complete'")
                )
                break
            except Exception:
                self.driver.refresh()
        isLoggedin = True
        if store_name == 'smart':
            self.tool.popupHandler(5,'smart')
        if store_name == 'onchan':
            self.tool.popupHandler(5,'onchan')
        if store_name == 'sellha':
            self.tool.popupHandler(5,'sellha')
        if store_name == 'coupang':
            self.tool.popupHandler(5,'coupang')
        if authPhase:
            print(" [*] Login process start.")
            input(f" [*] Process? id: {id}, password: {password}")
            print(" [*] Login successful")
            isLoggedin = True
            time.sleep(5)
            if store_name =='smart':
                self.driver.switch_to.window(windows[0])

        return isLoggedin
            
    def pageNavigator(self, url):
        self.driver.get(url)
        # wait the ready state to be complete
        WebDriverWait(driver=self.driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )

        error_message = "Incorrect url or other error."
        # get the errors (if there are)
        errors = self.driver.find_elements(By.CLASS_NAME,"flash-error")
        # if we find that error message within errors, then login is failed
        if any(error_message in e.text for e in errors):
            message = "[!] Navigation failed.\n"
            self.tool.append_to_text_widget(message, "red")
        else:
            print("[+] Navigation successful")

    def categoryButtonClicker(self,target_num):
        WebDriverWait(driver=self.driver, timeout=30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/section/main/div[2]/div/div/div[3]/div[1]/div/button')))
        button1 = self.driver.find_element(By.XPATH, '//*[@id="root"]/section/main/div[2]/div/div/div[3]/div[1]/div/button')
        button1.click()
        time.sleep(1)
        WebDriverWait(driver=self.driver, timeout=30).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="root"]/section/main/div[2]/div[1]/div/div[3]/div[1]/div/ul/li[{target_num}]/button')))
        button2 = self.driver.find_element(By.XPATH, f'//*[@id="root"]/section/main/div[2]/div[1]/div/div[3]/div[1]/div/ul/li[{target_num}]/button')
        button2.click()

        error_message = "error occur."
        # get the errors (if there are)
        errors = self.driver.find_elements(By.CLASS_NAME,"flash-error")
        # if we find that error message within errors, then login is failed
        if any(error_message in e.text for e in errors):
            message = "[!] Category button clicked failed.\n"
            self.tool.append_to_text_widget(message, "red")
        else:
            print("[+] Category button clicked successfully")

    def csvButtonClicker(self, click1):
        if click1:
            WebDriverWait(driver=self.driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="result"]/section/div[2]/div[1]/div[1]/button')))
            button1 = self.driver.find_element(By.XPATH, '//*[@id="result"]/section/div[2]/div[1]/div[1]/button')
            button1.click()
            WebDriverWait(driver=self.driver, timeout=30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="result"]/section/div[2]/div[1]/div[1]/div/div/div[2]/button/div')))
            button2 = self.driver.find_element(By.XPATH, '//*[@id="result"]/section/div[2]/div[1]/div[1]/div/div/div[2]/button/div')
            button2.click()
        if click1==False:
            WebDriverWait(driver=self.driver, timeout=30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="result"]/section/div[2]/div[1]/div[1]/div/div/div[2]/button/div')))
            button2 = self.driver.find_element(By.XPATH, '//*[@id="result"]/section/div[2]/div[1]/div[1]/div/div/div[2]/button/div')
            button2.click()
        
        error_message = "error occur."
        # get the errors (if there are)
        errors = self.driver.find_elements(By.CLASS_NAME,"flash-error")
        # if we find that error message within errors, then login is failed
        if any(error_message in e.text for e in errors):
            message = "[!] Download buttion click failed.\n"
            self.tool.append_to_text_widget(message, "red")
        else:
            print("[+] Download button clicked successfully")

    def downloadChecker(self, download_path, file_prefix, first_phase):
        counter = 0
        while True:
            time.sleep(3)
            files = os.listdir(download_path)
            matching_files = [file for file in files if file.startswith(file_prefix)]
            if not matching_files and counter < 3:
                print(f" [*] {file_prefix} no exist. I'll check again.")
                counter += 1
                continue
            elif not matching_files and counter >= 3:
                if first_phase:
                    return False
                input(f" [*] {file_prefix} no exist.Press enter to recheck.")
                counter = 0
                continue
            else:
                print(f"[+] {file_prefix} downloaded successfully. Start reading.")
                if first_phase:
                    return True
                # Construct the full path to the first matching file
                file_to_check = os.path.join(download_path, matching_files[0])
                file_extension = os.path.splitext(file_to_check)[1]
                if os.path.isfile(file_to_check):
                    # Assuming it's an Excel file, you can read it into a Pandas DataFrame
                    try:
                        dictionary = pd.read_excel(file_to_check, sheet_name=None)
                        # Concatenate all DataFrames from each sheet into one DataFrame
                        df = pd.concat(dictionary, ignore_index=True)
                        print(f"[+] {file_prefix} read with excel successfully.")
                    except Exception as e:
                        if file_extension.lower() == '.csv':
                            try:
                                print(e)
                                df = pd.read_csv(file_to_check, encoding='utf-8')
                                print(f"[+] {file_prefix} read with csv successfully.")
                            except Exception as e:
                                print(e)
                        else:
                            try:
                                tables = pd.read_html(file_to_check)
                                df = tables[0]
                                print(f"[+] {file_prefix} read with html successfully.")
                            except Exception as e:
                                print(e)
                                input("Error occur while read the file.")
                    # You can now work with the 'df' DataFrame.
                    return df
                
    def targetListMaker(self, preprocessed_df, isDaily):
        if not isDaily:
            csv_name = 'preprocesedSourced.csv'
        elif isDaily:
            csv_name = 'preprocessedNaverSourced.csv'
        files = os.listdir('/Users/papag/OneDrive/src/Projects/vogueSnack')
        matching_files = [file for file in files if file == csv_name]
        if matching_files:
            preprocessed_df = pd.read_csv(csv_name)
        else:
            preprocessed_df.insert(preprocessed_df.columns.get_loc('키워드') + 1, '바꾼키워드', None)
            preprocessed_df.insert(preprocessed_df.columns.get_loc('바꾼키워드') + 1, 'isSearched', False)
            preprocessed_df.insert(preprocessed_df.columns.get_loc('isSearched') + 1, 'isEdited', False)
        if not isDaily: # Not make the list when do the daily sourcing and uploading.
            print(f"There are number of {len(preprocessed_df)} items.")
            # Stack to keep history of DataFrame states
            history = []

            i = 0
            while i < len(preprocessed_df):
                isEdited = preprocessed_df['isEdited'][i]

                if not isEdited:
                    decision = input(f"({i}/{len(preprocessed_df)}), {preprocessed_df.iloc[i]['키워드']}; Tell me the word you want to change (1=delete, 2=maintain, 3=undo): ")
                    if decision == '3' and history:
                        preprocessed_df = history.pop()  # Revert to the last state
                        if i > 0:
                            i -= 1
                        preprocessed_df.reset_index(drop=True, inplace=True)
                        while True:
                            try:
                                preprocessed_df.to_csv(csv_name, encoding='utf-8-sig', index = False)
                                break
                            except PermissionError:
                                print("Permission error occuer. Close the opened file named preprocesedSourced.csv.")
                        continue
                    else:
                        history.append(preprocessed_df.copy())  # Save the current state

                    if decision == '1': # drop the row
                        preprocessed_df.drop(preprocessed_df.index[i], inplace=True)
                        preprocessed_df.reset_index(drop=True, inplace=True)
                        i -= 1
                        while True:
                            try:
                                preprocessed_df.to_csv(csv_name, encoding='utf-8-sig', index = False)
                                break
                            except PermissionError:
                                print("Permission error occuer. Close the opened file named preprocesedSourced.csv.")
                    elif decision == '2': # Maintain the keyword
                        preprocessed_df.at[i, '바꾼키워드'] = preprocessed_df.at[i, '키워드']
                        preprocessed_df.at[i, 'isEdited'] = True
                        while True:
                            try:
                                preprocessed_df.to_csv(csv_name, encoding='utf-8-sig', index = False)
                                break
                            except PermissionError:
                                print("Permission error occuer. Close the opened file named preprocesedSourced.csv.")
                    else: # Change the keyword
                        preprocessed_df.at[i, '바꾼키워드'] = decision
                        preprocessed_df.at[i, 'isEdited'] = True
                        while True:
                            try:
                                preprocessed_df.to_csv(csv_name, encoding='utf-8-sig', index = False)
                                break
                            except PermissionError:
                                print("Permission error occuer. Close the opened file named preprocesedSourced.csv.")
                i += 1
        if not isDaily:
            preprocessed_df.drop_duplicates(subset='바꾼키워드', inplace=True)
            while True:
                try:
                    preprocessed_df.to_csv(csv_name, encoding='utf-8-sig', index = False)
                    break
                except PermissionError:
                    print("Permission error occuer. Close the opened file named preprocesedSourced.csv.")
        if isDaily:
            preprocessed_df.to_csv(csv_name, encoding='utf-8-sig', index = False)
            return preprocessed_df
    
    # Make keyword list from the sorted dataframe.
    def preProcessor(self, df, search_volume):
        counter = 0
        sourced_list = []
        sourced_df = pd.DataFrame([], columns=df.columns)

        df.drop_duplicates(subset='키워드', inplace=True)
        df['진짜경쟁률'] = df['상품수'] / df['검색량']
        df.drop(df[df['카테고리전체'].str.startswith('도서')].index, inplace=True)
        df.drop(df[df['카테고리전체'].str.startswith('식품 > 주류')].index, inplace=True)
        df.drop(df[df['카테고리전체'].str.startswith('식품 > 건강식품')].index, inplace=True)
        df.drop(df[df['카테고리'].str.startswith('PC게임')].index, inplace=True)
        df.drop(df[df['카테고리'].str.startswith('구급')].index, inplace=True)
        df.drop(df[df['카테고리'].str.startswith('테마/놀이동산')].index, inplace=True)
        df.drop(df[df['카테고리'].str.startswith('전자담배')].index, inplace=True)
        df.drop(df[df['카테고리'].str.startswith('국내패키지')].index, inplace=True)
        df.drop(df[df['쇼핑성키워드'] == False].index, inplace=True)
        df.drop(df[df['브랜드점유율']>=0.5].index, inplace=True)
        while counter < 5:
            df.drop(df[df['검색량']<=search_volume].index, inplace=True)
            df.sort_values(by='진짜경쟁률', ascending=True, inplace=True)
            sourced_list.append(df.head(50))
            counter += 1
            search_volume += 10000
        sourced_df = pd.concat(sourced_list)
        sourced_df.drop_duplicates(subset='키워드', inplace=True)
        sourced_df.sort_values(by='진짜경쟁률', ascending=True, inplace=True)
        sourced_df.to_csv('sourced.csv', encoding='utf-8-sig', index = False)
        
        return sourced_df

    def daily_sourcing(self):
        files = os.listdir('/Users/papag/OneDrive/src/Projects/vogueSnack')
        matching_files = [file for file in files if file == 'naverSourced.csv']
        if not matching_files:
            # Append data from the naver data lab
            naver_datalab_url = 'https://datalab.naver.com/'
            self.pageNavigator(naver_datalab_url)
                # Get data
                # Select domain
            domain_dropdown = WebDriverWait(driver=self.driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/div[3]/div[1]/a')))
            naver_keyword_list = []
            print("[+] Daily sourcing start.")
            for i in range(3,10):
                domain_dropdown.click()
                time.sleep(3)
                domain = WebDriverWait(driver=self.driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="content"]/div[1]/div[3]/div[1]/ul/li[{i}]/a')))
                domain.click()
                # Get yesterday keyword data 1st ~ 10th
                for j in range(10):
                    while True:
                        time.sleep(1)
                        try:
                            keyword = WebDriverWait(driver=self.driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="content"]/div[1]/div[4]/div/div[1]/div/div/div[12]/div/div/ul/li[{j+1}]/a/span'))).text
                            naver_keyword_list.append(keyword)
                            break
                        except StaleElementReferenceException:
                            print(f"Stale element Exception at domain {i}, index {j}")
                percent = int(((i+1)/7)*100)
                print(f"\r [*] {percent}% complete..", end='')
                if percent == 100:
                    # Print a newline character at the end to move the cursor to the next line
                    print()
            naver_sourced_df = pd.DataFrame(naver_keyword_list, columns=['키워드'])
            naver_sourced_df.to_csv('naverSourced.csv', encoding='utf-8-sig', index = False)
        elif matching_files:
            naver_sourced_df = pd.read_csv('naverSourced.csv')
        return naver_sourced_df

class Uploading:
    def __init__(self, driver, tool=None):
        self.driver = driver
        # self.tool = tool or Tool(driver, uploading=self)
        self.tool = tool

    def sending_store(self, checkboxes_numb, originalTarget, btn_path, store_name, net_profit_ratio, max_delivery_charge_list, lowest_delivery_charge_list, discount_rate_calculation, isDaily, isDeliveryCharge):
        # print(f"[+] Sending to {store_name} store start." )
        while True:
            try:
                sending_store_btn = WebDriverWait(driver=self.driver, timeout=30).until(EC.presence_of_element_located(
                    (By.XPATH, btn_path)))
                ActionChains(self.driver).move_to_element(sending_store_btn).perform()
                WebDriverWait(driver=self.driver, timeout=30).until(EC.element_to_be_clickable(
                    (By.XPATH, btn_path)))
                sending_store_btn.click()
                break
            except ElementClickInterceptedException:
                message = "[!] Element intercepted while sending button clicking.\n"
                self.tool.append_to_text_widget(message, "red")
                message = "[*] Scroll down little bit and try again.\n"
                self.tool.append_to_text_widget(message, "blue")
                self.tool.scroll_downer(250)
        # Keyword appender
        time.sleep(3)
        parent_element = self.driver.find_element(By.CSS_SELECTOR, f'.{store_name}_modi_layer')
        # Find all input elements within this parent element
        input_elements = parent_element.find_elements(By.CSS_SELECTOR, f'.{store_name}_prd_nm')
        checkboxes_numb = len(input_elements)
        discount_rate_list = []
        for i in range(checkboxes_numb):
            while True:
                try:
                    if store_name == 'coupang':
                        # Check for the option edit button presence.
                        edit_button = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(
                            (By.XPATH, f'/html/body/div[3]/section/div/div[3]/ul/li[{i+1}]/ul/li[3]/button')))
                        retail_price = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[3]/section/div/div[3]/ul/li[{i + 1}]/ul/li[3]/span")))
                        wholesale_price = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[3]/section/div/div[3]/ul/li[{i+1}]/ul/li[4]")))
                        prd_code = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[3]/section/div/div[3]/ul/li[{i+1}]/ul/li[1]")))
                    elif store_name == 'smart':
                        # Check for the option edit button presence.
                        edit_button = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(
                            (By.XPATH, f'/html/body/div[3]/section/div/div[2]/ul/li[{i+1}]/ul/li[5]/button')))
                        retail_price = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[3]/section/div/div[2]/ul/li[{i + 1}]/ul/li[3]/span")))
                        wholesale_price = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[3]/section/div/div[2]/ul/li[{i+1}]/ul/li[4]")))
                        prd_code = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[3]/section/div/div[2]/ul/li[{i+1}]/ul/li[1]")))
                except TimeoutException:
                    i += 1
                    break    
                while True:
                    try:
                        retail_price = int(retail_price.text)
                        break
                    except Exception as e:
                        print(e)
                        # input(f"retail_price.text: {retail_price.text}. try again?")
                wholesale_price = int(wholesale_price.text.replace('원',''))
                prd_code = prd_code.text
                if store_name == 'coupang':
                    # Calculate the retail price
                    sc = 0.1199 # sales commission with VAT: sales commission is differed between category. But I set it to tme maximum sales commission(10.9%).
                    dc = 0.033 # delievery commission with VAT
                    ait = 6 # aggregate income tax(%)
                        # Iterate through the list to find the matching product code
                    for code, charge in lowest_delivery_charge_list:
                        if code == prd_code:
                            lowest_delivery_charge = charge
                            break  # Exit the loop once the match is found
                    #dp= delivery price that market pay, dpstar = consumer paid dp
                    dp = lowest_delivery_charge
                    if not isDeliveryCharge:
                        dpstar = 0 # Free shipping
                    elif isDeliveryCharge:
                        dpstar = dp
                    updated_retail_price = (1 / (1 - sc)) * (wholesale_price * (1 + ((net_profit_ratio / 100) / (1 - ait / 100))) - dpstar * (1 - dc) + dp)
                    updated_retail_price = round(updated_retail_price / 10) * 10 # round up from the first digit.    
                        # If is discount rate = True -> run the next code. else, just update the retail price
                    # if discount_rate_calculation == True:
                    #     if retail_price > updated_retail_price:
                    #         discount_rate = int((retail_price / updated_retail_price)*100 - 100)
                    #         discount_rate =(discount_rate+5)//10*10
                    #     else:
                    #         discount_rate = 0
                    edit_button.click()
                    time.sleep(0.5)
                    # Check if there are more than one option
                    retail_price_inputs = []
                    retail_price_inputs = WebDriverWait(self.driver, 2).until(EC.presence_of_all_elements_located(
                        (By.XPATH, f'/html/body/div[3]/section/div/div[3]/ul/li[{i + 1}]/ul/li[3]/div/ul/li/ul/li[2]/input[1]')))
                    isOpions = True
                    if len(retail_price_inputs) == 1:
                        isOpions = False
                        retail_price_input = retail_price_inputs[0]
                        retail_price_input.clear()
                        retail_price_input.send_keys(updated_retail_price)
                    elif isOpions:
                        prices = [input_element.get_attribute('value') for input_element in retail_price_inputs]
                        # Check if all option's prices are same
                        if len(set(prices)) > 1:# Not same
                            message = f" [!] {prd_code} has more than one option and the prices are different.\n"
                            self.tool.append_to_text_widget(message, "red")
                            for j in range(len(retail_price_inputs)):
                                wholesale_price = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[3]/section/div/div[3]/ul/li[{i+1}]/ul/li[3]/div/ul/li[{j+1}]/ul/li[3]")))
                                wholesale_price = int(wholesale_price.text.replace('원',''))
                                updated_retail_price = (1 / (1 - sc)) * (wholesale_price * (1 + ((net_profit_ratio / 100) / (1 - ait / 100))) - dpstar * (1 - dc) + dp)
                                updated_retail_price = round(updated_retail_price / 10) * 10
                                retail_price_input = retail_price_inputs[j]
                                retail_price_input.clear()
                                retail_price_input.send_keys(updated_retail_price)
                        else:
                            for j in range(len(retail_price_inputs)):
                                retail_price_input = retail_price_inputs[j]
                                retail_price_input.clear()
                                retail_price_input.send_keys(updated_retail_price)
                    done_btn = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(
                            (By.XPATH, f"/html/body/div[3]/section/div/div[3]/ul/li[{i + 1}]/ul/li[3]/div/div[2]/button[1]")))
                    done_btn.click()
                    i += 1
                    break
                elif store_name == 'smart':
                    while True:
                        try:
                            edit_button.click()
                            break
                        except ElementClickInterceptedException:
                            message = "[!] Element intercepted while sending button clicking.\n"
                            self.tool.append_to_text_widget(message, "red")
                            message = "[*] Scroll down little bit and try again.\n"
                            self.tool.append_to_text_widget(message, "blue")
                            self.tool.scroll_downer(250)
                    time.sleep(0.5)
                    # Calculate the retail price
                    omc = 0.0363 # Order managing commission
                    npic = 0.02 # Naver pay influx commission
                    ait = 6
                        # Iterate through the list to find the matching product code
                    for code, charge in lowest_delivery_charge_list:
                        if code == prd_code:
                            lowest_delivery_charge = charge
                            break  # Exit the loop once the match is found
                    #dp= delivery price that market pay, dpstar = consumer paid dp
                    dp = lowest_delivery_charge
                    if not isDeliveryCharge:
                        dpstar = 0 # Free shipping
                    elif isDeliveryCharge:
                        dpstar = dp
                    updated_retail_price = (1/(1-omc-npic))*(wholesale_price+dp+(((net_profit_ratio/100)*wholesale_price)/(1-ait/100)))-dpstar
                    updated_retail_price = round(updated_retail_price / 10) * 10
                        # If is discount rate = True -> run the next code. else, just update the retail price
                    if discount_rate_calculation == True:
                        if retail_price > updated_retail_price:
                            discount_rate = int((retail_price / updated_retail_price)*100 - 100)
                            discount_rate =(discount_rate+5)//10*10
                        else:
                            discount_rate = 0
                    # Check if there are more than one option
                    retail_price_inputs = []
                    retail_price_inputs = WebDriverWait(self.driver, 2).until(EC.presence_of_all_elements_located(
                        (By.XPATH, f'/html/body/div/section/div/div/ul/li[{i + 1}]/ul/li/div/ul/li/ul/li/input[@name="smart_option_modi_val"]')))
                    isOpions = True
                    if len(retail_price_inputs) == 1:
                        isOpions = False
                        retail_price_input = retail_price_inputs[0]
                        retail_price_input.clear()
                        retail_price_input.send_keys(updated_retail_price)
                    if isOpions:
                        prices = [input_element.get_attribute('value') for input_element in retail_price_inputs]
                        # Check if all the option's prices are same
                        if len(set(prices)) > 1: # Not same
                            message = f" [!] {prd_code} has more than one option and the prices are different.\n"
                            self.tool.append_to_text_widget(message, "red")
                            for j in range(len(retail_price_inputs)):
                                wholesale_price = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[3]/section/div/div[2]/ul/li[{i+1}]/ul/li[3]/div/ul/li[{j+1}]/ul/li[3]")))
                                wholesale_price = int(wholesale_price.text.replace('원',''))
                                updated_retail_price = (1/(1-omc-npic))*(wholesale_price+dp+(((net_profit_ratio/100)*wholesale_price)/(1-ait/100)))-dpstar
                                updated_retail_price = round(updated_retail_price / 10) * 10
                                retail_price_input = retail_price_inputs[j]
                                retail_price_input.clear()
                                retail_price_input.send_keys(updated_retail_price)
                        else:# Same
                            for j in range(len(retail_price_inputs)):
                                retail_price_input = retail_price_inputs[j]
                                retail_price_input.clear()
                                retail_price_input.send_keys(updated_retail_price)
                        
                    if discount_rate_calculation:
                        discount_rate_list.append((prd_code, discount_rate))
                    done_btn = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(
                            (By.XPATH, f"/html/body/div[3]/section/div/div[2]/ul/li[{i + 1}]/ul/li[3]/div/div[2]/button[1]")))
                    done_btn.click()
                    i += 1
                    break
        # print(f" [*] Sending to {store_name}...")
        if discount_rate_calculation == True:
            # Check for the existing smart_discount_rate_daily
            files = os.listdir('/Users/papag/OneDrive/src/Projects/vogueSnack')
            # Check if there is a smart_discount_rate_daily.csv
            matching_files = [file for file in files if file.startswith("smart_discount_rate_daily")]
            if matching_files:
                df_exist = pd.read_csv("smart_discount_rate_daily.csv")
            else:
                df_exist = pd.DataFrame(columns=['prd_code', 'discount_rate'])
            df_new = pd.DataFrame(discount_rate_list, columns=['prd_code', 'discount_rate'])
            df_discount = pd.concat([df_exist.astype(df_new.dtypes), df_new.astype(df_exist.dtypes)], ignore_index=True)
            # df_discount = pd.concat([df_exist, df_new], ignore_index=True)
            df_discount.to_csv("smart_discount_rate_daily.csv", encoding='utf-8-sig' , index = False)
        sendBtn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, f"//button[contains(@class, '{store_name}_modi_btn')]")))
        sendBtn.click()
        self.tool.popupHandler(100, store_name)
        # print("[+] Sending to store end." )

    def keywordCompare(self, preprocessed_df, net_profit_ratio, min_rating, prd_max_num, isDaily, discount_rate_calculation, isDeliveryCharge_coupang, isDeliveryCharge_smart, is_margin_descend):
        print("[+] Uploading process start.")
        if not isDaily:
            csv_name = 'preprocesedSourcedUpdated.csv'
        elif isDaily:
            csv_name = 'preprocesednaverSourcedUpdated.csv'
        files = os.listdir('/Users/papag/OneDrive/src/Projects/vogueSnack')
        # Check if there is a preprocessedSourcedUpdated.csv
        matching_files = [file for file in files if file == csv_name]
        if matching_files:
            preprocessed_df = pd.read_csv(csv_name)
        if not isDaily:
            targetList = preprocessed_df['바꾼키워드'].tolist()
        originalList = preprocessed_df['키워드'].tolist()
        if isDaily:
            targetList = originalList
        while True:
            try:
                for i in range(len(targetList)):
                    target = targetList[i]
                    originalTarget = originalList[i]
                    if isDaily:
                        target = originalTarget
                    isSearched = preprocessed_df['isSearched'].iloc[i]

                    while not isSearched:
                        # Perform Search
                        searchTextbox = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="prd_sear_txt"]')))
                        searchTextbox.clear()
                        ActionChains(self.driver).move_to_element(searchTextbox).click().send_keys(target).perform()
                        # if not isDaily:
                        #     print(f"[+] keyword typed in successfully: {target}({originalTarget})")
                        # if isDaily:
                        #     print(f"[+] keyword typed in successfully: {target}")
                        # Click on Search Button
                        WebDriverWait(driver=self.driver, timeout=30).until(EC.presence_of_element_located((By.CLASS_NAME, 'search_btn')))
                        search_btn = self.driver.find_element(By.CLASS_NAME, 'search_btn')
                        search_btn.click()
                        # print("[+] search button clicked successfully")
                        time.sleep(3)
                        
                        # Check for the existion of products
                        try:
                            self.driver.find_element(By.CLASS_NAME, 'product_set')
                            # print("[+] Exist. Uploading start.")
                            checkboxes = self.driver.find_elements(By.CLASS_NAME, "checkbox_label")
                            checkboxes_numb = len(checkboxes)
                            if checkboxes_numb < 5:
                                # Automatic checker
                                try:
                                    checked_prd_num, max_delivery_charge_list, lowest_delivery_charge_list = self.tool.product_checker(min_rating, prd_max_num, is_margin_descend)
                                except Exception as e:
                                    print(e)
                                if checked_prd_num == 0:
                                    # print("[+] Sending to Store passed.")
                                    preprocessed_df.loc[i, 'isSearched'] = True
                                    preprocessed_df.to_csv(csv_name, encoding='utf-8-sig' , index = False)
                                    break

                                else:
                                    smt_btn_path = "//div[@onclick='smartstore_download()']"
                                    coup_btn_path = "/html/body/div[3]/section/div/div[1]/div[4]"
                                    # print(f"Current item number info: ({i+1}/{len(targetList)})")
                                    self.sending_store(checkboxes_numb, originalTarget, coup_btn_path, 'coupang', net_profit_ratio, max_delivery_charge_list, lowest_delivery_charge_list, discount_rate_calculation, isDaily, isDeliveryCharge_coupang)
                                    self.sending_store(checkboxes_numb, originalTarget, smt_btn_path, 'smart', net_profit_ratio, max_delivery_charge_list, lowest_delivery_charge_list, discount_rate_calculation, isDaily, isDeliveryCharge_smart)
                                    preprocessed_df.loc[i, 'isSearched'] = True
                                    preprocessed_df.to_csv(csv_name, encoding='utf-8-sig' , index = False)
                                    break
                            else:
                                # Automatic checker
                                try:
                                    checked_prd_num, max_delivery_charge_list, lowest_delivery_charge_list = self.tool.product_checker(min_rating, prd_max_num, is_margin_descend)
                                except Exception as e:
                                    print(e)
                                if checked_prd_num == 0:
                                    # print(f"Current item number info: ({i+1}/{len(targetList)})")
                                    # print(" [*] Sending to Store passed.")
                                    preprocessed_df.loc[i, 'isSearched'] = True
                                    preprocessed_df.to_csv(csv_name, encoding='utf-8-sig' , index = False)
                                    break
                                else:
                                    smt_btn_path = "//div[@onclick='smartstore_download()']"
                                    coup_btn_path = "/html/body/div[3]/section/div/div[1]/div[4]"
                                    # print(f"Current item number info: ({i+1}/{len(targetList)})")
                                    self.sending_store(checkboxes_numb, originalTarget, coup_btn_path, 'coupang', net_profit_ratio, max_delivery_charge_list, lowest_delivery_charge_list, discount_rate_calculation, isDaily, isDeliveryCharge_coupang)
                                    self.sending_store(checkboxes_numb, originalTarget, smt_btn_path, 'smart', net_profit_ratio, max_delivery_charge_list, lowest_delivery_charge_list, discount_rate_calculation, isDaily, isDeliveryCharge_smart)
                                    preprocessed_df.loc[i, 'isSearched'] = True
                                    preprocessed_df.to_csv(csv_name, encoding='utf-8-sig' , index = False)
                                    break

                        except NoSuchElementException:
                            # print(f"Current item number info: ({i+1}/{len(targetList)})")
                            # print(" [*] Not exist")
                            preprocessed_df.loc[i, 'isSearched'] = True
                            preprocessed_df.to_csv(csv_name, encoding='utf-8-sig' , index = False)
                            break
                    percent = int(((i+1)/int(len(targetList)))*100)
                    print(f"\r [*] {percent}% complete..", end='')
                    if percent == 100:
                        # Print a newline character at the end to move the cursor to the next line
                        print()
                    i += 1
                break
            except Exception:
                self.driver.refresh()
        # print("[+] Uploading process end.")

class Tool:
    def __init__(self, driver, result_text, sourcing=None, uploading=None):
        self.driver = driver
        self.result_text = result_text
        self.sourcing = sourcing or Sourcing(driver)
        # self.uploading = uploading
        self.uploading = uploading or Uploading(driver)

    def prd_exsition_comparer(self, store_name):
        if store_name == 'smart':
            # Click the excel work dropdown
            dropdown = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[1]/div[2]/div/div/div[3]/div[1]/div')))
            time.sleep(0.5)
            dropdown.click()
            time.sleep(0.5)
            prd_list_download_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='seller-content']/ui-view/div/ui-view/div/div/div/div/div/div/div/div/div[@data-value='PRODUCT_DOWNLOAD']")))
            time.sleep(0.5)
            prd_list_download_btn.click()
            prd_list_smart_df = self.sourcing.downloadChecker('/Users/papag/Downloads', "스마트스토어상품", first_phase=False)
            prd_code_smart_series = prd_list_smart_df.iloc[:,1]
            prd_code_smart_df = prd_code_smart_series.to_frame(name='prd_code')
            prd_code_smart_df.insert(prd_code_smart_df.columns.get_loc('prd_code') + 1, 'isExist', False)
            prd_code_smart_df.to_csv('prd_code_smart_df.csv', index=False)
        if store_name == 'coupang':
            # Click the excel work dropdown
            dropdown = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[2]/span/div/ul[1]/li')))
            time.sleep(0.5)
            dropdown.click()
            time.sleep(0.5)
            prd_list_download_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='rootContainer']/div[6]/div[2]/div[2]/span/div/ul[2]/li[1]/div/div")))
            time.sleep(0.5)
            prd_list_download_btn.click()
            time.sleep(0.5)
            confirm_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='78380422-19cc-4696-bb9f-d00c7da901e6']")))
            time.sleep(0.5)
            confirm_btn.click()
            time.sleep(0.5)
            prd_info_checker = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='excel-download-request-catalogue']")))
            time.sleep(0.5)
            prd_info_checker.click()
            time.sleep(0.5)
            request_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='excelRequestDownload']/div[2]/button[2]")))
            time.sleep(0.5)
            request_btn.click()
            time.sleep(0.5)
            refresh_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='excelDownloadList']/div[2]/div[2]/button")))
            time.sleep(0.5)
            refresh_btn.click()
            time.sleep(0.5)
            download_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='excelDownloadList']/div[4]/table/tbody/tr[1]/td[6]/a")))
            time.sleep(0.5)
            download_btn.click()
            prd_list_coupang_df = self.sourcing.downloadChecker('/Users/papag/Downloads', "Coupang_detailinfo", first_phase=False)
            prd_code_coupang_series = prd_list_coupang_df.iloc[:,1]
            prd_code_coupang_df = prd_code_coupang_series.to_frame(name='prd_code')
            prd_code_coupang_df.insert(prd_code_coupang_df.columns.get_loc('prd_code') + 1, 'isExist', False)
            prd_code_coupang_df.dropna(inplace=True)
            prd_code_coupang_df.reset_index(drop=True, inplace=True)
            prd_code_coupang_df.drop(prd_code_coupang_df.index[0:14], inplace=True)
            prd_code_coupang_df.reset_index(drop=True, inplace=True)
            prd_code_coupang_df['prd_code'] = prd_code_coupang_df['prd_code'].str.split().str[0]
            prd_code_coupang_df.to_csv('prd_code_coupang_df.csv', index=False)

        if store_name == 'onchan':
            prd_list_smart_df = self.sourcing.downloadChecker('/Users/papag/Downloads', "prd_code_smart_df", first_phase=False)
            prd_list_coupang_df = self.sourcing.downloadChecker('/Users/papag/Downloads', "prd_code_coupang_df", first_phase=False)
            combined_df = pd.concat([prd_list_smart_df, prd_list_coupang_df])
            unique_df = combined_df.drop_duplicates(subset='prd_code', keep='first')

            for i in range(len(unique_df)):
                    while True:
                        try:
                            searchbox = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sale_search_txt"]')))
                            time.sleep(0.5)
                            searchbox.clear()
                            time.sleep(0.5)
                            searchbox.send_keys(unique_df['prd_code'][i])
                            break
                        except Exception:
                            self.driver.refresh()
                    time.sleep(0.5)
                    search_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/center/table/tbody/tr[3]/td[3]/table/tbody/tr[4]/td/table/tbody/tr[5]/td/table/tbody/tr[1]/td[2]/a/img')))
                    time.sleep(0.5)
                    search_btn.click()
                    percent = int(((i)/len(unique_df))*100)
                    print(f"\r [*] {percent}% complete..", end='')
                    if percent == 100:
                        # Print a newline character at the end to move the cursor to the next line
                        print()
                    counter = 0
                    while True:
                        try:
                            # print("\r [*] Wait for the table loading...", end='')
                            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/center/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table[@class="sa_mem_prd_li"]/tbody/tr[2]')))
                            # print()
                            # print(" [*] Table loaded successfully.")
                            isPrd = True
                            break
                        except Exception:
                            counter += 1
                            if counter == 2:
                                print()
                                print(" [*] There are no result.")
                                isPrd = False
                                break
                    if isPrd:
                        unique_df['isExist'][i] = True
            unique_df.to_csv('checked_prd_df.csv', index=False)
            message_smart_out_of_stock = " [*] Onchan: item checking success."
            print(message_smart_out_of_stock)

    def filtered_prd_deleter(self, store_name, prd_name_list):
        if store_name == 'coupang':
            print(f"[+] {store_name}: Filtering process start.")
            prd_name_list = []
            all_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchContainer"]/dd/div/dl[1]/dd[2]/span/span[1]/label')))
            time.sleep(0.5)
            all_btn.click()
            suspend_checker = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchContainer"]/dd/div/dl[1]/dd[2]/span/span[6]/label')))
            time.sleep(0.5)
            suspend_checker.click()
            rejected_checker = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchContainer"]/dd/div/dl[1]/dd[2]/span/span[10]/label')))
            time.sleep(0.5)
            rejected_checker.click()
            coupang_search_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchContainer"]/dd/div/dl[2]/dd/button[2]')))
            time.sleep(0.5)
            coupang_search_btn.click()
            show_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[1]/div[2]/div/div/ul[1]/li')))
            time.sleep(0.5)
            show_btn.click()
            show_500_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[1]/div[2]/div/div/ul[2]/li[5]/div/div')))
            time.sleep(0.5)
            show_500_btn.click()
            counter = 0
            while True:
                try:
                    print("\r [*] Wait for the table loading...", end='')
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[3]/div[1]/table/tbody/tr[1]/td[2]/span/input')))
                    print()
                    print(" [*] Table loaded successfully.")
                    break
                except Exception:
                    counter += 1
                    if counter >= 2:
                        print()
                        print(" [*] There are no result.")
                        break
            coupang_searched_num_element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[1]/div[1]/span/span')))
            checked_item_num = 0
            coupang_searched_num = coupang_searched_num_element.text
            if coupang_searched_num != "0":
                # Gathering the target prd_number
                while True:
                    counter = 0
                    try:
                        for i in range(int(coupang_searched_num)):
                            prd_name_full = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="rootContainer"]/div[6]/div[2]/div[3]/div[1]/table/tbody/tr[{i+1}]/td[5]/div[@class="product-name-block"]/span')))
                            time.sleep(0.5)
                            prd_name = prd_name_full.text.split()[0]
                            prd_name_list.append(prd_name)
                            prd_checkbox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="rootContainer"]/div/div/div/div/table/tbody/tr[{i+1}]/td/span/input[@type="checkbox"]')))
                            time.sleep(0.5)
                            prd_checkbox.click()
                            checked_item_num += 1
                            percent = int(((checked_item_num)/int(coupang_searched_num))*100)
                            # percent = int(((i+1)/int(coupang_searched_num))*100)
                            print(f"\r [*] {percent}% complete..", end='')
                            if percent == 100:
                                # Print a newline character at the end to move the cursor to the next line
                                print()
                        self.driver.execute_script("window.scrollTo(0, 0);")
                        time.sleep(0.5)
                        coupang_delete_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[2]/div[3]/div[1]/button[3]')))
                        time.sleep(0.5)
                        coupang_delete_btn.click()
                        coupang_confirm_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="container-wing-v2"]/div/div/div[@class="alert-buttons"]/button[contains(@class, "confirm") and contains(@class, "alert-confirm")]')))
                        time.sleep(0.5)
                        coupang_confirm_btn.click()
                        time.sleep(5)
                        self.driver.refresh()
                    except Exception as e:
                        # coupang_check_all_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[3]/div[1]/table/thead/tr/th[2]/span/input')))
                        # time.sleep(0.5)
                        # coupang_check_all_btn.click()
                        self.driver.execute_script("window.scrollTo(0, 0);")
                        time.sleep(0.5)
                        coupang_delete_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[2]/div[3]/div[1]/button[3]')))
                        time.sleep(0.5)
                        coupang_delete_btn.click()
                        # result = self.delete_suspend_confirmator('coupang',coupang_delete_btn)
                        coupang_confirm_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="container-wing-v2"]/div/div/div[@class="alert-buttons"]/button[contains(@class, "confirm") and contains(@class, "alert-confirm")]')))
                        time.sleep(0.5)
                        coupang_confirm_btn.click()
                        time.sleep(5)
                        # message_coupang_out_of_stock = f"Coupang(suspended, rejected): item deletion {result}."
                        self.driver.refresh()
                        while True:
                            try:
                                print("\r [*] Wait for the table loading...", end='')
                                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[3]/div[1]/table/tbody/tr[1]/td[2]/span/input')))
                                print()
                                print(" [*] Table loaded successfully.")
                                break
                            except TimeoutException:
                                counter += 1
                                if counter == 3:
                                    break
                        if counter ==3:
                            print()
                            print(" [*] There are no result.")
                            break
                return prd_name_list
            elif coupang_searched_num == "0":
                message_coupang_out_of_stock = " [*] Coupang(suspended, rejected): Item not found."
                print(message_coupang_out_of_stock)
                return prd_name_list
        if store_name == 'smart':
            if len(prd_name_list) != 0:
                print(f"[+] {store_name}: Filtering process start.")
                formatted_string = ','.join(f'{item}' for item in prd_name_list)
                smart_seller_prd_code_check = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[1]/div[2]/form/div[1]/div/ul/li[1]/div/div/div[1]/div/div[2]/label/span')))
                time.sleep(0.5)
                smart_seller_prd_code_check.click()
                smart_input_box = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[1]/div[2]/form/div[1]/div/ul/li[1]/div/div/div[2]/textarea')))
                time.sleep(0.5)
                smart_input_box.send_keys(formatted_string)
                smart_search_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[1]/div[2]/form/div[2]/div/button[1]')))
                time.sleep(0.5)
                smart_search_btn.click()
                counter = 0
                while True:
                    try:
                        print("\r [*] Wait for the table loading...", end='')
                        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div/ui-view/div/div/div/div/div/div/div/div/div/div[@row-index="0"]/div/div[@class="ag-cell-wrapper"]')))
                        print()
                        print(" [*] Table loaded successfully.")
                        break
                    except Exception:
                        counter += 1
                        if counter >= 2:
                            print()
                            print(" [*] There are no result.")
                            break
                smart_searched_num = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[1]/div[1]/h3/span')))
                if smart_searched_num.text != "0":
                    smart_check_all_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[2]/div[3]/div/div/div/div/div[1]/div[1]/div/div[1]/div[2]/div/label/span')))
                    time.sleep(0.5)
                    smart_check_all_btn.click()
                    smart_delete_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[2]/div[1]/div[1]/div/div[1]/button')))
                    # result = self.delete_suspend_confirmator('smart',smart_delete_btn)
                    time.sleep(0.5)
                    smart_delete_btn.click()
                    smart_confirm_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[@class="modal-content"]/div/div/span/button[contains(@class, "btn") and contains(@class, "btn-primary")]'))) 
                    time.sleep(0.5)
                    smart_confirm_btn.click()
                    self.popupHandler(5, 'smart')
                    time.sleep(0.5)
                    message_smart_out_of_stock = f" [*] Smart(suspended, rejected): item deletion {result}."
                else:
                    message_smart_out_of_stock = " [*] Smart(suspended, rejected): Item not found."
                print(message_smart_out_of_stock)
            elif len(prd_name_list) == 0:
                print(" [*] Smart(suspended, rejected): Item not found.")
            # Doing filtering in smart store.
            smart_prd_name_list = []
            smart_input_box = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[1]/div[2]/form/div[1]/div/ul/li[1]/div/div/div[2]/textarea')))
            smart_input_box.clear()
            on_saling_checker = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[1]/div[2]/form/div[1]/div/ul/li[2]/div/div/div/label[3]')))
            time.sleep(0.5)
            on_saling_checker.click()
            suspend_checker = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[1]/div[2]/form/div[1]/div/ul/li[2]/div/div/div/label[6]')))
            time.sleep(0.5)
            suspend_checker.click()
            # rejected_checker = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[1]/div[2]/form/div[1]/div/ul/li[2]/div/div/div/label[8]')))
            # time.sleep(0.5)
            # rejected_checker.click()
            smart_search_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[1]/div[2]/form/div[2]/div/button[1]')))
            time.sleep(0.5)
            smart_search_btn.click()
            # Click the prd view dropdown
            dropdown = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[1]/div[2]/div/div/div[2]/div[1]')))
            time.sleep(0.5)
            dropdown.click()
            #  Set to '500개씩'
            option = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='seller-content']/ui-view/div[2]/ui-view[2]/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/div/div[4]")))
            time.sleep(0.5)
            option.click()
            counter = 0
            while True:
                try:
                    print("\r [*] Wait for the table loading...", end='')
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div/ui-view/div/div/div/div/div/div/div/div/div/div[@row-index="0"]/div/div[@class="ag-cell-wrapper"]')))
                    print()
                    print(" [*] Table loaded successfully.")
                    break
                except Exception:
                    counter += 1
                    if counter >= 2:
                        print()
                        print(" [*] There are no result.")
                        return []
            smart_searched_num_element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[1]/div[1]/h3/span')))
            checked_item_num = 0
            smart_searched_num = smart_searched_num_element.text
            if smart_searched_num != "0":
                # Gathering the target prd_number
                while True:
                    counter = 0
                    try:
                        for i in range(int(smart_searched_num)):
                            prd_name_full = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[2]/div[3]/div/div/div/div/div[3]/div[1]/div[{i+1}]/div[5]')))
                            time.sleep(0.5)
                            prd_name = prd_name_full.text
                            smart_prd_name_list.append(prd_name)
                            prd_checkbox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[2]/div[3]/div/div/div/div/div[3]/div[1]/div[{i+1}]/div[1]/div/span[1]/i[2]')))
                            time.sleep(0.5)
                            prd_checkbox.click()
                            checked_item_num += 1
                            percent = int(((checked_item_num)/int(smart_searched_num))*100)
                            # percent = int(((i+1)/int(coupang_searched_num))*100)
                            print(f"\r [*] {percent}% complete..", end='')
                            if percent == 100:
                                # Print a newline character at the end to move the cursor to the next line
                                print()
                        # self.driver.execute_script("window.scrollTo(0, 0);")
                        time.sleep(0.5)
                        smart_delete_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[2]/div[1]/div[1]/div/div[1]/button')))
                        time.sleep(0.5)
                        smart_delete_btn.click()
                        smart_confirm_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[@class="modal-content"]/div/div/span/button[contains(@class, "btn") and contains(@class, "btn-primary")]'))) 
                        time.sleep(0.5)
                        smart_confirm_btn.click()
                        self.popupHandler(5, 'smart')
                        time.sleep(0.5)
                        while True:
                            try:
                                print("\r [*] Wait for the table loading...", end='')
                                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div/ui-view/div/div/div/div/div/div/div/div/div/div[@row-index="0"]/div/div[@class="ag-cell-wrapper"]')))
                                print()
                                print(" [*] Table loaded successfully.")
                                break
                            except TimeoutException:
                                counter += 1
                                if counter == 3:
                                    break
                        if counter ==3:
                            print()
                            print(" [*] There are no result.")
                            break
                    except Exception as e:
                        # coupang_check_all_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[3]/div[1]/table/thead/tr/th[2]/span/input')))
                        # time.sleep(0.5)
                        # coupang_check_all_btn.click()
                        # self.driver.execute_script("window.scrollTo(0, 0);")
                        time.sleep(0.5)
                        smart_delete_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[2]/div[1]/div[1]/div/div[1]/button')))
                        time.sleep(0.5)
                        smart_delete_btn.click()
                        time.sleep(0.5)
                        smart_confirm_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[@class="modal-content"]/div/div/span/button[contains(@class, "btn") and contains(@class, "btn-primary")]'))) 
                        time.sleep(0.5)
                        smart_confirm_btn.click()
                        time.sleep(0.5)
                        self.popupHandler(5, 'smart')
                        time.sleep(0.5)
                        while True:
                            try:
                                print("\r [*] Wait for the table loading...", end='')
                                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div/ui-view/div/div/div/div/div/div/div/div/div/div[@row-index="0"]/div/div[@class="ag-cell-wrapper"]')))
                                print()
                                print(" [*] Table loaded successfully.")
                                break
                            except TimeoutException:
                                counter += 1
                                if counter == 3:
                                    break
                        if counter ==3:
                            print()
                            print(" [*] There are no result.")
                            break
                prd_name_list.extend(smart_prd_name_list)
                return prd_name_list
        if store_name =='onchan':
            if len(prd_name_list) != 0:
                print(f"[+] {store_name}: Filtering process start.")
                for i in range(len(prd_name_list)):
                    while True:
                        try:
                            searchbox = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sale_search_txt"]')))
                            time.sleep(0.5)
                            searchbox.clear()
                            time.sleep(0.5)
                            searchbox.send_keys(prd_name_list[i])
                            break
                        except Exception:
                            self.driver.refresh()
                    time.sleep(0.5)
                    search_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/center/table/tbody/tr[3]/td[3]/table/tbody/tr[4]/td/table/tbody/tr[5]/td/table/tbody/tr[1]/td[2]/a/img')))
                    time.sleep(0.5)
                    search_btn.click()
                    percent = int(((i)/len(prd_name_list))*100)
                    print(f"\r [*] {percent}% complete..", end='')
                    if percent == 100:
                        # Print a newline character at the end to move the cursor to the next line
                        print()
                    counter = 0
                    while True:
                        try:
                            # print("\r [*] Wait for the table loading...", end='')
                            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/center/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table[@class="sa_mem_prd_li"]/tbody/tr[2]')))
                            # print()
                            # print(" [*] Table loaded successfully.")
                            isPrd = True
                            break
                        except Exception:
                            counter += 1
                            if counter == 2:
                                print()
                                print(" [*] There are no result.")
                                isPrd = False
                                break
                    if isPrd:
                        check_all_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/center/table/tbody/tr[3]/td[3]/table/tbody/tr[4]/td/table/tbody/tr[5]/td/table/tbody/tr[2]/td[1]/input')))
                        time.sleep(0.5)
                        check_all_btn.click()
                        delete_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/center/table/tbody/tr[3]/td[3]/table/tbody/tr[4]/td/table/tbody/tr[5]/td/table/tbody/tr[2]/td[2]/a[3]/button')))
                        time.sleep(0.5)
                        delete_btn.click()
                        time.sleep(0.5)
                        self.popupHandler(100, 'onchan')
                message_smart_out_of_stock = " [*] Onchan(suspended, rejected): item deletion success."
                print(message_smart_out_of_stock)
            elif len(prd_name_list) == 0:
                print(" [*] Onchan(suspended, rejected): Item not found.")
                return

    def order_gathering_handler(self, store_name):
        print(f"[+] Gathering order from {store_name} start.")
        gathering_order_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/center/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[@class='pg_btn']/a[@class = 'order_btn']")))
        time.sleep(0.5)
        gathering_order_btn.click()
        self.popupHandler(3, 'onchan')
        self.popupHandler(100, 'onchan')
        checkboxes = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="order_table"]/tbody/tr/td/input[@type="checkbox"]')))
        if len(checkboxes) < 2:
            print(" [*] No orders received")
            print(f"[+] Gathering order from {store_name} end.")
            return
        select_all_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/center/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table[@class='order_table']/tbody/tr/td[@class='ocheck comp']/input[@type='checkbox']")))
        time.sleep(0.5)
        select_all_btn.click()
        order_send_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/center/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table[@class='order_table']/tbody/tr/td[@class='pg_btn']/a[@class='order_send_btn']")))
        time.sleep(0.5)
        order_send_btn.click()
        self.popupHandler(3, 'onchan')
        self.driver.switch_to.window(self.driver.window_handles[1])
        order_send_point_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='order_send_btn']")))
        time.sleep(0.5)
        order_send_point_btn.click()
        alert_text = self.popupHandler(3, 'onchan')
        if "부족합니다" in alert_text:
            point_recharge_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/ul/li/p/a/button[@class='pnt_charge_btn']")))
            point_recharge_btn.click()
            print(" [*] Recharge the point and try again.")
            return
        self.driver.switch_to.window(self.driver.window_handles[0])
        confirm_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@class='order_lightbox']/div[@class='order_complete_box modal']/div[@class='modal_btn_wrap']/a[@class='confirm_btn']")))
        time.sleep(0.5)
        confirm_btn.click()
        print(f"[+] Gathering order from {store_name} end.")
        
    def out_of_stock_finisher(self):
        # Assume that we are in the onchan out of stock page.
        checkboxes = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@type="checkbox"]')))
        if len(checkboxes) <= 1:
            print("[+] Finisher: Out of stock products no exist.")
            return 
        check_out_of_stock_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/center/table[1]/tbody/tr[3]/td[3]/table/tbody/tr[4]/td/table/tbody/tr[4]/td/table/tbody/tr/td[2]/a[2]/button')))
        check_out_of_stock_btn.click()
        select_all_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/center/table[1]/tbody/tr[3]/td[3]/table/tbody/tr[4]/td/table/tbody/tr[4]/td/table/tbody/tr/td[2]/input')))
        select_all_btn.click()
        select_del_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/center/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/a[@class="btn_sel_del"]')))
        select_del_btn.click()
        self.popupHandler(5, 'onchan')
        self.popupHandler(5, 'onchan')
        print("[+] Finisher: Handling out of stock products finish.")
        
    def out_of_stock_checker(self):
        # Assume that we are in the onchan out of stock page.
        check_out_of_stock_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/center/table[1]/tbody/tr[3]/td[3]/table/tbody/tr[4]/td/table/tbody/tr[4]/td/table/tbody/tr/td[2]/a[2]/button')))
        time.sleep(0.5)
        check_out_of_stock_btn.click()
        checkboxes = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@type="checkbox"]')))
        time.sleep(0.5)
        if len(checkboxes) <= 1:
            print("[+] Out of stock products no exist.")
            return 'Empty', 'Empty'
        select_all_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/center/table[1]/tbody/tr[3]/td[3]/table/tbody/tr[4]/td/table/tbody/tr[4]/td/table/tbody/tr/td[2]/input')))
        time.sleep(0.5)
        select_all_btn.click()
        excel_download_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/center/table[1]/tbody/tr[3]/td[3]/table/tbody/tr[4]/td/table/tbody/tr[4]/td/table/tbody/tr/td[2]/a[1]/button')))
        time.sleep(0.5)
        excel_download_btn.click()
        self.popupHandler(5, 'onchan')
        # Read downloaded out of stock product list file
        out_of_stock_df = self.sourcing.downloadChecker('/Users/papag/Downloads', "excel_downdload", first_phase=False)
        # Preprocessing
        new_header = out_of_stock_df.iloc[0]  # Grab the first row for the header
        out_of_stock_df = out_of_stock_df[1:]
        out_of_stock_df.columns = new_header  # Set the header row as the df header
        new_out_of_stock_df = out_of_stock_df.loc[out_of_stock_df['분류'].isin(['단종', '품절'])] # Grab the 상품코드 which 분류 is 단종 or 품절
        new_out_of_stock_df.drop_duplicates(subset='상품코드', inplace=True)
        new_out_of_stock_temp_df = out_of_stock_df.loc[out_of_stock_df['분류'].isin(['일시품절'])] # Grab the 상품코드 which 분류 is 단종 or 품절
        new_out_of_stock_temp_df.drop_duplicates(subset='상품코드', inplace=True)
        # Sending the out of stock prd codes to coupang and smartstre and delete them.
        if len(new_out_of_stock_df) != 0:
            product_codes = new_out_of_stock_df['상품코드'].astype(str).tolist()
            out_of_stock_prd_string = ','.join(product_codes)
        elif len(new_out_of_stock_df) == 0:
            out_of_stock_prd_string = "Empty"
        if len(new_out_of_stock_temp_df) != 0:
            product_codes_temp = new_out_of_stock_temp_df['상품코드'].astype(str).tolist()
            out_of_stock_prd_temp_string = ','.join(product_codes_temp)
        elif len(new_out_of_stock_temp_df) == 0:
            out_of_stock_prd_temp_string = "Empty"
        return out_of_stock_prd_string, out_of_stock_prd_temp_string
    
    def delete_suspend_confirmator(self, store_name, delete_suspend_btn):
    # Check user confirmation before proceeding
        user_response = messagebox.askyesno("Confirmation", "Proceed?")
        if user_response:
            delete_suspend_btn.click()
            if store_name == 'coupang':
                coupang_confirm_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="container-wing-v2"]/div/div/div[@class="alert-buttons"]/button[contains(@class, "confirm") and contains(@class, "alert-confirm")]')))
                time.sleep(0.5)
                coupang_confirm_btn.click()
                return "Done"
            if store_name == 'smart':
                smart_confirm_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[@class="modal-content"]/div/div/span/button[contains(@class, "btn") and contains(@class, "btn-primary")]'))) 
                time.sleep(0.5)
                smart_confirm_btn.click()
                return "Done"
        elif not user_response:
            return "Cancelled"

    def out_of_stock_product_deleter(self, store_name, out_of_stock_prd_string, new_out_of_stock_temp_df):
        # coupang: Assume that we successfully navigate to the product list in the coupang wing
        if store_name == 'coupang':
            if out_of_stock_prd_string != "Empty":
                coupang_input_box = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchContainer"]/dd/div/dl[1]/dd[1]/span/span[2]/textarea')))
                coupang_input_box.send_keys(out_of_stock_prd_string)
                coupang_search_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchContainer"]/dd/div/dl[2]/dd/button[2]')))
                time.sleep(0.5)
                coupang_search_btn.click()
                counter = 0
                while True:
                    try:
                        print("\r [*] Wait for the table loading...", end='')
                        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[3]/div[1]/table/tbody/tr[1]/td[2]/span/input')))
                        print()
                        print(" [*] Table loaded successfully.")
                        break
                    except Exception:
                        counter += 1
                        if counter >= 2:
                            print()
                            print(" [*] There are no result.")
                            break
                coupang_searched_num = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[1]/div[1]/span/span')))
                if coupang_searched_num.text != "0":
                    coupang_check_all_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[3]/div[1]/table/thead/tr/th[2]/span/input')))
                    time.sleep(0.5)
                    coupang_check_all_btn.click()
                    coupang_delete_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[2]/div[3]/div[1]/button[3]')))
                    result = self.delete_suspend_confirmator('coupang',coupang_delete_btn)
                    message_coupang_out_of_stock = f"Coupang(out of stock): item deletion {result}."
                else:
                    message_coupang_out_of_stock = "Coupang(out of stock): Item not found."
                print(message_coupang_out_of_stock)
            if new_out_of_stock_temp_df != "Empty":
                coupang_input_box = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchContainer"]/dd/div/dl[1]/dd[1]/span/span[2]/textarea')))
                time.sleep(0.5)
                coupang_input_box.clear()
                time.sleep(0.5)
                coupang_input_box.send_keys(new_out_of_stock_temp_df)
                coupang_search_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchContainer"]/dd/div/dl[2]/dd/button[2]')))
                time.sleep(0.5)
                coupang_search_btn.click()
                counter = 0
                while True:
                    try:
                        print("\r [*] Wait for the table loading...", end='')
                        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[3]/div[1]/table/tbody/tr[1]/td[2]/span/input')))
                        print()
                        print(" [*] Table loaded successfully.")
                        break
                    except Exception:
                        counter += 1
                        if counter >= 2:
                            print()
                            print(" [*] There are no result.")
                            break
                coupang_searched_num = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[1]/div[1]/span/span')))
                time.sleep(0.5)
                if coupang_searched_num.text != "0":
                    coupang_check_all_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[3]/div[1]/table/thead/tr/th[2]/span/input')))
                    time.sleep(0.5)
                    coupang_check_all_btn.click()
                    coupang_change_stat_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[2]/div[3]/div[1]/div[2]/div/ul[1]/li')))
                    time.sleep(0.5)
                    coupang_change_stat_btn.click()
                    coupang_suspend_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[2]/div[3]/div[1]/div[2]/div/ul[2]/li[3]/div/div')))
                    result = self.delete_suspend_confirmator('coupang',coupang_suspend_btn)
                    message_coupang_temp = f"Coupang(temporally): item suspention {result}."
                else:
                    message_coupang_temp = "Coupang(temporally): Item not found."
                print(message_coupang_temp)
        
        if store_name == 'smart':
            if out_of_stock_prd_string != "Empty":
                smart_seller_prd_code_check = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[1]/div[2]/form/div[1]/div/ul/li[1]/div/div/div[1]/div/div[2]/label/span')))
                time.sleep(0.5)
                smart_seller_prd_code_check.click()
                smart_input_box = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[1]/div[2]/form/div[1]/div/ul/li[1]/div/div/div[2]/textarea')))
                time.sleep(0.5)
                smart_input_box.send_keys(out_of_stock_prd_string)
                smart_search_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[1]/div[2]/form/div[2]/div/button[1]')))
                time.sleep(0.5)
                smart_search_btn.click()
                counter = 0
                while True:
                    try:
                        print("\r [*] Wait for the table loading...", end='')
                        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div/ui-view/div/div/div/div/div/div/div/div/div/div[@row-index="0"]/div/div[@class="ag-cell-wrapper"]')))
                        print()
                        print(" [*] Table loaded successfully.")
                        break
                    except Exception:
                        counter += 1
                        if counter >= 2:
                            print()
                            print(" [*] There are no result.")
                            break
                smart_searched_num = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[1]/div[1]/h3/span')))
                if smart_searched_num.text != "0":
                    smart_check_all_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[2]/div[3]/div/div/div/div/div[1]/div[1]/div/div[1]/div[2]/div/label/span')))
                    time.sleep(0.5)
                    smart_check_all_btn.click()
                    smart_delete_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[2]/div[1]/div[1]/div/div[1]/button')))
                    result = self.delete_suspend_confirmator('smart',smart_delete_btn)
                    message_smart_out_of_stock = f"Smart(out of stock): item deletion {result}."
                else:
                    message_smart_out_of_stock = "Smart(out of stock): Item not found."
                print(message_smart_out_of_stock)
            if new_out_of_stock_temp_df != "Empty":
                smart_seller_prd_code_check = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[1]/div[2]/form/div[1]/div/ul/li[1]/div/div/div[1]/div/div[2]/label')))
                time.sleep(0.5)
                smart_seller_prd_code_check.click()
                smart_input_box = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[1]/div[2]/form/div[1]/div/ul/li[1]/div/div/div[2]/textarea')))
                time.sleep(0.5)
                smart_input_box.clear()
                time.sleep(0.5)
                smart_input_box.send_keys(new_out_of_stock_temp_df)
                smart_search_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[1]/div[2]/form/div[2]/div/button[1]')))
                time.sleep(0.5)
                smart_search_btn.click()
                counter = 0
                while True:
                    try:
                        print("\r [*] Wait for the table loading...", end='')
                        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div/ui-view/div/div/div/div/div/div/div/div/div/div[@row-index="0"]/div/div[@class="ag-cell-wrapper"]')))
                        print()
                        print(" [*] Table loaded successfully.")
                        break
                    except Exception:
                        counter += 1
                        if counter >= 2:
                            print()
                            print(" [*] There are no result.")
                            break
                smart_searched_num = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[1]/div[1]/h3/span')))
                if smart_searched_num.text != "0":
                    smart_check_all_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[2]/div[3]/div/div/div/div/div[1]/div[1]/div/div[1]/div[2]/div/label/span')))
                    time.sleep(0.5)
                    smart_check_all_btn.click()
                    smart_change_stat_dropbox = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[1]')))
                    time.sleep(0.5)
                    smart_change_stat_dropbox.click()
                    smart_suspend_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[3]')))
                    result = self.delete_suspend_confirmator('smart',smart_suspend_btn)
                    message_smart_temp = f"Smart(temporally): Item suspension {result}."
                else:
                    message_smart_temp = "Smart(temporally): Item not found."
                print(message_smart_temp)

    def delivery_charge_changer(self,storename, isDeliveryCharge):
        print(f"[+] Start delivery charge chaning process in {storename}. isDeliveryCharge = {isDeliveryCharge}")
        if not isDeliveryCharge:
            # Move to the view/edit products page
            if storename == 'coupang':
                self.sourcing.pageNavigator('https://wing.coupang.com/vendor-inventory/list?searchIds=&startTime=2000-01-01&endTime=2099-12-31&productName=&brandName=&manufacturerName=&productType=&autoPricingStatus=ALL&dateType=productRegistrationDate&dateRangeShowStyle=true&dateRange=all&saleEndDatePeriodType=&includeUsedProduct=&deleteType=false&deliveryMethod=&shippingType=&shipping=&otherType=&productStatus=SAVED,WAIT_FOR_SALE,VALID,SOLD_OUT,INVALID,END_FOR_SALE,APPROVING,IN_REVIEW,DENIED,PARTIAL_APPROVED,APPROVED,ALL&advanceConditionShow=false&displayCategoryCodes=&currentMenuCode=&rocketMerchantVersion=&registrationType=&upBundling=ALL&hasUpBundlingItem=&hasBadImage=false&page=1&countPerPage=50&sortField=vendorInventoryId&desc=true&fromListV2=true&locale=ko_KR&vendorItemViolationType=&coupangAttributeOptimized=FALSE&autoPricingActive=')
                time.sleep(0.5)
                all_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchContainer"]/dd/div/dl[1]/dd[2]/span/span[1]/label')))
                time.sleep(0.5)
                all_btn.click()
                time.sleep(0.5)
                on_sale_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchContainer"]/dd/div/dl[1]/dd[2]/span/span[4]/label')))
                time.sleep(0.5)
                on_sale_btn.click()
                time.sleep(0.5)
                advance_search_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchContainer"]/dd/div/dl[2]/dd/button[3]')))
                time.sleep(0.5)
                advance_search_btn.click()
                time.sleep(0.5)
                shipping_type_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchContainer"]/dd/div/dl[1]/dd[9]/div/span[6]/div/ul[1]/li')))
                time.sleep(0.5)
                shipping_type_btn.click()
                time.sleep(0.5)
                paid_shipping_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchContainer"]/dd/div/dl[1]/dd[9]/div/span[6]/div/ul[2]/li[3]/div')))
                time.sleep(0.5)
                paid_shipping_btn.click()
                time.sleep(0.5)
                show_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[1]/div[2]/div/div/ul[1]/li')))
                time.sleep(0.5)
                show_btn.click()
                time.sleep(0.5)
                show_500_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[1]/div[2]/div/div/ul[2]/li[5]/div/div')))
                time.sleep(0.5)
                show_500_btn.click()
                counter = 0
                while True:
                    try:
                        print("\r [*] Wait for the table loading...", end='')
                        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[3]/div[1]/table/tbody/tr[1]/td[2]/span/input')))
                        print()
                        print(" [*] Table loaded successfully.")
                        counter = 0
                        break
                    except TimeoutException:
                        counter += 1
                        if counter == 3:
                            input(" [!] No items found.")
                table = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[3]/div[1]/table')))
                # Assuming the scrollable container is a direct parent of the table
                scrollable_container = table.find_element(By.XPATH, "./..")
                scroll_script = "arguments[0].scrollLeft = 3200;"  # Adjust scrollLeft for 27th column
                self.driver.execute_script(scroll_script, scrollable_container)
                checked_item_num = 0
                coupang_searched_num_element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[1]/div[1]/span/span')))
                coupang_searched_num = coupang_searched_num_element.text
                while True:
                    counter = 0
                    try:
                        for i in range(int(coupang_searched_num)):
                            percent = int(((checked_item_num)/int(coupang_searched_num))*100)
                            print(f"\r [*] {percent}% complete..", end='')
                            if percent == 100:
                                # Print a newline character at the end to move the cursor to the next line
                                print()
                            time.sleep(0.5)
                            shipping_edit_btn = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, f"//*[@id='rootContainer']/div[6]/div[2]/div[3]/div[1]/table/tbody/tr[{i+1}]/td[27]")))
                            time.sleep(0.5)
                            shipping_edit_btn.click()
                            time.sleep(0.5)
                            paid_delievery_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[4]/div/div/div[2]/div[2]/div[2]/div/div/div[6]/div/div[1]/div/div[2]/div/div/ul[1]/li')))
                            time.sleep(0.5)
                            paid_delievery_btn.click()
                            time.sleep(0.5)
                            free_shipping_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[4]/div/div/div[2]/div[2]/div[2]/div/div/div[6]/div/div[1]/div/div[2]/div/div/ul[2]/li[1]/div')))
                            time.sleep(0.5)
                            free_shipping_btn.click()
                            time.sleep(0.5)
                            save_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[4]/div/div/div[3]/div/button[2]')))
                            time.sleep(0.5)
                            save_btn.click()
                            time.sleep(0.5)
                            confirm_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="container-wing-v2"]/div/div/div[@class="alert-buttons"]/button[contains(@class, "confirm") and contains(@class, "alert-confirm")]')))
                            time.sleep(0.5)
                            confirm_btn.click()
                            time.sleep(1)
                            checked_item_num += 1
                    except Exception as e:
                        self.driver.refresh()
                        while True:
                            try:
                                print("\r [*] Wait for the table loading...", end='')
                                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[3]/div[1]/table/tbody/tr[1]/td[2]/span/input')))
                                print()
                                print(" [*] Table loaded successfully.")
                                break
                            except TimeoutException:
                                counter += 1
                                if counter == 3:
                                    print()
                                    print(" [*] There are no result.")
                                    break
                        if counter != 3:
                            table = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rootContainer"]/div[6]/div[2]/div[3]/div[1]/table')))
                            # Assuming the scrollable container is a direct parent of the table
                            scrollable_container = table.find_element(By.XPATH, "./..")
                            scroll_script = "arguments[0].scrollLeft = 3200;"  # Adjust scrollLeft for 27th column
                            self.driver.execute_script(scroll_script, scrollable_container)
                        if counter ==3:
                            break
                print(f"[+] Delivery charge chaning process in {storename}. isDeliveryCharge = {isDeliveryCharge} end.")
    
    # Automate checking above the setted rate.
    def product_checker(self, rate_lowering, max_num, is_margin_descend):
        counter = 0
        max_delivery_charge_list = []
        lowest_delivery_charge_list = []
        if is_margin_descend:
            # Set order of descending with margin
            margin_descend_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="search_filter"]/tbody/tr/td[6]/div/a')))
            margin_descend_btn.click()
        prd_view_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/section/div/div[1]/div[5]')))
        prd_view_btn.click()
        view_200_btn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/section/div/div[1]/div[5]/ul/li[3]')))
        view_200_btn.click()
        rating_list = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="prd_form"]/ul/li//dd[@class="total_start_num"]')))
        for i in range(len(rating_list)):
            rating_list = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="prd_form"]/ul/li//dd[@class="total_start_num"]')))
            uploaded_list = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="prd_form"]/ul/li/dl/dd/span[@class="sale_state"]')))
            if rating_list[i].text == '신규' or rating_list[i].text == 'NaN' or uploaded_list[i].text == '판매신청완료':
                continue
            rating = float(rating_list[i].text)
            if rating > rate_lowering:
                prd_image = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="prd_form"]/ul/li[{i + 1}]/dl/dd[2]/a/img')))
                self.driver.set_page_load_timeout(10)
                try:
                    prd_image.click()
                except Exception:
                    self.driver.execute_script("window.stop();") # stop loading the page
                # Get if price autonomy or not
                price_autonomy_detail = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[2]/section/div/div[1]/div[3]/ul/li[3]/ul/li[3]/div[2]/span')))
                price_autonomy_detail_text = price_autonomy_detail.text
                prd_price = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, f'/html/body/div/section/div/div/div/div/div[@class="prod_cus_price"]')))
                prd_price_text = prd_price.text.strip().replace('원','')
                if price_autonomy_detail_text == "가격자율" and prd_price_text != "0":
                    # Get delevery charge(lower, max)
                    delievery_fee_detail = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[2]/section/div/div[1]/div[3]/ul/li[4]/ul/li[1]/div[2]')))
                    delievery_fee_detail_text = delievery_fee_detail.text
                        # Remove HTML tags if any exist
                    clean_delievery_fee_detail_text = re.sub('<[^<]+?>', '', delievery_fee_detail_text)
                        # Find all instances of numeric values (with potential commas)
                    delievery_fees = re.findall(r'\d+,?\d*', clean_delievery_fee_detail_text)
                        # Convert found numbers to integers, considering the commas
                    delievery_fees_int = [int(n.replace(',', '')) for n in delievery_fees]
                        # The lowest charge is the base charge, which is the first number
                    lowest_charge = delievery_fees_int[0]
                        # Calculate the maximum charge by adding the highest additional charge to the base charge
                        # Assuming additional charges are listed after the base charge
                    additional_charges = delievery_fees_int[1:]  # Skip the first number which is the base charge
                    max_charge = lowest_charge + max(additional_charges) if additional_charges else lowest_charge
                    # Get product code
                    prd_code = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, f"//div[@class='prod_detail_title' and contains(text(), '제품코드')]/following-sibling::div[1]")))
                    prd_code = prd_code.text
                    # Append to the delivery charge list
                    max_delivery_charge_list.append((prd_code, max_charge))
                    lowest_delivery_charge_list.append((prd_code, lowest_charge))
                    # Move to the back page
                    self.driver.back()
                    counter += 1
                else: # If the price autonomy is false, back to the page and deselect the product.
                    self.driver.back()
                    checkbox = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="prd_form"]/ul/li[{i+1}]/dl/dd[1]/span[1]')))
                    checkbox.click()
                    continue
            if counter == max_num:
                break
            elif rating <= rate_lowering:
                continue
        return counter, max_delivery_charge_list, lowest_delivery_charge_list

    def scroll_downer(self, howmuch):
        # Scroll down a little bit
        self.driver.execute_script(f"window.scrollBy(0, {howmuch});")  # Scrolls down 250 pixels

    def append_to_text_widget(self, message, tag=""):
        # Method to append text to the Text widget in gui.py
        self.result_text.insert(tk.END, message, tag)

    def popupHandler(self, waitTime, store_name):
        counter = 0
        while counter < waitTime + 1:
            # Handling JavaScript Alert Pop-Up
            try:
                alert = Alert(self.driver)
                alert_text = alert.text
                # print(" [*] Alert Text:", alert_text)
                alert.accept()  # Use alert.dismiss() if you want to cancel the alert
                # print(" [*] Alert closed")
                break
            except NoAlertPresentException:
                time.sleep(1)
                alert_text = " [*] There is no javascript alert."
                counter += 1
            
        # Handling Web Page Pop-Up
        if store_name == 'sellha':
            try:
                close_button = self.driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div[2]/div[2]/button")
                close_button.click()
                # print(" [*] Sellha: Web page pop-up closed")
            except Exception:
                pass
                # print(" [*] Sellha: No Web page pop-up")
        if store_name == 'smart':
            try:
                close_button = self.driver.find_element(By.XPATH, "//*[@class='modal-dialog']/div/div/ncp-manager-notice-view/ng-transclude/button[@class='close']/span")
                close_button.click()
                # print(" [*] Smart: Web page pop-up closed")
            except Exception:
                try:
                    close_button = self.driver.find_element(By.XPATH, "/html/body/div/div/div[@class='modal-content']/div/button[@class='close']/span")
                    close_button.click()
                    # print(" [*] Smart: Web page pop-up closed")
                except Exception:
                    try:
                        close_button = self.driver.find_element(By.XPATH, "//*[@id='seller-content']/div/div/div[@class='modal-content']/div/div/button[@class='close']/span")
                        close_button.click()
                        # print(" [*] Smart: Web page pop-up closed")
                    except Exception:
                        # print(" [*] Smart: No Web page pop-up")
                        pass
        return alert_text
    
    def discountRateSetting(self, store_name):
        print("[+] Pricing start.")
        if store_name == 'smart':
            while True:
                # Check for the existing smart_discount_rate_daily
                files = os.listdir('/Users/papag/Downloads')
                # Check if there is a smart_discount_rate_daily.csv
                matching_files = [file for file in files if file.startswith("스마트스토어상품")]
                if not matching_files:
                    print("[+] Download fixable form process start.")
                    # Move to the product list edit page
                    self.sourcing.pageNavigator('https://sell.smartstore.naver.com/#/products/origin-list')
                    # Click the prd view dropdown
                    dropdown = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[1]/div[2]/div/div/div[2]/div[1]')))
                    dropdown.click()
                    #  Set to '500개씩'
                    option = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='seller-content']/ui-view/div[2]/ui-view[2]/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/div/div[4]")))
                    option.click()
                    # Check the number of uploaded items checkboxes
                    all_checklBox = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[2]/div[3]/div/div/div/div/div[1]/div[1]/div/div[1]/div[2]/div/label/span')))
                    all_checklBox.click()
                    # Click the xlsx dropdown
                    dropdown_xlsx = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[1]/div[2]/div/div/div[3]/div[1]/div')))
                    dropdown_xlsx.click()
                    # Click the xlsx correction form
                    correction_form_download = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[1]/div[2]/div/div/div[3]/div[2]/div/div[4]')))
                    correction_form_download.click()
                    # Click the download button
                    download_btn = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, "//button[contains(., '다운로드')]")))
                    download_btn.click()
                    # Read the correction form and Edit
                    smart_df = self.sourcing.downloadChecker('/Users/papag/Downloads', "스마트스토어상품", first_phase=False)
                    print("[+] Download fixable form process end.")
                else:
                    # Check for the existing smart_discount_rate_daily
                    files = os.listdir('/Users/papag/OneDrive/src/Projects/vogueSnack')
                    # Check if there is a smart_discount_rate_daily.csv
                    matching_files = [file for file in files if file.startswith("스마트스토어상품_할인률추가")]
                    if not matching_files:
                        smart_df = self.sourcing.downloadChecker('/Users/papag/Downloads', "스마트스토어상품", first_phase=False)
                        print("[+] Appending discount rate start.")
                        smart_discount_rate_df = pd.read_csv('smart_discount_rate_daily.csv', encoding='utf-8-sig')
                        # Create new dataframe which is editable
                        new_header = smart_df.iloc[0]  # Grab the first row for the header
                        new_smart_df = smart_df.drop([1,2,3])
                        new_smart_df.columns = new_header  # Set the header row as the df header
                            # Drop the 1st,2nd, 3rd,4th row
                        new_smart_df['PC\n기본 할인 단위'] = '%'
                        new_smart_df['모바일\n기본할인 단위'] = '%'
                        new_smart_df = new_smart_df.drop([0])
                        new_smart_df.reset_index(drop=True, inplace=True)
                            # Create a mapping from prd_code to discount_rate
                        discount_map = smart_discount_rate_df.set_index('prd_code')['discount_rate'].to_dict()
                            # Update the discount values in smart_df
                            # Create temporary columns for the mapped discount rates
                        new_smart_df['temp_PC_discount'] = new_smart_df['판매자 상품코드'].map(discount_map)
                        new_smart_df['temp_mobile_discount'] = new_smart_df['판매자 상품코드'].map(discount_map)
                            # Update only the matched rows, leaving non-matched rows as they are
                        new_smart_df['PC\n기본할인 값'].update(new_smart_df['temp_PC_discount'])
                        new_smart_df['모바일\n기본할인 값'].update(new_smart_df['temp_mobile_discount'])
                            # Drop the temporary columns
                        new_smart_df.drop(['temp_PC_discount', 'temp_mobile_discount'], axis=1, inplace=True)
                            # Number of rows to replace in 'smart_df' from the 5th row onward
                        num_rows_to_replace = len(smart_df) - 4  # Adjust based on how many rows you want to replace
                            # Replace values in 'smart_df' from the 5th row with values from 'new_smart_df' from the 1st row
                        smart_df.iloc[4:4+num_rows_to_replace] = new_smart_df.iloc[0:num_rows_to_replace].values
                        smart_df.to_excel('스마트스토어상품_할인률추가.xlsx', index = False)
                        print("[+] Appending discount rate end.")
                    else:
                        print("[+] Uploading discount rate start.")
                        # Move to the product list edit page
                        self.sourcing.pageNavigator('https://sell.smartstore.naver.com/#/products/origin-list')
                        # Upload the discountRateSetted file to the smart store.
                        while True:
                            try:
                                while True:
                                    try:
                                        time.sleep(2)
                                        dropdown_xlsx = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[1]/div[2]/div/div/div[3]/div[1]')))
                                        time.sleep(2)
                                        dropdown_xlsx.click()
                                        break
                                    except TimeoutException:
                                        continue
                                while True:
                                    try:
                                        time.sleep(3)
                                        correction_form_upload = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[1]/div[2]/div/div/div[3]/div[2]/div/div[5]')))
                                        time.sleep(2)
                                        correction_form_upload.click()
                                        break
                                    except TimeoutException:
                                        continue
                                break
                            except ElementNotInteractableException:
                                continue
                        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='modal-body']//div[@class='seller-input']//a[text()='파일 찾기']")))
                        find_file = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='modal-body']//div[@class='seller-input']//a[text()='파일 찾기']")))
                        find_file.click()
                        print("[+] Uploading discount rate end.")
                        input("[+] Pricing end. If done, press enter.")
                        # Delete dummy files
                        os.remove('/Users/papag/OneDrive/src/Projects/vogueSnack/스마트스토어상품_할인률추가.xlsx')
                        print(f"Deleted file: 스마트스토어상품_할인률추가.xlsx")
                        os.remove('/Users/papag/OneDrive/src/Projects/vogueSnack/smart_discount_rate_daily.csv')
                        print(f"Deleted file: smart_discount_rate_daily.csv")
                        folder_path = '/Users/papag/Downloads/'
                        target_prefix = '스마트스토어'
                        for filename in os.listdir(folder_path):
                            if filename.startswith(target_prefix) and filename.endswith(".xlsx"):
                                file_path = os.path.join(folder_path, filename)
                                os.remove(file_path)
                                print(f"Deleted file: {filename}")
                        break
        # elif store_name == 'coupang':





