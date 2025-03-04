import pandas as pd
import re

# 定义一个函数来提取区县信息
def extract_county(address):
    # 确保输入为字符串类型
    address = str(address)  # 将输入转换为字符串
    match = re.search(r'([^省市区县自治州自治区]+(?:县|区|自治县|自治州))(?!社区|小区)', address)
    if match:
        # 返回匹配的区县信息，并去除空格
        county_district = match.group(1).strip()
        return county_district
    else:
        # 如果没有匹配，返回空字符串
        return ''

# 读取Excel文件
file_path = '全国养老机构信息_机构_社区_助餐_241101_李.xlsx'
xls = pd.ExcelFile(file_path)
temp_file_path = 'temp_file.xlsx'
with pd.ExcelWriter(temp_file_path, engine='openpyxl') as writer:
    # 遍历所有工作表
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name, engine='openpyxl')

        # 应用函数并创建新的区县列
        df['区县_ext'] = df['详细地址'].apply(extract_county)

        # 保存更新后的数据回到同一工作表
        df.to_excel(writer, sheet_name=sheet_name, index=False, engine='openpyxl')
print("所有工作表的区县信息已更新。")