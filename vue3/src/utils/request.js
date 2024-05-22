import { ElMessage } from 'element-plus'
import router from '../router'
import axios from "axios";

const request = axios.create({
    baseURL: import.meta.env.VITE_BASE_URL,
    timeout: 30000  // 后台接口超时时间设置
})

// request 拦截器
// 可以自请求发送前对请求做一些处理
// request.interceptors.request.use(config => {
//     config.headers['Content-Type','Authorization'] = ['application/json;charset=utf-8',`JWT ${localStorage.getItem('token')}`]
//     // config.headers['Content-Type'] = 'application/json;charset=utf-8';
//     return config
// }, error => {
//     return Promise.reject(error)
// });

request.interceptors.request.use(config => {
    config.headers['Content-Type'] = 'application/json;charset=utf-8';
    config.headers['Authorization'] = `JWT ${localStorage.getItem('token')}` || ' ';
    console.log('传递' + localStorage.getItem('token'))
    return config;
}, error => {
    return Promise.reject(error);
});


// response 拦截器
// 可以在接口响应后统一处理结果
request.interceptors.response.use(
    response => {
        let res = response;
        // 如果是返回的文件
        if (response.config.responseType === 'blob') {
            return res
        }
        // 兼容服务端返回的字符串数据
        if (typeof res.data === 'string') {
            res.data= res.data ? JSON.parse(res.data) : res.data
        }
        // 当权限验证不通过的时候给出提示
        if (res.status === '401') {
            ElMessage.error(res.msg);
            router.push("/login")
        }
        return res;
    },
        error => {
        console.log('err' + error)
        return Promise.reject(error)
    }
)


export default request
