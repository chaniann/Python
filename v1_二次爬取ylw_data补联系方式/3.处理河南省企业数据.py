import os
import pandas as pd


# 读取 Excel 文件
# excel_file = "补充联系方式（不含未关联上）.xlsx"  # 替换为你的 Excel 文件路径
# df_excel = pd.read_excel(excel_file, sheet_name='机构养老', engine='openpyxl',nrows=10)

# 从df_excel DataFrame中筛选出联系方式为空的所有行，并将其存储在新的DataFrame new_df 中
# new_df = df_excel.loc[df_excel['ahae0012'].isnull(), '名称':'ahae0012']
# print(new_df.head(5))


# 设置文件夹路径和输出文件名
folder_path = "Y:\公共文件\各省企业数据\河南"  # 替换为你的Excel文件夹路径
output_csv = "merged_result.csv"

# 要提取的字段名
required_columns = ["企业名称", "法定代表人", "联系电话"]

# 初始化输出文件（清空文件或创建新文件）
with open(output_csv, 'w') as f:
    f.write('')  # 确保文件为空

# 遍历文件夹中的所有 Excel 文件
for file in os.listdir(folder_path):
    if file.endswith(".xlsx") or file.endswith(".xls") and not file.startswith("~$"):
        file_path = os.path.join(folder_path, file)
        try:
            # 仅加载需要的列
            df = pd.read_excel(file_path, usecols=required_columns)

            # 确定是否写入表头
            write_header = not os.path.isfile(output_csv)

            # 写入 CSV 文件，追加模式
            df.to_csv(output_csv, mode='a', index=False, header=write_header, encoding='utf-8-sig')
            print(f"已处理文件: {file}")
        except Exception as e:
            print(f"处理文件 {file} 时出错: {e}")

print(f"所有 Excel 文件已合并，保存为 {output_csv}")
