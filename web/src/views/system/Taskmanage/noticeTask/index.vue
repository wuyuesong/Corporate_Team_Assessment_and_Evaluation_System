<script setup lang="ts">
import { request, downloadFile } from '/@/utils/service';
import {inject,onMounted,ref} from "vue";
import type { Action } from 'element-plus'
import { getBaseURL } from '/@/utils/baseUrl';
import { ElMessage, ElMessageBox } from 'element-plus'

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
const eail_index_starttime='2024-06-08 13:30'
const fetchexceptionlist=async()=>{
  try{
    exceptionDrawer.value=true
    const res = await request({
      url: 'api/system/evaluate_task/get_failed_email_list/',
      method: 'post',
      data: {
        start_time: eail_index_starttime,  
        end_time:  "2024-06-09 00:00",
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
                            <a href="#" class="notice-title">{{ item.task_name }}</a>
                            <div class="notice-details">
                                <span class="type">{{ "任务标识: "+item.task_id }}</span>
                            </div>
                            <span class="location">{{ "创建时间: "+item.task_create_date.replace('T',' ') }}</span>
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
                </div>
                <el-scrollbar>
                        <div class="notice" v-for="item in taskRandomList">
                            <a href="#" class="notice-title">{{ item.task_name }}</a>
                            <div class="notice-details">
                                <span class="type">{{ "任务标识: "+item.task_id }}</span>
                            </div>
                            <span class="location">{{ "创建时间: "+item.task_create_date.replace('T',' ') }}</span>
                        </div>
                </el-scrollbar>
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
                <a href="#" class="notice-title">{{ item.staff_name }}</a>
                <div class="notice-details">
                    <span class="type">{{ "邮件地址: "+item.addr }}</span>
                </div>
                <span class="location">{{ "账户名: "+item.username }}</span>
            </div>
        </el-scrollbar>
    </el-drawer>
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
</style>