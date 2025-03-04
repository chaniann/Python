import pandas as pd
import json

# Excel 文件路径
file_path = "../全国养老机构信息_机构_社区_助餐_241104_李.xlsx"
xls = pd.ExcelFile(file_path)
temp_file_path = "补充结果表_1206.xlsx"

# 定义关联文件及条件的配置
merge_configs = {
    0: [  # flag=0 的关联配置
        {"file_type": "json", "file_path": "D:\\代码\\pandas数据处理\\v1_二次爬取ylw_data补联系方式\\output.json", "left_on": ["名称"], "right_on": ["axbe0003"]},
        {"file_type": "json", "file_path": "D:\\代码\\AI\\人民政府网\\上海\\机构信息.json", "left_on": ["名称"],
         "right_on": ["agency_name"]},
        {"file_type": "csv", "file_path": "D:\\代码\\AI\\人民政府网\\北京\\北京养老机构信息.csv", "left_on": ["名称"],
         "right_on": ["机构名称"]},
        {"file_type": "json", "file_path": "D:\\代码\\AI\\人民政府网\\四川\\养老机构信息.json", "left_on": ["名称"],
         "right_on": ["name"]},
        {"file_type": "csv", "file_path": "D:\\代码\\AI\\人民政府网\\河南\\机构信息-最终结果数据.csv", "left_on": ["名称"],
         "right_on": ["orgName"]},
        {"file_type": "json", "file_path": "D:\\代码\\AI\\养老网_2\\电话信息.json", "left_on": ["名称"],
         "right_on": ["title"]},
        {"file_type": "csv", "file_path": "D:\\代码\\pandas数据处理\\v1_二次爬取ylw_data补联系方式\\merged_result.csv", "left_on": ["名称"],
         "right_on": ["企业名称"]},
    ],
    1: [  # flag=1 的关联配置
        {"file_type": "json", "file_path": "D:\\代码\\pandas数据处理\\v1_二次爬取ylw_data补联系方式\\output.json", "left_on": ["名称", "省"],
         "right_on": ["axbe0003",  "areaCodeName"]},
        {"file_type": "json", "file_path": "D:\\代码\\AI\\人民政府网\\上海\\机构信息.json", "left_on": ["名称"],
         "right_on": ["agency_name"]},
        {"file_type": "csv", "file_path": "D:\\代码\\AI\\人民政府网\\北京\\北京养老机构信息.csv", "left_on": ["名称"],
         "right_on": ["机构名称"]},
        {"file_type": "json", "file_path": "D:\\代码\\AI\\人民政府网\\四川\\养老机构信息.json", "left_on": ["名称"],
         "right_on": ["name"]},
        {"file_type": "csv", "file_path": "D:\\代码\\AI\\人民政府网\\河南\\机构信息-最终结果数据.csv", "left_on": ["名称"],
         "right_on": ["orgName"]},
        {"file_type": "json", "file_path": "D:\\代码\\AI\\养老网_2\\电话信息.json", "left_on": ["名称"],
         "right_on": ["title"]},
        {"file_type": "csv", "file_path": "D:\\代码\\pandas数据处理\\v1_二次爬取ylw_data补联系方式\\merged_result.csv", "left_on": ["名称"],
         "right_on": ["企业名称"]},
    ],
}


# 定义处理逻辑的函数
def process_flag_data(df, flag_value):
    filtered_df = df.loc[df['flag'] == flag_value]
    for config in merge_configs[flag_value]:
        # 加载文件
        if config["file_type"] == "json":
            with open(config["file_path"], "r", encoding="utf-8") as file:
                data = json.load(file)
            df_to_merge = pd.DataFrame(data)

            # 针对 output.json 进行去重和分组处理
            if config["file_path"] == "D:\\代码\\pandas数据处理\\v1_二次爬取ylw_data补联系方式\\output.json" and flag_value == 1:
                df_to_merge = (
                    df_to_merge.sort_values(by="axbe0017", ascending=False)  # 按时间降序
                    .groupby(["axbe0003", "areaCodeName"], as_index=False)  # 按 axbe0003 和 areaCodeName 分组
                    .first()  # 取每组的第一条（时间最大的）
                )

            df_to_merge = df_to_merge.drop_duplicates()  # 确保无其他重复

        elif config["file_type"] == "csv":
            df_to_merge = pd.read_csv(config["file_path"]).drop_duplicates()

        # 动态关联数据
        filtered_df = pd.merge(
            filtered_df,
            df_to_merge,
            left_on=config["left_on"],
            right_on=config["right_on"],
            how="left"
        )
    return filtered_df


# 遍历所有工作表并处理
with pd.ExcelWriter(temp_file_path, engine="openpyxl") as writer:
    for sheet_name in xls.sheet_names:
        # 读取当前 sheet 的数据
        df_excel = pd.read_excel(xls, sheet_name=sheet_name, engine="openpyxl")

        # 处理 flag=0 的数据
        result_flag_0 = process_flag_data(df_excel, flag_value=0)

        # 处理 flag=1 的数据
        result_flag_1 = process_flag_data(df_excel, flag_value=1)

        # 合并处理结果
        final_result = pd.concat([result_flag_0, result_flag_1], ignore_index=True)

        # 将结果写入新 Excel 文件的同名 sheet
        final_result.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"处理完成，结果已保存到: {temp_file_path}")
