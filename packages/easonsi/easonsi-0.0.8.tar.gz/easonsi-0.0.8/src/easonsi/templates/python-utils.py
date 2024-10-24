#%%
import time

#%% logging
import logging

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.DEBUG,
    filename=f'log/{time.strftime("%Y%m%d-%H:%M:%S", time.localtime())}.log',
)
logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

#%% argparse
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--dataname", type=str, choices=['semeval', 'meituan'], default='semeval',
                    help="semeval, meituan")
parser.add_argument("--train", default=None, action='store_true',
                    help="train or just get output")
args = parser.parse_args()

#%% time
localtime = time.localtime(time.time())     # 将秒数转化为 struct_time
print(time.asctime(time.time()))            # 将 struct_time 转为字符串

# 格式化成2016-03-20 11:45:39形式
time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
# 格式化成Sat Mar 28 22:24:24 2016形式
time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()) 
# 将格式字符串转换为时间戳
a = "Sat Mar 28 22:24:24 2016"
time.mktime(time.strptime(a,"%a %b %d %H:%M:%S %Y"))