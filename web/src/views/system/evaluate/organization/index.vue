<script setup lang="ts">
import { ref, onUpdated } from 'vue';
import Page1 from './department/index.vue'; // 导入页面1组件
import Page2 from './job/index.vue'; // 导入页面2组件

const activeTab = ref('Page1');

function refreshComponent() {
  // 切换 activeTab 的值来触发组件的更新
  activeTab.value = activeTab.value === 'Page1' ? 'Page2' : 'Page1';
}

onUpdated(() => {
  // 当组件更新后，再次切换回原来的 tab
  activeTab.value = activeTab.value === 'Page1' ? 'Page2' : 'Page1';
});
</script>


<template>
  <div>
    <el-tabs type="border-card" stretch="true" @tab-click="refreshComponent">
      <el-tab-pane label="部门管理">
        <div class="p1">
          <Page1 v-if="activeTab === 'Page1'"></Page1>
        </div>
      </el-tab-pane>
      <el-tab-pane label="职务管理">
        <div class="p2">
          <Page2 v-if="activeTab === 'Page2'"></Page2>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>


<style scoped>
.p1{
  background-color: #f8f1f1;
}
.p2{
  background-color: #ededed;
}
</style>
