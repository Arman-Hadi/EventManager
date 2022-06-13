import re


def evaluate_evand_fucking_data(data:dict):
    new_data = dict()
    for key, value in data.items():
        keys = key[5:].split('[')
        keys.reverse()
        dic = {keys[1][:-1]: {keys[0][:-1]: value,},}
        for i, k in enumerate(keys[1:-1]):
            k = k[:-1]
            dic[i+1][:1] = {k: dic.pop(k),}
        new_data[keys[-1][:-1]