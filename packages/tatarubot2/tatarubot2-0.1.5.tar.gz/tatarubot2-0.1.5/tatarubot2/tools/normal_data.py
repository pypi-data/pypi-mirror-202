# -*- coding: utf-8 -*-

import json


def run1():
    with open("tatarubot2/data/job.json", "r") as f_r:
        data_job = json.load(f_r)

    new_list = []
    for j in data_job:
        dict_now = {}
        dict_now["pk"] = j["pk"]
        dict_now["name"] = j["fields"]["name"]
        dict_now["cn_name"] = j["fields"]["cn_name"]
        nickname = eval(j["fields"]["nickname"])
        if nickname != {}:
            dict_now["nickname"] = eval(j["fields"]["nickname"])["nickname"]
        else:
            dict_now["nickname"] = []

        print(dict_now)
        new_list.append(dict_now)

    with open("tatarubot2/tools/new_job.json", "w") as f_w:
        json.dump(new_list, f_w, ensure_ascii=False, indent=2)


def run2():
    with open("tatarubot2/data/boss.json", "r") as f_r:
        data_job = json.load(f_r)

    new_list = []
    for j in data_job:
        dict_now = {}
        dict_now["pk"] = j["pk"]
        dict_now["quest"] = j["fields"]["quest"]
        dict_now["name"] = j["fields"]["name"]
        dict_now["cn_name"] = j["fields"]["cn_name"]
        nickname = eval(j["fields"]["nickname"])
        if nickname != {}:
            dict_now["nickname"] = eval(j["fields"]["nickname"])["nickname"]
        else:
            dict_now["nickname"] = []
        dict_now["patch"] = j["fields"]["patch"]
        dict_now["savage"] = j["fields"]["savage"]
        dict_now["global_server"] = j["fields"]["global_server"]
        dict_now["cn_server"] = j["fields"]["cn_server"]

        print(dict_now)
        new_list.append(dict_now)

    with open("tatarubot2/tools/new_boss.json", "w") as f_w:
        json.dump(new_list, f_w, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    run2()