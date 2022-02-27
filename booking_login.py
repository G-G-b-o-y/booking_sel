from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from modules.logger import log_creater
from modules.verCode import ddocr
import os
import sys
import time
import json


# 初始化
os.chdir(sys.path[0])  # 防vsc報錯
logg = log_creater()        # 日志
# logg.text_create('Hello world!')
# 修改瀏覽器 Edge
driver = webdriver.Edge(r'msedgedriver.exe')
url = r'https://hk.sz.gov.cn:8118/userPage/login'
driver.get(url)     # 打開指定URL
driver.set_window_size(1920,1080)
# driver.execute_script("document.body.style.zoom='0.66'") #缩小
time.sleep(1)


# 讀取信息      GBK
id_types_list = ["港澳居民來往內地通行證", "臺灣居民來往大陸通行證", "往來港澳通行證", "護照"]
with open('Person_info.json') as f:
    data = json.load(f)

def download_img(img_info):
    # img_info.location       # 得到元素位置
    # img_info.size    # 得到元素大小
    # surface屏幕適配
    left = img_info.location['x']+30
    right = img_info.location['x'] + img_info.size['width']+70
    top = img_info.location['y']+270
    botton = img_info.location['y'] + img_info.size['height']+290
    # Vcode = get_code((left, top, right, botton))        # 識別驗證碼 已棄用
    Vcode = ddocr((left, top, right, botton))
    return Vcode

def login(id_type=None, id_number=None, id_pass=None):
    global Vcode
    driver.find_element(By.ID, 'select_certificate').send_keys(id_type)
    driver.find_element(By.ID, 'input_idCardNo').send_keys(id_number)
    driver.find_element(By.ID, 'input_pwd').send_keys(id_pass)


def input_vcode():
    # input_verifyCode
    try:
        img_src = driver.find_element(By.ID, 'img_verify')
        driver.save_screenshot('Vcode.jpg')     # 截取整個網頁儲存
        Vcode = download_img(img_src)
        driver.find_element(By.ID, 'input_verifyCode').send_keys(Vcode)     # 填寫識別的驗證碼
        # driver.find_element(By.ID, 'btn_login').click()     # 點擊登錄
        # ENTER = '\ue007'   #回車鍵
        driver.find_element(By.ID, 'btn_login').send_keys(Keys.ENTER)  # 按下回車
        # 驗證是否成功，可以檢查的URL是否停留在登錄階段 https://hk.sz.gov.cn:8118/userPage/login
        logg.text_create('當前URL'+ driver.current_url)
        logg.text_create('正在加載所需資源......')
        # 如果URL不在登錄階段
        if driver.current_url != 'https://hk.sz.gov.cn:8118/userPage/login':
            return True     # 登錄成功
        else:
            return False    # 失敗
    except:
        pass

def input_sure_vcode():     # 預約確認
    try :
        img_src = driver.find_element(By.ID, 'img_verify')             # 驗證碼圖片
        driver.save_screenshot('Vcode.jpg')                            # 截取整個網頁儲存
        Vcode = download_img(img_src)                                # 提交OCR
        driver.find_element(By.ID, 'checkCode').send_keys(Vcode)     # 填寫識別出的驗證碼
        # driver.find_element(By.ID, 'btnSubmit').click()              # 點擊提交
        driver.find_element(By.ID, 'btnSubmit').send_keys(Keys.ENTER)  # 按下回車

        # 驗證是否成功，可以檢查的網頁上是否有提交按鈕，如果找不到。。。
        try :
            time.sleep(0.2)
            driver.find_element(By.XPATH, '//*[@id="layui-m-layer13"]/div[2]/div/div/div[2]/span[2]').click()   # 提交確認
            return True     # 登錄成功    找到了提交確認按鈕，説明驗證碼正確
        except:
            pass
            return False   # 失敗
    except:
        pass

def choose_hotel():
    try :  # 嘗試點擊
        driver.find_element(By.ID, 'a_canBookHotel').click()
        return True #
    except :
        return False

def order_down():
    # /html/body/div/div[2]/div/section[7]/div/p/button    # 最新的 +7天
    for days in range(7,0,-1):      # 遍歷每一天，如果按鈕是灰色，則沒有任何反應，將繼續上一天
        try :  # 嘗試預約，遍歷7天，如果成功，將會跳轉至驗證界面。驗證界面找不到該按鈕，因此會抛出異常
            time.sleep(0.2)
            driver.find_element(By.XPATH, '/html/body/div/div[2]/div/section[7]/div/p/button').click()        # 前往驗證頁面
            logg.text_create(str(days) + '-Day try')
        except Exception:        
            # 發生跳轉，找不到預約按鈕，視爲成功
            logg.text_create('Day:'+str(days-1))
            return days-1
            


def close_tip():
    try :  # 嘗試點擊
        driver.find_element(By.XPATH, '//*[@id="winOrderNotice"]/div/div/button').click()        # 關閉通告
        return True
    except :
        return False 

def imsure():
    try :  # 嘗試點擊
        driver.find_element(By.XPATH, '//*[@id="winSueccss"]/div/div/button[2]').click()
        return True #
    except :
        logg.text_create("搜索目標:確定")
        return False

def sure_submit():      # 最後一步
    try :  # 嘗試點擊
        driver.find_element(By.XPATH, '//*[@id="layui-m-layer13"]/div[2]/div/div/div[2]/span[2]').click()
        return True #
    except :
        logg.text_create("搜索目標:提交確定")
        return False
        

# https://tool.lu/timestamp/
# 2022-02-26 10:00:00 == 1645840800s
# 1645927200
# 差 86400s
test = int(time.time()) + 60    # 測試模式

def start():
    last_time = 0       # 存放時間
    try_times = 0       # init
    max_try_times = 1500  # 按鈕最大嘗試次數
    vcode_time = 1.3      # 驗證碼等待時間，越小越快，越大越穩定
    a = True
    # driver.find_element(By.XPATH, '//*[@id="winLoginNotice"]/div/div/button').click()        # 關閉通告
    driver.execute_script("closeLoginHint()")

    login(id_types_list[0], data['Id'], data['Password'])       # 填寫信息

    while not input_vcode():        # 填寫並驗證
        time.sleep(vcode_time)
        try :  # 這裏會出錯，原因未明，使用try函數無視
            driver.find_element(By.ID, 'input_verifyCode').clear()
            driver.find_element(By.XPATH, '//*[@id="img_verify"]').click()    # 切換驗證
        except:
            pass
        if try_times > 3:      # 超時判定
            logg.text_create('驗證碼超時')
            break # 如果嘗試次數大於  次，則跳出循環
        try_times = try_times +1  # 失敗次數
    # logg.text_create('驗證碼正確')
    try_times = 0

    # 10點
    if int(data['time_target']) == '0':
        am10 = test
    elif int(data['time_target']) != '0':
        am10 = int(data['time_target'])
    logg.text_create('target:' + str(am10) )

    # 以下是在登錄后
    while a:
        os.system('cls')
        logg.text_create('time:' + str(am10-time.time()))
        if int(time.time()) >= am10 -1 and try_times == 0:     # 時間到了只能執行一次
            #手動登錄 driver.find_element(By.ID, 'btn_login').click()        # 登錄btn按鈕
            time.sleep(0.2)     # DOM加載時間

            # close_tip()
            try:
                driver.execute_script("closeHint()")
            except:
                pass

            while not choose_hotel():       # 重複執行酒店選擇
                time.sleep(0.1)     # 慢一點嘗試，防止檢測
                if try_times > max_try_times:      # 超時判定
                    pass # 結果失敗
                    logg.text_create('失敗')
                    a = False       # 結束
                    break
                try_times = try_times +1  # 失敗次數
            logg.text_create('進入日期選擇')
            try_times = 0

            order_down()
            logg.text_create('進入酒店選擇/申報')
            
            # 點擊預約后的確認框xpath='//*[@id="winSueccss"]/div/div/button[2]'     # 防疫咨詢。。。
            # imsure()

            while not imsure():       # 重複嘗試執行確認
                if try_times > max_try_times:      # 超時判定
                    break
                try_times = try_times +1  # 失敗次數

            # 確認驗證碼圖片id='img_verify'     同登錄相同
            # 驗證碼輸入框id='checkCode'
            # 提交按鈕id='btnSubmit'
            while not input_sure_vcode():        # 填寫並驗證提交
                time.sleep(vcode_time)
                try :  # 這裏會出錯，原因未明，使用try函數無視
                    # 這裏缺少一個驗證碼切換的元素
                    # 用'//*[@id="img_verify'嘗試
                    driver.find_element(By.ID, 'checkCode').clear()
                    driver.find_element(By.XPATH, '//*[@id="img_verify').click()    # 切換驗證碼
                except:
                    logg.text_create("找不到目標:驗證碼")
                    pass
                
                if try_times > max_try_times:      # 超時判定
                    logg.text_create('驗證碼超時')
                    break # 如果嘗試次數大於  次，則跳出循環
                try_times = try_times +1  # 失敗次數

            # try_times = 0

            time.sleep(0.2)     # DOM
            # 提交確認按鈕xpath='//*[@id="layui-m-layer13"]/div[2]/div/div/div[2]/span[2]'
            sure_submit()

            # logg.text_create('成功')
            a = False       # 結束
            pass
        
        # done
        else: #
            if last_time != int(time.time()):
                last_time = int(time.time())
                logg.text_create('TIME:' + str(int(am10-time.time())) +'即將開始')

start()
logg.close_log()
