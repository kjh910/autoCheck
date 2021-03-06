from rest_framework.response import Response
from rest_framework import generics
from selenium import webdriver
import subprocess
import shutil
import requests
import time
import json
from django.shortcuts import redirect, reverse
from selenium.webdriver import FirefoxOptions
from django.conf import settings
import logging
import smtplib

from email.mime.text import MIMEText

logger = logging.getLogger('myAppDebug')

class TurnOnView(generics.GenericAPIView):

    def get(self, request):
        try:
            shutil.rmtree(r"c:\chrometemp")  #쿠키 / 캐쉬파일 삭제
        except FileNotFoundError:
            pass
        subprocess.Popen(['google-chrome','--remote-debugging-port=9224','--user-data-dir=/root/script/cache','--no-sandbox'])
        # subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9223 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동
        return redirect(reverse('search'))
# Create your views here.
class SearchView(generics.GenericAPIView):

    def get(self, request):
        try:
            shutil.rmtree(r"/app/cache")  #쿠키 / 캐쉬파일 삭제
        except FileNotFoundError:
            pass

        opts = FirefoxOptions()
        opts.add_argument("--headless")
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        opts.add_argument('--disable-gpu')
        opts.add_argument("--disable-notifications")
        opts.add_argument("--remote-debugging-port=9224")
        opts.add_argument("--user-data-dir=/app/cache")
        opts.set_headless(headless=True)
        opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
        driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver',firefox_options=opts)

        try:
            logger.debug(2)
            print(2)
            search_url = "https://jp.louisvuitton.com/jpn-jp/products/papillon-bb-bicolor-monogram-empreinte-leather-nvprod3400010v#M45980"
            logger.debug(search_url)
            logger.debug(settings.BASE_DIR)
            driver.get(search_url)
            time.sleep(10)
            driver.save_screenshot("/app/capture.png")
            able_class_name = driver.find_elements_by_css_selector('.lv-stock-indicator.-available')
            not_able_class_Name = driver.find_elements_by_css_selector('.lv-stock-indicator.-not-available')
            
            logger.debug(len(able_class_name))
            logger.debug(len(not_able_class_Name))
            if len(able_class_name) != 0 and len(not_able_class_Name) == 0:
                logger.debug(able_class_name)
                time.sleep(1)
                driver.close()
                logger.debug(1)
                
                return redirect(reverse('send-email'))
            else:
                time.sleep(1)
                driver.close()
                return Response({'MESSAGE':'在庫なし','able_class_name':able_class_name,'not_able_class_Name':not_able_class_Name},status=200)
            
        except Exception as e:
            print('error')
            print(e)
            logger.debug(e)
            time.sleep(2)
            driver.close()
            return Response({'MESSAGE':search_url},status=200)

class SendEmail(generics.GenericAPIView):
    
    def get(self, request):
        s = smtplib.SMTP(settings.SMTP, settings.SMTP_PORT)
        
        s.starttls()
        s.login(settings.FROM_EMAIL, settings.APP_PASSWORD)
        
        body = """
            링크 : {}
            내용 : 재고떴따!! 확인 꼬!!
        """.format(settings.SEARCH_URI)
        msg = MIMEText(body)
        msg['Subject'] = '제목 : 재고 떴따!!!'

        s.sendmail(settings.FROM_EMAIL, settings.TO_EMAIL, msg.as_string())
        s.sendmail(settings.FROM_EMAIL, settings.FROM_EMAIL, msg.as_string())

        s.quit()
        return Response({'MESSAGE':'SEND_MAIL_SUCCESS'},status=200)
        
class KakaoLogin(generics.GenericAPIView):

    def get(self,request):
        client_id = settings.CLIENT_ID
        redirect_uri = settings.REDIRECT_URI
        return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=talk_message,friends")

class KakaoLoginCallback(generics.GenericAPIView):
    def get(self, request):
        code = request.GET.get("code")
        search_url = settings.SEARCH_URI
        client_id = settings.CLIENT_ID
        redirect_uri = settings.REDIRECT_URI
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
        import logging
        logger = logging.getLogger('myAppDebug')
        
        friend_result= requests.get(friend_url, headers=headers).json()
        uuidsData = {"receiver_uuids": '["{}"]'.format(friend_result.get('elements')[0].get("uuid"))}
        logger.debug(uuidsData)
        print(friend_result)
        send_url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
        # post = {
        #     "object_type": "text",
        #     "text": "재고 떴따!!",
        #     "link": {
        #         "web_url": search_url,
        #         "mobile_web_url": search_url
        #     },
        #     "button_title": "바로 확인"
        # }
        
        # data = {'template_object': json.dumps(post)}
        # uuidsData.update(data)
        data={
            "receiver_uuids": '["{}"]'.format(friend_result.get('elements')[0].get("uuid")),
            "template_object": json.dumps({
                "object_type":"text",
                "text":"재고 떴따!!",
                "link":{
                    # "web_url":search_url,
                    "mobile_web_url": search_url
                },
                "button_title": "바로 확인"
            })
        }
        logger.debug(data)
        response = requests.post(send_url, headers=headers, data=data)
        return Response({'MESSAGE':'KAKAO_SEND_SUCCESS'},status=200)
