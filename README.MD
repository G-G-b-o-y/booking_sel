# 健康驛站搶名額
# 禁止商業用途！！！

所需的包放在 'requirements.txt' 中
你可以使用 'pip install -r requirements.txt' 命令來安裝

請將瀏覽器driver路徑填寫在'booking_login.py' line17中
個人資料填寫在Preson_info.json中，裏面有詳細説明

在 'Person_info.json' 中，存有個人資料信息，均為必填
其中 'time_target' 參數 測試==0 即在按下開始執行按鈕后打開網站，測試模式將無視時間！
其中 'time_target' 參數 運行==目標時間，比如開搶時間為2022-02-25 10:00:00，則填寫時間戳（秒）'1645754400'
關於時間戳計算可參考 'https://tool.lu/timestamp/'


V0.2版本更新詳情:
1.增加了七日全搶功能，提高成功率
2.驗證碼破解功能，無需手動輸入驗證碼