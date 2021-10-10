import configparser
import datetime
import json
import os
import sys
import time
from distutils.util import strtobool

import jsonpath
import requests
from dateutil.relativedelta import relativedelta
from google.protobuf.json_format import MessageToJson

from bili_pb2 import DmSegMobileReply


class Config:

    def SlowRequestRank(rank):
        ranks = {
            1: 0.5,
            2: 2.0,
            3: 10.0,
            4: 60.0,
            5: 300.0
        }
        return ranks.get(rank, None)

    config = configparser.RawConfigParser()
    config_path = "./config/user.ini" if os.path.exists("./config/user.ini") else "./config/default.ini"
    try:
        config.read(config_path)
    except Exception as e:
        print("\033[5;31;47m 配置文件丢失，%s \033[0m" % e)
        sys.exit()
    try:
        cookies = config.get("users", "cookie")
        user_agent = config.get("user-agent", "user-agent")
        bv = config.get("options", "bv")
        start_date = datetime.datetime.date(datetime.datetime.now()) if str(
            config.get("options", "end-date")) == "" else (datetime.datetime.date(
            datetime.datetime.strptime(config.get("options", "start-date"), "%Y-%m-%d")) if datetime.datetime.date(
            datetime.datetime.now()) > datetime.datetime.date(
            datetime.datetime.strptime(config.get("options", "start-date"), "%Y-%m-%d")) else datetime.datetime.date(
            datetime.datetime.now()))
        end_date = datetime.datetime.date(datetime.datetime.now()) if str(
            config.get("options", "end-date")) == "" else (datetime.datetime.date(
            datetime.datetime.strptime(config.get("options", "end-date"), "%Y-%m-%d")) if datetime.datetime.date(
            datetime.datetime.now()) > datetime.datetime.date(
            datetime.datetime.strptime(config.get("options", "end-date"), "%Y-%m-%d")) else datetime.datetime.date(
            datetime.datetime.now()))
        if start_date > end_date:
            temp_date = start_date
            start_date = end_date
            end_date = temp_date
        headers = {
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "cookie": str(cookies),
            "origin": "https://www.bilibili.com",
            "referer": f"https://www.bilibili.com/video/{bv}",
            "user-agent": str(user_agent),
        }
        response = requests.get(url=f"https://api.bilibili.com/x/player/pagelist?bvid={bv}&jsonp=jsonp")
        oid = response.json()["data"][0]["cid"]
        switch_default = ["DEFAULT", "Default", "default", "D", "d", ""]
        JOSN_output_switch = False if config.get("switch", "JSON-output-switch") in switch_default else strtobool(
            config.get("switch", "JSON-output-switch"))
        bs_output_switch = True if config.get("switch", "BulletScreen-output-switch") in switch_default else strtobool(
            config.get("switch", "BulletScreen-output-switch"))
        data_save_model = True if config.get("switch",
                                             "DataSaveModel-DailyMonthly-switch") in switch_default else strtobool(
            config.get("switch", "DataSaveModel-DailyMonthly-switch"))
        AllInOne_switch = False if config.get("switch", "AllInOne-switch") in switch_default else strtobool(
            config.get("switch", "AllInOne-switch"))
        date_debug_switch = True if config.get("switch", "date-debug-switch") in switch_default else strtobool(
            config.get("switch", "date-debug-switch"))
        SlowRequest = True if config.get("switch", "SlowRequest-switch") in switch_default else strtobool(
            config.get("switch", "SlowRequest-switch"))
        SlowRank = SlowRequestRank(3) if config.get("options", "SlowRank") in switch_default else SlowRequestRank(
            int(config.get("options", "SlowRank")) if int(config.get("options", "SlowRank")) >= 1 and int(
                config.get("options", "SlowRank")) <= 5 else (1 if int(config.get("options", "SlowRank")) < 1 else 5))
        loop_flag = True
        if date_debug_switch:
            if datetime.datetime.date(datetime.datetime.now()) < (datetime.datetime.date(
                    datetime.datetime.strptime(config.get("options", "end-date"),
                                               "%Y-%m-%d")) if datetime.datetime.date(
                    datetime.datetime.strptime(config.get("options", "start-date"),
                                               "%Y-%m-%d")) < datetime.datetime.date(
                    datetime.datetime.strptime(config.get("options", "end-date"),
                                               "%Y-%m-%d")) else datetime.datetime.date(
                    datetime.datetime.strptime(config.get("options", "start-date"), "%Y-%m-%d"))):
                print(
                    f"\033[1;33;47m 用户定义的最大时间超过当前时间，最大时间默认返回当前日期：{datetime.datetime.date(datetime.datetime.now())} \033[0m\n")
    except Exception as e:
        print("\033[5;31;47m 配置错误，请检查配置填写格式，%s \033[0m" % e)
        sys.exit()

    def __init__(self, cookies, user_agent, start_date, end_date, bv, oid, JOSN_output_switch, bs_output_switch,
                 data_save_model, AllInOne_switch, date_debug_switch, SlowRequest, SlowRank, loop_flag):
        self.cookies = cookies
        self.user_agent = user_agent
        self.start_date = start_date
        self.end_date = end_date
        self.bv = bv
        self.oid = oid
        self.JOSN_output_switch = JOSN_output_switch
        self.bs_output_switch = bs_output_switch
        self.data_save_model = data_save_model
        self.AllInOne_switch = AllInOne_switch
        self.date_debug_switch = date_debug_switch
        self.SlowRequest = SlowRequest
        self.SlowRank = SlowRank
        self.loop_flag = loop_flag


def get_response(html_url):
    headers = Config.headers
    response = requests.get(url=html_url, headers=headers)
    try:
        if str(response.json()["code"]) == "-509":
            print("\033[1;31;40m 请求过于频繁，请稍后再试 \033[0m")
            Config.loop_flag = False
    except Exception as e:
        if Config.date_debug_switch:
            print("\033[5;32;40m seg.so接口数据返回正常，未出现错误 \033[0m")
    return response


def date_begin_clear(dates):
    dates_clear = dates
    if datetime.datetime.date(datetime.datetime.strptime(dates[0], "%Y-%m-%d")) < Config.start_date:
        if Config.date_debug_switch:
            print(f"\033[1;34;47m Warning:(month)api接口返回的最小日期小于用户设定的开始日期\"{dates[0]}\"，从日期列表删除\"{dates[0]}\" \033[0m")
        if len(dates) != 1:
            dates_clear = date_begin_clear(dates[1:len(dates)])
        else:
            dates_clear = None
    elif datetime.datetime.date(datetime.datetime.strptime(dates[0], "%Y-%m-%d")) > Config.start_date:
        Config.start_date = Config.start_date + datetime.timedelta(days=1)
        if Config.date_debug_switch:
            print(f"\033[1;34;47m Warning:(month)api接口未返回用户设定的开始日期\"{dates[0]}\"，开始日期后移1天 \033[0m")
        dates_clear = date_begin_clear(dates)
    elif datetime.datetime.date(datetime.datetime.strptime(dates[0], "%Y-%m-%d")) == Config.start_date:
        dates_clear = dates
    return dates_clear


def date_end_clear(dates):
    dates_clear = dates
    if datetime.datetime.date(datetime.datetime.strptime(dates[-1], "%Y-%m-%d")) > Config.end_date:
        if Config.date_debug_switch:
            print(f"\033[1;34;47m Warning:(month)api接口返回的最大日期大于用户设定的结束日期\"{dates[-1]}\"，从日期列表删除\"{dates[-1]}\" \033[0m")
        dates_clear = date_end_clear(dates[0:len(dates) - 1])
    elif datetime.datetime.date(datetime.datetime.strptime(dates[-1], "%Y-%m-%d")) < Config.start_date:
        if Config.date_debug_switch:
            print(f"\033[1;34;47m Warning:(month)api接口未返回用户设定的结束日期\"{dates[-1]}\"，结束日期前移1天 \033[0m")
        Config.end_date = Config.end_date + datetime.timedelta(days=-1)
        if len(dates) != 1:
            dates_clear = date_end_clear(dates[0:len(dates) - 1])
        else:
            dates_clear = None
    elif datetime.datetime.date(datetime.datetime.strptime(dates[-1], "%Y-%m-%d")) == Config.end_date:
        dates_clear = dates
    return dates_clear


def get_date(html_url, loop, max_loop):
    response = get_response(html_url)
    if response.json()["code"] == "-509":
        print("\033[1;31;47m 请求过于频繁，请稍后再试 \033[0m")
        Config.loop_flag = False
    dates_clear = response.json()["data"]
    if dates_clear is None:
        Config.loop_flag = False
    if loop == 1 and dates_clear is not None:
        Config.loop_flag = True
        dates_clear = date_begin_clear(dates_clear)
    if (loop == (max_loop + 1) or (max_loop == 0)) and dates_clear is not None:
        if Config.date_debug_switch:
            print("\n")
        dates_clear = date_end_clear(dates_clear)
    else:
        pass

    return dates_clear


def main(html_url, loop, max_loop):
    dates = get_date(html_url, loop, max_loop)
    if dates is None:
        return False
    else:
        if Config.date_debug_switch:
            print(f"\n日期列表\n{dates}")
        for date in dates:
            if Config.SlowRequest:
                if Config.date_debug_switch:
                    print(f"线程暂停{Config.SlowRank}秒钟")
                time.sleep(Config.SlowRank)  # 延时访问,由低到高5个等级
            url = f'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={Config.oid}&date={date}'
            html_data = get_response(url).content
            decode_data = DmSegMobileReply()
            decode_data.ParseFromString(html_data)
            contents = jsonpath.jsonpath(json.loads(MessageToJson(decode_data)), '$..content')

            JSON_save_path = f"./data/JSON/[oid]({Config.oid}) [bv]({Config.bv}){'' if Config.AllInOne_switch else ('' if not Config.data_save_model else str(f'/{date[0:7]}'))}"
            contents_save_path = f"./data/contents/[oid]({Config.oid}) [bv]({Config.bv}){'' if Config.AllInOne_switch else ('' if not Config.data_save_model else str(f'/{date[0:7]}'))}"

            if Config.JOSN_output_switch:
                True and os.path.exists(JSON_save_path) or os.makedirs(JSON_save_path)
                with open(
                        f"{JSON_save_path}/JSON_{Config.oid}{str('_all') if Config.AllInOne_switch else (str(f'_{date}') if Config.data_save_model else str(f'{date[0:7]}'))}.json",
                        "a", encoding="utf-8") as f1:
                    f1.write(json.dumps(json.loads(MessageToJson(decode_data)), ensure_ascii=False, indent=4))

            if Config.bs_output_switch:
                True and os.path.exists(contents_save_path) or os.makedirs(contents_save_path)
                with open(
                        f"{contents_save_path}/contents_{Config.oid}{str('_all') if Config.AllInOne_switch else (str(f'_{date}') if Config.data_save_model else str(f'{date[0:7]}'))}.txt",
                        "a", encoding="utf-8") as f2:
                    for content in contents[0:len(contents) - 1]:
                        f2.write(f"{content}\n")
                    f2.write(f"{contents[-1]}")

        return True


if __name__ == '__main__':
    months = (Config.end_date.year - Config.start_date.year) * 12 + Config.end_date.month - Config.start_date.month
    month_range = ['%s-%s' % (Config.start_date.year + mon // 12, mon % 12 + 1) for mon in
                   range(Config.start_date.month - 1, Config.start_date.month + months)]
    count_month = 1
    for month in month_range:
        if count_month != 1:
            if Config.SlowRequest:
                if Config.date_debug_switch:
                    print(f"线程暂停{Config.SlowRank}秒钟")
                time.sleep(Config.SlowRank)  # 延时访问,由低到高5个等级
        months_url = f'https://api.bilibili.com/x/v2/dm/history/index?type=1&oid={Config.oid}&month={str(month[0:4])}{int(month[5:7]) >= 10 and str(f"-{month[5:7]}") or str(f"-0{month[-1]}")}'
        if main(months_url, count_month, months) is False:
            if Config.loop_flag is False:
                if count_month == 1 and months != 0:
                    months = months - 1
                    if Config.date_debug_switch:
                        print(
                            f"\033[1;33;47m 当前定义的开始日期所在月份（{Config.start_date.year}年{Config.start_date.month}月）接口返回值为空，开始日期后移至下个月1日 \033[0m")
                    Config.start_date = Config.start_date + datetime.timedelta(
                        days=1 - int(Config.start_date.day)) + relativedelta(months=1)
                    continue
                elif count_month == 1 and months == 0:
                    print("\033[1;31;47m 用户定义的时间区间小于接口区间，请修改时间区间 \033[0m")
                    break
        else:
            count_month = count_month + 1
