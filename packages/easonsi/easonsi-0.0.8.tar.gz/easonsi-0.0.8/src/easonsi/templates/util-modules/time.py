import time

localtime = time.localtime(time.time())     # 将秒数转化为 struct_time
print(time.asctime(time.time()))            # 将 struct_time 转为字符串

# 格式化成2016-03-20 11:45:39形式
time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
# 格式化成Sat Mar 28 22:24:24 2016形式
time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()) 
# 将格式字符串转换为时间戳
a = "Sat Mar 28 22:24:24 2016"
time.mktime(time.strptime(a,"%a %b %d %H:%M:%S %Y"))