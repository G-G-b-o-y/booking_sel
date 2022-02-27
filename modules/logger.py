import os
import sys
import time

os.chdir(sys.path[0])  # 防vsc報錯


class log_creater:
    def __init__(self) -> None:
        self.log_path = r"D:/code/booking_sel/logs/" + time.strftime("%m%d %H%M%S")
        self.path =  self.log_path + '.txt'
        self.file = open(self.path, 'w')

    def text_create(self, msg):
        info_log = '['+time.strftime("%H:%M:%S")+']'+msg
        self.file.write(info_log+'\n')
        # self.file.write('\n')
        print(info_log)

    def close_log(self):
        self.file.close()
