"""
机构养老数据爬取脚本
"""
import json
import os
import requests
import csv
import time
import logging
import random

# 配置日志
logging.basicConfig(filename='failed_pages_jg.log',
                    level=logging.INFO, format='%(asctime)s - %(message)s')

# 定义常量
BASE_URL = "https://yanglao.mca.gov.cn/ylxxptapi/ylfwpt/ylfw/queryOrganizationDataList"
HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Authorization': 'Basic ZHNycHQ6ZHNycHQ=',  # 注意：需要根据具体的授权信息修改
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
}
MAX_RETRIES = 5
PAGES = 390
PAGE_SIZE = 100
# CSV_FILE = 'policy_jgyl_all.csv'
# areaCode='370000000000'
# 定义文件名
JSON_FILE = 'output.json'
def fetch_page(page_num):
    """获取指定页码的数据，带有重试机制"""
    retries = 0
    while retries < MAX_RETRIES:
        try:
            data = {'current': page_num, 'size': PAGE_SIZE}
            response = requests.post(BASE_URL, headers=HEADERS, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                retries += 1
                print(f"\n第{page_num}页请求失败，重试{retries}/{MAX_RETRIES}")
                time.sleep(2)  # 重试前等待2秒
        except Exception as e:
            retries += 1
            print(f"\n第{page_num}页请求异常: {str(e)}，重试{retries}/{MAX_RETRIES}")
            time.sleep(2)
    # 如果重试5次仍失败，记录失败的页码
    logging.info(f"Page {page_num} failed after {MAX_RETRIES} retries.")
    return None


def save_to_json(data):
    # """将数据保存到CSV文件"""
    # with open(CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
    #     writer = csv.writer(csvfile)
    #     for record in data['records']:
    #         writer.writerow([
    #             record.get('axbe0003', ''),  # 名称
    #             record.get('areaCodeName', ''),  # 省市区
    #             record.get('axbe0017', ''),  # 时间
    #             record.get('axbe0021', ''),  # 联系人
    #             record.get('axbe0019', ''),  # 类型
    #             record.get('ahae0012', ''),  # 联系电话
    #             record.get('axbe0013', ''),  # 详细地址
    #             record.get('tag', ''),  # 标签
    #             record.get('point', ''),  # 经纬度
    #             record.get('infoDatail', '')  # 详情
    #         ])
    """
    将完整的 records 数组保存到 JSON 文件中。
    """
    # 检查是否存在目标文件，若无则创建一个空列表
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'w', encoding='utf-8') as file:
            json.dump([], file, ensure_ascii=False, indent=4)

    # 读取当前文件中的数据
    with open(JSON_FILE, 'r', encoding='utf-8') as file:
        existing_data = json.load(file)

    # 将新数据追加到现有数据中
    if 'records' in data:
        existing_data.extend(data['records'])

    # 将更新后的数据写回文件
    with open(JSON_FILE, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)

def main():
    # # 创建CSV文件，并写入表头
    # with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['名称', '省市区', '时间', '联系人', '类型',
    #                     '联系电话', '详细地址', '标签', '经纬度', '详情'])

    # 遍历每一页，抓取数据
    for page_num in range(1, PAGES + 1):
        print(f"\r正在处理第 {page_num}/{PAGES} 页.", end="", flush=True)
        page_data = fetch_page(page_num)
        if page_data and page_data.get('data') and page_data['data'].get('records'):
            save_to_json(page_data['data'])
        else:
            print(f"\n第 {page_num} 页抓取失败，已记录日志")
        # 每次请求后随机等待10-50秒
        time.sleep(random.randint(10, 40))


if __name__ == "__main__":
    main()

