<script setup lang="ts">
import { Opportunity } from '@element-plus/icons-vue'
import { ref } from 'vue';
const tableData = ref([])
const deleteRow = (index: number) => {
  tableData.value.splice(index, 1)
}
</script>
<template>
    <div class="evaitem_container">
        
        <el-card class="title_left">

        </el-card>
        <el-card class="contain_middle">
            <el-table :data="tableData" style="width: 100%" max-height="250">
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
            <el-input
                style="width: 110px"
                size="large"
                placeholder="权重"
                :suffix-icon="Opportunity"
                />
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
    align-items: center;
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
</style>