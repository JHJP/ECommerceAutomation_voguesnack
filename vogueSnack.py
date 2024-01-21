from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
import os.path
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, StaleElementReferenceException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
import tkinter as tk

class Sourcing:
    def __init__(self, driver, tool=None):
        self.driver = driver
        self.tool = tool

    def login(self, url, id, password, usernameBox, passwordBox, loginbtn, isNewTab):
        if not isNewTab:
            self.driver.get(url)
        else:
            print("[+] Move to the opend tab.")
            smart_url = 'https://accounts.commerce.naver.com/login?url=https%3A%2F%2Fsell.smartstore.naver.com%2F%23%2Flogin-callback'
            # Move to the data center hompage and compare keywords if there is in the center or not.
            self.pageNavigator(smart_url)
            time.sleep(5)
            self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div/div[5]/div[1]/ul/li[2]/button').click()
            time.sleep(5)
            # move to the opend window
            windows = self.driver.window_handles
            smart_login_windows = windows[1]
            self.driver.switch_to.window(smart_login_windows)
            print("[+] Move to the opend tab successful.")
        self.driver.find_element(By.NAME, usernameBox).send_keys(id)
        self.driver.find_element(By.NAME, passwordBox).send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, loginbtn).click() # use CSS_SELECTOR to change class name format. Because there are spaces on class name, which means not a single class.
        # wait the ready state to be complete
        WebDriverWait(driver=self.driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )
        print("[+] Login successful")
        # error_message = "Incorrect username or password."
        # # get the errors (if there are)
        # errors = self.driver.find_element(By.CLASS_NAME,"flash-error")
        # # if we find that error message within errors, then login is failed
        # if any(error_message in e.text for e in errors):
        #     print("[!] Login failed")
        # else:
        #     print("[+] Login successful")

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
            # print("[!] Navigation failed")
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
            # print("[!] Category button clicked failed")
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
            # print("[!] Download buttion click failed")
            message = "[!] Download buttion click failed.\n"
            self.tool.append_to_text_widget(message, "red")
        else:
            print("[+] Download button clicked successfully")
        

    def downloadChecker(self, download_path, file_prefix):
        counter = 0
        while True:
            time.sleep(3)
            files = os.listdir(download_path)
            matching_files = [file for file in files if file.startswith(file_prefix)]
            if not matching_files and counter < 3:
                print(f"{file_prefix} no exist. I'll check again.")
                counter += 1
                continue
            elif not matching_files and counter >= 3:
                input(f"{file_prefix} no exist. Download again.If you ready, press enter.")
                counter = 0
                continue
            else:
                print("[+] Excel file downloaded successfully. Start reading.")
                # Construct the full path to the first matching file
                file_to_check = os.path.join(download_path, matching_files[0])
                if os.path.isfile(file_to_check):
                    # Assuming it's an Excel file, you can read it into a Pandas DataFrame
                    try:
                        dictionary = pd.read_excel(file_to_check, sheet_name=None)
                        # Concatenate all DataFrames from each sheet into one DataFrame
                        df = pd.concat(dictionary, ignore_index=True)
                        print("[+] Excel file read successfully.")
                    except ValueError:
                        df = pd.read_csv(file_to_check, encoding='utf-8')
                        print("[+] CSV file read successfully.")
                    # You can now work with the 'df' DataFrame.
                    return df
                
    def targetListMaker(self, preprocessed_df, isDaily):
        if not isDaily:
            csv_name = 'preprocesedSourced.csv'
        elif isDaily:
            csv_name = 'naverSourced.csv'
        files = os.listdir('/Users/papag/OneDrive/src/Projects/vogueSnack')
        matching_files = [file for file in files if file.startswith(csv_name)]
        if matching_files:
            preprocessed_df = pd.read_csv(csv_name)
        else:
            preprocessed_df.insert(preprocessed_df.columns.get_loc('키워드') + 1, '바꾼키워드', None)
            preprocessed_df.insert(preprocessed_df.columns.get_loc('바꾼키워드') + 1, 'isSearched', False)
            preprocessed_df.insert(preprocessed_df.columns.get_loc('isSearched') + 1, 'isEdited', False)

        print(f"There are number of {len(preprocessed_df)} items.")
         # Stack to keep history of DataFrame states
        history = []

        i = 0
        while i < len(preprocessed_df):
            isEdited = preprocessed_df['isEdited'][i]

            if not isEdited:
                decision = input(f"i={i}, {preprocessed_df.iloc[i]['키워드']}; Tell me the word you want to change (1=delete, 2=maintain, 3=undo): ")
                if decision == '3' and history:
                    preprocessed_df = history.pop()  # Revert to the last state
                    if i > 0:
                        i -= 1
                    preprocessed_df.reset_index(drop=True, inplace=True)
                    preprocessed_df.to_csv(csv_name, encoding='utf-8-sig', index = False)
                    continue
                else:
                    history.append(preprocessed_df.copy())  # Save the current state

                if decision == '1': # drop the row
                    preprocessed_df.drop(preprocessed_df.index[i], inplace=True)
                    preprocessed_df.reset_index(drop=True, inplace=True)
                    i -= 1
                    preprocessed_df.to_csv(csv_name, encoding='utf-8-sig', index = False)
                elif decision == '2': # Maintain the keyword
                    preprocessed_df.at[i, '바꾼키워드'] = preprocessed_df.at[i, '키워드']
                    preprocessed_df.at[i, 'isEdited'] = True
                    preprocessed_df.to_csv(csv_name, encoding='utf-8-sig', index = False)
                else: # Change the keyword
                    preprocessed_df.at[i, '바꾼키워드'] = decision
                    preprocessed_df.at[i, 'isEdited'] = True
                    preprocessed_df.to_csv(csv_name, encoding='utf-8-sig', index = False)
            i += 1
        preprocessed_df.drop_duplicates(subset='바꾼키워드', inplace=True)
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
        matching_files = [file for file in files if file.startswith('naverSourced')]
        if not matching_files:
            # Append data from the naver data lab
            naver_datalab_url = 'https://datalab.naver.com/'
            self.pageNavigator(naver_datalab_url)
                # Get data
                # Select domain
            domain_dropdown = WebDriverWait(driver=self.driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/div[3]/div[1]/a')))
            naver_keyword_list = []
            print()
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
                            print(f"Stale element at domain {i}, index {j}")
            naver_sourced_df = pd.DataFrame(naver_keyword_list, columns=['키워드'])
        elif matching_files:
            naver_sourced_df = pd.read_csv('naverSourced.csv')
        return naver_sourced_df

class Uploading:
    def __init__(self, driver, tool=None):
        self.driver = driver
        # self.tool = tool or Tool(driver, uploading=self)
        self.tool = tool

    def sending_store(self, checkboxes_numb, originalTarget, btn_path, store_name, margin):
        print("[+] Wait until the button presence." )
        sending_store_btn = WebDriverWait(driver=self.driver, timeout=30).until(EC.presence_of_element_located(
            (By.XPATH, btn_path)))
        print("[+] Scroll down to the button." )
        ActionChains(self.driver).move_to_element(sending_store_btn).perform()
        # print("[+] Wait until the button visible." )
        # WebDriverWait(driver=self.driver, timeout=30).until(EC.invisibility_of_element(
        #     (By.CSS_SELECTOR, "div.loading_box")))
        print("[+] Wait until the button clickable." )
        WebDriverWait(driver=self.driver, timeout=30).until(EC.element_to_be_clickable(
            (By.XPATH, btn_path)))
        # while True:
        #     try:
        sending_store_btn.click()
            #     break
            # except ElementClickInterceptedException:
            #     message = "[!] Element intercpeted. Move the page and press enter.\n"
            #     self.tool.append_to_text_widget(message, "red")
            #     input("[!] Element intercpeted. Move the page and press enter.")
        print(f" [*] Sending to {store_name} Store button clicked.")
        # Keyword appender
        print(" [*] Appending keyword process start.")
        time.sleep(3)
        parent_element = self.driver.find_element(By.CSS_SELECTOR, f'.{store_name}_modi_layer')
        # Find all input elements within this parent element
        input_elements = parent_element.find_elements(By.CSS_SELECTOR, f'.{store_name}_prd_nm')
        checkboxes_numb = len(input_elements)
        for i in range(checkboxes_numb):
            inputTextbox = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, f"//ul[@class='{store_name}_page_li']/li[{i+1}]/ul/li[2]/input[@class='{store_name}_prd_nm']")))
            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, f"//ul[@class='{store_name}_page_li']/li[{i+1}]/ul/li[2]/input[@class='{store_name}_prd_nm']")))
            ActionChains(self.driver).move_to_element(inputTextbox).click().perform()
            inputTextbox.send_keys(Keys.END)
            inputTextbox.send_keys(" " + originalTarget + " 대용")
        print(" [*] Appending keyword process end.")
        # Price manager
        print(f" [*] Price managing process start.Margin = {margin}%")
        discount_rate_list = []
        optionEditButtons = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, f"//ul[@class='{store_name}_page_li']/li/ul/li/button[@class='{store_name}_option_modi_btn']")))
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, f"//ul[@class='{store_name}_page_li']/li/ul/li/button[@class='{store_name}_option_modi_btn']")))
        print("*option edit button defined")
        retail_prices = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, f"//ul[@class='{store_name}_page_li']/li/ul/li/span[@class='{store_name}_cus_price']")))
        print("Retail input boxes defined")
        wholesale_prices = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, f"//ul[@class='{store_name}_page_li']/li//li[@class='{store_name}_option_price']")))
        print("Wolesale texts defined")
        prd_codes = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, f"//ul[@class='{store_name}_page_li']/li/ul/li[@class='{store_name}_prd_code']")))
        print("Product codes defined")
        done_btns = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, f"//ul[@class='{store_name}_page_li']//button[@class='{store_name}_op_done']")))
        print("Edit done buttons defined")
        edditable_gap = len(wholesale_prices) - len(optionEditButtons)
        checkboxes_numb -= edditable_gap
        for i in range(checkboxes_numb):
            isOptEditable = True
            while isOptEditable:
                # Check for the option edit button presence.
                checker_list = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located(
                    (By.XPATH, f'/html/body/div[3]/section/div/div[2]/ul/li[{i+1}]/ul/li[5]/button')))
                if len(checker_list) > 0:
                    print(f"----------------{i+1}th iteration--------------------")
                    retail_price = int(retail_prices[i].text)
                    print("Retail price defined")
                    wholesale_price = int(wholesale_prices[i].text.replace('원',''))
                    print("Wolesale price defined")
                    if store_name == 'coupang':
                        updated_retail_price = str(round(wholesale_price*(margin*0.01+1),-1))
                        option_edit_btn = optionEditButtons[i]
                        option_edit_btn.click()
                        print("Option edit button clicked")
                        time.sleep(1)
                        # Check if there are more than one option
                        retail_price_inputs = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located(
                            (By.XPATH, f'/html/body/div[3]/section/div/div[3]/ul/li[{i + 1}]/ul/li[3]/div/ul/li/ul/li[2]/input[1]')))
                        if len(retail_price_inputs) == 0:
                            retail_price_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[3]/section/div/div[2]/ul/li[{i + 1}]/ul/li[3]/div/ul/li/ul/li[2]/input[1]')))
                            time.sleep(1)
                            retail_price_input.clear()
                            print("Retail price cleared")
                            time.sleep(1)
                            retail_price_input.send_keys(updated_retail_price)
                            print("Retail price updated")
                            time.sleep(1)                
                        else:
                            prd_code = prd_codes[i].text
                            message = f" [!] {prd_code} has more than one option.\n"
                            self.tool.append_to_text_widget(message, "red")
                            for j in range(len(retail_price_inputs)):
                                retail_price_input = retail_price_inputs[j]
                                time.sleep(1)
                                retail_price_input.clear()
                                print("Retail price cleared")
                                time.sleep(1)
                                retail_price_input.send_keys(updated_retail_price)
                                print("Retail price updated")
                        # Save the discount rate for the pricing
                        discount_rate = round(1 - ((wholesale_price*(margin*0.01+1))/retail_price),2)*100
                        prd_code = prd_codes[i].text
                        discount_rate_list.append((prd_code, discount_rate))
                        done_btns[i].click()
                        print("Done button clicked")
                    elif store_name == 'smart':
                        # Save the discount rate for the pricing
                        discount_rate = round(1 - ((wholesale_price*(margin*0.01+1))/retail_price),2)*100
                        prd_code = prd_codes[i].text
                        discount_rate_list.append((prd_code, discount_rate))
                elif len(checker_list) == 0:
                    isOptEditable = False
                    i += 1
        print(" [*] Price managing process end.")
        print(f" [*] Sending to {store_name} start.")
        sendBtn = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, f"//button[contains(@class, '{store_name}_modi_btn')]")))
        sendBtn.click()
        print(f" [*] Sending to {store_name} start.")
        self.tool.popupHandler(100)
        print(f" [*] Sending to {store_name} end.")
        return discount_rate_list
        # try:
        #     alert = Alert(self.driver)
        #     alert.accept()  # Use alert.dismiss() if you want to cancel the alert
        #     print("[+] Alert closed")
        #     pass
        # except NoAlertPresentException:
        #     print("[+] No JavaScript alert present")

    def keywordCompare(self, preprocessed_df, isDaily, margin):
        if not isDaily:
            csv_name = 'preprocesedSourcedUpdated.csv'
        elif isDaily:
            csv_name = 'naverSourcedUpdated.csv'
        files = os.listdir('/Users/papag/OneDrive/src/Projects/vogueSnack')
        # Check if there is a preprocessedSourcedUpdated.csv
        matching_files = [file for file in files if file.startswith(csv_name)]
        if matching_files:
            preprocessed_df = pd.read_csv(csv_name)
        targetList = preprocessed_df['바꾼키워드'].tolist()
        originalList = preprocessed_df['키워드'].tolist()
        nested_discount_rate_list = []

        for i in range(len(targetList)):
            target = targetList[i]
            originalTarget = originalList[i]
            isSearched = preprocessed_df['isSearched'].iloc[i]

            while not isSearched:
                # Perform Search
                searchTextbox = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="prd_sear_txt"]')))
                searchTextbox.clear()
                ActionChains(self.driver).move_to_element(searchTextbox).click().send_keys(target).perform()
                print(f"[+] keyword typed in successfully: {target}({originalTarget})")
                # time.sleep(5)

                # Click on Search Button
                WebDriverWait(driver=self.driver, timeout=30).until(EC.presence_of_element_located((By.CLASS_NAME, 'search_btn')))
                search_btn = self.driver.find_element(By.CLASS_NAME, 'search_btn')
                search_btn.click()
                print("[+] search button clicked successfully")
                time.sleep(3)
                
                # Check for the existion of products
                try:
                    self.driver.find_element(By.CLASS_NAME, 'product_set')
                    print("[+] Exist. Uploading start.")
                    checkboxes = self.driver.find_elements(By.CLASS_NAME, "checkbox_label")
                    checkboxes_numb = len(checkboxes)
                    if checkboxes_numb < 5:
                        # Automatic checker
                        # for checkbox in checkboxes:
                        #     checkbox.click()
                        # print(" [*] Checkbox clicked successfully")
                        # time.sleep(1)
                        isQuestioned = False
                        while True:
                            try:
                                if not isQuestioned:
                                    isQuestioned = True
                                    checkboxes_numb = int(input(" [*] Type 1 to operate sending function.(0 = pass):"))
                                    break
                                else:
                                    checkboxes_numb = int(input(""))
                            except Exception as e:
                                if 'ERROR:fallback_task_provider.cc(124)' in str(e):
                                    continue
                                else:
                                    message = " [!] Error occur. Try again?(Y/N).\n"
                                    self.tool.append_to_text_widget(message, "red")
                                    isStop = input(" [!] Error occur. Try again?(Y/N).").strip().lower()
                                    if isStop == 'n':
                                        checkboxes_numb = 0
                                        break
                                    else:
                                        isQuestioned = False
                                        continue

                        if checkboxes_numb == 0:
                            print("[+] Sending to Store passed.")
                            preprocessed_df['isSearched'].iloc[i] = True
                            preprocessed_df.to_csv(csv_name, encoding='utf-8-sig' , index = False)
                            break
                        else:
                            smt_btn_path = "//div[@onclick='smartstore_download()']"
                            coup_btn_path = "/html/body/div[3]/section/div/div[1]/div[4]"
                            # coup_btn_path = "//div[@onclick='coupang_download()']"
                            discount_rate_list_empty = self.sending_store(checkboxes_numb, originalTarget, coup_btn_path, 'coupang', margin)
                            discount_rate_list = self.sending_store(checkboxes_numb, originalTarget, smt_btn_path, 'smart', margin)
                            nested_discount_rate_list.append(discount_rate_list)
                            preprocessed_df.to_csv(csv_name, encoding='utf-8-sig' , index = False)
                            break
                    else:
                        # Automatic checker
                        # for checkbox in checkboxes[:5]:
                        #     checkbox.click()
                        # print(" [*] Checkbox clicked successfully")
                        # time.sleep(1)
                        checkboxes_numb = int(input(" [*] Type 1 to operate sending function.(0 = pass):"))
                        if checkboxes_numb == 0:
                            print(" [*] Sending to Store passed.")
                            preprocessed_df['isSearched'].iloc[i] = True
                            preprocessed_df.to_csv(csv_name, encoding='utf-8-sig' , index = False)
                            break
                        else:
                            smt_btn_path = "//div[@onclick='smartstore_download()']"
                            # coup_btn_path = "//div[@onclick='coupang_download()']"
                            coup_btn_path = "/html/body/div[3]/section/div/div[1]/div[4]"
                            discount_rate_list_empty = self.sending_store(checkboxes_numb, originalTarget, coup_btn_path, 'coupang', margin)
                            discount_rate_list = self.sending_store(checkboxes_numb, originalTarget, smt_btn_path, 'smart', margin)
                            nested_discount_rate_list.append(discount_rate_list)
                            preprocessed_df['isSearched'].iloc[i] = True
                            preprocessed_df.to_csv(csv_name, encoding='utf-8-sig' , index = False)
                            break

                except NoSuchElementException:
                    print(" [*] Not exist")
                    preprocessed_df['isSearched'].iloc[i] = True
                    preprocessed_df.to_csv(csv_name, encoding='utf-8-sig' , index = False)
                    break
            flattened_list = [item for sublist in nested_discount_rate_list for item in sublist]
            df = pd.DataFrame(flattened_list, columns=['prd_code', 'discount_rate'])
            if not isDaily:
                df.to_csv('smart_discount_rate.csv', index = False)
            elif isDaily:
                df.to_csv('smart_discount_rate_daily.csv', index = False)
            i += 1
        print("[+] Uploading end.")

class Tool:
    def __init__(self, driver, result_text, sourcing=None, uploading=None):
        self.driver = driver
        self.result_text = result_text
        self.sourcing = sourcing or Sourcing(driver)
        # self.uploading = uploading
        self.uploading = uploading or Uploading(driver)

    def append_to_text_widget(self, message, tag=""):
        # Method to append text to the Text widget in gui.py
        self.result_text.insert(tk.END, message, tag)

    def popupHandler(self, waitTime):
        counter = 0
        while counter < waitTime + 1:
            # Handling JavaScript Alert Pop-Up
            try:
                alert = Alert(self.driver)
                alert_text = alert.text
                print("Alert Text:", alert_text)
                alert.accept()  # Use alert.dismiss() if you want to cancel the alert
                print("Alert closed")
                break
            except NoAlertPresentException:
                time.sleep(1)
                counter += 1
        # Handling Web Page Pop-Up
        # try:
        #     # Assuming the close button has a unique identifier (e.g., ID, class, or XPath)
        #     close_button = self.driver.find_element(By.XPATH, closeBtnXPath)
        #     close_button.click()
        #     print("Web page pop-up closed")
        # except NoSuchElementException:
        #     print("No web page pop-up present")
    
    def priceSetting(self, url, id, pw, store_name, login_btn):
        print("[+] Pricing start.")
        download_path = '/Users/papag/Downloads'
        file_prefix_smart = "스마트스토어상품"
        if store_name == 'smart':
            self.sourcing.login(url,id,pw,'id','pw',login_btn, True)
            # Move to the product list edit page
            self.sourcing.pageNavigator('https://sell.smartstore.naver.com/#/products/origin-list')
            # Click the dropdown and set to '1000개씩'
            dropdown = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.selectize-input.items.ng-valid.has-options.ng-dirty.full.has-items')))
            dropdown.click()
            option = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='seller-content']/ui-view/div[2]/ui-view[2]/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/div/div[5]")))
            option.click()
            # Check the number of uploaded items checkboxes
            all_checlBox = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[2]/div[3]/div/div/div/div/div[1]/div[1]/div/div[1]/div[2]/div/label/input')))
            all_checlBox.click()
            # Download and read the editable xlsx files
            dropdown_xlsx = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[1]/div[2]/div/div/div[3]/div[1]/div')))
            dropdown_xlsx.click()
            correction_form_download = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[1]/div[2]/div/div/div[3]/div[2]/div/div[4]')))
            correction_form_download.click()
            # Read the correction form and Edit
            smart_df = self.sourcing.downloadChecker(download_path, file_prefix_smart)
            smart_discount_rate_df = pd.read_csv('smart_discount_rate.csv', encoding='utf-8')
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
            new_smart_df['PC\n기본 할인 값'].update(new_smart_df['temp_PC_discount'])
            new_smart_df['모바일\n기본할인 값'].update(new_smart_df['temp_mobile_discount'])
                # Drop the temporary columns
            new_smart_df.drop(['temp_PC_discount', 'temp_mobile_discount'], axis=1, inplace=True)
                # Number of rows to replace in 'smart_df' from the 5th row onward
            num_rows_to_replace = len(smart_df) - 4  # Adjust based on how many rows you want to replace
                # Replace values in 'smart_df' from the 5th row with values from 'new_smart_df' from the 1st row
            smart_df.iloc[4:4+num_rows_to_replace] = new_smart_df.iloc[0:num_rows_to_replace].values
            smart_df.to_excel('discountRateSetted.csv', index = False)
            # Upload the discountRateSetted file to the smart store.
            dropdown_xlsx.click()
            correction_form_upload = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="seller-content"]/ui-view/div[2]/ui-view[2]/div[1]/div[1]/div[2]/div/div/div[3]/div[2]/div/div[5]')))
            correction_form_upload.click()
            find_file = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '.btn.btn-single')))
            find_file.click()
            input("[+] Pricing end. If done, press enter.")
        # elif store_name == 'coupang':





