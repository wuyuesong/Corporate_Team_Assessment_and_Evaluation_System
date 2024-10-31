<script setup lang="ts">
import { ElMessageBox , ElMessage} from 'element-plus';
import { RefreshLeft ,Histogram} from '@element-plus/icons-vue';
import { request } from '/@/utils/service';
import { getBaseURL } from '/@/utils/baseUrl';
import { onMounted, ref } from 'vue'
const presenting =ref(-1)

onMounted(() => {
    featchMatrixQnn()
    feachMatrixRes()

})


const matrixStatus=ref()
const departmentlist=ref()
const feachMatrixRes=async()=>{
    matrixStatus.value={}
    departmentlist.value=[]
    try {
        const response=await request({
            url: 'api/system/weight_task/get_weight_matrix/',
            method: 'get',
        })
        const data = await response.data;
        if(response.code===2000){
            matrixStatus.value=data
            departmentlist.value = Object.keys(matrixStatus.value);
        }else{
            ElMessage({
                showClose: true,
                message: response.msg,
                type: 'error',
            })
        }
    } catch (error) {
        
    }
}

const processList=ref([])
const processData=ref()
const featchMatrixQnn=async()=>{
    //将processList清空 
    processList.value=[]
    processData.value={}
    try {
        const response=await request({
            url: 'api/system/weight_task/weight_task_status/',
            method: 'get',
        })
        const data = await response.data;
        if(response.code===2000){

            processData.value=data
            processList.value=data.completed_list
            if(data.task_status===-1){
                presenting.value=-1
            }else if(data.task_status===0){
                presenting.value=0
            }else{
                presenting.value=1
            }

            checkSubmit()
            console.log(!(checkSubmitres.value))
        }else{
            ElMessage({
                showClose: true,
                message: response.msg,
                type: 'error',
            })
        }
    } catch (error) {
        
    }
}
const presentWeightQnn=async()=>{
    try {
        const response=await request({
            url: 'api/system/weight_task/weight_task_create/',
            method: 'post',
            data:{
                task_name:"部门权重问卷",
                task_describe:"部门权重问卷"
            }
        })
        const data = await response.data;
        if(response.code===2000){
            ElMessage({
                showClose: true,
                message: "发布成功",
                type: 'success',
            })
            presenting.value=0
            processData.value.task_status=0
            featchMatrixQnn()
            feachMatrixRes()
        }else{
            ElMessage({
                showClose: true,
                message: response.msg,
                type: 'error',
            })
        }
    } catch (error) {
        
    }
}

const gobackQnn=()=>{
    ElMessageBox.confirm('此操作将撤销权重问卷, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        try {
            request({
                url: 'api/system/weight_task/reset_weight_task/',
                method: 'get',
            }).then((response)=>{
                if(response.code===2000){
                    ElMessage({
                        showClose: true,
                        message: "撤销成功",
                        type: 'success',
                    })
                    presenting.value=-1
                    featchMatrixQnn()
                    feachMatrixRes()
                }else{
                    ElMessage({
                        showClose: true,
                        message: response.msg,
                        type: 'error',
                    })
                }
            })
        } catch (error) {
            
        }
      }).catch(() => {
        ElMessage({
            showClose: true,
            message: "已取消",
            type: 'info',
        })
      });
}

const computecolor=(item)=>{
    if(item.completed===1){
        return 'green'
    }else {
        return 'red'
    }
}

const submitcal=async()=>{
    try {
        const response=await request({
            url: 'api/system/weight_task/cal_weight_task/',
            method: 'get',
        })
        const data = await response.data;
        if(response.code===2000){
            ElMessage({
                showClose: true,
                message: "计算成功",
                type: 'success',
            })
            //刷新
            featchMatrixQnn()
            feachMatrixRes()
        }else{
            ElMessage({
                showClose: true,
                message: response.msg,
                type: 'error',
            })
        }
    } catch (error) {
        
    }
}
const checkSubmitres=ref(true)
const checkSubmit=()=>{
    console.log(processList.value)
    for ( let item in processList.value){
        //获取item
        if(processList.value[item].completed === 0){
            checkSubmitres.value=false
            return
        }
    }
    return
}
</script>
<template>
<div >
    <div class="rounded-lg shadow-xl hover:shadow-2xl ..." style="margin: 30px; padding: 20px; height: 700px;">
        <el-row style="height: 100%;">
            <el-col :span="4">
                <div class="leftside">  
                    <button type="button" class=" rounded-lg bg-teal-400  box-content h-16 w-52  hover:bg-teal-700" v-if="presenting===-1" @click="presentWeightQnn">
                        <p class="font-sans text-xl tracking-wide font-bold ..." >发布权重问卷</p>
                    </button>
                    <button type="button" class=" rounded-lg bg-teal-700 box-content h-16 w-52 " v-if="presenting===0" >
                        <p class="font-sans text-xl tracking-wide font-bold ..." >发布中。。。</p>
                    </button>
                    <button type="button" class=" rounded-lg bg-green-700 box-content h-16 w-52 " v-if="presenting===1" >
                        <p class="font-sans text-xl tracking-wide font-bold ..." >已生成</p>
                    </button>
                    <el-button-group style="margin-top: 20px;">
                        <el-button   plain size="large" @click="gobackQnn"><el-icon><RefreshLeft/></el-icon>撤销</el-button>
                        <el-button size="large" key="1" :disabled="(!checkSubmitres)||presenting===1" @click="submitcal">计算<el-icon class="el-icon--right" ><Histogram/></el-icon></el-button>
                    </el-button-group>
                    <el-scrollbar height="500px" style="margin-top: 10px;">
                    <el-timeline style="margin: 10px;">
                        <el-timeline-item v-for="(item,index) in processList" :key="index" :color="computecolor(item)" >
                            <el-card>
                                <p>{{item.department}}</p>
                            </el-card>
                        </el-timeline-item>
                    </el-timeline>
                    </el-scrollbar>
                </div>
            </el-col>
            <el-col :span="20">
                <div class="MatrixRes" style="max-height: 600px; overflow: auto;">
                    <table  class="table-content border-separate border border-slate-400 ...">
                    <caption class="text-2xl font-bold" style="margin-bottom: 10px;">部门间相关权重矩阵</caption>
                    <thead>
                        <tr>
                        <th class="border border-slate-400 w-36 text-xl">\</th>
                        <th v-for="item in departmentlist" class="border border-slate-400 w-36 text-xl">{{ item }}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item,index) in departmentlist" :key="index">
                            <td class="border border-slate-400 w-36 text-xl">{{ item }}</td>
                            <td v-for="(item1,index1) in departmentlist" :key="index1" class="border border-slate-400 w-36 text-xl"> {{matrixStatus[item][item1] !== undefined && matrixStatus[item][item1] !== null && typeof matrixStatus[item][item1] === 'number' ? matrixStatus[item][item1].toFixed(2) : matrixStatus[item][item1] }}</td>
                        </tr>
                    </tbody>
                    </table>
                </div>
            </el-col>

        </el-row>
        
        
    </div>
</div>
</template>
<style scoped>
.leftside {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
}
.MatrixRes{
    max-width: 100%;
    max-height: 600px; /* 固定最大高度 */
    margin: 20px;
    padding: 20px;
    display: flex;
    text-align: center;
    overflow: auto; /* 超出部分滚动 */
}
.table-content {
    margin-top: 20px;
    width: 100%;
}

.table-content th,
.table-content td {
  padding: 8px;
  text-align: center;
}

</style>