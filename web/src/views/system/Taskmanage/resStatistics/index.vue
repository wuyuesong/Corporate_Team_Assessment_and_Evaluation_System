<script setup lang="ts">
import { onMounted, ref,reactive, markRaw } from 'vue';
import dayjs from 'dayjs'
import { ElMessageBox , ElMessage} from 'element-plus';
import { request } from '/@/utils/service';
import { getBaseURL } from '/@/utils/baseUrl';
import type { Action } from 'element-plus'
import {Edit, Refresh} from '@element-plus/icons-vue'
import { copyFileSync, writeFile, writeFileSync } from 'fs';
import { utils, write } from 'xlsx';
import * as echarts from 'echarts';
import { maxBy } from 'lodash';
import { info } from 'console';
const Selectedtitle=ref('')
const OTtasklist =ref([])
const currentTask=ref('')
onMounted(()=>{
    const res2=fetchAllTaskList()

    // //回到之前处理的任务上去
    // Promise.all([res2]).then(()=>{
    //     var selectedTask = localStorage.getItem('selectedTask');
    //     if (selectedTask) {
    //         // 如果有选中的任务，选中这个任务
    //         currentTask.value = selectedTask;
    //         // 清除 localStorage 中的选中任务
    //         ObTask(currentTask.value)
    //         Selectedtitle.value=OTtasklist.value.find(item => item.task_id === currentTask.value).task_name
    //         localStorage.removeItem('selectedTask');
    //     }
    // });


})
const options = [
  '公司领导',
  '总监',
  '部门正职',
  '部门副职',
]
const weight=ref({
    '公司领导':{
        '公司领导':0,
        '总监':0,
        '部门正职':0,
        '部门副职':0,
    },
    '总监':{
        '公司领导':0,
        '总监':0,
        '部门正职':0,
        '部门副职':0,
    },
    '部门正职':{
        '公司领导':0,
        '总监':0,
        '部门正职':0,
        '部门副职':0,
    },
    '部门副职':{
        '公司领导':0,
        '总监':0,
        '部门正职':0,
        '部门副职':0,
    },
})


const value = ref('公司领导')
const fetchAllTaskList=async()=>{
    try {
        const response=await request({
                url: 'api/system/task/task_list_all/',
                method: 'get',
        })
        if(response.code==2000){
            //去掉task_type=0的
           OTtasklist.value=response.data.filter(item => item.task_type !== 1)
        } 
    } catch (error) {
       
    }
}
const ObTask=(value)=>{
    currentTask.value=value
}
</script>


<template>
  <div>
    <div class="rounded-lg shadow-xl hover:shadow-2xl ..." style="margin: 30px; padding: 20px; min-height: 650px;">
        <div class="OTheader">
                <el-select v-model="Selectedtitle" placeholder="Select" size="large" style="width: 340px">
                    <el-option
                                v-for="item in OTtasklist"
                                :key="item.task_name"
                                :value="item.task_name"
                                @click="ObTask(item.task_id)"
                            />
                </el-select>
        </div>
        <div class="ContentBody" v-if=true>
            <h1 class="text-3xl font-extrabold text-center text-gray-700 bg-clip-text bg-gradient-to-r  drop-shadow-lg">
                评价结果统计配置
            </h1>
            <el-segmented class="segment" v-model="value" :options="options" block >
                <template #default="{ item }">
                    <div class="text-1xl font-bold text-center bg-clip-text">{{ item }}</div>
                </template>
            </el-segmented>
            <div v-for="item in options">
                <div class="evacontent" v-if="item==value">
                    <span class="text-xl  text-center text-gray-700 bg-clip-text">被评价对象层级 ----- {{ item }}</span>
                    <div class="wightFillblock" v-for="evaitem in options">
                        <span class="text-xl  text-center text-gray-700 bg-clip-text"style="width: 300px;">{{ evaitem }}(权重%)</span>
                        <el-input v-model.number="weight[item][evaitem]"/>
                    </div>

                    <div class="submitbutton">
                        <el-button type="primary" >统计结果</el-button>
                    </div>

                </div>
            </div>
        </div>
        <div class="ContentBody" v-else>
            <el-empty description="请选择任务进行配置" />
        </div>

    </div>
  </div>
</template>

<style lang="scss" scoped>
.OTheaderBlank{
    display: flex;
    align-items: center;
    padding-left: 30px;
    width: 80%;
}
.ContentBody{
    display: flex;
    width: 100%;
    padding-top: 20px;   
    flex-direction: column;
}
.segment{
    margin-top: 20px;
    background-color: #dadada; /* 白色背景 */
}
.evacontent{
    margin-top: 20px;
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;

}
.wightFillblock{
    display: flex;
    flex-direction: row;
    align-items: center; 
    background-color: #ffffff; /* 白色背景 */
    border-radius: 10px;        /* 圆角5px */
    border: 1px solid #cccccc; /* 灰色边框 */
    width: 600px;               /* 宽度300px */
    height: 50px;              /* 高度100px */
    margin: 10px;
    padding: 10px;
}
.submitbutton{
    width: 80%;
    display: flex;
    justify-content: right;
    align-items: right; 
    text-align: right;
}
</style>