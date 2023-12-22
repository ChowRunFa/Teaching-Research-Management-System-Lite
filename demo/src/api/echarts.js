// µº»Îrequest
import request from '@/utils/request'

export function teacherInfo(){
    return request.get("/api/teacherRank")
}

export function paperCount(){
    return request.get("/api/paperCount")
}

export function teacherCompare(){
    return request.get("/api/teacherCompare")
}