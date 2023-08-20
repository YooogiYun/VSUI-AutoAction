import time

import YAutoFramework

# \\VSUI-AutoAction\YAutoFramework\Dataout\
root_folder_screenshot = YAutoFramework.dataout_folder  # 截图文件夹根目录
_time_stamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())  # 时间戳
screenshot_name_default = 'screenshot'  # 默认的截图文件名
screenshot_extension_default = '.png'  # 默认的截图文件扩展名

# print(YAutoFramework.datain_folder)
# print(os.path.exists(YAutoFramework.datain_folder))
