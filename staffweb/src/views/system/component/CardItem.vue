<script setup lang="ts">
import { defineProps,ref } from 'vue';
import cardform from './Scoringform.vue'


const props = defineProps({
  title: String,
  Btime: String,
  Etime: String,
  state: Boolean,
});


import { ElMessageBox } from 'element-plus'

const dialogVisible = ref(false)

const handleClose = (done: () => void) => {
  ElMessageBox.confirm('Are you sure to close this dialog?')
    .then(() => {
      done()
    })
    .catch(() => {
      // catch error
    })
}


</script>

<template>
    <el-card  class="card-item" shadow="always"  @click="dialogVisible = true">
        <template #header>
            <div class="card-header">
                <h2 class="Title">{{title}}</h2>
            </div>
        </template>
        <div class="decontent">
            <p>开始时间: {{ Btime }}</p>
            <p>结束时间: {{ Etime }}</p>
        </div>
    </el-card>
    <el-dialog
        v-model="dialogVisible"
        title="Tips"
        width="1000"
        :before-close="handleClose">
        <cardform></cardform>

    </el-dialog>

    
</template>

<style scoped>

.el-card{
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


.el-card:hover {
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
}
.el-dialog{
    display: flex;
    justify-content: center; /* horizontally center */
}
</style>