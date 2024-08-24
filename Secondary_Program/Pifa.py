import os
import pandas as pd

def pifa_process(filter_dataframe,pifa_xlsx_sheet1,leibie):
    Storage_Path=r'./DataOutput/Pifa/'+leibie+'_'+'子类批发表.xlsx'
    #print(filter_dataframe['单品编码'])        # CHK：查看单品编码
    colum_filter_code = filter_dataframe['单品编码'] # 存储这列单品编码的Series对象
    colum_filter_name = filter_dataframe['单品名称'] # 存储这列单品名称的Series对象
    for i in filter_dataframe.index:          #  遍历index可迭代对象属性

        temp_code = colum_filter_code[i]                                                     # 遍历列，获取单品编码
        temp_name = colum_filter_name[i]                                                     # 遍历列，获取单品名称

        if temp_code in pifa_xlsx_sheet1['单品编码'].values:                              # 判断单品编码是否在批发表中
            temp_dataframe = pifa_xlsx_sheet1[pifa_xlsx_sheet1['单品编码'] == temp_code]  # 筛选出单品编码为temp的所有数据行



            #print(temp_dataframe)                                                       # CHK：查看temp_dataframe
            """
            日期             单品编码  批发价格(元/千克)
35290 2022-05-18  106971563780002        2.87
35602 2022-05-24  106971563780002        2.87
35657 2022-05-25  106971563780002        3.00
35708 2022-05-26  106971563780002        3.00
            """


            if os.path.exists(Storage_Path): # 判断文件是否存在,存在则追加写入表单，不存在则创建xlsx文件并写入表单
                with pd.ExcelWriter(Storage_Path, mode='a') as writer:
                    temp_dataframe.to_excel(writer, sheet_name=temp_name, index=False)
            else:
                with pd.ExcelWriter(Storage_Path) as writer:
                    temp_dataframe.to_excel(writer, sheet_name=temp_name, index=False)

        else:# 如果单品编码不在批发表中，则创建一个空的表单,但是表单名还在
            temp_dataframe = pifa_xlsx_sheet1[pifa_xlsx_sheet1['单品编码'] == temp_code]  # 筛选出单品编码为temp的所有数据行
            if os.path.exists(Storage_Path):
                if i == 0:
                    with pd.ExcelWriter(Storage_Path) as writer:
                        temp_dataframe.to_excel(writer, sheet_name=temp_name + '(空)', index=False)
                else:
                    with pd.ExcelWriter(Storage_Path, mode='a') as writer:
                        temp_dataframe.to_excel(writer, sheet_name=temp_name + '(空)', index=False)
            else:
                with pd.ExcelWriter(Storage_Path, mode='a') as writer:
                    temp_dataframe.to_excel(writer, sheet_name=temp_name + '(空)', index=False)
