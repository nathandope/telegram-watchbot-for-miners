# -*- coding: utf-8 -*-
import requests
import json
import config
import logging
import time


def request(host_name):
    try:
        response = requests.get(host_name)
        response.raise_for_status()

    except requests.exceptions.ConnectTimeout as err:
        logging.error(err)
        time.sleep(5)
        print(config.current_time() + ' Connection timeout occurred!')
        response_list = 'Connection timeout occurred!'

    except requests.exceptions.ConnectionError as err:
        logging.error(err)
        time.sleep(5)
        print(config.current_time() + ' Connection error occurred!')
        response_list = 'Connection error occurred!'

    except requests.exceptions.HTTPError as err:
        logging.error(err)
        time.sleep(5)
        print(config.current_time() + ' HTTP error occurred!')
        response_list = 'HTTP error occurred!'

    except requests.exceptions.ReadTimeout as err:
        logging.error(err)
        time.sleep(5)
        print(config.current_time() + ' Read time out!')
        response_list = 'Read time out!'

    else:
        response = response.json()
        response = json.dumps(response, separators=(',', ':'))
        response = response[response.find('[', 0, -1): -1]
        response_list = json.loads(response)

    return response_list


def gpu_count(host_name):
    response_list = request(host_name)

    if type(response_list) is str:
        return 0
    else:
        return len(response_list)


def complete_report(host_name, gpu_amount):
    response_list = request(host_name)
    result_str = ''

    if type(response_list) is str:
        result_str = response_list
    else:
        for key, value in response_list[gpu_amount].items():
            result_str = result_str + str(key) + ': ' + str(value) + '\n'

        result_str = 'Current status:\n' + result_str

    return result_str


def quick_report(host_name, parameter, measures, gpu_amount):
    response_list = request(host_name)
    result_str = ''

    if type(response_list) is str:
        result_str = response_list
    else:
        sum_value = 0
        sum_str = 'Sum:'
        av_str = 'Avr:'

        for d in response_list:
            result_str = result_str + str(d.get(parameter)) + '\t\t'
            sum_value += d.get(parameter)

        av_value = round((sum_value / gpu_amount), 2)

        result_str = parameter.capitalize() + ', ' + measures + ':\n' + result_str + '\n' + sum_str + ' ' +\
                     str(sum_value) + '\n' + av_str + ' ' + str(av_value)

    return result_str


def watching(host_name, parameter, param_measures, value):
    response_list = request(host_name)
    result_str = ''

    if type(response_list) is str:
        result_str = response_list
    else:
        for d in response_list:
            if (parameter == 'temperature' and d.get(parameter) >= value) or \
                    (parameter == 'speed_sps' and d.get(parameter) == value):
                result_str = result_str + 'GPU ' + str(d.get('gpuid')) + ':  ' + \
                             str(d.get(parameter)) + ' ' + param_measures.get(parameter) + '\n'

        if len(result_str) > 0:
            result_str = 'Warning!\n' + result_str

    return result_str
