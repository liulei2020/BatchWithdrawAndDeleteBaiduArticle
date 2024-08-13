import requests
import json
import time
import random

headers = {
    'Cookie': '填写你的Cookie，详见README.md',
    'token': '填写你的token，详见README.md',
    'User-Agent': '填写你的User-Agent，详见README.md',
}

def process_article(article):
    article_id = article["article_id"]
    title = article["title"]
    can_withdraw = article["can_withdraw"]
    read_amount = article["read_amount"]
    rec_amount = article["rec_amount"]

    
    print(f"当前文章id {article_id} ，能否撤回：{can_withdraw},推荐量：{rec_amount},阅读量：{read_amount}开始处理")
    if can_withdraw == -1:
        print("调用接口删除文章")
        # 调用接口删除文章
        url = 'https://baijiahao.baidu.com/pcui/article/remove'
        params = {'article_id': article_id}

        response = requests.post(url, headers=headers, data=params)
        print(response)
        result = json.loads(response.text)

        if result["errmsg"] == "success":
            print(f"文章 {title} 删除成功")
        else:
            print(f"文章 {title} 删除失败")

    elif can_withdraw == 1 and read_amount < 1000 and rec_amount < 10000:
	# 可以自行定义上面要撤回的文章的条件，这里是can_withdraw == 1并且阅读量小于1000并且推荐量小于10000
        print("调用接口撤回文章")
        # 调用接口撤回文章
        url = 'https://baijiahao.baidu.com/pcui/article/withdraw'
        params = {'article_id': article_id}

        response = requests.post(url, headers=headers, data=params)
        print(response)
        result = json.loads(response.text)

        if result["errmsg"] == "success":
            print(f"文章 {title} 撤回成功")
        else:
            print(f"文章 {title} 撤回失败")
    else:
        print("暂时不处理")

if __name__ == "__main__":
    # 之前提取的文章数据，包含文章id,推荐量、阅读量、能否撤回等
    json_file_path = 'content.json'

    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    # 过滤出 can_withdraw 等于 -1 的文章
    filtered_data = [article for article in data if article["can_withdraw"] == -1]
    # 按照 rec_amount 由小到大排序
    # data.sort(key=lambda x: x["rec_amount"])
    print(f"总共有 {len(filtered_data)} 篇文章需要删除")
    #print(f"总共有 {len(data)} 篇文章需要处理，优先处理推荐量少的")
    #for article in data:
    for article in filtered_data:
        process_article(article)
        time.sleep(random.uniform(2, 4))  # 随机停顿2到4秒
