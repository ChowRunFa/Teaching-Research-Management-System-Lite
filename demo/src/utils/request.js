import axios from 'axios';
//����axiosʵ��
const request = axios.create(
    {
        // baseURL : 'http://81.68.155.137:5000',
        baseURL : 'http://localhost:5000',
        timeout : 5000
    }
)


//�����������
request.interceptors.request.use(function (config){
    //�������ͷ
  config.headers.Authorization = "Bearer "+localStorage.getItem("token");
      return config;
})

//����
export default request