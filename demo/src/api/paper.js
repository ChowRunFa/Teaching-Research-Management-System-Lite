// µº»Îrequest
import request from '@/utils/request'

export function Papers(){
    return request.get("/api/papers")
}

export function DelPaper(id){
    return request.delete('/api/del/paper/'+id)
}

export function PostPaper(form){
    return request.post('/api/add/paper',form)
}

export function UpdatePaper(form){
    return request.post('/api/update/paper',form)
}

export function Publications(id){
    return request.get('/api/publication/'+id)
}




