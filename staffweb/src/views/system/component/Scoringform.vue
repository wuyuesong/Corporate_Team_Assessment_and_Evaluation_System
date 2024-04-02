<script setup lang="ts">
import { defineProps ,ref} from 'vue';
import type { FormInstance } from 'element-plus'
import { ITEM_RENDER_EVT } from 'element-plus/es/components/virtual-list/src/defaults';
import { isNull, isNumber, last } from 'lodash';
import { ElMessageBox } from 'element-plus'
import { trace } from 'console';
const dialogVisible = ref(false)
const formRef = ref<FormInstance | null>(null)
const errmessage=ref({
  lastnum:'',
  nextnum:''
})
let mySet: Set<object> = new Set();

interface evaItem{
  department:String,
  office:String,
  name:String,
  ID:String,          //ID
  score:number,
  rank:number,
}


const gridData :evaItem[]=[
  {
    department:'长春分公司',
    office:'总经理',
    ID:'1',
    name: 'Peter Parker',
    score:NaN,
    rank:-1

  },
  {
    department:'长春分公司',
    office:'总经理',
    ID:'2',
    name: 'Peter Parker',
    score:NaN,
    rank:-1
  

  },
  {
    department:'长春分公司',
    office:'总经理',
    ID:'3',
    name: 'Peter Parker',
    score:NaN,
    rank:-1

  },
  {
    department:'长春分公司',
    office:'总经理',
    ID:'4',
    name: 'Peter Parker',
    score:NaN,
    rank:-1

  },
  {
    department:'长春分公司',
    office:'总经理',
    ID:'5',
    name: 'Peter Parker',
    score:NaN,
    rank:-1

  },
  {
    department:'长春分公司',
    office:'总经理',
    ID:'6',
    name: 'Peter Parker',
    score:NaN,
    rank:-1


  },
  {
    department:'长春分公司',
    office:'总经理',
    ID:'7',
    name: 'Peter Parker',
    score:NaN,
    rank:-1

  },
  {
    department:'长春分公司',
    office:'总经理',
    ID:'8',
    name: 'Peter Parker',
    score:NaN,
    rank:-1

  },
]

function hasDuplicateScores(gridData:any) {

//查重
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

  gridData.forEach(item => {
    if(typeof item.score === 'object'||isNaN(item.score)){
      item.rank = -1
    }
  });



  const filteredData = gridData.filter(item => !(isNaN(item.score)||typeof item.score === 'object'));
  filteredData.sort((a, b) => b.score - a.score);
  filteredData.forEach((item, index) => {
      item.rank = index + 1;
  });
  if(num1===rows.rowIndex||num2===rows.rowIndex){

    return { color:'#8B000F'}
  }else {
    return { color:'#00008B'}
  }
}

const handlesame =(row:any)=>{

  
  const [num1, num2] = hasDuplicateScores(gridData)
  if(!(num1===num2)){
    
    let flag:boolean=false;
    let target:number=gridData[num1].score;
    console.log(target)
    row.score=NaN;
    
    const filteredData = gridData.filter((item, index) => {return !(index=== num1);}).filter(item => !(isNaN(item.score)||typeof item.score === 'object'));
    filteredData.sort((a, b) => b.score-a.score);
    console.log(filteredData)
    let min:number=60;
    let max:number=100;
    
    for (const item of filteredData) {
        if (target > item.score) {
          console.log(item.score);
          target = item.score;
          flag = true;
          break; // 使用 break 跳出整个循环
        }
        max = item.score;
    }

    if(flag){
      errmessage.value.lastnum=target.toString();
      errmessage.value.nextnum=max.toString();
    }else{
      errmessage.value.lastnum=min.toString();
      errmessage.value.nextnum=max.toString();
    }
    console.log("**********************************")
    dialogVisible.value = true;
  }
}

const handleClose = (done: () => void) => {

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

<el-dialog
    v-model="dialogVisible"
    v-bind="errmessage"
    title="Tips"
    width="500"
    :before-close="handleClose"
  >
    <span>输入重复，请重新输入 ,{{ errmessage.lastnum }} 和 {{ errmessage.nextnum }}</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>
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
            <el-input-number v-model="row.score" controls-position="right" :precision="2" :step="0.01" :min="60" :max="100" @keyup.enter="handlesame(row)" @blur="handlesame(row)"/>

        </template>
      </el-table-column>
    <el-table-column  label="排名" property="rank" />
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