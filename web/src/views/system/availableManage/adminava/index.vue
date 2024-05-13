<script setup lang="ts">
import { useFs } from '@fast-crud/fast-crud';
import { createCrudOptions } from './crud';
import { onMounted } from 'vue';
const { crudBinding, crudRef, crudExpose } = useFs({ createCrudOptions });
// crud组件的ref

// 页面打开后获取列表数据
onMounted(() => {
  crudExpose.doRefresh();
});
</script>

<template>
    <div class="ava_container"  style="padding-top: 20px; padding-bottom: 30px;padding-left: 50px; padding-right: 50px; height: 800px">
        <fs-crud v-bind="crudBinding" ref="crudRef">
        </fs-crud>
    </div>

</template>

<style scoped>

</style>