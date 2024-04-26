<script setup lang="ts">
import {Cpu } from '@element-plus/icons-vue'

import { ref } from 'vue'
const presenting =ref(true)


const presentWeightQnn=()=>{
    presenting.value=false
    setTimeout(() => {
        presenting.value=true
    }, 2000);

}
</script>
<template>
<div >
    <div class="rounded-lg bg-gray-200 shadow-xl hover:shadow-2xl ..." style="margin: 30px; padding: 20px; height: 700px;">
        <el-row>
            <el-col :span="4">
                <div>  
                    <button type="button" class=" rounded-lg bg-teal-400  box-content h-16 w-40  hover:bg-teal-700" v-if="presenting" @click="presentWeightQnn">
                        <p class="font-sans text-xl tracking-wide font-bold ..." >发布权重问卷</p>
                    </button>
                    <button type="button" class=" rounded-lg bg-teal-700 box-content h-16 w-40 " v-if="!presenting" >
                        <p class="font-sans text-xl tracking-wide font-bold ..." >发布中。。。</p>
                    </button>
                </div>
            </el-col>

        </el-row>
        
        
    </div>
</div>
</template>
<style scoped>

</style>