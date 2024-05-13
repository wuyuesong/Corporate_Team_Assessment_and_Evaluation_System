<script setup lang="ts">
import { defineProps ,ref,onMounted,getCurrentInstance,inject} from 'vue';
import type { FormInstance } from 'element-plus'
import { request } from '/@/utils/service';
import { getBaseURL } from '/@/utils/baseUrl';
import Cookies from 'js-cookie';
import type { Action } from 'element-plus'
import { ElMessageBox ,ElMessage} from 'element-plus'
import { el } from 'element-plus/es/locale';
const refreshView = inject('refreshView')
import { watchEffect } from 'vue';


onMounted(() => {
    fetchquestionList()
})
const items=ref([])
const subscoreloading=ref(false)
const fetchquestionList=async()=>{
    try {
        const response=await request({
            url: 'api/system/weight_task/weight_task_info/',
            method: 'post',
            data:{
                staff_id:Cookies.get('staff_id'),
                task_id:props.task_id
            }
        })
        const data = await response.data;
        if(response.code===2000){
            items.value=data
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


const QNNsave=async()=>{
  try {
    let saveweights: { evaluated_department: any; weight: any; }[] = []
    items.value.forEach((item)=>{
        saveweights.push({
            evaluated_department:item.evaluated_department,
            weight:item.weight
        })
    })
    const response = await request({
          url: 'api/system/weight_task/submit_weight_task/',
          method: 'post',
          data:{
            staff_id:Cookies.get('staff_id'),
            task_id:props.task_id,
            submit_type:0,
            weights:saveweights
          }
        })
        const data = await response.data;
        if(response.code===2000){
          ElMessage({
            type: 'success',
            message: "保存成功",
          })
        }else{
          ElMessage({
          type: 'error',
          message: response.msg,
          })
        }
  } catch (error) {
    
  }
}

const QNNsubmit=()=>{
  ElMessageBox.confirm(
    '是否确认提交?',
    'Warning',
    {
      confirmButtonText: 'OK',
      cancelButtonText: 'Cancel',
      type: 'warning',
    }
    )
    .then(async() => {
      subscoreloading.value=true;
      try {
        let saveweights: { evaluated_department: any; weight: any; }[] = []
        items.value.forEach((item)=>{
            saveweights.push({
                evaluated_department:item.evaluated_department,
                weight:item.weight
            })
        })
        const response = await request({
          url: 'api/system/weight_task/submit_weight_task/',
          method: 'post',
          data:{
            staff_id:Cookies.get('staff_id'),
            task_id:props.task_id,
            weights:saveweights,
            submit_type:1,
          }
        })
        const data = await response.data;
        if(response.code===2000){
          subscoreloading.value=false;
          ElMessageBox.alert('Success', '成功提交', {
            confirmButtonText: 'OK',
            callback: (action: Action) => {
              location.reload()
            },
          })
        }else{
          ElMessage({
          type: 'error',
          message: response.msg,
          })
          subscoreloading.value=false;
        }

        
      } catch (error) {
        ElMessage({
        type: 'error',
        message: "提交错误",
        })
        subscoreloading.value=false;
      }
      



      
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: 'Submit canceled',
      })
    })
}




//percentage等于items的总分数

const percentage=ref()

watchEffect(() => {
    percentage.value = items.value.reduce((pre, cur) => pre + cur.weight, 0);
});


const colormethod=(percentage:number)=>{
    if(percentage>100){
        //红色
        return '#f56c6c'
    }else if(percentage==100){
        //绿色
        return '#67c23a'
    }else{
        //蓝色
        return '#409eff'
    }

}
const props = defineProps({
  task_id:String,
  title:String,
  discribe:String
});


</script>

<template>

    <div v-loading="subscoreloading">
        <!-- 问卷头（保持不动） -->
        <div class="qnnhead">
            <p class="text-3xl tracking-widest text-blue-500 ...">{{ title }}</p>
            
            <el-input class="Scorediscription" v-model="$props.discribe" style="margin-top: 20px;" type="textarea"  disabled="true" autosize="true" />
        </div>

        <el-scrollbar height="420px" >
            <div class="qnnbody">
                <div v-for=" (item,idx) in items">
                    <p style="margin-bottom: 20px;margin-top: 20px;" class="text-xl italic ">{{ (idx+1)+".请输入"+item.evaluated_department +"对你们部门的关系权重"}}</p>
                    <el-slider v-model="item.weight" show-input :show-input-controls="false"></el-slider>
                </div>
            </div>
        </el-scrollbar>
        <div class="qnnfoot">
            <el-progress 
            :percentage="percentage"
            :text-inside="true"
            :stroke-width="18" 
            :color="colormethod(percentage)"
            >
            </el-progress>
            <div style="margin-top: 10px;display: flex;">
                <el-button size="large" type="info"  style=" margin-right: 20px;"  @click="QNNsave">保存</el-button>
                <el-tooltip
                effect="dark"
                content="请确保总分数为100分,后提交"
                >
                <el-button size="large" :disabled="percentage!==100" @click="QNNsubmit">提交</el-button>
                </el-tooltip>
            </div>
            
            
            
        </div>

    </div>

</template>


<style scoped>
.qnnhead{
    display: flex;
    background-color: #f5f5f5;
    padding: 10px;
    border-bottom: 1px solid #ebeef5;
    font-size: 20px;
    font-weight: bold;
    color: #303133;
    margin-bottom: 10px;
    justify-content: center;
    text-align: center;
    flex-direction: column;
}

.Scorediscription{
  font-size: large;
}
</style>