<script setup lang="ts">
import { request, downloadFile } from '/@/utils/service';
import {inject,ref} from "vue";
import type { Action } from 'element-plus'
import { getBaseURL } from '/@/utils/baseUrl';
import { ElMessage, ElMessageBox } from 'element-plus'
//通知接口
const email_inform=async()=>{
  try{
    const res = await request({
      url: getBaseURL() + 'api/system/evaluate_task/send_email/',
      method: 'get',
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
    })}
  }catch(error){
    ElMessage({
      showClose: true,
      message: "通知失败",
      type: 'error',
  })
  
}
}


const random_inform=async()=>{
  try{
    downloadFile({
					url: getBaseURL() + 'api/system/evaluate_task/generate_excel',
					params: {},
					method: 'get'
    })
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
        <el-col :span="4">
            <div class="email_notice">
                <el-button  @click="email_inform" size="large" type="danger" >邮件通知</el-button>
            </div>
        </el-col>
        <el-col :span="7">
            <div class="random_notice">
                
            </div>
        </el-col>
        <el-col :span="1">
            <div class="divider">
                <div class="div_line"/>
            </div>
        </el-col>
        <el-col :span="8">
            <div class="random_notice">
                
            </div>
        </el-col>
        <el-col :span="4">
            <div class="random_notice">
                <el-button  @click="random_inform" size="large" type="danger" >随机抽取</el-button>
            </div>
        </el-col>
    </el-row>
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

.div_line {
    width: 2px;
    height: 100%;
    background-image: linear-gradient(black 50%, transparent 50%);
    background-size: 100% 4px;
    
}
</style>