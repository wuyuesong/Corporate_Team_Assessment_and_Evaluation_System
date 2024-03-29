<script setup lang="ts">
import { useFs } from '@fast-crud/fast-crud';
import { createCrudOptions } from './crud';
import { onMounted } from 'vue';
const { crudBinding, crudRef,crudExpose } = useFs({ createCrudOptions });


onMounted(() => {
	crudExpose.doRefresh();
});

</script>


<template>
    <div class="container"  style="padding-top: 20px; padding-bottom: 30px;padding-left: 50px; padding-right: 50px; height: 800px">
        <fs-crud ref="crudRef" v-bind="crudBinding" > </fs-crud>
    </div>
</template>