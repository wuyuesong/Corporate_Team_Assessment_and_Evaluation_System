<script setup lang="ts">
import { defineProps ,ref,onMounted,getCurrentInstance,inject} from 'vue';
import type { FormInstance } from 'element-plus'
import { request } from '/@/utils/service';
import { getBaseURL } from '/@/utils/baseUrl';
import Cookies from 'js-cookie';
import type { Action } from 'element-plus'
import { ElMessageBox ,ElMessage} from 'element-plus'
import { el } from 'element-plus/es/locale';
const refreshView = inject('refreshView')



const props = defineProps({
  task_id:String,
  title:String,
  discribe:String
});


</script>

<template>

    <div>
        <!-- 问卷头（保持不动） -->
        <div>
            <p>{{ title }}</p>
        </div>
    </div>

</template>


<style scoped>
</style>