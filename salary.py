# -*- coding: UTF-8 -*-
"""
@author: linus
@file: utils_cv.py
@time: 2022/7/19 18:00:00
"""
import re
import json
from zhconv import convert


def get_salary_year_cv(salary):
    """
    获取年薪的数字,以k为单位
    """
    # 转中文简体
    salary = convert(salary, "zh-hans")
    # 转英文小写
    salary = salary.lower()

    # case 10.5k*15.5
    res = re.search(r'(\d+\.*\d*)([k,w])[\*,x, ]+(\d+\.*\d*)', salary)
    if res:
        num1 = float(res.group(1))
        unit = res.group(2)
        num3 = float(res.group(3))
        print(num1, unit, num3)
        salary_year = int(num1 * num3) 
        return salary_year if unit == "k" else 10 * salary_year
    
    # case 10.5*15.5k
    res = re.search(r'(\d+\.*\d*)[\*,x, ]+(\d+\.*\d*)([k,w])', salary)
    if res:
        num1 = float(res.group(1))
        num2 = float(res.group(2))
        unit = res.group(3)
        print(num1, num2, unit)
        salary_year = int(num1 * num2) 
        return salary_year if unit == "k" else 10 * salary_year

    # case 10万/年
    res = re.search(r'(\d+)([万,w,元])/年', salary)
    if res:
        num = float(res.group(1))
        unit = res.group(2)
        salary_year = int(num * 10) if unit in ['万', 'w'] else int(num / 1000)
        return salary_year
    
    # case 10w/月
    res = re.search(r'(\d+)([万,w,元])/月', salary)
    if res:
        num = float(res.group(1))
        unit = res.group(2)
        # 默认12个月
        salary_year = int(num * 10) * 12 if unit in ['万', 'w'] else int(num / 1000) * 12
        return salary_year
 
    # 30k
    res = re.search(r'(\d+)k', salary)
    if res:
        num = float(res.group(1))
        # 默认12个月
        salary_year = int(num * 12)
        return salary_year
    
    # 42万
    res = re.search(r'(\d+)[万,w]', salary)
    if res:
        num = float(res.group(1))
        salary_year = int(num * 10)
        return salary_year

    # 9000元/月*12月
    res = re.search(r'(\d+)元/月[\*,x, ]+(\d+)', salary)
    if res:
        num1 = float(res.group(1))
        num2 = float(res.group(2))
        salary_year = int(num1 * num3 / 1000) 
        return salary_year
    
    # 都没匹配上
    return -1
