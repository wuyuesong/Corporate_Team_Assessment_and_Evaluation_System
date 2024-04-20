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
                <p>开始时间: {{ Btime?.replace('T','-') }}</p>
                <p>结束时间: {{ Etime?.replace('T','-') }}</p>
            </div>
            <div style="width: 500px;"></div>
            
            <div>
                <p class="cardwarn">不在时间范围内</p>
            </div>
            
        </div>
    </el-card>
    <el-card  class="card-outtime" shadow="always"  v-if="cardstate&&complete_status=='1'" >
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
            
            <div>
                <p class="cardwarn">已完成</p>
            </div>
            
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
    background-image:  url('../../../assets/cardbg.jpg');

    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    border-radius: 20px; 
    height: 160px;
    transition: box-shadow 0.3s ease; /* 添加过渡效果 */
}

.card-outtime{
    padding: 10px;
    margin-top: 50px;
    margin-bottom: 50px;
    margin-left: 50px;
    margin-right: 50px;
    
    background-image: linear-gradient(rgba(210, 209, 209, 0.6), rgba(210, 209, 209, 0.6)),
                    url('../../../assets/cardbg.jpg');
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    border-radius: 20px; 
    height: 160px;
}


.card-item:hover {
    background-image: linear-gradient(rgba(195, 195, 195, 0.4), rgba(195, 195, 195, 0.4)),
                    url('../../../assets/cardbg.jpg');
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