<script setup lang="ts">
import { useFs } from '@fast-crud/fast-crud';
import { createCrudOptions } from './crud';
const { crudBinding, crudRef } = useFs({ createCrudOptions });
</script>
<template>
    <div class="container"  style="padding-top: 20px; padding-bottom: 30px;padding-left: 50px; padding-right: 50px; height: 800px">
        <fs-crud ref="crudRef" v-bind="crudBinding" > </fs-crud>
    </div>
</template>