<script setup lang="ts">
import { ref, onMounted ,nextTick} from 'vue';


const judge=ref(true);
const revert=()=>{
    





    judge.value=false;
}
interface evaluatedPerson{
    name:String,
    ID:String,
}

const griddata:evaluatedPerson[]=[{
        name:'xiaoming',
        ID:'1'
},
{
        name:'xiaomhong',
        ID:'2'
}
]




</script>


<template>
    <div class="evaluated_container">
        <el-empty v-if="judge" id="emptyElement" description="Empty" style="width: 100%;" @click="revert"/>
        <el-table v-if="!judge" id="EvaluatedTable"
                  :data="griddata">
                  <el-table-column prop="name" label="名字"/>
                  <el-table-column prop="ID" label="编号"/>
        </el-table>
    </div>
</template>
<style>
.evaluated_container{
    width: 100%; /* 让 div 宽度充满父容器 */
    height: 100vh; /* 让 div 高度充满整个视窗 */
    box-sizing: border-box; /* 让 padding 和 border 不会增加元素的宽度和高度 */
    padding: 20px; /* 可选：为了美观，添加一些内边距 */
}
.el-empty{
    /* border: 1px solid rgb(100, 100, 100); 添加一个 2px 宽度的黑色边框 */
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5); /* 添加一个 10px 的模糊黑色阴影 */
    /* background-color: lightgray; 当鼠标悬停时，改变背景色为浅灰色 */
    
}
/* .el-table{
    display: none;
} */

.el-empty:hover{
    background-color: lightgray; /* 当鼠标悬停时，改变边框颜色为深灰色 */
}

</style>