import time
import schedule
import queue
import threading
import pandas as pd
import dateutil.relativedelta
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.edge.options import Options as EdgeOptions
from vogueSnack import Sourcing, Uploading, Tool
import os

# -------------------------------------------------
# 환경 설정 (GUI에서 입력받던 값을 스크립트에서 직접 지정)
# -------------------------------------------------
SELLHA_ID = os.getenv('SELLHA_ID')
SELLHA_PW = os.getenv('SELLHA_PW')
ONCHAN_ID = os.getenv('ONCHAN_ID')
ONCHAN_PW = os.getenv('ONCHAN_PW')
SMART_ID = os.getenv('SMART_ID')
SMART_PW = os.getenv('SMART_PW')
COUPANG_ID = os.getenv('COUPANG_ID')
COUPANG_PW = os.getenv('COUPANG_PW')

NET_PROFIT_RATIO = 5            # net_profit_ratio_var
MIN_RATING = 3.5                # min_rating_var
PRD_MAX_NUM = 10                # prd_max_num_var
MIN_SEARCHED_NUM = 10000        # min_searched_num_var
SOURCING_SIZE = 100000          # sourcing_size_var
PRD_MIN_PRICE = 15000           # prd_min_price_var

# 배송비 유무 설정
DELIVERY_CHARGE_COUPANG = False # delivery_charge_var_coupang
DELIVERY_CHARGE_SMART = True    # delivery_charge_var_smart
MARGIN_DESCEND = False          # margin_descend_var

# -------------------------------------------------
# URL 등 고정 값들
# -------------------------------------------------
URL_SELLHA_LOGIN = "https://sellha.kr/member/login"
URL_SELLHA_DISCOVER = "https://sellha.kr/discover"
URL_ONCHAN_LOGIN = "https://www.onch3.co.kr/login/login_web.php"
URL_ONCHAN_DB = "https://www.onch3.co.kr/dbcenter_renewal/index.php"
URL_SMARTSTORE_LOGIN = "https://accounts.commerce.naver.com/login?url=https%3A%2F%2Fsell.smartstore.naver.com%2F%23%2Flogin-callback"
URL_COUPANG_LOGIN = "https://xauth.coupang.com/auth/realms/seller/protocol/openid-connect/auth?response_type=code&client_id=wing&redirect_uri=https%3A%2F%2Fwing.coupang.com%2Fsso%2Flogin?returnUrl%3D%252F&state=456c3cf5-a6dd-4f52-abe4-cd3364bad4e4&login=true&scope=openid"
COUPANG_RETURN_MGMT_URL = "https://wing.coupang.com/tenants/sfl-portal/return-delivery/list"
COUPANG_PRD_LIST_URL = "https://wing.coupang.com/vendor-inventory/list?searchIds=&startTime=2000-01-01&endTime=2099-12-31&productName=&brandName=&manufacturerName=&productType=&autoPricingStatus=ALL&dateType=productRegistrationDate&dateRangeShowStyle=true&dateRange=all&saleEndDatePeriodType=&includeUsedProduct=&deleteType=false&deliveryMethod=&shippingType=&shipping=&otherType=&productStatus=SAVED,WAIT_FOR_SALE,VALID,SOLD_OUT,INVALID,END_FOR_SALE,APPROVING,IN_REVIEW,DENIED,PARTIAL_APPROVED,APPROVED,ALL&advanceConditionShow=false&displayCategoryCodes=&currentMenuCode=&rocketMerchantVersion=&registrationType=&upBundling=ALL&hasUpBundlingItem=&hasBadImage=false&page=1&countPerPage=50&sortField=vendorInventoryId&desc=true&fromListV2=true&locale=ko_KR&vendorItemViolationType=&coupangAttributeOptimized=FALSE&autoPricingActive="
URL_NAVER_DATALAB = "https://datalab.naver.com/"
ONCHAN_PRD_STAT_URL = "https://www.onch3.co.kr/admin_mem_clo_list_2.php?ost=&sec=&ol=&npage="
ONCHAN_PRD_STAT_URL2 = "https://www.onch3.co.kr/admin_mem_sold_list.html"
ONCHAN_ORDER_STAT_COUPANG_URL = "https://www.onch3.co.kr/admin_api_order.html?api_name=coupang"
ONCHAN_ORDER_STAT_SMART_URL = "https://www.onch3.co.kr/admin_api_order.html?api_name=smartstore"
ONCHAN_PRD_LIST_URL = "https://www.onch3.co.kr/admin_mem_prd_list.html"
ONCHAN_SMART_PRD_MANAGEMENT_URL = "https://www.onch3.co.kr/admin_smart_manage.html#"
ONCHAN_COUPANG_PRD_MANAGEMENT_URL = "https://www.onch3.co.kr/admin_coupang_manage.html"
ONCHAN_MY_PRD_LIST_URL = "https://www.onch3.co.kr/admin_mem_prd.html"
COUPANG_CATALOG_MATCHING_URL = "https://wing.coupang.com/tenants/seller-web/post-matching/page/inventory-list"

# 기타 셀렉터
LOGINBTN_SELLHA = '.sc-iAEyYk.loQZmZ'
LOGINBTN_ONCHAN_XPATH = '//button[@name = "login"]'
LOGINBTN_SMART = 'ul.panel_wrap li.panel_item .panel_inner .btn_login_wrap .btn_login'
LOGINBTN_COUPANG = '.cp-loginpage__form__submit'

BASE_PATH = '/Users/papag/OneDrive/desktop/vogueSnack'
DOWNLOAD_PATH = '/Users/papag/Downloads'
FILE_PREFIX_ALL = "셀하 아이템 발굴 EXCEL_전체"
FILE_PREFIX_EDITABLE = "스마트스토어상품"
CLOSEBTN_XPATH = '//*[@id="ch-shadow-root-wrapper"]/article/div/div/div[2]/button'

# -------------------------------------------------
# 전역 객체 (WebDriver, Tool, Sourcing, Uploading)
# -------------------------------------------------
driver = None
EdgeTool = None
EdgeSourcing = None
EdgeUploading = None

# 탭(윈도우 핸들) 보관용
window_smart = None
window_coupang = None
window_onchan = None
window_sellha = None
window_empty = None

# 로그인 상태
isLoggedin_smart = False
isLoggedin_coupang = False
isLoggedin_onchan = False
isloggedin_sellha = False

# -------------------------------------------------
# WebDriver 초기화
# -------------------------------------------------
def initialize_webdriver():
    global driver, EdgeSourcing, EdgeUploading, EdgeTool
    
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument('--log-level=3')  # 불필요한 로그 최소화
    
    driver = webdriver.Edge(options=options)
    driver.maximize_window()
    
    # vogueSnack 라이브러리의 Tool, Sourcing, Uploading 객체 생성
    EdgeTool = Tool(driver, None)  # GUI의 result_text 자리에 None
    EdgeSourcing = Sourcing(driver, tool=EdgeTool)
    EdgeUploading = Uploading(driver, tool=EdgeTool)
    
    print("[+] WebDriver Initialized")

# -------------------------------------------------
# 탭 오픈 & 로그인
# -------------------------------------------------
def open_tabs():
    """
    스마트스토어, 쿠팡, 온찬, 셀하 탭을 오픈하고, 각각 로그인 상태를 확인한다.
    """
    global isLoggedin_smart, isLoggedin_coupang, isLoggedin_onchan, isloggedin_sellha
    global window_smart, window_coupang, window_onchan, window_sellha, window_empty
    
    # 먼저 스마트스토어(현재 탭)에서 로그인
    driver.get(SMART_ID)  # 실수로 URL 대신 SMART_ID 를 넣지 않도록 주의!
    driver.get(URL_SMARTSTORE_LOGIN)
    isLoggedin_smart = EdgeSourcing.login('smart',
                                          URL_SMARTSTORE_LOGIN,
                                          SMART_ID,
                                          SMART_PW,
                                          'id', 'pw', 
                                          LOGINBTN_SMART, 
                                          authPhase=True)
    
    # 새 탭 4개 생성 (coupang, onchan, sellha, 빈 탭)
    for _ in range(4):
        driver.execute_script("window.open('about:blank', '_blank');")
        time.sleep(1)
        
    windows = driver.window_handles
    window_smart = windows[0]   # 첫 번째 탭
    window_coupang = windows[1] # 두 번째 탭
    window_onchan = windows[2]  # 세 번째 탭
    window_sellha = windows[3]  # 네 번째 탭
    window_empty = windows[4]   # 다섯 번째 탭
    
    # 쿠팡 탭 로그인
    driver.switch_to.window(window_coupang)
    driver.get(URL_COUPANG_LOGIN)
    isLoggedin_coupang = EdgeSourcing.login('coupang',
                                            URL_COUPANG_LOGIN,
                                            COUPANG_ID,
                                            COUPANG_PW,
                                            'username', 'password',
                                            LOGINBTN_COUPANG,
                                            authPhase=False)
    
    # 온찬 탭 로그인
    driver.switch_to.window(window_onchan)
    driver.get(URL_ONCHAN_LOGIN)
    isLoggedin_onchan = EdgeSourcing.login('onchan',
                                           URL_ONCHAN_LOGIN,
                                           ONCHAN_ID,
                                           ONCHAN_PW,
                                           'username','password',
                                           LOGINBTN_ONCHAN_XPATH,
                                           False)
    
    # 셀하 탭 로그인
    driver.switch_to.window(window_sellha)
    driver.get(URL_SELLHA_LOGIN)
    isloggedin_sellha = EdgeSourcing.login('sellha',
                                           URL_SELLHA_LOGIN,
                                           SELLHA_ID,
                                           SELLHA_PW,
                                           'email', 'password',
                                           LOGINBTN_SELLHA,
                                           False)
    print("[+] Open tab successful")

# -------------------------------------------------
# 이하부턴 원본 함수 구조를 유지하되, 
# GUI 관련(Entry 값, Text 위젯) 코드 삭제/수정 -> 스크립트용으로 변환
# -------------------------------------------------

def sourcing_action():
    """
    월 단위로 셀하 데이터를 받아서 sourced.csv를 생성한다.
    """
    print("[+] Sourcing phase start.")
    global isloggedin_sellha
    
    min_searched_num = MIN_SEARCHED_NUM
    sourcing_size = SOURCING_SIZE
    
    current_date = datetime.now()
    before_date = current_date - dateutil.relativedelta.relativedelta(years=1) + \
                                  dateutil.relativedelta.relativedelta(months=1)
    current_formatted_date = f"{current_date.year}-{current_date.month}"
    before_formatted_date = f"{before_date.year}-{before_date.month}"
    
    # 파일 다운로드 체크
    isDownloaded_sellha_df_current = EdgeSourcing.downloadChecker(
        DOWNLOAD_PATH,
        f"셀하 아이템 발굴 EXCEL_전체_{current_formatted_date}",
        first_phase=True
    )
    isDownloaded_sourced = EdgeSourcing.downloadChecker(
        BASE_PATH,
        "sourced.csv",
        first_phase=True
    )
    
    while True:
        try:
            # 셀하 탭으로 전환
            driver.switch_to.window(window_sellha)
            
            if not isDownloaded_sellha_df_current:
                # 로그인 안 되어 있으면 로그인
                if not isloggedin_sellha:
                    EdgeSourcing.login('sellha',
                                       URL_SELLHA_LOGIN,
                                       SELLHA_ID,
                                       SELLHA_PW,
                                       'email', 'password',
                                       LOGINBTN_SELLHA,
                                       False)
                    EdgeTool.popupHandler(5, 'sellha')
                
                EdgeTool.popupHandler(5, 'sellha')
                EdgeSourcing.pageNavigator(URL_SELLHA_DISCOVER)
                time.sleep(0.5)
                EdgeSourcing.categoryButtonClicker(1)  # All
                time.sleep(0.5)
                EdgeSourcing.csvButtonClicker(True)
                time.sleep(0.5)
                
                sellha_df_current = EdgeSourcing.downloadChecker(
                    DOWNLOAD_PATH,
                    f"셀하 아이템 발굴 EXCEL_전체_{current_formatted_date}",
                    first_phase=False
                )
                sellha_df_before = EdgeSourcing.downloadChecker(
                    DOWNLOAD_PATH,
                    f"셀하 아이템 발굴 EXCEL_전체_{before_formatted_date}",
                    first_phase=False
                )
                
                # 전처리
                sellha_df_current_preProcessed = EdgeSourcing.preProcessor(
                    sellha_df_current,
                    min_searched_num,
                    sourcing_size
                )
                sellha_df_before_preProcessed = EdgeSourcing.preProcessor(
                    sellha_df_before,
                    min_searched_num,
                    sourcing_size
                )
                merged_df = pd.concat([sellha_df_current_preProcessed,
                                       sellha_df_before_preProcessed],
                                      axis=0)
                merged_df.to_csv('sourced.csv', encoding='utf-8-sig', index=False)
                
                # targetListMaker
                EdgeSourcing.targetListMaker(pd.read_csv('sourced.csv', encoding='utf-8-sig'), False)
                break
            
            else:
                # 이미 다운로드 되었다면 sourced.csv 체크
                if isDownloaded_sourced:
                    EdgeSourcing.targetListMaker(pd.read_csv('sourced.csv', encoding='utf-8-sig'), isDaily=False)
                    break
                else:
                    sellha_df_current = EdgeSourcing.downloadChecker(
                        DOWNLOAD_PATH,
                        f"셀하 아이템 발굴 EXCEL_전체_{current_formatted_date}",
                        first_phase=False
                    )
                    sellha_df_before = EdgeSourcing.downloadChecker(
                        DOWNLOAD_PATH,
                        f"셀하 아이템 발굴 EXCEL_전체_{before_formatted_date}",
                        first_phase=False
                    )
                    sellha_df_current_preProcessed = EdgeSourcing.preProcessor(
                        sellha_df_current,
                        min_searched_num,
                        sourcing_size
                    )
                    sellha_df_before_preProcessed = EdgeSourcing.preProcessor(
                        sellha_df_before,
                        min_searched_num,
                        sourcing_size
                    )
                    merged_df = pd.concat([sellha_df_current_preProcessed,
                                           sellha_df_before_preProcessed],
                                          axis=0)
                    merged_df.to_csv('sourced.csv', encoding='utf-8-sig', index=False)
                    EdgeSourcing.targetListMaker(pd.read_csv('sourced.csv', encoding='utf-8-sig'), isDaily=False)
                    break
        
        except ElementClickInterceptedException:
            print("[!] Element intercepted. Scroll down the page.")
            EdgeTool.scroll_downer(250)
    
    print("[+] Sourcing phase end.")

def uploading_action():
    """
    sourcing_action() 후, 전처리된 CSV 기반으로 업로드를 진행한다.
    """
    print("[+] Uploading phase start.")
    
    min_rating = MIN_RATING
    prd_max_num = PRD_MAX_NUM
    net_profit_ratio = NET_PROFIT_RATIO
    min_price = PRD_MIN_PRICE
    
    # 로그인 상태 확인
    isLoggedin_onchan, isLoggedin_coupang = EdgeTool.login_checker(
        window_onchan, URL_ONCHAN_LOGIN,
        window_coupang, URL_COUPANG_LOGIN
    )
    
    # 온찬 탭
    driver.switch_to.window(window_onchan)
    while True:
        try:
            # 로그인 안 되어 있으면 로그인
            if not isLoggedin_onchan:
                EdgeSourcing.login('onchan',
                                   URL_ONCHAN_LOGIN,
                                   ONCHAN_ID,
                                   ONCHAN_PW,
                                   'username','password',
                                   LOGINBTN_ONCHAN_XPATH,
                                   False)
            EdgeTool.popupHandler(3, 'onchan')
            
            preprocesedSourced_df = pd.read_csv('preprocesedSourced.csv', encoding='utf-8-sig')
            EdgeUploading.keywordCompare(
                preprocesedSourced_df,
                net_profit_ratio,
                min_rating,
                prd_max_num,
                min_price,
                isDaily=False,
                discount_rate_calculation=False,
                isDeliveryCharge_coupang=DELIVERY_CHARGE_COUPANG,
                isDeliveryCharge_smart=DELIVERY_CHARGE_SMART,
                is_margin_descend=MARGIN_DESCEND
            )
            break
        
        except ElementClickInterceptedException:
            print("[!] Element intercepted while uploading. Scroll down the page.")
            EdgeTool.scroll_downer(250)
    
    print("[+] Uploading phase end.")

def monthly_sourcing_uploading_action():
    """
    월 단위 소싱 & 업로드를 순차 실행.
    """
    print("[+] Monthly phase start.")
    sourcing_action()
    uploading_action()
    
    # 쿠팡 배송비 변경 등
    isLoggedin_onchan, isLoggedin_coupang = EdgeTool.login_checker(
        window_onchan, URL_ONCHAN_LOGIN,
        window_coupang, URL_COUPANG_LOGIN
    )
    if not isLoggedin_coupang:
        driver.switch_to.window(window_coupang)
        EdgeSourcing.login('coupang',
                           URL_COUPANG_LOGIN,
                           COUPANG_ID,
                           COUPANG_PW,
                           'username','password',
                           LOGINBTN_COUPANG,
                           authPhase=False)
    
    driver.switch_to.window(window_coupang)
    EdgeTool.delivery_charge_changer(
        'coupang',
        COUPANG_PRD_LIST_URL,
        isDeliveryCharge=DELIVERY_CHARGE_COUPANG
    )
    
    # 네이버(스마트스토어) 중복상품 제거
    naver_duplicate_handling_action()
    
    print("[+] Monthly phase end.")
    EdgeTool.dummy_deleter(BASE_PATH, 'preprocesedSourcedUpdated')

def daily_sourcing_uploading_action():
    """
    매일 네이버 데이터(랭킹/조회수 등) 기반 소싱 후 업로드.
    """
    print("[+] Daily sourcing & uploading start.")
    
    net_profit_ratio = NET_PROFIT_RATIO
    min_rating = MIN_RATING
    prd_max_num = PRD_MAX_NUM
    min_price = PRD_MIN_PRICE
    
    # 로그인 확인
    isLoggedin_onchan, isLoggedin_coupang = EdgeTool.login_checker(
        window_onchan, URL_ONCHAN_LOGIN,
        window_coupang, URL_COUPANG_LOGIN
    )
    if not isLoggedin_onchan:
        driver.switch_to.window(window_onchan)
        EdgeSourcing.login('onchan',
                           URL_ONCHAN_LOGIN,
                           ONCHAN_ID,
                           ONCHAN_PW,
                           'username','password',
                           LOGINBTN_ONCHAN_XPATH,
                           False)
    if not isLoggedin_coupang:
        driver.switch_to.window(window_coupang)
        EdgeSourcing.login('coupang',
                           URL_COUPANG_LOGIN,
                           COUPANG_ID,
                           COUPANG_PW,
                           'username','password',
                           LOGINBTN_COUPANG,
                           authPhase=False)
    
    while True:
        try:
            driver.switch_to.window(window_empty)
            naver_sourced_df = EdgeSourcing.daily_sourcing(BASE_PATH)
            naver_sourced_isEdited_df = EdgeSourcing.targetListMaker(naver_sourced_df, isDaily=True)
            
            # 온찬으로 이동 후 업로드
            driver.switch_to.window(window_onchan)
            EdgeUploading.keywordCompare(
                naver_sourced_isEdited_df,
                net_profit_ratio,
                min_rating,
                prd_max_num,
                min_price,
                isDaily=True,
                discount_rate_calculation=False,
                isDeliveryCharge_coupang=DELIVERY_CHARGE_COUPANG,
                isDeliveryCharge_smart=DELIVERY_CHARGE_SMART,
                is_margin_descend=MARGIN_DESCEND
            )
            
            # 쿠팡 배송비 변경, 네이버 중복 처리
            driver.switch_to.window(window_coupang)
            EdgeTool.delivery_charge_changer(
                'coupang',
                COUPANG_PRD_LIST_URL,
                isDeliveryCharge=DELIVERY_CHARGE_COUPANG
            )
            naver_duplicate_handling_action()
            break
        
        except ElementClickInterceptedException:
            print("[!] Element intercepted while daily sourcing. Scroll down the page.")
            EdgeTool.scroll_downer(250)
    
    print("[+] Daily sourcing & uploading successfully end.")
    EdgeTool.dummy_deleter(BASE_PATH, 'preprocesednaverSourcedUpdated')
    EdgeTool.dummy_deleter(BASE_PATH, 'naverSourced')
    EdgeTool.dummy_deleter(BASE_PATH, 'preprocessedNaverSourced')


# 이하 함수들도 동일한 로직. GUI 레이블·Entry·버튼 대신 print/logging 사용.
# 필요시 호출해서 쓰면 됨.
def discount_rate_pricing_action():
    print("[+] Discount rate pricing start.")
    while True:
        try:
            EdgeTool.discountRateSetting('smart')
            break
        except ElementClickInterceptedException:
            print("[!] Element intercepted. Scroll down the page.")
            EdgeTool.scroll_downer(250)
    print("[+] Discount rate pricing end.")

def prd_stat_checking_action():
    print("[+] Product stat checking start.")
    isLoggedin_onchan, isLoggedin_coupang = EdgeTool.login_checker(
        window_onchan, URL_ONCHAN_LOGIN,
        window_coupang, URL_COUPANG_LOGIN
    )
    if not isLoggedin_onchan:
        driver.switch_to.window(window_onchan)
        EdgeSourcing.login('onchan',
                           URL_ONCHAN_LOGIN,
                           ONCHAN_ID,
                           ONCHAN_PW,
                           'username','password',
                           LOGINBTN_ONCHAN_XPATH,
                           False)
    if not isLoggedin_coupang:
        driver.switch_to.window(window_coupang)
        EdgeSourcing.login('coupang',
                           URL_COUPANG_LOGIN,
                           COUPANG_ID,
                           COUPANG_PW,
                           'username','password',
                           LOGINBTN_COUPANG,
                           authPhase=False)
    # 이하 동일...
    print("[+] Product stat checking end.")

def gathering_order_action():
    print("[+] Order gathering process start.")
    isLoggedin_onchan, isLoggedin_coupang = EdgeTool.login_checker(
        window_onchan, URL_ONCHAN_LOGIN,
        window_coupang, URL_COUPANG_LOGIN
    )
    # ...
    print("[+] Order gathering process end.")

def prd_filtering_action():
    print("[+] Product filtering start.")
    isLoggedin_onchan, isLoggedin_coupang = EdgeTool.login_checker(
        window_onchan, URL_ONCHAN_LOGIN,
        window_coupang, URL_COUPANG_LOGIN
    )
    # ...
    print("[+] Product filtering end.")

def prd_exsition_comparing_action():
    print("[+] Product existion comparing start.")
    # ...
    print("[+] Product existion comparing end.")

def return_manager_action():
    print("[+] Return management start.")
    # ...
    print("[+] Return management end.")

def naver_duplicate_handling_action():
    print("[+] Naver duplicate handling start.")
    # ...
    print("[+] Naver duplicate handling end.")

def delivery_charge_changer_action():
    print("[+] Delivery charge changer start.")
    # ...
    print("[+] Delivery charge changer end.")

def out_of_stock_finisher_action():
    print("[+] Out of stock finisher start.")
    # ...
    print("[+] Out of stock finisher end.")

def catalog_matching_action():
    print("[+] Catalog matching start.")
    # ...
    print("[+] Catalog matching end.")

# -------------------------------------------------
# 스케줄러 / 태스크 큐 (선택적으로 사용)
# -------------------------------------------------
task_queue = queue.Queue()

def run_scheduled_jobs():
    while True:
        schedule.run_pending()
        time.sleep(1)

def task_worker():
    while True:
        task = task_queue.get()
        try:
            task()
        except Exception as e:
            print(f"[!] Task worker error: {e}")
        finally:
            task_queue.task_done()

def enqueue_task(task):
    task_queue.put(task)

def schedule_actions():
    """
    예: 매일/매월 특정 시각에 함수 실행 등의 자동화를 원한다면 사용.
    """
    # 아래는 예시이므로 실제 시간에 맞게 수정 가능
    schedule.every().day.at("10:00").do(lambda: enqueue_task(daily_sourcing_uploading_action))
    schedule.every().day.at("00:30").do(lambda: enqueue_task(prd_stat_checking_action))

# -------------------------------------------------
# 메인 실행부 (예시)
# -------------------------------------------------
def main():
    # 1. 드라이버 초기화
    initialize_webdriver()
    # 2. 탭 오픈 & 로그인
    open_tabs()
    
    # 3. 원하는 작업 순서대로 수행 (필요시 주석 해제)
    # monthly_sourcing_uploading_action()
    # daily_sourcing_uploading_action()
    # discount_rate_pricing_action()
    # prd_stat_checking_action()
    # prd_filtering_action()
    # gathering_order_action()
    # return_manager_action()
    # naver_duplicate_handling_action()
    # delivery_charge_changer_action()
    # out_of_stock_finisher_action()
    # catalog_matching_action()
    
    # 4. (선택) 스케줄 기반 동작
    # schedule_actions()
    # 스케줄 쓰레드, 태스크 쓰레드 동작
    # scheduler_thread = threading.Thread(target=run_scheduled_jobs, daemon=True)
    # scheduler_thread.start()
    # worker_thread = threading.Thread(target=task_worker, daemon=True)
    # worker_thread.start()
    
    # -- 여기서는 간단히 대기 후 종료
    # input("Press Enter to quit...")  # 필요시 사용
    driver.quit()
    print("[+] Script finished.")

if __name__ == "__main__":
    main()
