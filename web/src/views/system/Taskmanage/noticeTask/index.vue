<script setup lang="ts">
import { request, downloadFile } from '/@/utils/service';
import {inject,onMounted,ref} from "vue";
import type { Action } from 'element-plus'
import { getBaseURL } from '/@/utils/baseUrl';
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router';
import { asyncCompute } from '@fast-crud/fast-crud';
import { pa } from 'element-plus/es/locale';
import { all } from 'axios';
onMounted(() => {
    //初始化
    featchTaskList()
})

const email_inform_loading=ref(false)
const random_inform_loading=ref(false)
const exceptionDrawer=ref(false)
const taskEmailList=ref([])
const taskRandomList=ref([])
const featchTaskList = async () => {
    try {
        const res = await request({
            url:  'api/system/task/task_list_all/',
            method: 'get',
        })
        if (res.code == 2000) {
            for (let i = 0; i < res.data.length; i++) {
                if (res.data[i].inform_type == 1) {
                    taskEmailList.value.push(res.data[i])
                } else if(res.data[i].inform_type == 2) {
                    taskRandomList.value.push(res.data[i])
                }
            }
        } else {
            ElMessage({
                showClose: true,
                message: "获取任务列表失败",
                type: 'error',
            })
        }
    } catch (error) {
        ElMessage({
            showClose: true,
            message: "获取任务列表失败",
            type: 'error',
        })
    }
}




//通知接口
const email_inform=async()=>{
  try{
    email_inform_loading.value=true
    const res = await request({
      url: 'api/system/evaluate_task/send_email/',
      method: 'get',
    })
    if(res.code==2000){
        email_inform_loading.value=false
      ElMessage({
        showClose: true,
        message: "通知成功",
        type: 'success',
    })
    }else{
      email_inform_loading.value=false
      ElMessage({
        showClose: true,
        message: "通知失败",
        type: 'error',
    })}
  }catch(error){
    email_inform_loading.value=false
    ElMessage({
      showClose: true,
      message: "通知失败",
      type: 'error',
  })
  
}
}


const random_inform=async()=>{
  try{
    random_inform_loading.value=true
    downloadFile({
					url: 'api/system/evaluate_task/generate_excel/',
					params: {},
					method: 'get'
    })
    random_inform_loading.value=false
    }catch(error){
    random_inform_loading.value=false
    ElMessage({
      showClose: true,
      message: "通知失败",
      type: 'error',
  })
}
}

const taskExceptionList=ref([])

const eail_index_starttime=ref()


const featch_starttime = async()=>{
    try{
        const res = await request({
        url: 'api/system/system_status/get_status/',
        method: 'get',
        })
        if(res.code==2000){
            let dateTimeStr = res.data[1].value
            eail_index_starttime.value= new Date(dateTimeStr);

        }else{
            ElMessage({
                showClose: true,
                message: "通知失败",
                type: 'error',
            })
        }
    }catch(error){

        ElMessage({
        showClose: true,
        message: "获取时间失败",
        type: 'error',
    })
}
  
}



const fetchexceptionlist=async()=>{
  try{
    await featch_starttime()
    exceptionDrawer.value=true
    const now = new Date();
    
    // 计算差值（毫秒）
    const diff =  now.getTime()-eail_index_starttime.value.getTime();

    // 将差值转换为天数
    const days = diff / (1000 * 60 * 60 * 24);
    if(days>7){
        //eail_index_starttime设为现在时间的前7天
        eail_index_starttime.value.setDate(now.getDate()-6)
    }

    const form_end = `${now.getFullYear()}-${(now.getMonth() + 1).toString().padStart(2, '0')}-${now.getDate().toString().padStart(2, '0')} ${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
    const form_start = `${eail_index_starttime.value.getFullYear()}-${(eail_index_starttime.value.getMonth() + 1).toString().padStart(2, '0')}-${eail_index_starttime.value.getDate().toString().padStart(2, '0')} ${eail_index_starttime.value.getHours().toString().padStart(2, '0')}:${eail_index_starttime.value.getMinutes().toString().padStart(2, '0')}`;
    const res = await request({
      url: 'api/system/evaluate_task/get_failed_email_list/',
      method: 'post',
      data: {
        start_time: form_start,  
        end_time:  form_end,
      }
    })
    if(res.code==2000){
        taskExceptionList.value=res.data
    }else{
      ElMessage({
        showClose: true,
        message: "获取异常任务列表失败",
        type: 'error',
    })}
  }catch(error){
    ElMessage({
      showClose: true,
      message: "获取异常任务列表失败",
      type: 'error',
  })
  
}
}


const router = useRouter();

const gotoNotice=(currentTaskid:any)=>{
    localStorage.setItem('selectedTask', currentTaskid);
    router.push('/observeTask/');

}

// 路由过滤递归函数
const filterRoutesFun = <T extends RouteItem>(arr: T[]): T[] => {
	return arr
		.filter((item: T) => !item.meta?.isHide)
		.map((item: T) => {
			item = Object.assign({}, item);
			if (item.children) item.children = filterRoutesFun(item.children);
			return item;
		});
};


const dialogVisible =ref(false)
const EditInFailfomation=(username)=>{
    dialogVisible.value=true
    fetchStaffInfotoEdit(username)
    console.log('编辑失败通知信息')
}

const thisStaffInfo=ref({})
const fetchStaffInfotoEdit=async(username)=>{
    try{
        const res = await request({
        url: '/api/system/staff/',
        params: {
            limit: 10,
            page: 1,
            staff_id: username
        },
        method: 'get',
        })
        if(res.code==2000){
            thisStaffInfo.value=res.data[0]
        }else{
            ElMessage({
                showClose: true,
                message: "获取员工信息失败",
                type: 'error',
            })
        }
    }catch(error){
        ElMessage({
        showClose: true,
        message: "获取员工信息失败",
        type: 'error',
    })
}
}
const updateStaffInfotoEdit=async(staff_id)=>{
    dialogVisible.value = false
    try{
        const res = await request({
        url: '/api/system/staff/'+staff_id + '/',
        method: 'put',
        data: thisStaffInfo.value
        })
        if(res.code==2000){
            ElMessage({
                showClose: true,
                message: "修改成功",
                type: 'success',
            })
            thisStaffInfo.value={}
        }else{
            ElMessage({
                showClose: true,
                message: "修改失败",
                type: 'error',
            })
            thisStaffInfo.value={}
        }
    }catch(error){
        ElMessage({
        showClose: true,
        message: "修改失败",
        type: 'error',
    })
    thisStaffInfo.value={}
} 
}


const reinform_email=async()=>{
    try{
        let list = []
        taskExceptionList.value.forEach((item)=>{
            list.push(item.username)
        })
        const res = await request({
        url: 'api/system/evaluate_task/send_failed_email/',
        method: 'post',
        data: {all_evaluate_id: list}
        })
        if(res.code==2000){
            ElMessage({
                showClose: true,
                message: "通知成功",
                type: 'success',
            })
        }else{
            ElMessage({
                showClose: true,
                message: "通知失败",
                type: 'error',
            })
        }
    }catch(error){
        ElMessage({
        showClose: true,
        message: "通知失败",
        type: 'error',
    })
}
}



</script>




<template>
<div style="height: 88vh;">
    <el-row>
        <el-col :span="12">
            <div class="infolist">
            <div class="notice-postings" >
                <div class="notice-postings-title">

                    <h1 class=" antialiased "  style="margin-bottom:10px;">实名任务列表</h1>
                    <el-button  @click="email_inform" size="large" type="danger" :loading="email_inform_loading">
                    <template #loading>
                        <div style="margin-right: 5px;">
                            <svg width="24" height="24" viewBox="0 0 38 38" xmlns="http://www.w3.org/2000/svg">
                                <defs>
                                    <linearGradient x1="8.042%" y1="0%" x2="65.682%" y2="23.865%" id="a">
                                        <stop stop-color="#fff" stop-opacity="0" offset="0%"/>
                                        <stop stop-color="#fff" stop-opacity=".631" offset="63.146%"/>
                                        <stop stop-color="#fff" offset="100%"/>
                                    </linearGradient>
                                </defs>
                                <g fill="none" fill-rule="evenodd">
                                    <g transform="translate(1 1)">
                                        <path d="M36 18c0-9.94-8.06-18-18-18" id="Oval-2" stroke="url(#a)" stroke-width="2">
                                            <animateTransform
                                                attributeName="transform"
                                                type="rotate"
                                                from="0 18 18"
                                                to="360 18 18"
                                                dur="0.9s"
                                                repeatCount="indefinite" />
                                        </path>
                                        <circle fill="#fff" cx="36" cy="18" r="1">
                                            <animateTransform
                                                attributeName="transform"
                                                type="rotate"
                                                from="0 18 18"
                                                to="360 18 18"
                                                dur="0.9s"
                                                repeatCount="indefinite" />
                                        </circle>
                                    </g>
                                </g>
                            </svg>
                        </div>
                    </template>
                    邮件通知
                </el-button>
                </div>
                

                <el-scrollbar>
                        <div class="notice" v-for="item in taskEmailList">
                            <a @click="gotoNotice(item.task_id)" class="notice-title">{{ item.task_name }}</a>
                            <div class="notice-details">
                                <span class="type">{{ "任务标识: "+item.task_id }}</span>
                            </div>
                            
                            <span class="location">{{ "创建时间: "+item.task_create_date.replace('T',' ').substring(0, 19) }}</span>
                        </div>
                </el-scrollbar>
            </div>
        </div>
        </el-col>
        <el-col :span="11">
            <div class="infolist">
                <div class="notice-postings" >
                    <div class="notice-postings-title">
                        <h1 class="antialiased" style="margin-bottom:10px;">匿名任务列表</h1>
                        <el-button  @click="random_inform" size="large" type="danger" :loading="random_inform_loading" >
                            <template #loading>
                                <div style="margin-right: 5px;">
                                    <svg width="24" height="24" viewBox="0 0 38 38" xmlns="http://www.w3.org/2000/svg">
                                        <defs>
                                            <linearGradient x1="8.042%" y1="0%" x2="65.682%" y2="23.865%" id="a">
                                                <stop stop-color="#fff" stop-opacity="0" offset="0%"/>
                                                <stop stop-color="#fff" stop-opacity=".631" offset="63.146%"/>
                                                <stop stop-color="#fff" offset="100%"/>
                                            </linearGradient>
                                        </defs>
                                        <g fill="none" fill-rule="evenodd">
                                            <g transform="translate(1 1)">
                                                <path d="M36 18c0-9.94-8.06-18-18-18" id="Oval-2" stroke="url(#a)" stroke-width="2">
                                                    <animateTransform
                                                        attributeName="transform"
                                                        type="rotate"
                                                        from="0 18 18"
                                                        to="360 18 18"
                                                        dur="0.9s"
                                                        repeatCount="indefinite" />
                                                </path>
                                                <circle fill="#fff" cx="36" cy="18" r="1">
                                                    <animateTransform
                                                        attributeName="transform"
                                                        type="rotate"
                                                        from="0 18 18"
                                                        to="360 18 18"
                                                        dur="0.9s"
                                                        repeatCount="indefinite" />
                                                </circle>
                                            </g>
                                        </g>
                                    </svg>
                                </div>
                            </template>
                            随机抽取
                        </el-button>
                    </div>
                

                <el-scrollbar>
                        <div class="notice" v-for="item in taskRandomList">
                            
                            <a @click="gotoNotice(item.task_id)" class="notice-title">{{ item.task_name }}</a>
                            <div class="notice-details">
                                <span class="type">{{ "任务标识: "+item.task_id }}</span>
                            </div>
                            <span class="location">{{ "创建时间: "+item.task_create_date.replace('T',' ').substring(0,19) }}</span>
                        </div>
                </el-scrollbar>
                </div>
            </div>
        </el-col>
        <el-col :span="1">
                <button class="random_notice" @click="fetchexceptionlist">
                <svg t="1715151001215" :height="25" :width="25" class="animate-bounce"  viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4252" xmlns:xlink="http://www.w3.org/1999/xlink" width="200" height="200">
                    <path d="M443.7 972.5c-11.52 0-23.03-4.39-31.82-13.18L25.92 573.36C9.53 556.97 0.5 535.18 0.5 512s9.03-44.97 25.42-61.36L411.88 64.68c17.57-17.57 46.07-17.57 63.64 0s17.57 46.07 0 63.64L91.84 512l383.68 383.68c17.57 17.57 17.57 46.07 0 63.64-8.79 8.79-20.31 13.18-31.82 13.18z" fill="#E58585" p-id="4253">
                    </path>
                    <path d="M979 557H46c-24.85 0-45-20.15-45-45s20.15-45 45-45h933c24.85 0 45 20.15 45 45s-20.15 45-45 45z" fill="#E58585" p-id="4254">
                    </path>
                </svg>
                </button>
        </el-col>
    </el-row>
    <el-drawer
        title="邮件通知异常任务列表"
        v-model="exceptionDrawer"
        :destroy-on-close="true"
        :with-header="true"
        :width="800">
        <el-scrollbar max-height="1000px">
            <div class="list_item" v-for="item in taskExceptionList"> 
                
                <h2 style="color: crimson; font-size: large;">{{ item.staff_name }}</h2>
                <div class="notice-details">
                    <span class="type">{{ "邮件地址: "+item.addr }}</span>
                    <a class="cursor-pointer" style="font-size: medium; margin-right: 10px;"  @click="EditInFailfomation(item.username)"><el-icon><EditPen /></el-icon>修改信息 </a>
                </div>
                <span class="location">{{ "账户名: "+item.username }}</span>
            </div>
            <div style="margin: 20px;font-size: large;">
                <el-button type="success" size="large" @click="reinform_email">重发邮件</el-button>
            </div>
            
        </el-scrollbar>
    </el-drawer>

    <el-dialog v-model="dialogVisible" title="基本信息" width="1200">
        <el-form label-width="120px" :inline="true">
            <el-form-item label="单位名称" >
                <el-select
                v-model="thisStaffInfo.staff_department"
                placeholder="Select"
                style="width: 400px"
                disabled>
                </el-select>
            </el-form-item>
            <el-form-item label="员工姓名" >
                <el-input style="width: 400px" v-model="thisStaffInfo.staff_name" disabled></el-input>
            </el-form-item>
            <el-form-item label="职位等级" >
                <el-select
                v-model="thisStaffInfo.staff_rank"
                placeholder="Select"
                style="width: 400px"
                disabled>
                </el-select>
            </el-form-item>
            

            <el-form-item label="岗位等级">
                <el-input style="width: 400px" v-model="thisStaffInfo.staff_job" disabled></el-input>
            </el-form-item>

            <el-form-item label="职称">
                <el-input style="width: 400px" v-model="thisStaffInfo.job_title" disabled></el-input>
            </el-form-item>

            <el-form-item label="第一年KPI">
                <el-input style="width: 400px" v-model="thisStaffInfo.staff_kpi1" disabled></el-input>
            </el-form-item>
            <el-form-item label="第二年KPI">
                <el-input style="width: 400px" v-model="thisStaffInfo.staff_kpi2" disabled></el-input>
            </el-form-item>
            <el-form-item label="第三年KPI">
                <el-input style="width: 400px" v-model="thisStaffInfo.staff_kpi3" disabled></el-input>
            </el-form-item>
            <el-form-item label="第一年考核结果">
                <el-input style="width: 400px" v-model="thisStaffInfo.assessment1" disabled></el-input>
            </el-form-item>
            <el-form-item label="第二年考核结果">
                <el-input style="width: 400px" v-model="thisStaffInfo.assessment2" disabled></el-input>
            </el-form-item>
            <el-form-item label="第三年考核结果">
                <el-input style="width: 400px" v-model="thisStaffInfo.assessment3" disabled></el-input>
            </el-form-item>
            <el-form-item label="政治面貌">
                <el-input style="width: 400px" v-model="thisStaffInfo.staff_status" disabled></el-input>
            </el-form-item>
            <el-form-item label="员工企业ID">
                <el-input style="width: 400px" v-model="thisStaffInfo.staff_firm_id" disabled></el-input>
            </el-form-item>
            <el-form-item label="员工电话">
                <el-input style="width: 400px" v-model="thisStaffInfo.staff_telephone" disabled></el-input>
            </el-form-item>
            <el-form-item label="员工邮箱">
                <el-input style="width: 400px" v-model="thisStaffInfo.staff_email" ></el-input>
            </el-form-item>
            <el-form-item label="备注">
                <el-input type="textarea" style="width: 400px" v-model="thisStaffInfo.description" disabled></el-input>
            </el-form-item>
            <el-form-item label="修改人">
                <el-input style="width: 400px" v-model="thisStaffInfo.modifier_name" disabled></el-input>
            </el-form-item>
            <el-form-item label="创建人">
                <el-input style="width: 400px" v-model="thisStaffInfo.creator_name" disabled></el-input>
            </el-form-item>
            <el-form-item label="更新时间">
                <el-input style="width: 400px" v-model="thisStaffInfo.update_datetime" disabled></el-input>
            </el-form-item>
            <el-form-item label="创建时间">
                <el-input style="width: 400px" v-model="thisStaffInfo.create_datetime" disabled></el-input>
            </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="updateStaffInfotoEdit(thisStaffInfo.id)">确 定</el-button>
        </span>

    </el-dialog>



</div>
</template>

<style scoped>
.email_notice{
    height: 88vh;
    background-color: #f0f0f0;
    border-radius: 10px;
    padding: 10px;
    margin: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
}
.random_notice{
    height: 88vh;
    background-color: #f0f0f0;
    border-radius: 10px;
    padding: 10px;
    margin: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
}

.divider {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 88vh;
    margin-bottom: 10px;
    margin-top: 10px;
}

.infolist{
    height: 88vh;
    background-color: #f0f0f0;
    border-radius: 10px;
    padding: 10px;
    padding-left: 15px;
    padding-right: 15px;
    padding-top: 20px;
    margin: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.list_item{
    display: block;
    align-items: center;
    justify-content: center;
    height: 90px;
    margin: 10px;
    padding: 5px;
    background-color: rgb(255, 238, 223);
    color: var(--el-color-primary);
    border-radius: 5px;
    
}
.notice-postings {
    width: 100%;
    background-color: #ffffff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1 {
    font-size: 22px;
}

.notice {
    padding: 15px 0;
    border-bottom: 1px solid #e0e0e0;
}

.notice:last-child {
    border-bottom: none;
}

.notice-title {
    font-size: 18px;
    color: #6a5acd;
    text-decoration: none;
}

.notice-title:hover {
    text-decoration: underline;
}

.notice-details {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    color: #999999;
    font-size: 14px;
    margin-top: 5px;
}

.department, .type, .location {
    display: inline-block;
}
.notice-postings-title{
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.cursor-pointer {
    cursor: pointer;
}
.cursor-pointer:hover {
    color: #4463ff; /* 添加这行代码 */
}
</style>