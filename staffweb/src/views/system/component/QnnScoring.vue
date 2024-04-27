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
const items=ref([{
    question:"你的性别是？",
    score:10,

},{
    question:"你的性别是？",
    score:16,
}])

//percentage等于items的总分数

const percentage=ref()

watchEffect(() => {
    percentage.value = items.value.reduce((pre, cur) => pre + cur.score, 0);
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

    <div>
        <!-- 问卷头（保持不动） -->
        <div class="qnnhead">
            <p class="text-3xl tracking-widest text-blue-500 ...">{{ title }}</p>
            
            <el-input class="Scorediscription" v-model="$props.discribe" style="margin-top: 20px;" type="textarea"  disabled="true" autosize="true" />
        </div>

        <el-scrollbar height="420px" >
            <div class="qnnbody">
                <div v-for=" (item,idx) in items">
                    <p style="margin-bottom: 20px;margin-top: 20px;" class="text-xl italic ">{{ (idx+1)+"."+item.question }}</p>
                    <el-slider v-model="item.score" show-input :show-input-controls="false"></el-slider>
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
            <el-tooltip
            effect="dark"
            content="请确保总分数为100分,后提交"
            >
                <el-button size="large" style="margin-top: 10px;" :disabled="percentage!==100" @click="submit">提交</el-button>
            </el-tooltip>
            
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