import logging
import time

# __init__.py
# 定义全局常量

# 默认日志保存文件夹路径
__folder_log_default = 'logs'

# 默认日志文件名
__filename_log_default = 'log'

# 默认日志文件扩展名
__file_extension_log_default = 'txt'

# 创建时间戳
__timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())

# 默认日志文件路径
# ./logs/log/log_20230815_123456.txt
file_log_default = f'{__folder_log_default}/{__filename_log_default}_{__timestamp}.{__file_extension_log_default}'

# 日志文件的最大大小 (10 MB)
maxSize_bytes_log_default = 1024 * 1024 * 10

# 日志文件的编码方式
encoding_log_default = 'utf8'

# 日志文件的备份数量
backup_count_log_default = 2

# 日子记录写入模式
mode_log_default = 'a'

# 日志记录的默认级别 (INFO)
level_log_default = logging.INFO

# 日志记录的默认格式
format_log_default = '%(asctime)s - %(levelname)s - %(message)s'

'''
logging 常用内置字段
%(asctime)s：日志记录时间（格式化）
%(levelname)s：日志级别名称
%(message)s：日志消息内容
%(threadName)s：线程名称
%(funcName)s：函数名称
%(module)s：模块名
%(filename)s：文件名
%(lineno)d：行号
'''
