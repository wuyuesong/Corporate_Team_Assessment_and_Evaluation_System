<script setup lang="ts">
import { ElMessageBox , ElMessage} from 'element-plus';
import { request } from '/@/utils/service';
import { getBaseURL } from '/@/utils/baseUrl';
import { ref } from 'vue'
const presenting =ref(true)


const presentWeightQnn=async()=>{
    try {
        const response=await request({
            url: getBaseURL() +'api/system/weight_task/evaluate_task_create/',
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
</script>
<template>
<div >
    <div class="rounded-lg bg-gray-200 shadow-xl hover:shadow-2xl ..." style="margin: 30px; padding: 20px; height: 700px;">
        <el-row>
            <el-col :span="4">
                <div>  
                    <button type="button" class=" rounded-lg bg-teal-400  box-content h-16 w-40  hover:bg-teal-700" v-if="presenting" @click="presentWeightQnn">
                        <p class="font-sans text-xl tracking-wide font-bold ..." >发布权重问卷</p>
                    </button>
                    <button type="button" class=" rounded-lg bg-teal-700 box-content h-16 w-40 " v-if="!presenting" >
                        <p class="font-sans text-xl tracking-wide font-bold ..." >发布中。。。</p>
                    </button>
                </div>
            </el-col>
            <el-col :span="20">
                <div class="MatrixRes">
                    
                </div>
            </el-col>

        </el-row>
        
        
    </div>
</div>
</template>
<style scoped>

</style>