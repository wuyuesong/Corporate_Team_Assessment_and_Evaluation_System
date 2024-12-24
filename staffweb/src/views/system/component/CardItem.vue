<script setup lang="ts">
import { defineProps,onMounted,ref } from 'vue';
import cardform from './Scoringform.vue'



const props = defineProps({
  title: String,
  Btime: String,
  Etime: String,
  task_id:String,
  discribe:String,
  complete_status:String
});
const cardstate=ref(true);
onMounted(() => {
	let enddate = new Date(props.Etime);
    let startdate = new Date(props.Btime);
    let currentdate=new Date();
    if ((currentdate.getTime() >startdate.getTime())&&(currentdate.getTime()<enddate.getTime())) {
        cardstate.value=true;
    }else{
        cardstate.value=false;
    }
});




import { ElMessageBox } from 'element-plus'

const dialogVisible = ref(false)

const handlescore=()=>{
    dialogVisible.value = true
}

const handleClose = (done: () => void) => {
  ElMessageBox.confirm('是否要关闭窗口?',{
    confirmButtonText: '确认',
    cancelButtonText: '取消'
  })
    .then(() => {
      done()
    })
    .catch(() => {
      // catch error
    })
}


</script>

<template>
    <el-card  class="card-item" shadow="always"  v-if="cardstate&&complete_status=='0'"  @click="dialogVisible = true">
        <template #header>
            <div class="card-header">
                <h2 class="Title">{{title}}</h2>
            </div>
        </template>
        <div class="decontent">
            <div>
                <p>开始时间: {{ Btime?.replace('T','') }}</p>
                <p>结束时间: {{ Etime?.replace('T','') }}</p>
            </div>
            <div style="width: 500px;"></div>
        </div>
    </el-card>
    <el-card  class="card-outtime" shadow="always"  v-if="!cardstate" >
        <template #header>
            <div class="card-header">
                <h2 class="Title">{{title}}</h2>
            </div>
        </template>
        <div class="decontent">
            <div>
                <p >开始时间: {{ Btime?.replace('T','-') }}</p>
                <p>结束时间: {{ Etime?.replace('T','-') }}</p>
            </div>
            <div style="width: 500px;"></div>
            
    
            
        </div>
    </el-card>
    <el-card  class="card-already" shadow="always"  v-if="cardstate&&complete_status=='1'" >
        <template #header>
            <div class="card-header">
                <h2 class="Title">{{title}}</h2>
            </div>
        </template>
        <div class="decontent">
            <div>
                <p>开始时间: {{ Btime?.replace('T','-') }}</p>
                <p>结束时间: {{ Etime?.replace('T','-') }}</p>
            </div>
            <div style="width: 500px;"></div>
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
    /* background-image: linear-gradient(rgba(255, 254, 254, 0.25), rgba(255, 241, 241, 0.25)),
                    url('../../../assets/cardbg.jpg'); */
    -webkit-backdrop-filter: blur(10px);/* 使文字等内容在模糊的背景前面显示清晰 */
    /* background-image:  url('../../../assets/cardbg.jpg'); */
    background-color: #0ABAB5;

    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    border-radius: 20px; 
    height: 180px;
    transition: box-shadow 0.3s ease; /* 添加过渡效果 */
}

.card-outtime{
    padding: 10px;
    margin-top: 50px;
    margin-bottom: 50px;
    margin-left: 50px;
    margin-right: 50px;
    
    background-color:  rgba(101, 147, 145, 0.6);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    border-radius: 20px; 
    height: 180px;
    position: relative;
}
.card-outtime::after {
    content: "已过期";
    position: absolute;
    top: 10%;
    left: 60%;
    color: red;  /* 设置文字颜色 */
    font-size: 1.8em;  /* 设置文字大小 */
    font-weight: bold;
    text-align: center;  /* 让文字居中显示 */
    border: 4px solid red;  /* 添加这一行，创建一个红色的边框 */
    border-radius: 50%;  /* 添加这一行，使得边框成为圆形 */
    width: 130px;  /* 设置伪元素的宽度，这将决定圆形边框的大小 */
    height: 130px;  /* 设置伪元素的高度，这将决定圆形边框的大小 */
    line-height: 120px;  /* 使得文字垂直居中，这个值应该和 .card-outtime 的 height 属性值相同 */
    opacity: 0.6;
    z-index: 1;
}


.card-already{
    padding: 10px;
    margin-top: 50px;
    margin-bottom: 50px;
    margin-left: 50px;
    margin-right: 50px;
    
    background-color:  rgba(93, 143, 116, 0.6);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    border-radius: 20px; 
    height: 180px;
    position: relative;
}
.card-already::after {
    content: "已完成";
    position: absolute;
    top: 10%;
    left: 60%;
    color: rgb(2, 167, 150);  /* 设置文字颜色 */
    font-size: 2em;  /* 设置文字大小 */
    font-weight: bold;
    text-align: center;  /* 让文字居中显示 */
    border: 4px solid rgb(2, 167, 150);  /* 添加这一行，创建一个红色的边框 */
    border-radius: 50%;  /* 添加这一行，使得边框成为圆形 */
    width: 130px;  /* 设置伪元素的宽度，这将决定圆形边框的大小 */
    height: 130px;  /* 设置伪元素的高度，这将决定圆形边框的大小 */
    line-height: 120px;  /* 使得文字垂直居中，这个值应该和 .card-outtime 的 height 属性值相同 */
    opacity: 0.6;
    z-index: 1;
}

.card-item:hover {
    background-color: rgba(15, 140, 136, 0.7);
    backdrop-filter:blur(10px) ;
}

.Title{
    color: white; /* 设置文本颜色为白色 */
    text-shadow: 1px 1px 2px rgba(0,0,0,1); /* 在文本下方添加阴影 */
    font-size:30px;
    font-weight: bold;
}
.decontent{
    color: white; /* 设置文本颜色为白色 */
    text-shadow: 1px 1px 2px rgba(0,0,0,1); /* 在文本下方添加阴影 */
    display: flex;
    font-size: large;
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