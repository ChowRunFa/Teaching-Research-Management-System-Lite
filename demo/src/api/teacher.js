// ����request
import request from '@/utils/request'
// ������¼����
export function Teachers(){
    return request.get("/api/teachers")
}

export function NewTeacher(form){
    return request.post('/api/new/teacher',form)
}
