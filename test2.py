import json
import time
from pprint import pprint
import requests

API_URL = 'https://pl.wikipedia.org/w/api.php'


def query_categories(category_name, api_url=API_URL):
    params = {"action": "query",
              "list": "categorymembers",
              "cmtitle": f"Category:{category_name}",
              "cmtype": "subcat",
              'format': "json",
              "cmlimit": 500}
    try:
        time.sleep(0.5)
        response = requests.get(url=api_url, params=params)
    except ConnectionError as e:
        raise Exception("Query failed: ", e)

    if response.status_code == 200:
        data = response.json()['query']['categorymembers']
        print(category_name)
        print(data)
        print("-----------")
        return data
    else:
        raise Exception(f"Query failed, returned status code {response.status_code}, and message: {response.text}")


def recursive_query(category, category_tree, depth, max_depth):
    if depth > max_depth:
        return
    sub_cats = query_categories(category)
    sub_cats = {'_'.join(sub_cat['title'].split(":")[1].split()): None for sub_cat in sub_cats[:2]}
    # print(sub_cats)
    # if category is None:
    category_tree[category] = sub_cats
    # else:
    #     print(category_tree)
    #     category_tree[top_cat][category] = sub_cats
    for sub_cat in sub_cats:

        # sub_cat = '_'.join(sub_cat['title'].split(":")[1].split())
        recursive_query(sub_cat, category_tree[category], depth=depth + 1, max_depth=max_depth)
        # break


if __name__ == "__main__":
    category_tree = {}
    # top_cat = "Historia"
    recursive_query("Historia", category_tree=category_tree, depth=0, max_depth=4)
    pprint(category_tree)
    with open("category_tree.json", "w+") as out_file:
        json.dump(category_tree, out_file, indent=4)

    # print()
    # query_categories("Historia_według_epok")
    # first = query_categories(top_cat)
    # category_tree[top_cat] = first

    # print(first)
    # data = response.json()
    # print(data['query']['categorymembers'])
    # print(len(data['query']['categorymembers']))
    # print(response.json())
    # print(response.text)
