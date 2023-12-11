// 导入request
import request from '@/utils/request'
// 导出登录方法
export function Teachers(){
    return request.get("/api/teachers")
}

export function NewTeacher(form){
    return request.post('/api/new/teacher',form)
}
