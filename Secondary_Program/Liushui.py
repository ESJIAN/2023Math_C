import os
import pandas as pd  #
"""
这个程序是遍历商品信息表检索的一大类的商品单号
"""

def liushui_process(filter_dataframe, pifa_xlsx_sheet1, liushui_sheet_dataframe):
    Storage_Path = r'./DataOutput/Liushui/' + '花叶类' + '_' + '子类流水表.xlsx'

    #print(filter_dataframe['单品编码'])        # CHK：查看单品编码
    colum_filter_code = filter_dataframe['单品编码']  # 存储这列单品编码的Series对象
    colum_filter_name = filter_dataframe['单品名称']  # 存储这列单品名称的Series对象
    for i in filter_dataframe.index:  #  遍历index可迭代对象属性
        print("总共需分类" + str(filter_dataframe.index.max()) + "项")
        print("流水子类已分类:第" + str(i) + "项")
        temp_code = colum_filter_code[i]  # 遍历列，获取单品编码
        temp_name = colum_filter_name[i]  # 遍历列，获取单品名称

        if temp_code in liushui_sheet_dataframe['单品编码'].values:  # 判断单品编码是否在流水表中
            temp_dataframe = liushui_sheet_dataframe[
                liushui_sheet_dataframe['单品编码'] == temp_code]  # 筛选出单品编码为temp_code的所有数据行
            #print(temp_dataframe)                                                              # CHK：查看temp_dataframe

            if os.path.exists(Storage_Path):  # 判断文件是否存在,存在则追加写入表单，不存在则创建xlsx文件并写入表单
                with pd.ExcelWriter(Storage_Path, mode='a') as writer:
                    temp_dataframe.to_excel(writer, sheet_name=temp_name, index=False)
            else:
                with pd.ExcelWriter(Storage_Path) as writer:
                    temp_dataframe.to_excel(writer, sheet_name=temp_name, index=False)

        else:
            temp_dataframe = pifa_xlsx_sheet1[pifa_xlsx_sheet1['单品编码'] == temp_code]
            if os.path.exists(Storage_Path):
                if i == 0:
                    with pd.ExcelWriter(Storage_Path) as writer:
                        temp_dataframe.to_excel(writer, sheet_name=temp_name + '(未)', index=False)
                else:
                    with pd.ExcelWriter(Storage_Path, mode='a') as writer:
                        temp_dataframe.to_excel(writer, sheet_name=temp_name + '(未)', index=False)
            else:
                with pd.ExcelWriter(Storage_Path, mode='a') as writer:
                    temp_dataframe.to_excel(writer, sheet_name=temp_name + '(未)', index=False)


# Debug
if __name__ == '__main__':
    pifa_xlsx_sheet1 = pd.read_excel(r'../DataStorage/批发价格.xlsx', sheet_name='Sheet1')  # 读取批发价格.xlsx文件为pandas 数据框
    xinxi_xlsx_sheet1 = pd.read_excel(r'../DataStorage/商品信息.xlsx', sheet_name='Sheet1')
    liushui_xlsx_sheet1 = pd.read_excel(r'../DataStorage/销售流水.xlsx', sheet_name='Sheet1')
    pifa_xlsx_sheet_filter = xinxi_xlsx_sheet1[xinxi_xlsx_sheet1['分类名称'] == '花叶类']

    Storage_Path = r'../DataOutput/Liushui/' + '花叶类' + '_' + '子类流水表.xlsx'

    colum_filter_code = pifa_xlsx_sheet_filter['单品编码']  # 存储这列单品编码的Series对象
    colum_filter_name = pifa_xlsx_sheet_filter['单品名称']  # 存储这列单品名称的Series对象
    for i in range(18, 21):
        temp_name = colum_filter_name[i]  # CHK:修改数值定位程序到具体的表单打印
        temp_code = colum_filter_code[i]
        temp_dataframe = liushui_xlsx_sheet1[liushui_xlsx_sheet1['单品编码'] == temp_code]
        if temp_code in liushui_xlsx_sheet1['单品编码'].values:  # 判断单品编码是否在流水表中,在则写表,不在则创建空表
            if os.path.exists(Storage_Path):  # 判断文件是否存在,存在则追加写入表单，不存在则创建xlsx文件并写入表单
                with pd.ExcelWriter(Storage_Path, mode='a') as writer:
                    temp_dataframe.to_excel(writer, sheet_name=temp_name, index=False)
            else:
                with pd.ExcelWriter(Storage_Path) as writer:
                    temp_dataframe.to_excel(writer, sheet_name=temp_name, index=False)
        else:
            with pd.ExcelWriter(Storage_Path, mode='a') as writer:
                # Notice:写入带上第一行的空表
                temp_dataframe.to_excel(writer, sheet_name=temp_name + '(未)', index=False)