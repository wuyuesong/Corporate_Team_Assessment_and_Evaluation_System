import { request } from "/@/utils/service";


export function login(params: object) {
    return request({
        url: '/api/staff_login/',
        method: 'post',
        data: params
    });
}