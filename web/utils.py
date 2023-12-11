import datetime
import hashlib
import re
import time
import simplejson as json#pip install simplejson 或者 pip install python-simplejson
import base64
import hmac
from dateutil.parser import parse

level_dict = {
    1: "博士后",
    2: "助教",
    3: "讲师",
    4: "副教授",
    5: "特任教授",
    6: "教授",
    7: "助理研究员",
    8: "特任副研究员",
    9: "副研究员",
    10: "特任研究员",
    11: "研究员"
}

semester_dict = {
    1: "春季学期",
    2: "夏季学期",
    3: "秋季学期"
}

property_dict = {
    1: "必修",
    2: "选修",
    3: "公选",
    4: "通识"
}

semester_code_dict = {
    "春季学期": 1,
    "夏季学期": 2,
    "秋季学期": 3
}

property_code_dict = {
    "必修": 1,
    "选修": 2,
    "公选": 3,
    "通识": 4
}

paper_level_dict = {
    1: "CCF-A",
    2: "CCF-B",
    3: "CCF-C",
    4: "中文 CCF-A",
    5: "中文 CCF-B",
    6: "无级别"
}

paper_code_dict = {
    "CCF-A": 1,
    "CCF-B": 2,
    "CCF-C": 3,
    "中文CCF-A": 4,
    "中文CCF-B": 5,
    "无级别": 6
}

paper_type_dict = {
    1: "full paper",
    2: "short paper",
    3: "poster paper",
    4: "demo paper"
}

paper_type_code_dict = {
    "full paper": 1,
    "short paper": 2,
    "poster paper": 3,
    "demo paper": 4
}

project_type_dict = {
    1: "国家级项目",
    2: "省部级项目",
    3: "市厅级项目",
    4: "企业合作项目",
    5: "其它类型项目"
}

project_type_code_dict = {
    "国家级项目": 1,
    "省部级项目": 2,
    "市厅级项目": 3,
    "企业合作项目": 4,
    "其它类型项目": 5
}

def is_dict_valid(dict_obj):
    return all(value is not None and value != '' for value in dict_obj.values())

def remove_quotes_and_spaces(string):
    string = string.strip()
    string = re.sub(r'^[\'"]+|[\'"]+$', '', string)
    return string

def filter_props(obj):
    return {k: v for k, v in vars(obj).items() if not k.startswith("_sa_")}

def filter_props_date(obj):
    date_format = "%Y" # modify the date format as needed
    props = {}
    for k, v in vars(obj).items():
        if k.startswith("_sa_"):
            continue
        elif isinstance(v, datetime.date):
            props[k] = v.strftime(date_format)
        else:
            props[k] = v
    return props

def str2date(str_year):
    if len(str_year) == 4:
        return datetime.date.fromisoformat(str_year + '-01-01')
    else:
        return datetime.date.fromisoformat(str(re.search(re.compile(r'\d{4}'), str_year).group()) + '-01-01')

def date2int(date_str):
    return int(parse(date_str).strftime('%Y'))


def md5(m):
    return hashlib.md5(m.encode()).hexdigest()

def getNowDataTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

def getTimeStamp():
    return time.time()

def getOrderNum():
    orderNum = str(getTimeStamp()).replace('.','')
    return orderNum

def convert_data(all_items):
    modify_items = []
    for items in all_items:
        items["level"] = level_dict.get(items["level"], "")
        for course in items.get("courseInfo", []):
            course["semester"] = semester_dict.get(course.get("semester", ""), "")
            course["property"] = property_dict.get(course.get("property", ""), "")
        for paper in items.get("paperInfo", []):
            paper["level"] = paper_level_dict.get(paper.get("level", ""), "")
            paper["type"] = paper_type_dict.get(paper.get("type", ""), "")
        for project in items.get("projectInfo", []):
            project["type"] = project_type_dict.get(project.get("type", ""), "")
        modify_items.append(items)

    return modify_items

#生成token 入参：用户id
def generate_token(key, expire=3600):
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr  = hmac.new(key.encode("utf-8"),ts_byte,'sha1').hexdigest()
    token = ts_str+':'+sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")

#验证token 入参：用户id 和 token
def certify_token(key, token):
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        # token expired
        return False
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"),ts_str.encode('utf-8'),'sha1')
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        # token certification failed
        return False
    # token certification success
    return True

