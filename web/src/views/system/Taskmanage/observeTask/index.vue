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

const OTtasklist =ref([])
const currentTask=ref('')
const Selectedtitle=ref('')
const MatrixCanvas=ref()

const resranktable=ref()
//图例dom
// const legendDom=ref()
// const abnoramlDom=ref()
let BTime: Date = new Date();
let ETime: Date = new Date();
const parammul=ref(2)

const tempTime=ref({
    starttemptime:'',
    endtemptime:'',
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
    task_done:0,
    info_type:0
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
            //去掉task_type=0的
           OTtasklist.value=response.data.filter(item => item.task_type !== 1)
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

            console.log(OTtaskcontent.value)
            if(OTtaskcontent.value.task_done===1){
                fetchrankresinfo()
                fetchallevaluate()
            }
            
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
    //pageinfo初始化
    departmentMap.clear();
    OTtaskcontent.value={
        task_name:'',
        task_create_date:'',
        task_describe:'',
        task_start_date:'',
        task_end_date:'',
        task_state:0,
        undo_staff:[],
        staff_count:0,
        task_done:0,
        info_type:0
    }
    tempTime.value={
        starttemptime:'',
        endtemptime:''
    }
    // if(legendDom.value){
    //     echarts.init(legendDom.value).clear()
    // }
    fetchTaskpageInfo()
}

//ntp 解决时间同步（dgram不兼容问题没法解决）
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
        console.log(typeof tempTime.value.starttemptime); // 应该打印 "string"
        console.log(typeof tempTime.value.endtemptime); // 应该打印 "string"
        const response=await request({
                url: getBaseURL() + 'api/system/task/modify_task/',
                method: 'post',
                data:{
                    task_id:currentTask.value,
                    task_name:OTtaskcontent.value.task_name,
                    task_describe:OTtaskcontent.value.task_describe,
                    task_start_date:tempTime.value.starttemptime,
                    task_end_date:tempTime.value.endtemptime,
                    inform_type:OTtaskcontent.value.info_type
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
                   task_id:currentTask.value,
                   mul:parammul.value
                }
        })
        if(response.code==2000){
            ElMessage({
                showClose: true,
                message: "生成结果成功",
                type: 'success',
            })
            location.reload()
        }
    }catch (error) {
        ElMessage({
            showClose: true,
            message: error.message,
            type: 'error',
        })
    }
}

const ranktabledata=ref([])

const itemkey=ref()

//获取结果排名分数的信息
const fetchrankresinfo=async()=>{
    try {
        const response=await request({
                url: getBaseURL() + 'api/system/evaluate_task/get_rank/',
                method: 'post',
                data:{
                   task_id:currentTask.value
                }
        })
        if(response.code==2000){

            if(response.data){
                let temp=[]
                response.data.forEach(ele =>{

                    //保留ele.evaluated_score两位小数四舍五入
                    ele.evaluated_score=ele.evaluated_score.toFixed(2)
                    temp.push({
                        rank:ele.evaluated_rank,
                        name:ele.evaluated_name,
                        score:ele.evaluated_score,
                        evaluated_id:ele.evaluated_id,
                    })
                })
                ranktabledata.value=temp
                itemkey.value=Math.random()
                fetchabnorinfo()

                // drawMatrixTable()
                //initrankcharts(rankdata,rankname,rankscore)
            }
        }else{
            ElMessage({
                message: "获取数据失败",
                type: 'error',
            })
        }
    }catch(error){
        ElMessage({
            message: error.message,
            type: 'error',
        })
    }
}


const fetchallevaluate=async()=>{
    try {
        const response=await request({
                url: getBaseURL() + 'api/system/evaluate_task/get_all_evaluate/',
                method: 'post',
                data:{
                   task_id:currentTask.value
                }
        })
        if(response.code==2000){
            if(response.data){
                let temp=[]
                let index=0
                response.data.forEach(ele =>{
                    map.set(ele.staff_id,index++)
                    abnormaltemp.push({
                            name:ele.staff_name,
                            evaluate_id:ele.staff_id
                        })
                })
            }
        }
    }catch(error){
        ElMessage({
            message: error.message,
            type: 'error',
        })
    
    }

}
let map=new Map()
let abnormaltemp=[]
const abnormaltabledata=ref([])
//获取异常分数的信息
const fetchabnorinfo=async()=>{
    try {
        const response=await request({
                url: getBaseURL() + 'api/system/evaluate_task/get_abnormal_data/',
                method: 'post',
                data:{
                   task_id:currentTask.value
                }
        })
        if(response.code==2000){
            
            if(response.data){
                response.data.forEach(item=>{

                    //保留两位
                    item.origin_value=item.origin_value.toFixed(2)
                    item.fix_value=item.fix_value.toFixed(2)

                    if(map.has(item.evaluate_id)){
                        abnormaltemp[map.get(item.evaluate_id)][item.evaluated_id]=item.origin_value+"/"+item.fix_value
                    }
                })
                abnormaltabledata.value=abnormaltemp
                abnormaltemp=[]
            }
        }
    }catch(error){
        ElMessage({
            message: error.message,
            type: 'error',
        })
    }
}


// const drawMatrixTable=()=>{
//     if(MatrixCanvas){
//         let ctx=MatrixCanvas.value.getContext('2d');
//         ctx.lineWidth = 0.5;
//         ctx.font = "10px serif";
//         let len=ranktabledata.value.length
//         for(let i=1;i<len+1;i++){
//             ctx.beginPath()
//             ctx.fillText("Hello world", (i-1)*(700/len)+10, 10,(700/len));
//             ctx.lineTo(i*(700/len), 0);
//             ctx.lineTo(i*(700/len), 700);
//             ctx.stroke();
//             ctx.closePath()
//         }
        
//     }
// }


// #region 废弃图标改用表格
// //INIT结果图标
// const initrankcharts=(rankdata,rankname,rankscore)=>{
//     if(legendDom.value){
//         let myChart = echarts.init(legendDom.value);
//         myChart.setOption( {
//         title: {
//           text: '处理后结果RANK'
//         },
//         tooltip: {
//             trigger: 'axis',
//             axisPointer: {
//             type: 'cross',
//             crossStyle: {
//                 color: '#999'
//             }
//             }
//         },
//         legend: {
//           data: ['分数','排名']
//         },
//         xAxis: {
//           data: rankname
//         },
//         yAxis: {},
//         series: [
//           {
//             name: '分数',
//             type: 'bar',
//             tooltip: {
//                 valueFormatter: function (value) {
//                     return value 
//                 }
//             },
//             data: rankscore
//           },
//           {
//             name: '排名',
//             type: 'bar',
//             tooltip: {
//                 valueFormatter: function (value) {
//                     return value 
//                 }
//             },
//             data: rankdata
//           }
//         ]
//       });
//    }else{
//         ElMessage({
//             showClose: true,
//             message: 'legendDom.value is null',
//             type: 'error',
//         })
//         return;
//     }
// }

// const initabnomalcharts=(xaxis,origindata,fixdata)=>{
//     if(abnoramlDom.value){
//         let myChart = echarts.init(abnoramlDom.value);
//         myChart.setOption( {
//             tooltip: {
//                 trigger: 'axis',
//                 axisPointer: {
//                     type: 'cross',
//                     crossStyle: {
//                         color: '#999'
//                     }
//                 }
//             },
//             legend: {
//                 data: ['Origin', 'Fix']
//             },
//             grid: {
//                 left: '3%',
//                 right: '4%',
//                 bottom: '3%',
//                 containLabel: true
//             },
//             xAxis: [
//                 {
//                     type: 'value',
                     
//                 },
                
//             ],
//             yAxis: [
//                 {
//                 type: 'category',
//                 axisTick: {
//                     show: false
//                 },
//                 data: xaxis
//                 }
//             ],
//             series: [
//                 {
//                 name: 'Origin',
//                 type: 'bar',
//                 label: {
//                     show: true,
//                     position: 'inside'
//                 },
//                 itemStyle: {
//                     color: 'red'  // 设置柱状图的颜色为红色
//                 },
//                 emphasis: {
//                     focus: 'series'
//                 },
//                 data: origindata
//                 },
//                 {
//                 name: 'Fix',
//                 type: 'bar',
//                 stack: 'Total',
//                 label: {
//                     show: true,
//                 },
//                 emphasis: {
//                     focus: 'series'
//                 },
//                 data: fixdata
//                 },
//             ]
//       });
//    }else{
//         ElMessage({
//             showClose: true,
//             message: 'legendDom.value is null',
//             type: 'error',
//         })
//         return;
//     }
// }
// #endregion



const openresetRES=()=>{
    ElMessageBox.confirm(
        '确认重置任务?',
        '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        icon:markRaw(Refresh)
      }).then(async() => {
        try {
            const response=await request({
                    url: getBaseURL() + 'api/system/evaluate_task/reset_taskres/',
                    method: 'post',
                    data:{
                        task_id:currentTask.value
                    }
            })
            if(response.data.code==200){
                ElMessage({
                    type: 'success',
                    message: '重置成功!'
                });
            }
            ObTask(currentTask.value)
        }catch(error) {
            ElMessage({
                    type: 'error',
                    message: '重置失败!'
            });
        }
        
      })
}


//具体详情
const indexundo=(title)=>{
    ElMessageBox.alert('<strong style="font-size: 16px;">'+departmentMap.get(title).map(item=>item.staff_name+' --- '+item.staff_firm_id).join('</br>')+'</strong>',
    title, {
        confirmButtonText: 'OK',
        dangerouslyUseHTMLString: true,
        callback: (action: Action) => {
        if(action==='confirm'){
            }
        },
    })

}

//导出EXCEL
const exportExcel=()=>{


    
    //列名
    const title=[OTtaskcontent.value.task_name]
    const headers = ['排名', '姓名','分数','编号'];
    const dataWithHeaders = [title,headers, ...ranktabledata.value.map(item => Object.values(item))];
    const ws = utils.aoa_to_sheet(dataWithHeaders);
    const wb = utils.book_new();
    utils.book_append_sheet(wb, ws, 'Sheet1');

    // 创建 Blob 对象
    const blob = new Blob([write(wb, { bookType: 'xlsx', type: 'array' })], { type: 'application/octet-stream' });

    
    // 创建下载链接
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'output.xlsx';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

}

const exportExpExcel=()=>{
    //列名
    const title=[OTtaskcontent.value.task_name]
    const headers = ['评价人/被评价人', ...ranktabledata.value.map(item => item.name)];
    let abnomaltabledata=[]
    abnormaltabledata.value.forEach(item=>{
        let temp=[]
        temp.push(item.name)
        for(let i=0;i<ranktabledata.value.length;i++){
            if(!item[ranktabledata.value[i].evaluated_id]){
                temp.push(' ')
            }else{
                temp.push(item[ranktabledata.value[i].evaluated_id])
            }
        }
        abnomaltabledata.push(temp)
    })
    const dataWithHeaders = [title,headers, ...abnomaltabledata];
    const ws = utils.aoa_to_sheet(dataWithHeaders);
    const wb = utils.book_new();
    utils.book_append_sheet(wb, ws, 'Sheet1');

    // 创建 Blob 对象
    const blob = new Blob([write(wb, { bookType: 'xlsx', type: 'array' })], { type: 'application/octet-stream' });

    
    // 创建下载链接
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'output.xlsx';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

}

</script>

<template>
    <div class="OTbody">
        <div  class="OTcontainer">
            <div class="OTheader">
                
                <div class="OTheaderBlank">
                    <el-button type="primary" :icon="Edit" :disabled="!(currentTask.length>0)||OTtaskcontent.task_done===1" @click="dialogVisible=true" >修改任务</el-button>
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
                    <el-form-item label="任务标题">
                        <div class="mb-2 text-sm">
                        <el-radio-group v-model="OTtaskcontent.info_type">
                            <el-radio value="1" size="large" border>邮件通知</el-radio>
                            <el-radio value="2" size="large" border>匿名通知</el-radio>
                        </el-radio-group>
                </div>
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
                        <el-tag size="large" type="success" v-if="OTtaskcontent.task_state===2&&OTtaskcontent.task_done===0">进行中</el-tag>
                        <el-tag size="large" type="danger" v-if="OTtaskcontent.task_state===1&&OTtaskcontent.task_done===0">未开始</el-tag>
                        <el-tag size="large" type="info" v-if="OTtaskcontent.task_state===3&&OTtaskcontent.task_done===0">已结束</el-tag>
                        <el-tag size="large" type="primary" v-if="OTtaskcontent.task_state===3&&OTtaskcontent.task_done===1">已生成结果</el-tag>
                        <el-tag size="large" type="primary" v-if="OTtaskcontent.task_state===2&&OTtaskcontent.task_done===1">已生成结果</el-tag>
                        <el-button v-if="OTtaskcontent.task_done===1" style="margin-left: 20px;"  @click="openresetRES">重置结果</el-button>
                    </el-descriptions-item>
                    <el-descriptions-item label="任务描述"></el-descriptions-item>
                    <el-descriptions-item label="任务发布状态">
                        <el-tag size="large" type="primary" v-if="OTtaskcontent.info_type===0">未确认通知</el-tag>
                        <el-tag size="large" type="primary" v-if="OTtaskcontent.info_type===1">邮件通知</el-tag>
                        <el-tag size="large" type="primary" v-if="OTtaskcontent.info_type===2">匿名通知</el-tag>

                    </el-descriptions-item>
                </el-descriptions>
                <div>
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
                                        <div v-for="item in departmentMap"  v-if="OTtaskcontent.info_type===1">
                                            <p class="font-sans text-sky-400/100 text-wrap text-xl hover:text-indigo-800 cursor-pointer ..." @click="indexundo(item[0])">{{ item[0]}} 还剩 {{item[1].length}}个人尚未完成</p>
                                        </div>
                                        <div v-for="item in departmentMap"  v-if="OTtaskcontent.info_type!==1">
                                            <p class="font-sans text-sky-400/100 text-wrap text-xl  cursor-pointer ...">{{ item[0]}} 还剩 {{item[1].length}}个人尚未完成</p>
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
                <div class="updatemul"  v-if="OTtaskcontent.task_done===0">
                    <span>偏差倍数(默认为2)</span>
                    <el-input-number v-model="parammul"  :precison="1" :step="0.1" :min="0"  :max="10"  controls-position="right"  style="width: 150px; margin-left: 20px;"/>
                </div>
               
                <el-collapse v-if="OTtaskcontent.task_done===1">
                     <el-collapse-item title="详细信息-结果及排名" name="1">
                        <div class="chartzone">

                            <!-- 使用 :key 解决响应刷新问题 -->
                            <el-table  ref="resranktable" :data="ranktabledata" :key="itemkey" height="400px" stripe border style="width: 800px; " >
                                <el-table-column prop="rank" label="排名"  width="160px" />
                                <el-table-column prop="name" label="姓名" width="400px"  />
                                <el-table-column prop="score" label="分数"  width="240px" />
                            </el-table>
                        </div>
                        <el-button size="large" style="font-size: large; font-weight: bold; border-width: 2px;"  @click="exportExcel">
                            导出excel
                        </el-button>
                    </el-collapse-item>
                    <el-collapse-item title="详细信息-异常数据" name="2">
                        <div class="chartzone">
                        
                            <el-table :data="abnormaltabledata" border style="width: 1200px; height: 500px;" height="500">
                                <el-table-column fixed prop="name" label="" width="180px">
                                    <template #header>
                                        <div class="group-bias-divide">
                                            <div class="top">被评价人</div>
                                            <div class="bottom">评价人</div>
                                        </div>
                                        </template>
                                        <template #default="{ row }">
                                        <span style="padding-left: 1em;">{{ row.name }}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column v-for="(item,index) in ranktabledata" :key="index" :prop="item.evaluated_id" :label="item.name" width="200px" />

                            </el-table>
                        </div>
                        <el-button size="large" style="font-size: large; font-weight: bold; border-width: 2px; margin-top: 10px;"  @click="exportExpExcel">
                            导出excel
                        </el-button>
                    </el-collapse-item>
                </el-collapse>

                <div class="refButton">
                    <div class="button_item" >
                        <div class="backbox" @click="deleteTask" v-if="currentTask.length>0&&OTtaskcontent.task_done===0">
                            <p class="gT">删除任务</p>
                        </div>
                        <div class="backbox locked" v-if="!(currentTask.length>0&&OTtaskcontent.task_done===0)">
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
                        <div class="forwardbox"  @click="generateResult" v-if="(OTtaskcontent.task_state===3||OTtaskcontent.undo_staff.length===0)&&OTtaskcontent.task_done===0">
                            <p class="gT">生成结果</p>
                        </div>
                        <div class="forwardbox locked" v-if="!((OTtaskcontent.task_state===3||OTtaskcontent.undo_staff.length===0)&&OTtaskcontent.task_done===0)">
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

.chartzone{
    display: flex;
    margin-top: 30px;
    justify-content: center;
    align-items: center;
    text-align: center;
}


.MatrixCanvas{
    border: 2px solid rgb(199, 198, 198);
    border-radius: 15px;
}
.updatemul{
    display: flex;
    margin-top: 20px;
    margin-bottom: 20px;
    align-items: center;
}

</style>
<style lang="scss" scoped>
:deep(.group-bias-divide) {
    .top {
      text-align: right;
      padding-right: .5em;
      box-sizing: border-box;
    }
 
    .bottom {
      text-align: left;
      padding-left: 1em;
      box-sizing: border-box;
 
      &::before {
        content: "";
        position: absolute;
        width: 1px !important;
        height: 187px !important;
        top: auto !important;
        left: auto !important;
        bottom: 0 !important;
        right: 5px !important;
        background-color: #d6d6d6;
        display: block;
        transform: rotate(289deg);
        transform-origin: bottom;
      }
    }
}
</style>