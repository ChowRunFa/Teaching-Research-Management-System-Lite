# -*- coding: utf-8 -*-
# @Time    : 2023/6/10 9:16
# @Author  : ChowRunFa
# @File    : api_create.py
# @Software: PyCharm
from dateutil.parser import parse
from flask import request
from models import *

from flask import Blueprint

from utils import remove_quotes_and_spaces, is_dict_valid, date2int, str2date

api_create = Blueprint('api_create', __name__)

@api_create.route('/api/add/paper', methods=['POST'])
def add_paper():
    data = request.get_json()
    if not is_dict_valid(data):
        return result(400, 'error: 请求数据不完整或不合法')

    id = int(data['id'])
    if id < 0:
        return result(400, 'error: 论文序号应该是一个正整数')

    title = remove_quotes_and_spaces(data['title'])
    source = data['source']
    # year = datetime.datetime(data['year'], 1, 1).strftime('%Y-%m-%d')
    year = parse(data['year']).strftime('%Y-%m-%d')
    type = data['type']
    level = data['level']
    authors = data['authors']
    corresponding_author = data['corresponding_author']

    if Paper.query.filter_by(id=id).first() is not None:
        return result(400,'error :Paper with id {} already exists'.format(id))

    # Check if the corresponding author is in the authors list
    if corresponding_author not in authors:
        return result(400,'error: 通信作者应该是所有作者之一')

    # Check if author rankings are unique
    if len(set([author['ranking'] for author in authors])) != len(authors):
        return result(400, 'error: Author rankings must be unique.')

    # Check if the paper type and level are valid
    valid_types = [1, 2, 3, 4]
    valid_levels = [1, 2, 3, 4, 5, 6]
    type = int(type)
    level = int(level)
    id = int(id)
    if  type not in valid_types:
        return result(400,f'error: Paper type must be one of {valid_types}.')
    if  level not in valid_levels:
        return result(400,f'error: Paper level must be one of {valid_levels}.')


# Create the paper object and save it to the database
    paper = Paper(id=id,title=title, source=source, year=year, type=type, level=level)
    db.session.add(paper)
    db.session.commit()

    # Create the publication objects and save them to the database
    for author in authors:
        publication = Publication(id=id,workno=author['workno'], ranking=author['ranking'], corresponding=(author['workno'] == corresponding_author))
        db.session.add(publication)
    db.session.commit()

    return result(200,'Paper registered successfully.'), 201

# Define the API endpoints for course registration
@api_create.route('/api/add/course', methods=['POST'])
def add_course():
    data = request.get_json()
    if not is_dict_valid(data):
        return result(400, 'error: 请求数据不完整或不合法')

    id = data['id']
    name = remove_quotes_and_spaces(data['name'])

    hours = data['hours']
    property = data['property']
    teachings = data['teachings']

    # Check if the total hours is equal to the sum of teachings
    if hours != sum([teaching['hours'] for teaching in teachings]):
        return result(100,'The total hours must be equal to the sum of teachings.',{})

    # Check if the semester is valid
    valid_semesters = [1, 2, 3]
    for teaching in teachings:
        if teaching['semester'] not in valid_semesters:
            return result(400, f'Teaching semester must be one of {valid_semesters}.',{}), 400

    # Create the course object and save it to the database
    course = Course(id=id, name=name, hours=hours, property=property)
    # db.session.add(course)
    # db.session.commit()

    # Create the teaching objects and save them to the database
    for teaching in teachings:
        teaching_obj = Teaching(workno=teaching['workno'], id=course.id, year=teaching['year'], semester=teaching['semester'], hours=teaching['hours'])
        db.session.add(teaching_obj)
    db.session.commit()

    return result(200,'Course registered successfully.',{}), 201

# Define the API endpoints for project registration
@api_create.route('/api/add/project', methods=['POST'])
def add_project():
    data = request.get_json()
    print(data)
    if not is_dict_valid(data):
        return result(400, 'error: 请求数据不完整或不合法')

    id = data['id']
    name = remove_quotes_and_spaces(data['name'])
    source = data['source']
    type = int(data['type'])
    totalfund = int(data['totalfund'])
    startyear = data['startyear']
    startyear = date2int(str(str2date(startyear)))+1
    endyear = data['endyear']
    endyear = date2int(str(str2date(endyear)))+1
    charges = data['charges']

    # Check if charge rankings are unique
    if len(set([charge['ranking'] for charge in charges])) != len(charges):
        # return jsonify({'error': 'Charge rankings must be unique.'}), 400
        return result(400,'error: 教师的排名不能重复！')

    # Check if the total fund is equal to the sum of charges
    if totalfund != sum([charge['fund'] for charge in charges]):
        return result(400,'error: 教师的经费之和应该等于项目总经费！')

    # Check if the project type is valid
    valid_types = [1, 2, 3, 4, 5]
    if type not in valid_types:
        return result(400, f'error: 项目类型必须是{valid_types}之一.')

    # Create the project object and save it to the database
    project = Project(id=id,name=name, source=source, type=type, totalfund=totalfund, startyear=startyear, endyear=endyear)
    db.session.add(project)
    db.session.commit()

    # Create the charge objects and save them to the database
    for charge in charges:
        charge_obj = Charge(workno=charge['workno'], id=project.id, ranking=charge['ranking'], fund=charge['fund'])
        db.session.add(charge_obj)
    db.session.commit()

    return result(200, 'Project registered successfully.',{})

@api_create.route('/api/new/course', methods=['POST'])
def new_course():
    data = request.get_json()
    if not is_dict_valid(data):
        return result(400, 'error: 请求数据不完整或不合法')

    id = data['id']
    name = data['name']
    hours = data['hours']
    property = data['property']

    if Course.query.filter_by(id=id).first() is not None:
        return result(400,'error :课程 {} 已经存在！请勿重复添加！'.format(id))


    course = Course(id=id, name=name, hours=hours, property=property)
    db.session.add(course)
    db.session.commit()

    return result(200,'Course {} Created Successfully'.format(name))

@api_create.route('/api/new/teacher', methods=['POST'])
def new_teacher():
    data = request.get_json()
    if not is_dict_valid(data):
        return result(400, 'error: 请求数据不完整或不合法')

    workno = data['workno']
    name = data['name']
    gender = data['gender']
    level = data['level']
    if Teacher.query.filter_by(workno=workno).first() is not None:
        return result(400,'error :Teacher with workno {} already exists'.format(id))

    # Check if the Teacher level are valid

    valid_levels = [1, 2, 3, 4, 5, 6,7 ,8 ,9, 10,11]
    level = int(level)

    if  level not in valid_levels:
        return result(400,f'error: Teacher level must be one of {valid_levels}.')

# Create the teacher object and save it to the database
    teacher = Teacher(workno = workno, name=name,gender=gender,level=level)
    db.session.add(teacher)
    db.session.commit()

    return result(200,'Teacher registered successfully.'), 201



