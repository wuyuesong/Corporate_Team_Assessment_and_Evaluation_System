<script setup lang="ts">
import { defineProps,onMounted,ref } from 'vue';
import cardform from './QnnScoring.vue'
import { ElMessageBox } from 'element-plus'
import { number } from 'echarts';


const props = defineProps({
  title: String,
  task_id:String,
  discribe:String,
  complete_status:Number
});
const cardstate=ref(true);
onMounted(() => {

});



const dialogVisible = ref(false)

const handlescore=()=>{
    dialogVisible.value = true
}

const handleClose = (done: () => void) => {
  ElMessageBox.confirm('是否要关闭窗口?')
    .then(() => {
      done()
    })
    .catch(() => {
      // catch error
    })
}


</script>

<template>
    <el-card class="card-item" shadow="always" v-if="props.complete_status===0"  @click="dialogVisible = true">
        <div class="card-header">
            <h4 class="Title">{{title}}</h4>
        </div>
    </el-card>
    <el-card class="card-outtime" shadow="always" v-if="props.complete_status===1">
        <div class="card-header">
            <h4 class="Title">{{title}}</h4>
        </div>
    </el-card>
            
   
   

    <el-dialog
        v-model="dialogVisible"
        title="打分表"
        width="1500"
        :before-close="handleClose">
        <div>
            <cardform :task_id="task_id" :title="title" :discribe="discribe"></cardform>
        </div>
    </el-dialog>

    
</template>

<style scoped>

.card-item{
    padding: 10px;
    margin-top: 50px;
    margin-bottom: 50px;
    margin-left: 50px;
    margin-right: 50px;

    background-color: rgb(8,57,73);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    border-radius: 20px; 
    height: 160px;
    transition: box-shadow 0.3s ease; /* 添加过渡效果 */
}




.card-outtime{
    position: relative;
    padding: 10px;
    margin-top: 50px;
    margin-bottom: 50px;
    margin-left: 50px;
    background-color: rgb(22,78,99);
    margin-right: 50px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    border-radius: 20px; 
    height: 160px;
    overflow: hidden; /* 隐藏超出边界的背景 */
}

.card-outtime::after {
    content: "已完成";
    font-size: 30px;
    font-weight: bolder;
    position: absolute;
    top: 0;
    left: 0;
    color: rgba(255, 255, 255, 0.5);
    transform: rotate(-45deg);
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 3px solid white; /* 设置边框颜色和宽度 */
    border-radius: 50%; /* 使元素变为圆形 */
}


.card-item:hover {
    backdrop-filter:blur(10px) ;
    background-color: rgb(18,47,73);
}

.Title{
    color: white; /* 设置文本颜色为白色 */
    text-shadow: 1px 1px 2px rgba(0,0,0,1); /* 在文本下方添加阴影 */
    font-size:35px;
    font-weight: bold;
}
.decontent{
    color: white; /* 设置文本颜色为白色 */
    text-shadow: 1px 1px 2px rgba(0,0,0,1); /* 在文本下方添加阴影 */
    display: flex;
}
.el-dialog{
    display: flex;
    justify-content: center; /* horizontally center */
}
.cardwarn{
    font-size:28px;
    font-weight: bold;
    color: #ff0000;
}
</style>