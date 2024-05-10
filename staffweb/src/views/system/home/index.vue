
<script setup lang="ts">
import { ref } from 'vue';
import {onMounted } from 'vue';
import { request } from '/@/utils/service';
import { getBaseURL } from '/@/utils/baseUrl';
import Header from '../component/header.vue'
import CardItem from '../component/CardItem.vue'
import QnnItem from '../component/QnnItem.vue'
import { NextLoading } from '/@/utils/loading';
import { ElMessageBox , ElMessage} from 'element-plus';
import Cookies from 'js-cookie';

import { on } from 'e-icon-picker/utils';
const loading = ref(true); // 标记是否正在加载用户信息

// 创建一个响应式的 Tasks 数组 数组为空
const Tasks = ref([]);
const WeightQnn=ref([]);

// 页面加载时
onMounted(() => {
  NextLoading.done();
	fetchTaskInfo();
});



const fetchTaskInfo = async() => {
  try {
        // 发送请求并获取数据
        const response = await request({
          url: 'api/system/task/task_list/',
          method: 'post',
          data:{
            staff_id:Cookies.get('staff_id')
          }
        })
        const data = await response.data;
        if(response.code===2000){
            Tasks.value=data.filter(item => item.task_type !== 1)
            WeightQnn.value=data.filter(item => item.task_type === 1)
        }else{
          ElMessage({
            showClose: true,
            message: response.msg,
            type: 'error',
            })
        }
    } catch (error) {
        ElMessage({
        showClose: true,
        message: "获取任务信息失败",
        type: 'error',
        })
    }
}



</script>


<template>
	<div class="common-layout">
    <el-container>
      <el-header class="no-padding-header">
        <Header></Header>
	    </el-header>
      <el-main class="no-padding-main">
        <div class="container">
          <div class="mainpage">
            <div class="cardpage" v-for=" (qnn,index) in WeightQnn" :key="index">
                <QnnItem :title="qnn.task_name"   :task_id="qnn.task_id" :discribe="qnn.task_describe" :complete_status=qnn.complete_status></QnnItem>
            </div>
            <div class="cardpage" v-for=" (task,index) in Tasks" :key="index">
                <CardItem :title="task.task_name" :Btime="task.task_start_date" :Etime="task.task_end_date" :task_id="task.task_id" :discribe="task.task_describe" :complete_status="task.complete_status"/>
            </div>
          </div>
        </div>
	    </el-main>
    </el-container>
  </div>
</template>


<style scoped>
.common-layout{
  background-image: linear-gradient(to bottom right, rgb(1,125,159) , rgb(97,197,213),rgb(247,249,252) ); 
  height: 100vh; /* 设置 body 的高度为视口的高度 */
  overflow-y: auto; /* 启用垂直滚动 */
}

.no-padding-main{
  display: flex;
  justify-content: center; /* horizontally center */
  padding: 0 !important;
}
.no-padding-header {
  padding: 0 !important;
}

.container{
  display: flex;
  justify-content: center; /* horizontally center */
}
.mainpage{
  background-color: #ffffff;
  min-height: 800px;
  width: 1200px;
  -webkit-box-shadow: 0 5px 15px rgba(0,0,0,0.5);
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
}

.cardpage{
  width: 100%; 
}
</style>