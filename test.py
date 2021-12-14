from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import shutil
import requests
import time

try:
    shutil.rmtree(r"/home/teste/script/cache/")  #쿠키 / 캐쉬파일 삭제
except FileNotFoundError:
    pass

# subprocess.Popen(r'/usr/bin/google-chrome-stable --remote-debugging-port=9223 --user-data-dir="/home/teste/script/cache"') # 디버거 크롬 구동
path = chromedriver_autoinstaller.install()


chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--user-data-dir='/home/teste/script/cache'")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.binary_location='/usr/bin/google-chrome-stable'
chrome_driver_binary = "/usr/bin/chromedriver"
driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)

# option = Options()
# option.add_experimental_option("debuggerAddress", "127.0.0.1:9223")

# chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
# driver = webdriver.Chrome(executable_path=chrome_driver_binary, options=option)
try:
    # driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
    print(2)
    driver.get('https://jp.louisvuitton.com/jpn-jp/products/multi-pochette-accessoires-monogram-nvprod1770359v#M44840')
    # driver.get('https://www.naver.com')
    # time.sleep(2)
    # driver.refresh()
    time.sleep(10)
    driver.save_screenshot("/home/capture.png")
    className =driver.find_elements_by_css_selector('.lv-stock-indicator.-not-available')
    # className = driver.find_element_by_class_name('lv-stock-indicator').text.encode("utf-8")
    print(className)
    # if className == '在庫あり':
    #     client_id = 'a468f795c397c1f6cd93ba2531ae6753'
    #     redirect_uri = "http:///users/login/kakao/callback"
    #     requests = requests.get(f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code")
    #     print(requests)
    time.sleep(2)
    driver.close()
except Exception as e:
    time.sleep(2)
    driver.close()
    # chromedriver_autoinstaller.install(True)
    # driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
# driver.implicitly_wait(10)