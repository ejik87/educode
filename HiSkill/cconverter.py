import json
import requests

cache_dict = {}
coast = 0.0
dict_json = {}


def cache(it):
    global dict_json
    a = it.lower()
    print("Checking the cache...")
    if a not in cache_dict:
        print("Sorry, but it is not in the cache!")
        cache_dict[a] = dict_json[a]
        return math_coin(a)
    else:
        print("Oh! It is in the cache!")
        return math_coin(a)


def math_coin(x):
    rec = coast * cache_dict[x]["rate"]
    return round(rec, 2)


def main():
    global dict_json
    global coast
    nal = str(input()).upper()
    json_net = requests.get(f"http://www.floatrates.com/daily/{nal.lower()}.json").text
    dict_json = json.loads(json_net)
    demo = ['USD', 'EUR']
    if nal in demo:
        demo.remove(nal)
    for c in demo:
        a = c.lower()
        cache_dict[a] = dict_json[a]

    while True:
        curr = input()
        if curr == '':
            break
        else:
            coast = float(input())
            print(f'You received {str(cache(curr))} {curr.upper()}.')
            continue


main()
