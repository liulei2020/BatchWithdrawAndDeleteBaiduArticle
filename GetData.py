import requests
import json
import time
import random
import pandas as pd


headers = {
    'Cookie': '填写你的Cookie，详见README.md',
    'token': '填写你的token，详见README.md',
    'User-Agent': '填写你的User-Agent，详见README.md'
}

content_data = []


def get_data(current_page):
    url = "https://baijiahao.baidu.com/pcui/article/lists"
    params = {
        "currentPage": current_page,
        "pageSize": 10,
        "search": "",
        "type": "",
        "collection": "",
        "dynamic": 1
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    return data.get("data", {}).get("list", []), data.get("data", {}).get("page", {})

def save_data_to_json(data):
    for article in data:
        article_id = article.get("article_id")
        title = article.get("title")
        read_amount = article.get("read_amount")
        rec_amount = article.get("rec_amount")
        can_withdraw = article.get("withdraw_status", {}).get("can_withdraw")

        content_data.append({
            "article_id": article_id,
            "title": title,
            "read_amount": read_amount,
            "rec_amount": rec_amount,
            "can_withdraw": can_withdraw
        })
            
# 将json数据转换为DataFrame
def json_to_dataframe(json_data):
    df = pd.DataFrame(json_data)
    return df
# 保存到Excel文件
def save_to_excel(dataframe, output_file):
    dataframe.to_excel(output_file, index=False)

def main():
    current_page = 1
    total_page = 24 # 这里写你自己百家号后台文章的页数，替换这个24

    while current_page <= total_page:
        print(f"开始查询第{current_page}页数据")
        data, page_info = get_data(current_page)
        save_data_to_json(data)
        current_page += 1
        time.sleep(random.uniform(1, 2))

    with open("content.json", "w", encoding="utf-8") as json_file:
        json.dump(content_data, json_file, ensure_ascii=False, indent=4)
    # 替换成你想要保存的Excel文件路径
    excel_output_file = 'content.xlsx'
    result_df = json_to_dataframe(content_data)
    # 保存到Excel文件
    save_to_excel(result_df, excel_output_file)

    print(f"数据已成功保存到 {excel_output_file}")


if __name__ == "__main__":
    main()
