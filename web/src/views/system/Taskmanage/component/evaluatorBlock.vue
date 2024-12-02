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

    console.log(model.value.tableData)
    proxy.$emit('removeallmapone',model.value.tableData[index].staff_id)
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
                <el-table-column prop="staff_name" label="姓名" width="150" />
                <el-table-column prop="staff_firm_id" label="人员ID" width="150" />
                <el-table-column fixed="right" label="操作" width="200">
                <template #default="scope">
                    <el-button
                    link
                    type="primary"
                    size="small"
                    @click.prevent="deleteRow(scope.$index)"
                    >
                    删除
                    </el-button>
                </template>
                </el-table-column>
            </el-table>
        </el-card>
        <!-- <el-card class="weight_right">
            <el-input-number class="weight_input" v-model="weightchange" :min="0" :max="100"  placeholder="权重(总和100)"  controls-position="right"/>
        </el-card> -->
    </div>
</template>

<style>
.evaitem_container{
    display: flex;
    padding: 5px;
    /* margin: 10px; */
    width: 95%;
    /* height: 95%; */
}
.title_left{
    width: 15%;
    display: flex;
    text-align: center;
    align-items: center;
    justify-content: center;
    height: auto; /* 让所有卡片的高度占满父容器 */
    background-color: rgb(248, 246, 246);
}

.contain_middle{
    width: 80%;
    margin-left: 10px;
    margin-right: 10px;
    align-items: center;
    height: 100%; /* 让所有卡片的高度占满父容器 */
    background-color: rgb(248, 246, 246);
}
.weight_right{
    width: 22%;
    display: flex;
    text-align: center;
    align-items: center;
    justify-content: center;
    height: auto; /* 让所有卡片的高度占满父容器 */
    background-color: rgb(248, 246, 246);
}
.evatitle_span{
    font-size: 16px;
    font-weight: 600;
}
.weight_input{
    width: 150px;
}
</style>