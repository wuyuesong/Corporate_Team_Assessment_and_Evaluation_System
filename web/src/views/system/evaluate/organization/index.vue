<script setup lang="ts">
import Page1 from './department/index.vue'; // 导入页面1组件
import Page2 from './job/index.vue'; // 导入页面2组件
</script>


<template>
    <el-tabs type="border-card"   stretch="true">
      <el-tab-pane label="部门管理" lazy="true">
        <div class="p1">
          <Page1></Page1>
        </div>
        
      </el-tab-pane>
      <el-tab-pane label="职务管理">
        <div class="p2">
          <Page2></Page2>
        </div>
      </el-tab-pane>
    </el-tabs>
</template>


<style scoped>
.p1{
  background-color: #f8f1f1;
}
.p2{
  background-color: #ededed;
}
</style>