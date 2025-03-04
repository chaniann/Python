import pandas as pd
import json

# 读取 Excel 文件
excel_file = "Z:\DRG\大模型知识库\养老获取数据\养老机构_20241129_v_2.xlsx"  # 替换为你的 Excel 文件路径
df_excel = pd.read_excel(excel_file, sheet_name='机构养老', engine='openpyxl')
# print(df_excel.loc[df_excel['名称']=='卧龙中心敬老院', '详细地址'])

# 从df_excel DataFrame中筛选出'flag'列为0的所有行，并将其存储在新的DataFrame new_df 中
# new_df = df_excel.loc[df_excel['flag']==0]


# 读取 上海JSON 文件
json_file1 = "D:\代码\AI\养老网_2\电话信息.json"  # 替换为你的 JSON 文件路径
with open(json_file1, "r", encoding="utf-8") as file:
    data1 = json.load(file)

# 将 JSON 数据转换为 DataFrame
df_json1 = pd.DataFrame(data1).drop_duplicates()

# 关联数据（左连接，保留原始 Excel 数据）
merged_df1 = pd.merge(df_excel, df_json1, left_on="名称", right_on="title", how="left", suffixes=("_旧", "_新"))

output_file1 = "补充养老网_2中的联系方式.xlsx"

merged_df1.to_excel(output_file1, index=False, sheet_name='机构养老', engine='openpyxl')

print(f"数据处理完成，结果已保存到 {output_file1}")