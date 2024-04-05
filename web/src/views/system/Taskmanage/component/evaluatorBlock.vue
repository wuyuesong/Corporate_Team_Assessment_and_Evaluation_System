<script setup lang="ts">
import { Opportunity,Delete } from '@element-plus/icons-vue'
import { getCurrentInstance } from 'vue';
import { computed } from 'vue';
import { ref } from 'vue';

//emit声明
const emit=defineEmits(['update:modelValue:']);
const {proxy} = getCurrentInstance();
//props声明
const model = defineModel({ 
    type: Object,
    required:true,
 })


 const deletethisItem=()=>{
    proxy.$emit('remove');
 }


//计算属性处理子组件改动权重,防止打破单向流
const weightchange=computed({
    get(){
        return model.value.task_weight;
    },
    set(value){
        model.value.task_weight=value;
    }
})

const deleteRow = (index: number) => {
  model.value.tableData.splice(index, 1)
}
</script>
<template>
    <div class="evaitem_container">
        
        <el-card class="title_left">
            <el-button type="danger"  @click="deletethisItem" size="large" :icon="Delete" circle />
        </el-card>
        <el-card class="contain_middle">
            <el-table :data="model.tableData" style="width: 100%" max-height="250">
                <el-table-column prop="staff_name" label="姓名" width="120" />
                <el-table-column prop="staff_firm_id" label="ID" width="120" />
                <el-table-column fixed="right" label="Operations" width="120">
                <template #default="scope">
                    <el-button
                    link
                    type="primary"
                    size="small"
                    @click.prevent="deleteRow(scope.$index)"
                    >
                    Remove
                    </el-button>
                </template>
                </el-table-column>
            </el-table>
        </el-card>
        <el-card class="weight_right">
            <el-input-number v-model="weightchange" :min="0" :max="100" style="width: 110px" placeholder="权重(总和100)"  controls-position="right"/>
        </el-card>
    </div>
</template>

<style>
.evaitem_container{
    display: flex;
    margin: 10px;
}
.title_left{
    width: 100px;
    display: flex;
    text-align: center;
    align-items: center;
    justify-content: center;
    height: auto; /* 让所有卡片的高度占满父容器 */
    background-color: rgb(248, 246, 246);
}

.contain_middle{
    width: 450px;
    margin-left: 10px;
    margin-right: 10px;
    align-items: center;
    height: 100%; /* 让所有卡片的高度占满父容器 */
    background-color: rgb(248, 246, 246);
}
.weight_right{
    width: 150px;
    padding: 0px;
    align-items: center;
    display: flex;
    height: auto; 
    background-color: rgb(248, 246, 246);
}
.evatitle_span{
    font-size: 16px;
    font-weight: 600;
}
</style>