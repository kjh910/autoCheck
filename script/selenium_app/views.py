from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import shutil
import requests
import time
import json
import datetime
from django.shortcuts import redirect, reverse
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import geckodriver_autoinstaller

class TurnOnView(generics.GenericAPIView):

    def get(self, request):
        try:
            shutil.rmtree(r"c:\chrometemp")  #쿠키 / 캐쉬파일 삭제
        except FileNotFoundError:
            pass
        subprocess.Popen(['google-chrome','--remote-debugging-port=9223','--user-data-dir=/root/script/cache','--no-sandbox'])
        # subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9223 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동
        return redirect(reverse('search'))
# Create your views here.
class SearchView(generics.GenericAPIView):

    def get(self, request):
        try:
            shutil.rmtree(r"c:\chrometemp")  #쿠키 / 캐쉬파일 삭제
        except FileNotFoundError:
            pass

        # subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9223 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동
        subprocess.Popen(['google-chrome','--remote-debugging-port=9223','--user-data-dir=/root/script/cache',"--no-sandbox" "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",'--headless'])

        option = Options()
        # option.add_argument("--no-sandbox")
        # option.add_argument("--disable-setuid-sandbox")
        # option.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        option.add_experimental_option("debuggerAddress", "127.0.0.1:9223")

        # geckodriver_autoinstaller.install()
        # chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
        chromedriver_autoinstaller.install()
        # driver = webdriver.Remote(
        #     command_executor='http://selenium-hub:4444/wd/hub',
        #     desired_capabilities=DesiredCapabilities.CHROME)
        driver = webdriver.Chrome(options=option)
        # driver = webdriver.Firefox()

        try:
            # driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
            driver.get('https://jp.louisvuitton.com/jpn-jp/new/for-women/the-latest/_/N-1wl5ky9')
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            dt = datetime.datetime.today()
            dtstr = dt.strftime("%Y%m%d%H%M%S")
            driver.save_screenshot('images/' + dtstr + '.png')
            # className = driver.find_elements_by_class_name('lv-product-card__url')
            # file= open("C:/Users/systemi/Desktop/teste/config/selenium_app/file_name.txt",'r')
            # file.write(className[0].text)
            # file.close()
            # print(className[0].text)
            # className = driver.find_element_by_class_name('lv-stock-indicator').text
            # if className != 'サックプラ BB':
            #     time.sleep(2)
            #     driver.close()
            #     return redirect(reverse('kakao-login'))

            time.sleep(2)
            driver.close()
            return Response({'MESSAGE':'在庫なし'},status=200)
        except Exception as e:
            print('error')
            print(e)
            time.sleep(2)
            driver.close()
            return Response({'MESSAGE':'在庫なし'},status=200)

class KakaoLogin(generics.GenericAPIView):

    def get(self,request):
        client_id = '938935bd8b2079f6a525b60757f1c3ff'  
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback/"
        return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=talk_message,friends")

class KakaoLoginCallback(generics.GenericAPIView):
    def get(self, request):
        code = request.GET.get("code")
        client_id = '938935bd8b2079f6a525b60757f1c3ff'
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback/"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        access_token = token_json.get("access_token")
        print(access_token)
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization" : "Bearer " + access_token
            }
        friend_url = "https://kapi.kakao.com/v1/api/talk/friends"
        # send_url= "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        # post = {
        # "object_type": "text",
        # "text": "テストです",
        # "link": {
        #     "web_url": "https://developers.kakao.com",
        #     "mobile_web_url": "https://developers.kakao.com"
        #     },
        #     "button_title": "바로 확인"
        # }
        # data = {
        #     "template_object" : json.dumps({ "object_type" : "text",
        #                                     "text" : "하나의 첫 카카오톡 메시지입니다.",
        #                                     "link" : {
        #                                                 "web_url" : "www.naver.com"
        #                                             }
        #     })
        # }
        # data = {"template_object": json.dumps(post)}
        # response=requests.post(send_url, headers=headers, data=data)
        # print(response)
        # return Response({'MESSAGE':'SUCCESS'},status=200)
        
        friend_result= requests.get(friend_url, headers=headers).json()
        print(friend_result)
        send_url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
        data={
            'receiver_uuids': '["{}"]'.format(friend_result.get('elements')[0].get("uuid")),
            "template_object": json.dumps({
                "object_type":"text",
                "text":"재고 떴따!!",
                "link":{
                    "web_url":"https://jp.louisvuitton.com/jpn-jp/products/multi-pochette-accessoires-monogram-nvprod1770359v#M44840",
                },
                "button_title": "바로 확인"
            })
        }
        response = requests.post(send_url, headers=headers, data=data)
        return Response({'MESSAGE':'SUCCESS'},status=200)
