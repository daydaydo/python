import requests
import csv


def fetch_data(page=1, per_page=100):
    url = 'http://dohurd.ah.gov.cn/epoint-mini/rest/function/searchAllPeople'
    # url= 'http://dohurd.ah.gov.cn/site/tpl/9321'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://dohurd.ah.gov.cn/site/tpl/9321',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        #'Cookie':'wzws_sessionid=gWYxZjZiMoAxMTUuMjE0LjY0LjU2gmZkNzRjZKBmeppT; SHIROJSESSIONID=e478b5db-3088-4a20-a886-efc3a3871882; b-user-id=eac7a78d-5544-c725-56d5-a8e36f6335b2; wzaConfigTime=1719310938501'
    }

    data = {
        'pagesize': per_page,
        'pageindex': page,
        'type': '2',
        'PersonName': '',
        'IDCard': '',
        'CorpName': '',
        'persontype': '',
        'txt1': ''
    }

    try:
        response = requests.post(url=url,data=data,headers=headers)
        response.raise_for_status()  # 抛出异常，如果请求不成功
        data = response.json()
        return data['all']['listinfo']

    except requests.exceptions.RequestException as e:
        print(f"请求数据时发生错误: {e}")
        return None


def write_to_csv(data, filename):
    fields = ['name', 'idcard', 'rylb', 'corpname']

    try:
        with open(filename, mode='a', newline='', encoding='utf-8-sig') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())

            # 如果文件为空，则写入表头
            if file.tell() == 0:
                writer.writeheader()

            # 写入数据
            for item in data:
                if item['corpname'] is None:
                    writer.writerow(item)

        print(f"数据已成功写入文件: {filename}")

    except IOError as e:
        print(f"写入 CSV 文件时发生错误: {e}")


def main():
    page = 1200
    per_page = 1000
    total_pages = 2000  # 假设总共有 5 页数据
    filename = 'paged_data.csv'

    while page <= total_pages:
        data = fetch_data(page, per_page)

        if data:
            write_to_csv(data, filename)

        page += 1


if __name__ == "__main__":
    main()
