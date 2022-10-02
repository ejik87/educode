import json
import re


def check_data(data):
    err_dict = {
        'bus_id': 0,
        'stop_id': 0,
        'stop_name': 0,
        'next_stop': 0,
        'stop_type': 0,
        'a_time': 0
    }
    eq_type = {
        'bus_id': [int, r'\d+'],
        'stop_id': [int, r'\d+'],
        'stop_name': [str, r'([A-Z]\w+) ([A-Z]\w+ )?(Avenue|Street|Boulevard|Road)$'],
        'next_stop': [int, r'\d+'],
        'stop_type': [str, '^[SOF]$|$'],
        'a_time': [str, '^2[0-4]|[01][0-9]:[0-5][0-9]$']
    }
    for val in data:  # Переделать FIXME
        for k, v in val.items():
            if not isinstance(v, eq_type[k][0]) or re.match(eq_type[k][1], str(v)) is None:
                err_dict[k] += 1
    if sum(err_dict.values()) == 0:
        return True
    else:
        return False


def bus_stop_count(data):
    stop_id_count = {}
    for i in data:
        stop_id_count[i['bus_id']] = stop_id_count.get(i['bus_id'], 0) + 1
    # bus_id_print(stop_id_count)
    return stop_id_count


#
# def bus_id_print(data):
#     print('Line names and number of stops:')
#     for k, v in data.items():
#         print(f'bus_id: {k}, stops: {v}')


def stop_check(data):
    for bus_id in set(item['bus_id'] for item in data):
        if sum(i['stop_type'] == 'S' for i in data if i['bus_id'] == bus_id) != 1 \
                or sum(i['stop_type'] == 'F' for i in data if i['bus_id'] == bus_id) != 1:
            print(f'There is no start or end stop for the line: {bus_id}')
            exit(0)

    stops_print(data)


def stops_print(data):
    starts = set(i['stop_name'] for i in data if i['stop_type'] == 'S')
    print(f'Start stops: {len(starts)} {sorted(list(starts))}')

    tranfers = set(stops['stop_name'] for stops in data if sum(i['stop_name'] == stops['stop_name'] for i in data) > 1)
    print(f'Transfer stops: {len(tranfers)} {sorted(list(tranfers))}')

    finishes = set(i['stop_name'] for i in data if i['stop_type'] == 'F')
    print(f'Finish stops: {len(finishes)} {sorted(list(finishes))}')


def time_check(data):
    err_flag = False
    err_dict = {}
    last_time = 0
    parse_dict = {}
    for item in data:
        parse_dict[item["bus_id"]] = parse_dict.get(item['bus_id'], []) + [(item["stop_name"], item["a_time"])]
    # print(parse_dict)
    for bus, val in parse_dict.items():
        last_time = 0
        for i in val:
            if i[1] > str(last_time):
                last_time = i[1]
            else:
                err_flag = True
                err_dict[bus] = i[0]
                break

    print('Arrival time test:')
    if err_flag:
        for k, v in err_dict.items():
            print(f'bus_id line {k}: wrong time on station {v}')
    if not err_flag:
        print('OK')


def demand_check(data):
    # transfer_stops = set(stops['stop_name'] for stops in data if sum(i['stop_name'] == stops['stop_name'] for i in data) > 1)
    # s_f_stops = set(stop['stop_name'] for stop in data if stop['stop_type'] == 'S' or stop['stop_type'] == 'F')
    wrong_stop = []
    # for item in data:
    #     if item['stop_type'] == 'O' and (item['stop_name'] in transfer_stops or item['stop_name'] in s_f_stops):
    #         wrong_stop.append(item["stop_name"])
    print('On demand stops test:')
    # if wrong_stop:
    #     print(f"Wrong stop type: {sorted(wrong_stop)}")
    # else:
    #     print('Wrong stop type: OK')
    for o_stop_id in set(stop['stop_id'] for stop in data if stop['stop_type'] == 'O'):
        if sum(stop['stop_id'] == o_stop_id for stop in data) > 1:
            wrong_stop.append(next(filter(lambda stop: stop['stop_id'] == o_stop_id, data))['stop_name'])
    print(sorted(wrong_stop) if wrong_stop else 'OK')



def main(data):
    # check_data(data)
    # stop_check(data)
    # time_check(data)
    demand_check(data)


input_data = '''[
    {"bus_id": 128, "stop_id": 1, "stop_name": "Prospekt Avenue", "next_stop": 3, "stop_type": "S", "a_time": "08:12"},
    {"bus_id": 128, "stop_id": 3, "stop_name": "Elm Street", "next_stop": 5, "stop_type": "O", "a_time": "08:19"},
    {"bus_id": 128, "stop_id": 5, "stop_name": "Fifth Avenue", "next_stop": 7, "stop_type": "O", "a_time": "08:25"},
    {"bus_id": 128, "stop_id": 7, "stop_name": "Sesame Street", "next_stop": 0, "stop_type": "F", "a_time": "08:37"},
    {"bus_id": 256, "stop_id": 2, "stop_name": "Pilotow Street", "next_stop": 3, "stop_type": "S", "a_time": "09:20"},
    {"bus_id": 256, "stop_id": 3, "stop_name": "Elm Street", "next_stop": 6, "stop_type": "", "a_time": "09:45"},
    {"bus_id": 256, "stop_id": 6, "stop_name": "Abbey Road", "next_stop": 7, "stop_type": "O", "a_time": "09:59"},
    {"bus_id": 256, "stop_id": 7, "stop_name": "Sesame Street", "next_stop": 0, "stop_type": "F", "a_time": "10:12"},
    {"bus_id": 512, "stop_id": 4, "stop_name": "Bourbon Street", "next_stop": 6, "stop_type": "S", "a_time": "08:13"},
    {"bus_id": 512, "stop_id": 6, "stop_name": "Abbey Road", "next_stop": 0, "stop_type": "F", "a_time": "08:16"}]'''

if __name__ == "__main__":
    json_data = json.loads(input())
    # json_data = json.loads(input_data)
    main(json_data)
