import XEUtils from 'xe-utils'
import {BtnPermissionStore} from "/@/plugin/permission/store.permission";
import {EvaPermissionStore} from "/@/plugin/permission/store.permission";

export default {
  hasPermissions (value:string | string[]) {
    const BtnPermission = BtnPermissionStore().data
    if (import.meta.env.VITE_PM_ENABLED) {
      if(value instanceof Array){
        return XEUtils.includeArrays(BtnPermission, value)
      }else if(typeof value === 'string'){
        const index = XEUtils.arrayIndexOf(BtnPermission, value)
        return index>-1?true:false
      }
     }
    return true
  }



  
}


/**
 * 单个权限验证
 * @param value 权限值 0 尚未生成账号密码 1 生成账号密码
 * @returns 有权限，返回 `true`，反之则反
 */
export function Evaauth(value: string): boolean {
	const stores = EvaPermissionStore();
  if(stores.data[0].value==='1'){
    return false
  }
  console.log("未生成账号密码")
	return true
}

