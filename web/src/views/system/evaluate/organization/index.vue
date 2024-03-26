<script setup lang="ts">
import { useFs } from '@fast-crud/fast-crud';
import { createCrudOptions } from './crud';
const { crudBinding1, crudRef } = useFs({ createCrudOptions });
import Page1 from './department.vue'; // 导入页面1组件
</script>


<template>
    <el-tabs type="border-card"   stretch="true">
      <el-tab-pane label="部门管理" lazy="true">
        <Page1></Page1>
      </el-tab-pane>
      <el-tab-pane label="职务管理">Config</el-tab-pane>
    </el-tabs>
</template>


