
<script setup lang="ts">
import { ref } from 'vue';
import {onMounted } from 'vue';
import Header from '../component/header.vue'
import CardItem from '../component/CardItem.vue'
import { NextLoading } from '/@/utils/loading';
import { on } from 'e-icon-picker/utils';
const loading = ref(true); // 标记是否正在加载用户信息

// 定义 Task 对象的类型
interface Task {
  title: string;
  starttime: string;
  endtime: string;
}

// 创建一个响应式的 Tasks 数组 数组为空
const Tasks = ref<Task[]>([]);


// 页面加载时
onMounted(() => {
  NextLoading.done();
	fetchTaskInfo();

});


const fetchTaskInfo = async() => {
  let task1: Task = {
  title: "完成报告1",
  starttime: "2024-03-30 09:00",
  endtime: "2024-03-30 12:00"
  };
  let task2: Task = {
  title: "完成报告2",
  starttime: "2024-03-30 09:00",
  endtime: "2024-03-30 12:00"
  };
  Tasks.value.push(task1);
  Tasks.value.push(task2);
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
            <div class="cardpage" v-for=" (task,index) in Tasks" :key="index">
                <CardItem :title="task.title" :Btime="task.starttime" :Etime="task.endtime" />
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
  height: 800px; 
  width: 1200px;
  -webkit-box-shadow: 0 5px 15px rgba(0,0,0,0.5);
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
}

.cardpage{
  width: 100%; 
}
</style>