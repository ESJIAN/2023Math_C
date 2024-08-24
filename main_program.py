'''
Python3.10
'''
import multiprocessing
import pandas as pd #
from Secondary_Program.Pifa import pifa_process
from Secondary_Program.Liushui import liushui_process


# 改进：多线程IO读取


"""
创建子线程
"""

def read_pifa_excel():
    """
    子进程与主进程变量空间共享复杂,这边以返回值替代共享变量空间
    """
    pifa_xlsx_sheet1 = pd.read_excel(r'./DataStorage/批发价格.xlsx', sheet_name='Sheet1')  # 读取批发价格.xlsx文件为pandas 数据框
    return pifa_xlsx_sheet1
def read_liushui_excel():
    liushui_xlsx_sheet1 = pd.read_excel(r'./DataStorage/销售流水.xlsx', sheet_name='Sheet1')
    return liushui_xlsx_sheet1
def read_xinxi_excel():
    xinxi_xlsx_sheet1 = pd.read_excel(r'./DataStorage/商品信息.xlsx', sheet_name='Sheet1')
    return xinxi_xlsx_sheet1


read_pifa_excel_subprocess = multiprocessing.Process(target=read_pifa_excel)
read_liushui_excel_subprocess = multiprocessing.Process(target=read_liushui_excel)
read_xinxi_excel_subprocess = multiprocessing.Process(target=read_xinxi_excel)

# pifa_xlsx_sheet1 = pd.read_excel(r'./DataStorage/批发价格.xlsx', sheet_name='Sheet1')  # 读取批发价格.xlsx文件为pandas 数据框
# xinxi_xlsx_sheet1 = pd.read_excel(r'./DataStorage/商品信息.xlsx', sheet_name='Sheet1')
# liushui_xlsx_sheet1 = pd.read_excel(r'./DataStorage/销售流水.xlsx', sheet_name='Sheet1')

def main():
    global pifa_xlsx_sheet1, xinxi_xlsx_sheet1, liushui_xlsx_sheet1

    # 启动子进程
    print("Data Loading Starts")
    read_pifa_excel_subprocess.start()
    read_liushui_excel_subprocess.start()
    read_xinxi_excel_subprocess.start()

    # 等待所有进程完成,才会进行下一步,相当于这三行合并成一行代码
    read_pifa_excel_subprocess.join()
    read_liushui_excel_subprocess.join()
    read_xinxi_excel_subprocess.join()
    print("Data Loading Finished")
    # 保存返回的数据框
    pifa_xlsx_sheet1 = read_pifa_excel()
    liushui_xlsx_sheet1 = read_liushui_excel()
    xinxi_xlsx_sheet1 = read_xinxi_excel()



    #  过滤出分类名称为花叶类的数据框
    #  xinxi_xlsx_sheet1是Framework对象，xinxi_xlsx_sheet1['分类名称']是Series对象，返回一个Framework对象


    #print(xinxi_xlsx_sheet1['分类名称'].unique())                                           # CHK：查看列名
    """
    ['花叶类' '花菜类' '水生根茎类' '茄类' '辣椒类' '食用菌']
    """

    #print(pifa_xlsx_sheet_filter.head())                                                  # CHK：查看头五行，0索引
    """
    单品编码    单品名称        分类编码 分类名称
0  102900005115168    牛首生菜  1011010101  花叶类
1  102900005115199   四川红香椿  1011010101  花叶类
2  102900005115625  本地小毛白菜  1011010101  花叶类
3  102900005115748     白菜苔  1011010101  花叶类
4  102900005115762      苋菜  1011010101  花叶类
    """


    for i in xinxi_xlsx_sheet1['分类名称'].unique():
        pifa_xlsx_sheet_filter = xinxi_xlsx_sheet1[xinxi_xlsx_sheet1['分类名称'] == i]
        # 创建子进程对象
        pifa_subprocess = multiprocessing.Process(target=pifa_process,args=(pifa_xlsx_sheet_filter,pifa_xlsx_sheet1,i))
        liushui_subprocess = multiprocessing.Process(target=liushui_process,args=(pifa_xlsx_sheet_filter,pifa_xlsx_sheet1,liushui_xlsx_sheet1,i))
        # 启动子进程
        pifa_subprocess.start()
        liushui_subprocess.start()
        # 等待子进程完成
        pifa_subprocess.join()
        liushui_subprocess.join()


if __name__ == '__main__':
    # 只有在直接运行这个脚本时才调用 main 函数,才能
    main()


# 主函数在子函数进行模块化的时,子函数用到的全局变量全部要以传参的方式传入子模块
