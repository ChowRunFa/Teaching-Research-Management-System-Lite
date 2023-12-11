// ����request
import request from '@/utils/request'
// ������¼����
export function Projects(){
    return request.get("/api/projects")
}
export function DelProject(id){
    return request.delete("/api/del/project/"+id)
}

export function PostProject(form){
    return request.post('/api/add/project',form)
}

export function UpdateProject(form){
    return request.post('/api/update/project',form)
}


export function Charges(id){
    return request.get('/api/charge/'+id)
}