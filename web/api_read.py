# -*- coding: utf-8 -*-
# @Time    : 2023/6/10 9:17
# @Author  : ChowRunFa
# @File    : api_read.py
# @Software: PyCharm
from flask import  request

from sqlalchemy import extract, and_
from models import *
import re
from utils import convert_data, filter_props, filter_props_date
from flask import Blueprint
api_read = Blueprint('api_read', __name__)


@api_read.route('/api/teaching/<string:id>', methods=['GET'])
def get_teachings_by_course(id):
    course = Course.query.get(id)
    if not course:
        return result(400, 'Course not found.'), 404

    teachings = db.session.query(Teaching, Teacher.name, Teacher.gender, Teacher.level)\
                .join(Teacher, Teaching.workno == Teacher.workno)\
                .filter(Teaching.id == id)\
                .all()

    totalhours = Course.query.get(id).hours


    result_list = []
    for teaching, name, gender, level in teachings:
        result_list.append({
            'workno': teaching.workno,
            'name': name,
            'gender': gender,
            'level': level,
            'semester': teaching.semester,
            'year': teaching.year,
            'hours': teaching.hours
        })

    return result(200, 'Teachings found.', {'totalhours':totalhours,'teachings': result_list})

@api_read.route('/api/charge/<string:id>', methods=['GET'])
def get_project_charges(id):
    charges = db.session.query(Charge, Teacher.name, Teacher.gender, Teacher.level)\
                .join(Teacher, Charge.workno == Teacher.workno)\
                .filter(Charge.id == id)\
                .all()
    if not Project.query.get(id):
        return result(400,"error:查无此项目！")

    if not charges:
        return result(400,"error:该项目无参与人员！")

    totalfund = Project.query.get(id).totalfund


    result_list = []
    for charge, name, gender, level in charges:
        result_list.append({
            'workno': charge.workno,
            'name': name,
            'gender': gender,
            'level': level,
            'ranking': charge.ranking,
            'fund': charge.fund
        })

    return result(200, 'Project charges found.', {'totalfund':totalfund,'charges': result_list})

@api_read.route('/api/publication/<int:id>', methods=['GET'])
def get_paper_publication(id):
    publications = db.session.query(Publication, Teacher.name, Teacher.gender, Teacher.level)\
                .join(Teacher, Publication.workno == Teacher.workno)\
                .filter(Publication.id == id)\
                .all()
    paper =  filter_props_date(Paper.query.get(id))


    result_list = []
    for publication, name, gender, level in publications:
        result_list.append({
            'workno': publication.workno,
            'name': name,
            'gender': gender,
            'level': level,
            'ranking': publication.ranking,
            'corresponding': publication.corresponding
        })

    return result(200, 'Paper Publication found.', {'paperInfo':paper,'publication': result_list})



@api_read.route("/api/teacherInfo",methods=["GET"])
def getTeacherInfo():
        Teachers = Teacher.query.all()
        items = []
        for teacher in Teachers:
            teacherno = teacher.workno
            teacher = teacher.__dict__
            del teacher['_sa_instance_state']
            #老师的基础信息

            # 获取老师教授的所有课程号和学期信息
            teaching_list = Teaching.query.filter(Teaching.workno == teacherno).all()
            course_semester = {teaching.id: teaching.semester for teaching in teaching_list}
            course_parthours = {teaching.id: teaching.hours for teaching in teaching_list}
            course_year = {teaching.id: teaching.year for teaching in teaching_list}

            # 根据课程号获取对应的课程信息
            courseIds = [teaching.id for teaching in teaching_list]
            courses = Course.query.filter(Course.id.in_(courseIds)).all()

            courses_dict = []
            if len(courses) > 0:
                for course in courses:
                    course_dict = filter_props(course)
                    if course.id in course_semester:
                        course_dict["semester"] = course_semester[course.id]
                        course_dict["year"] = course_year[course.id]
                        course_dict["parthours"] = course_parthours[course.id]
                    # del course_dict['property']
                    courses_dict.append(course_dict)

            # 获取老师教授的所有科研号和排名、是否通讯作者信息
            publication_list = Publication.query.filter(Publication.workno == teacherno).all()
            paper_ranking = {publication.id: publication.ranking for publication in publication_list}
            paper_correspond = {publication.id: publication.corresponding for publication in publication_list}

            # 根据论文号获取对应的论文信息
            paperIds = [publication.id for publication in publication_list]
            papers = Paper.query.filter(Paper.id.in_(paperIds)).all()

            papers_dict = []
            if len(papers) > 0:
                for paper in papers:
                    paper_dict = filter_props_date(paper)
                    if paper.id in paper_ranking:
                        paper_dict["ranking"] = paper_ranking[paper.id]
                    if paper.id in paper_correspond:
                        paper_dict["corresponding"] = paper_correspond[paper.id]
                    papers_dict.append(paper_dict)

            # 获取老师负责的所有项目号
            charge_list = Charge.query.filter(Charge.workno == teacherno and Charge.ranking == 1).all()
            project_fund = {charge.id: charge.fund for charge in charge_list}
            project_ranking = {charge.id: charge.ranking for charge in charge_list}

            # 根据项目号获取对应的项目信息
            projectIds = [charge.id for charge in charge_list]
            projects = Project.query.filter(Project.id.in_(projectIds)).all()

            projects_dict = []
            if len(projects) > 0:
                for project in projects:
                    project_dict = filter_props_date(project)
                    if project.id in project_fund:
                        project_dict["fund"] = project_fund[project.id]
                        project_dict["ranking"] = project_ranking[project.id]
                    projects_dict.append(project_dict)

            #将该教师教授的课程信息添加到一个新属性courseInfo中
            teacher.update({'courseInfo':courses_dict})
            teacher.update({'paperInfo':papers_dict})
            teacher.update({'projectInfo':projects_dict})

            items.append(teacher)

        return result(200,'success',{'items':convert_data(items),'total':len(items)})

@api_read.route("/api/yearInfo", methods=["POST"])
def year_info():
        data = request.get_json()

        startyear = int(re.search(re.compile(r'\d{4}'), data['startYear']).group())+1
        endyear = int(re.search(re.compile(r'\d{4}'), data['endYear']).group())+1
        # print("startyear:",startyear,data['startYear'])
        # print("endyear:",endyear, data['endYear'])
        Teachers = Teacher.query.all()
        items = []
        for teacher in Teachers:
            teacherno = teacher.workno
            teacher = teacher.__dict__
            del teacher['_sa_instance_state']
            #老师的基础信息

            # 获取老师教授的所有课程号和学期信息
            teaching_list = Teaching.query.filter(Teaching.workno == teacherno).all()
            course_semester = {teaching.id: teaching.semester for teaching in teaching_list}
            course_year = {teaching.id: teaching.year for teaching in teaching_list}

            # 根据课程号获取对应的课程信息
            courseIds = [teaching.id for teaching in teaching_list]
            course_parthours = {teaching.id: teaching.hours for teaching in teaching_list}
            courses = Course.query.filter(Course.id.in_(courseIds)).all()

            courses_dict = []
            if len(courses) > 0:
                for course in courses:
                    if course_year[course.id] >= startyear \
                        and course_year[course.id] <= endyear:
                        course_dict = filter_props(course)
                        if course.id in course_semester:
                            course_dict["semester"] = course_semester[course.id]
                            course_dict["year"] = course_year[course.id]
                            course_dict["parthours"] = course_parthours[course.id]
                        # del course_dict['property']
                        courses_dict.append(course_dict)

            # 获取老师教授的所有科研号和排名、是否通讯作者信息
            publication_list = Publication.query.filter(Publication.workno == teacherno).all()
            paper_ranking = {publication.id: publication.ranking for publication in publication_list}
            paper_correspond = {publication.id: publication.corresponding for publication in publication_list}

            # 根据论文号获取对应的论文信息
            paperIds = [publication.id for publication in publication_list]
            # papers = Paper.query.filter(Paper.id.in_(paperIds)).all()
            papers = Paper.query.filter(
                Paper.id.in_(paperIds),
                and_(
                    extract('year', Paper.year) >= startyear,
                    extract('year', Paper.year) <= endyear
                )
            ).all()

            papers_dict = []
            if len(papers) > 0:
                for paper in papers:
                    paper_dict = filter_props_date(paper)
                    if paper.id in paper_ranking:
                        paper_dict["ranking"] = paper_ranking[paper.id]
                    if paper.id in paper_correspond:
                        paper_dict["corresponding"] = paper_correspond[paper.id]
                    papers_dict.append(paper_dict)

            # 获取老师负责的所有项目号
            charge_list = Charge.query.filter(Charge.workno == teacherno and Charge.ranking == 1).all()
            project_fund = {charge.id: charge.fund for charge in charge_list}

            # 根据项目号获取对应的项目信息
            projectIds = [charge.id for charge in charge_list]
            # projects = Project.query.filter(Project.id.in_(projectIds)).all()
            projects = Project.query.filter(
                Project.id.in_(projectIds),
                and_(
                    extract('year', Project.startyear) >= startyear,
                    extract('year', Project.endyear) <= endyear
                )
            ).all()

            projects_dict = []
            if len(projects) > 0:
                for project in projects:
                    project_dict = filter_props_date(project)
                    if project.id in project_fund:
                        project_dict["fund"] = project_fund[project.id]
                    projects_dict.append(project_dict)

            #将该教师教授的课程信息添加到一个新属性courseInfo中
            teacher.update({'courseInfo':courses_dict})
            teacher.update({'paperInfo':papers_dict})
            teacher.update({'projectInfo':projects_dict})

            items.append(teacher)

        return result(200,'success',{'items':convert_data(items),'total':len(items)})

@api_read.route("/api/teachers",methods=["GET"])
def getTeacherList():
    Teachers = Teacher.query.all()
    items = []
    for teacher in Teachers:
        teacher = filter_props(teacher)
        items.append(teacher)

    return result(200, 'success',{'items': items, 'total': len(items)})

@api_read.route("/api/papers",methods=["GET"])
def getPaperList():
    Papers = Paper.query.all()
    items = []
    for paper in Papers:
        temp = filter_props_date(paper)
        # paper的基础信息
        items.append(temp)

    return result(200, 'success',{'items': items, 'total': len(items)})

@api_read.route("/api/courses",methods=["GET"])
def getCourseList():
    Courses = Course.query.all()
    items = []
    for course in Courses:
        course = filter_props(course)
        # course的基础信息
        items.append(course)

    return result(200, 'success',{'items': items, 'total': len(items)})\

@api_read.route("/api/projects",methods=["GET"])
def getProjectList():
    Projects = Project.query.all()
    items = []
    for project in Projects:
        project = filter_props(project)
        # Project的基础信息
        items.append(project)

    return result(200, 'success',{'items': items, 'total': len(items)})
