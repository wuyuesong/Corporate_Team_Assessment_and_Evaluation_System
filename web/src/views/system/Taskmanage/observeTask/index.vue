<script setup lang="ts">
import { onMounted, ref,reactive } from 'vue';
import dayjs from 'dayjs'
import { ElMessageBox , ElMessage} from 'element-plus';
import { request } from '/@/utils/service';
import { getBaseURL } from '/@/utils/baseUrl';
import type { Action } from 'element-plus'
import {Edit} from '@element-plus/icons-vue'

const OTtasklist =ref([])
const currentTask=ref('')
const Selectedtitle=ref('')

let BTime: Date = new Date();
let ETime: Date = new Date();


const tempTime=ref({
    starttemptime:'',
    endtemptime:''
})
const dialogVisible=ref(false);
const departmentMap = reactive( new Map());
const OTtaskcontent=ref({
    task_name:'',
    task_create_date:'',
    task_describe:'',
    task_start_date:'',
    task_end_date:'',
    task_state:0,
    undo_staff:[],
    staff_count:0,
})
const overloading=ref(false)

onMounted(()=>{
    fetchTimeFromNTP()
    fetchAllTaskList()
})


const fetchAllTaskList=async()=>{
    try {
        const response=await request({
                url: getBaseURL() + 'api/system/task/task_list_all/',
                method: 'get',
        })
        if(response.code==2000){
           OTtasklist.value=response.data
        } 
    } catch (error) {
       
    }
}

const fetchTaskpageInfo=async()=>{
    try {
        const response=await request({
                url: getBaseURL() + 'api/system/evaluate_task/task_info/',
                method: 'post',
                data:{
                    task_id:currentTask.value
                }
        })
        if(response.code==2000){
            OTtaskcontent.value=response.data as any
            if(OTtaskcontent.value.task_start_date.length>0){
                BTime=new Date(OTtaskcontent.value.task_start_date)
            }
            if(OTtaskcontent.value.task_end_date.length>0){
                ETime=new Date(OTtaskcontent.value.task_end_date)
            }
            if(OTtaskcontent.value.undo_staff.length>0){
                departmentMap.clear();
                OTtaskcontent.value.undo_staff.forEach(ele =>{
                    if (departmentMap.has(ele.staff_department)) {
                         departmentMap.get(ele.staff_department).push(ele)
                    } else {
                        departmentMap.set(ele.staff_department,[])
                        departmentMap.get(ele.staff_department).push(ele)
                    }
                })
            }

            tempTime.value.starttemptime=OTtaskcontent.value.task_start_date
            tempTime.value.endtemptime=OTtaskcontent.value.task_end_date
            
        } 
        
    } catch (error) {
        ElMessage({
        showClose: true,
        message: error.message,
        type: 'error',
        })
    }
}

const ObTask=(value)=>{
    currentTask.value=value
    fetchTaskpageInfo()
}


let currentTime: Date=new Date()
const fetchTimeFromNTP=async()=>{
    try {
       
    } catch (error) {
        ElMessage({
        showClose: true,
        message: error.message,
        type: 'error',
        })
    }
}


//TODO: 判断任务时间与当前时间关系（待优化 当前时间必须和服务器时间相同）
function judgeTasktime() {
    currentTime=new Date()
    if(currentTask.value==='') return;


    if (currentTime.getTime()< BTime.getTime()) {
        //未开始
        OTtaskcontent.value.task_state=1
    }else if(currentTime.getTime()>=BTime.getTime()&&currentTime.getTime()<=ETime.getTime()){
        //进行中
        OTtaskcontent.value.task_state=2
    }else{
        //已结束
        OTtaskcontent.value.task_state=3
    }

}

// 每秒获取一次当前时间,更新系统时间
// setInterval(fetchTimeFromNTP, 1000);
setInterval(judgeTasktime, 1000);


const deleteTask=()=>{
    ElMessageBox.alert('是否确定删除此任务', '警告', {
    confirmButtonText: 'OK',
    callback: (action: Action) => {
    if(action==='confirm'){
            ElMessage({
                type: 'info',
                message: `action: ${action}`,
            })
            confirmdeleteTask()
        }
    },
    
  })
}
const confirmdeleteTask = async()=>{
    try {
        const response=await request({
                url: getBaseURL() + 'api/system/evaluate_task/task_delete_single/',
                method: 'post',
                data:{
                    task_id:currentTask.value
                }
        })
        if(response.code==2000){
            ElMessage({
            showClose: true,
            message: "删除成功",
            type: 'success',
            })
            location.reload()
        }
    } catch (error) {
        ElMessage({
        showClose: true,
        message: error.message,
        type: 'error',
        })
    }
}

const handleDialogClose=()=>{
    location.reload()
}

const confirmsEditTask=async()=>{
    try {
        const response=await request({
                url: getBaseURL() + 'api/system/task/modify_task/',
                method: 'post',
                data:{
                    task_id:currentTask.value,
                    task_name:OTtaskcontent.value.task_name,
                    task_describe:OTtaskcontent.value.task_describe,
                    task_start_date:tempTime.value.starttemptime,
                    task_end_date:tempTime.value.endtemptime,
                }
        })
        if(response.code==2000){
            ElMessage({
                showClose: true,
                message: "修改成功",
                type: 'success',
            })
            location.reload()
        }else{
            ElMessage({
                showClose: true,
                message: "修改失败",
                type: 'error',
            })
        }
    }catch (error) {
        ElMessage({
            showClose: true,
            message: error.message,
            type: 'error',
        })
    }
}



const generateResult=async()=>{
    try {
        const response=await request({
                url: getBaseURL() + 'api/system/evaluate_task/task_calc/',
                method: 'post',
                data:{
                   task_id:currentTask.value
                }
        })
        if(response.code==2000){
            ElMessage({
                showClose: true,
                message: "生成结果成功",
                type: 'success',
            })
            // location.reload()
        }
    }catch (error) {
        ElMessage({
            showClose: true,
            message: error.message,
            type: 'error',
        })
    }
}
</script>

<template>
    <div class="OTbody">
        <div  class="OTcontainer">
            <div class="OTheader">
                
                <div class="OTheaderBlank">
                    <el-button type="primary" :icon="Edit" :disabled="!(currentTask.length>0)" @click="dialogVisible=true" >修改任务</el-button>
                </div>
                
                <el-select v-model="Selectedtitle" placeholder="Select" size="large" style="width: 340px">
                    <el-option
                                v-for="item in OTtasklist"
                                :key="item.task_name"
                                :value="item.task_name"
                                @click="ObTask(item.task_id)"
                            />
                </el-select>
            </div>
            <el-dialog
                title="修改任务"
                v-model="dialogVisible"
                width="60%"
                :before-close="handleDialogClose"
                >
                <el-form :model="OTtaskcontent" label-width="120px">
                    <el-form-item label="任务标题">
                        <el-input v-model="OTtaskcontent.task_name"></el-input>
                    </el-form-item>
                    <el-form-item label="任务开始时间">
                        <el-date-picker
                            v-model=tempTime.starttemptime
                            type="datetime"
                            placeholder="选择日期时间"
                            value-format="YYYY-MM-DD HH:mm:ss "
                            ></el-date-picker>
                    </el-form-item>
                    <el-form-item label="任务结束时间">
                        <el-date-picker
                            v-model=tempTime.endtemptime
                            type="datetime"
                            placeholder="选择日期时间"
                            value-format="YYYY-MM-DD HH:mm:ss "
                            ></el-date-picker>
                    </el-form-item>
                    <el-form-item label="任务描述">
                        <el-input
                            type="textarea"
                            placeholder="请输入内容"
                            v-model="OTtaskcontent.task_describe"
                            :rows="6"
                            limit="300"
                            >
                        </el-input>
                    </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                    <el-button type="primary" @click="confirmsEditTask">确 定</el-button>
                </span>
            </el-dialog>

            <div class="OTmainer">
                <el-descriptions title="TASK INFO" >
                    
                    <el-descriptions-item label="任务标题">{{OTtaskcontent.task_name}}</el-descriptions-item>
                    <el-descriptions-item label="任务创建时间">{{OTtaskcontent.task_create_date.replace('T',' ')}}</el-descriptions-item>
                    <el-descriptions-item label="状态">
                        <el-tag size="large" type="success" v-if="OTtaskcontent.task_state===2">进行中</el-tag>
                        <el-tag size="large" type="danger" v-if="OTtaskcontent.task_state===1">未开始</el-tag>
                        <el-tag size="large" type="info" v-if="OTtaskcontent.task_state===3">已结束</el-tag>
                    </el-descriptions-item>
                </el-descriptions>
                <div>
                <p>任务描述</p>
                <el-input
                    v-model="OTtaskcontent.task_describe"
                    maxlength="300"
                    rows="6"
                    placeholder="请对任务进行必须的描述"
                    show-word-limit
                    type="textarea"
                    disabled="true"
                    style="font-size: large;padding-top: 10px;padding-right: 20px;"
                />

                </div>
                <div style="height: 20px;"/>
                
                <div class="OTstatistics">
                    <el-col :span="10">
                        <el-statistic title="任务时间" :value="OTtaskcontent.task_start_date.replace('T',' ')+' ~ '+OTtaskcontent.task_end_date.replace('T',' ')">
                            
                        </el-statistic>
                    </el-col>

                    <el-col :span="8">
                        <el-statistic title="完成情况" :value="OTtaskcontent.staff_count-OTtaskcontent.undo_staff.length" >
                            <template #suffix>
                                <el-popover
                                    placement="top-start"
                                    title="未完成"
                                    :width="600"
                                    trigger="hover"
                                    popper-style="box-shadow: rgb(14 18 22 / 20%) 0px 10px 38px -10px, rgb(14 18 22 / 20%) 0px 10px 20px -15px; padding: 20px; border-radius: 15px;"
                                    >
                                    <template #reference>
                                        <p>/{{  OTtaskcontent.staff_count}}</p>
                                    </template>
                                    <template #default>
                                        <div v-for="item in departmentMap" >
                                            {{ item[0]}} 还剩 {{item[1].length}}个人尚未完成
                                        </div>
                                    </template>
                                </el-popover>
                            </template>
                        </el-statistic>
                    </el-col>

                    <el-col :span="10">
                        <el-countdown format="DD [days] HH:mm:ss" :value="dayjs(OTtaskcontent.task_end_date==='' ? new Date() :OTtaskcontent.task_end_date)">
                            <template #title>
                            <div style="display: inline-flex; align-items: center">
                                <el-icon style="margin-right: 4px" :size="12">
                                <Calendar />
                                </el-icon>
                                剩余时间
                            </div>
                            </template>
                        </el-countdown>
                        
                    </el-col>
                </div>
                <el-collapse>
                     <el-collapse-item title="详细信息" name="1">
                    </el-collapse-item>
                </el-collapse>

                <div class="refButton">
                    <div class="button_item" >
                        <div class="backbox" @click="deleteTask" v-if="currentTask.length>0">
                            <p class="gT">删除任务</p>
                        </div>
                        <div class="backbox locked" v-if="!(currentTask.length>0)">
                            <p class="gT">删除任务</p>
                        </div>
                    </div>

                    <div class="button_item">
                        
                    </div>
                    <div class="button_item">
                        
                    </div>
                    <div class="button_item">
                        
                    </div>

                    <div class="button_item">
                        <div class="forwardbox"  @click="generateResult" v-if="OTtaskcontent.task_state===3||OTtaskcontent.undo_staff.length===0">
                            <p class="gT">生成结果</p>
                        </div>
                        <div class="forwardbox locked" v-if="!(OTtaskcontent.task_state===3||OTtaskcontent.undo_staff.length===0)">
                            <p class="gT">生成结果</p>
                        </div>
                    </div>
                </div>              
            </div>
            
        </div>
    </div>
</template>

<style scoped>
.OTcontainer{
    margin: 30px;
    box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.2); /* 添加一个 10px 的模糊黑色阴影 */
    background-color: #ffffff;
    padding: 20px; /* 可选：为了美观，添加一些内边距 */
    display: block;
    border-radius: 10px;
    transition: all ease 0.3s;
    overflow: hidden;
    background: var(--el-color-white);
    color: var(--el-text-color-primary);
    border: 1px solid var(--next-border-color-light);
}
.OTcontainer:hover{
    box-shadow: 0 2px 12px var(--next-color-dark-hover);
        transition: all ease 0.3s;
}
.OTheader{
    display: flex;
    width: 100%;
}
.OTheaderBlank{
    display: flex;
    align-items: center;
    padding-left: 30px;
    width: 80%;
}
.OTmainer{
    display: block;
    margin: 30px;
}
.OTstatistics{
    margin-top: 30px;
    display: flex;
}
.refButton{
    margin-top: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    padding: 20px;
    
}
.button_item{
    width: 20%;
    
}
.forwardbox{
    margin: auto;
    height: 50px;
    width: 100px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #1308ad;
    border-radius: 20px;
    background: #ffffff;
    cursor: pointer;
    transition: all 0.3s ease;
    border: #1308ad 3px solid;
    
}
.forwardbox:hover {
    background: #c4c0ff;
    transition: all 0.3s ease;
    
}

.forwardbox.locked{
    background-color: #ddd;
    color: #aaa;
    cursor: not-allowed;
}
.forwardbox.locked:hover {
     background-color: #ddd; /* 与锁定状态背景色相同 */
     color: #aaa; /* 与锁定状态字体颜色相同 */
}


.backbox{
    margin: auto;
    height: 50px;
    width: 100px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #e11e1e;
    border-radius: 20px;
    background: #ffffff;
    cursor: pointer;
    transition: all 0.3s ease;
    border: #e11e1e 3px solid;
    
    
}
.backbox.locked{
    background-color: #ddd;
    color: #aaa;
    cursor: not-allowed;
}
.backbox.locked:hover {
     background-color: #ddd; /* 与锁定状态背景色相同 */
     color: #aaa; /* 与锁定状态字体颜色相同 */
}
.backbox:hover {
    background: #ffbebe;
    transition: all 0.3s ease;
}
.gT{
    font-size: large;
    font-weight: bold;
}






</style>