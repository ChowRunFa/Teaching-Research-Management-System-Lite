# -*- coding: utf-8 -*-
# @Time    : 2023/6/10 9:17
# @Author  : ChowRunFa
# @File    : api_update.py
# @Software: PyCharm

from flask import request
from models import *

from utils import paper_code_dict, paper_type_code_dict, project_type_code_dict, str2date, date2int, \
    is_dict_valid, semester_code_dict, property_code_dict
from flask import Blueprint
api_update = Blueprint('api_update', __name__)

@api_update.route('/api/update/paper', methods=['POST'])
def update_paper():
    # 获取论文信息
    # result(400,request.get_json())
    paper_data = request.get_json()["_value"]
    if not is_dict_valid(paper_data):
        return result(400, 'error: 请求数据不完整或不合法')

    paper_modifyId = int(paper_data.get('id'))
    if paper_modifyId < 0:
        return result(400, 'error: 论文序号不合法！')
    paper_originId = paper_data.get('originId')
    if  Paper.query.filter_by(id=paper_modifyId).first() and paper_modifyId != paper_originId:
        return result(400, 'error: 论文序号冲突！')

    paper_title = paper_data.get('title')
    paper_source = paper_data.get('source')
    paper_year = paper_data.get('year')

    paper_year = str2date(paper_year)

    paper_type = paper_data.get('type')
    if paper_type in paper_type_code_dict:
        paper_type = paper_type_code_dict[paper_type]
    paper_level = paper_data.get('level')
    if paper_level in paper_code_dict:
        paper_level = paper_code_dict[paper_level]
    pub_rank = int(paper_data.get('ranking'))
    pub_corresponding = paper_data.get('corresponding')
    if pub_corresponding == 'true':
        pub_corresponding = True
    if pub_corresponding == 'false':
        pub_corresponding = False
    pub_workno = paper_data.get('workno')

    # 检查约束条件
    if not Paper.query.filter_by(id=paper_originId).first():
        return result(400, 'error: 论文不存在')
    if pub_rank <= 0:
        return result(400, 'error: 发表排名必须大于0')
    if not Teacher.query.filter_by(workno=pub_workno).first():
        return result(400, 'error: 作者工号不存在')

    # 查询要更新的论文和相关的发表信息
    paper = Paper.query.get_or_404(paper_originId)
    publication = Publication.query.filter_by(id=paper_originId, workno=pub_workno).first()

    # 查询所有作者信息
    authors = []
    for pub in Publication.query.filter_by(id=paper_originId).all():
        author = Teacher.query.filter_by(workno=pub.workno).first()
        if author:
            authors.append(author)

    # 处理作者信息
    # author_ranks = []  # 存储作者排名
    corresponding_author_count = 0  # 计数器，统计通讯作者数量
    corresponding_workno = -1
    for author in authors:
        author_rank = Publication.query.filter_by(id=paper_originId, workno=author.workno).first().ranking
        author_corresponding = Publication.query.filter_by(id=paper_originId, workno=author.workno).first().corresponding
        if pub_rank == author_rank and author.workno != pub_workno:
            return result(400, 'error: 作者排名不能重复')
        # author_ranks.append(author_rank)
        if author_corresponding:
            corresponding_workno = author.workno
            corresponding_author_count += 1
    if corresponding_author_count != 0 and corresponding_workno != pub_workno and pub_corresponding:
        return result(400, 'error: 只能有一位通讯作者')

    # 关闭外键检查
    db.session.execute("SET FOREIGN_KEY_CHECKS = 0")

    # 更新论文信息
    paper.id = paper_modifyId
    paper.title = paper_title
    paper.source = paper_source
    paper.year = paper_year
    paper.type = paper_type
    paper.level = paper_level

    # 更新发表信息
    if publication:
        publication.id = paper_modifyId
        publication.ranking = pub_rank
        publication.corresponding = pub_corresponding
    else:
        return result(400, 'error: 该论文未登记，请先新建论文信息！')


    # 提交更改
    db.session.commit()

    # 启用外键检查
    db.session.execute("SET FOREIGN_KEY_CHECKS = 1")

    return result(200, 'success: 修改成功')

@api_update.route('/api/update/project', methods=['POST'])
def update_project():
    # 获取project信息
    project_data = request.get_json()['_value']
    print("project_data:",project_data)
    if not is_dict_valid(project_data):
        return result(400, 'error: 请求数据不完整或不合法')


    project_modifyId = project_data.get('id')
    if project_modifyId == "":
        return result(400, 'error: 项目号不合法！')

    project_originId = project_data.get('originId')
    if  Project.query.filter_by(id=project_modifyId).first() and project_modifyId != project_originId:
        return result(400, 'error: 项目号冲突！'+Project.query.filter_by(id=project_originId).first().id)
    if not Project.query.filter_by(id=project_originId).first():
        return result(400, 'error: 项目不存在')

    project_name = project_data.get('name')
    if project_name == "":
        return result(400, 'error: 项目名不合法！')

    project_modifyTotalfund = float(project_data.get('totalfund'))
    if project_modifyTotalfund <= 0:
        return result(400, 'error: 总经费太少了！想白嫖啊？！')

    charge_modifyFund = float(project_data.get('fund'))
    if charge_modifyFund <= 0:
        return result(400, 'error: 经费太少了！打黑工啊？！')
    #
    # project_originFund = float(project_data.get('originFund'))


    project_source = project_data.get('source')
    if project_source == "":
        return result(400, 'error: 项目来源为空！')

    project_type = project_data.get('type')
    if project_type == "":
        return result(400, 'error: 项目类型为空！')
    if project_type in project_type_code_dict:
        project_type = project_type_code_dict[project_type]
    valid_types = [1, 2, 3, 4, 5]
    if project_type not in valid_types:
        return result(400, 'error: 项目类型不合法！')

    project_startyear = project_data.get('startyear')
    # project_startyear = str2date(project_startyear)
    project_startyear = date2int(str(str2date(project_startyear)))+1

    project_endyear = project_data.get('endyear')
    project_endyear = date2int(str(str2date(project_endyear)))+1

    if project_startyear > project_endyear:
        return result(400, 'error: 立项时间应该早于结项时间')

    charge_workno = project_data.get('workno')
    if not Teacher.query.filter_by(workno=charge_workno).first():
        return result(400, 'error: 教工工号不存在')

    charge_ranking = int(project_data.get('ranking'))
    if charge_ranking <= 0:
        return result(400, 'error: 排名必须大于0')


    # 查询要更新的project和相关的charge信息
    project = Project.query.get_or_404(project_originId)
    charge = Charge.query.filter_by(id=project_originId, workno=charge_workno).first()

    # 查询所有作者信息
    authors = []
    for cha in Charge.query.filter_by(id=project_originId).all():
        author = Teacher.query.filter_by(workno=cha.workno).first()
        if author:
            authors.append(author)

    fundSum = 0
    for author in authors:
        author_ranking = Charge.query.filter_by(id=project_originId, workno=author.workno).first().ranking

        if author.workno != charge_workno:
            fundSum += Charge.query.filter_by\
                (id=project_originId, workno=author.workno).first().fund

        if fundSum + charge_modifyFund != project_modifyTotalfund:
            return result(400, 'error: 所有教师承担经费之和不等于总经费！')

        if charge_ranking == author_ranking and author.workno != charge_workno:
            return result(400, 'error: 作者排名不能重复')


    # 关闭外键检查
    db.session.execute("SET FOREIGN_KEY_CHECKS = 0")

    # 更新论文信息
    project.id = project_modifyId
    project.type = project_type
    project.name = project_name
    project.totalfund = project_modifyTotalfund
    project.source = project_source
    project.startyear = project_startyear
    project.endyear = project_endyear

    # 更新发表信息
    if charge:
        charge.id = project_modifyId
        charge.ranking = charge_ranking
        charge.fund = charge_modifyFund
    else:
        return result(400, 'error: 该项目未登记，请先新建项目信息！')

    # 提交更改
    db.session.commit()
    # 启用外键检查
    db.session.execute("SET FOREIGN_KEY_CHECKS = 1")

    return result(200,'success: 修改成功')

@api_update.route('/api/update/course', methods=['POST'])
def update_course():
    # 获取project信息
    course_data = request.get_json()['_value']
    print("course_data:",course_data)
    if not is_dict_valid(course_data):
        return result(400, 'error: 请求数据不完整或不合法')

    originId = course_data['originId']
    modifyId = course_data['id']
    name = course_data['name']
    modifyHours = int(course_data['hours'])
    modifyPartHours = int(course_data['parthours'])
    property = course_data['property']
    semester = course_data['semester']
    year = course_data['year']
    workno = course_data['workno']


    year = date2int(str(str2date(year)))+1
    if property in property_code_dict:
        property = property_code_dict[property]
    if semester in semester_code_dict:
        semester = semester_code_dict[semester]

    if modifyId == "":
        return result(400, 'error: 课程号为空！')
    if name == "":
        return result(400, 'error: 课程名为空！')

    if Course.query.filter_by(id=modifyId).first() and modifyId != originId:
        return result(400, 'error: 课程号冲突！' + Course.query.filter_by(id=originId).first().id)
    if not Course.query.filter_by(id=originId).first():
        return result(400, 'error: 课程不存在')
    if modifyHours <=0:
        return result(400, 'error: 总学时这么少？我也要选这个课！')
    if modifyPartHours <0:
        return result(400, 'error: 承担学时这么少？你是校长还是院长？！')

    # 查询所有任课教师信息
    authors = []
    for tea in Teaching.query.filter_by(id=originId,semester = semester,year = year).all():
        author = Teacher.query.filter_by(workno=tea.workno).first()
        if author:
            authors.append(author)
    print("authors:",authors)
    hoursSum = 0
    for author in authors:
        # author_ranking = Teaching.query.filter_by(id=originId, workno=author.workno).first().ranking

        if author.workno != workno:
            hoursSum += Teaching.query.filter_by\
                (id=originId, workno=author.workno).first().hours

    if hoursSum + modifyPartHours > modifyHours:
        return result(400, 'error: 所有教师承担学时之和超出了总学时！')

    if hoursSum + modifyPartHours < modifyHours:
        return result(400, 'error: 所有教师承担学时之和小于总学时！')

    # 查询要更新的project和相关的charge信息
    course = Course.query.get_or_404(originId)
    teaching = Teaching.query.filter_by(id=originId, workno=workno).first()
    # 关闭外键检查
    db.session.execute("SET FOREIGN_KEY_CHECKS = 0")

    # 更新课程信息
    course.id = modifyId
    course.name = name
    course.hours = modifyHours
    course.property = property


    # 更新发表信息
    if teaching:
        teaching.id = modifyId
        teaching.hours = modifyPartHours
        teaching.year = year
        teaching.semester = semester
    else:
        return result(400, 'error: 该课程未登记，请先新建项目信息！')

    # 提交更改
    db.session.commit()
    # 启用外键检查
    db.session.execute("SET FOREIGN_KEY_CHECKS = 1")


    return result(200,'课程信息更新成功！')