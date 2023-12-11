# -*- coding: utf-8 -*-
# @Time    : 2023/6/10 9:17
# @Author  : ChowRunFa
# @File    : api_delete.py
# @Software: PyCharm
from models import *

from flask import Blueprint
api_delete = Blueprint('api_delete', __name__)

# Define the API endpoints for paper deletion
@api_delete.route('/api/del/paper/<id>', methods=['DELETE'])
def delete_paper(id):
    try:
        id = int(id)
    except ValueError:
        return result(400, 'error: ID输入有误，请检查是否为整数！')

    publications = Publication.query.filter_by(id=id).all()
    if  publications:
        for publication in publications:
            db.session.delete(publication)
        db.session.commit()

    paper = Paper.query.get(id)
    if paper is None:
        return result(400,'error：未找到该论文！')

    db.session.delete(paper)
    db.session.commit()

    return result(200, '论文删除成功！')

# Define the API endpoints for project deletion
@api_delete.route('/api/del/project/<string:id>', methods=['DELETE'])
def delete_project(id):
    charges = Charge.query.filter_by(id=id).all()
    # 关闭外键检查
    db.session.execute("SET FOREIGN_KEY_CHECKS = 0")
    if not charges:
        for charge in charges:
            db.session.delete(charge)
        db.session.commit()


    project = Project.query.get(id)
    if project is None:
        return result(400,'error：未找到该项目！')

    db.session.delete(project)
    db.session.commit()
    # 启用外键检查
    db.session.execute("SET FOREIGN_KEY_CHECKS = 1")
    return result(200,'项目删除成功！')

# Define the API endpoints for course deletion
@api_delete.route('/api/del/course/<string:id>', methods=['DELETE'])
def delete_course(id):
    teachings = Teaching.query.filter_by(id=id).all()
    if not teachings:
        for teaching in teachings:
            db.session.delete(teaching)
        db.session.commit()

    course = Course.query.get(id)
    if course is None:
        return result(400,'error：未找到该课程！'), 404

    db.session.delete(course)
    db.session.commit()

    return result(200,'课程删除成功！')