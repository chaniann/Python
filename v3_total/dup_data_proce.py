import pandas as pd

# 最新表文件路径
latest_file_path = "补充结果表_1206.xlsx"
output_file_path = "final_filtered_file——3.xlsx"

# 指定处理的 sheet 名称
target_sheet_name = "机构养老"  # 替换为你的实际 sheet 名称

# 读取 Excel 文件
xls = pd.ExcelFile(latest_file_path)

# 检查是否包含目标 sheet
if target_sheet_name not in xls.sheet_names:
    raise ValueError(f"指定的 sheet 名称 '{target_sheet_name}' 不存在！")

# 读取目标 sheet
df = pd.read_excel(xls, sheet_name=target_sheet_name, engine="openpyxl")

# 确保数据包含所需字段
required_columns = ["名称", "省","详细地址","经纬度", "update_date","联系电话"]
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise ValueError(f"目标数据缺少以下必需字段: {missing_columns}")

# 处理数据：按名称和省分组，保留 update_date 最大的记录
filtered_df = (
    df.sort_values(by=["update_date","联系电话"], ascending=[False,False])  # 按 update_date 降序排列
    .groupby(["名称", "省","详细地址","经纬度"], as_index=False)  # 按名称、省、详细地址、经纬度分组
    .first()  # 每组取第一条记录
)

# 将处理后的数据写入新文件
with pd.ExcelWriter(output_file_path, engine="openpyxl") as writer:
    # 保存去重后的数据到新文件的目标 sheet
    filtered_df.to_excel(writer, sheet_name=target_sheet_name, index=False)
    # 复制其他 sheet 不修改
    for sheet_name in xls.sheet_names:
        if sheet_name != target_sheet_name:
            original_sheet_data = pd.read_excel(xls, sheet_name=sheet_name, engine="openpyxl")
            original_sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"数据去重完成，结果已保存到: {output_file_path}")
