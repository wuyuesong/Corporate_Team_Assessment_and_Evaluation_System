<script setup lang="ts">
import { defineProps ,ref} from 'vue';
import type { FormInstance } from 'element-plus'


const formRef = ref<FormInstance | null>(null)

let mySet: Set<object> = new Set();

interface evaItem{
  department:String,
  office:String,
  name:String,
  ID:String,          //ID
  score:number
}

const gridData :evaItem[]=[
  {
    department:'长春分公司',
    office:'总经理',
    ID:'1',
    name: 'Peter Parker',
    score:NaN
  },
  {
    department:'长春分公司',
    office:'总经理',
    ID:'2',
    name: 'Peter Parker',
    score:NaN

  },
  {
    department:'长春分公司',
    office:'总经理',
    ID:'3',
    name: 'Peter Parker',
    score:NaN
  },
  {
    department:'长春分公司',
    office:'总经理',
    ID:'4',
    name: 'Peter Parker',
    score:NaN
  },
  {
    department:'长春分公司',
    office:'总经理',
    ID:'5',
    name: 'Peter Parker',
    score:NaN
  },
  {
    department:'长春分公司',
    office:'总经理',
    ID:'6',
    name: 'Peter Parker',
    score:NaN

  },
  {
    department:'长春分公司',
    office:'总经理',
    ID:'7',
    name: 'Peter Parker',
    score:NaN
  },
  {
    department:'长春分公司',
    office:'总经理',
    ID:'8',
    name: 'Peter Parker',
    score:NaN
  },
]

function hasDuplicateScores(gridData:any) {
    let i=0,j=0;
    for (i=0;i<gridData.length;i++) {
        for(j=i+1;j<gridData.length;j++){
          if(gridData[i].score===gridData[j].score){
            return [i,j]
          }
        }
    }
    return [i,j]; // No duplicate scores found
}

function changestyle(rows:any){
  const [num1, num2] = hasDuplicateScores(gridData)
  if(num1===rows.rowIndex||num2===rows.rowIndex){
    console.log([num1,num2])
    return { color:'#8B000F'}
  }else {
    return { color:'#00008B'}
  }
}
  




const tableRowClassName = ({
  row,
  rowIndex,
}: {
  row: evaItem
  rowIndex: number
}) => {
}


const inputValue = ref<string>('');
</script>





<template>
  <el-form
    ref="formRef"
    label-width="auto"
    class="demo-ruleForm"
    >
    <el-table  :data="gridData"  :row-class-name="tableRowClassName" :row-style="changestyle">
      <el-table-column type="index" width="50" />
      <el-table-column property="department" label="部门" width="150" />
      <el-table-column property="office" label="职位" width="200" />
      <el-table-column property="name" label="姓名" width="200" />
      <el-table-column label="得分" width="250">
        <template v-slot:default="{ row }">
            <el-input-number v-model="row.score" controls-position="right" :precision="2" :step="0.01" :min="60" :max="100"/>
        </template>
      </el-table-column>
    </el-table>
  </el-form> 

  
</template>



<style>
.el-form{
    display: flex;
    justify-content: center; /* horizontally center */
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.el-table{
    display: flex;
    justify-content: center; /* horizontally center */
    font-size: 20px; /* 设置表格中字体的大小 */

}

.same-score {
  background-color: #ff1d1d; /* 警示背景色 */
}


.el-table .success-row {
  --el-table-tr-bg-color: #ff1d1d;
}

</style>