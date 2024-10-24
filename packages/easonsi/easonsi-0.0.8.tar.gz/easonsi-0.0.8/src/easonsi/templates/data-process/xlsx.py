### 1 pandas
import pandas as pd

df = pd.read_excel('test_user_data.xlsx')
data=df.values
print("获取到所有的值:\n{}".format(data))

#读取第一列、第二列、第四列
df = pd.read_excel('test_user_data.xlsx',sheet_name='TestUserLogin',usecols=[0,1,3])
data = df.values
print(data)

#读取第一行
df = pd.read_excel('test_user_data.xlsx',sheet_name='TestUserLogin',nrows=1)
data = df.values
print(data)


### 2 xldr
import xlrd
#打开excel
wb = xlrd.open_workbook('test_user_data.xlsx')
#按工作簿定位工作表
sh = wb.sheet_by_name('TestUserLogin')
print(sh.nrows) #有效数据行数
print(sh.ncols) #有效数据列数
print(sh.cell(0,0).value)   #输出第一行第一列的值
print(sh.row_values(0))     #输出第一行的所有值
#将数据和标题组合成字典
print(dict(zip(sh.row_values(0), sh.row_values(1))))
#遍历excel，打印所有数据
for i in range(sh.nrows):
    print(sh.row_values(i))
