import pandas as pd
# 假设CSV文件的路径是'your_data.csv'
file_path = 'D:/代码/pandas数据处理/全国养老机构信息_机构_社区_助餐_241028_李.xlsx'
# 读取Excel文件
# 使用pandas函数读取文件，并将其存储在DataFrame中
xls = pd.ExcelFile(file_path)
print(xls)
# 遍历所有工作表
for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet_name, engine='openpyxl')

    # 假设原始数据在'省'这一列
    # 遍历原始'省'列，分解字符串
    for index, row in df.iterrows():
        original_string = str(row['省'])    # 确保字符串类型
        if pd.notna(original_string):   # 检查是否空值
            # 处理省
            if '省' in original_string:
                df.at[index, '省份'] = original_string.split('省')[0] + '省'
            elif '自治区' in original_string:
                df.at[index, '省份'] = original_string.split('自治区')[0] + '自治区'
            else:
                df.at[index, '省份'] = original_string
            # 处理市和区县
            remaining_string = original_string.replace(df.at[index,'省份'],'',1).strip()
            if '市' in remaining_string:
                if '自治州' in remaining_string:
                    df.at[index, '城市'] = remaining_string.split('自治州')[0] + '自治州'
                else:
                    df.at[index, '城市'] = remaining_string.split('市')[0] + '市'
                county_district = remaining_string.replace(df.at[index, '城市'], '', 1).strip()
                df.at[index, '区县'] = county_district
            else:
                df.at[index, '城市'] = ''
                df.at[index, '区县'] = remaining_string

        else:
            # 如果没有'省'字，那么省份为空
            df.at[index, '省份'] = ''
            df.at[index, '城市'] = ''
            df.at[index, '区县'] = ''

    # 更新'省'列，只保留省份信息
    df['省'] = df['省份']

    # 删除临时创建的'省份'列
    df.drop(columns=['省份'], inplace=True)

    # 保存更新后的数据回到同一工作表
    df.to_excel(file_path, sheet_name=sheet_name, index=False, engine='openpyxl')

print("所有工作表处理完成。")