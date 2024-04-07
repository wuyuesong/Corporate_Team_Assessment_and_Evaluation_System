<script setup lang="ts">
import { defineProps ,ref,onMounted,getCurrentInstance,inject} from 'vue';
import type { FormInstance } from 'element-plus'
import { request } from '/@/utils/service';
import { getBaseURL } from '/@/utils/baseUrl';
import Cookies from 'js-cookie';
import type { Action } from 'element-plus'
import { ElMessageBox ,ElMessage} from 'element-plus'
const refreshView = inject('refreshView')
onMounted(() => {
	  fetchscoreList()
   
});
const subscoreloading=ref(false)
const loadingData=ref(false)
const fetchscoreList= async()=>{
  try {
        // 发送请求并获取数据
        const response = await request({
          url: getBaseURL() + 'api/system/evaluate_task/evaluate_task_info/',
          method: 'post',
          data:{
            staff_id:Cookies.get('staff_id'),
            task_id:props.task_id

          }
        })
        const data = await response.data;
        if(response.code===2000){
            for (let index = 0; index < data.length; index++) {
              const element = data[index];
              let item: evaItem = {
                department: element.evaluated_department,
                office: element.evaluated_rank,
                name: element.evaluated_name,
                ID: element.evaluated_id,
                score:NaN,             
                rank:-1
              };
              gridData.push(item);
            }
            loadingData.value=!loadingData.value
        }else{
          ElMessage({
            showClose: true,
            message: response.msg,
            type: 'error',
            })
        }
    } catch (error) {
        ElMessage({
        showClose: true,
        message: error.message,
        type: 'error',
        })
    }
}

const dialogVisible = ref(false)
const formRef = ref<FormInstance | null>(null)
const errmessage=ref({
  lastnum:'',
  nextnum:''
})

const props = defineProps({
  task_id:String,
  title:String,
  discribe:String
});



let mySet: Set<object> = new Set();

interface evaItem{
  department:String,
  office:String,
  name:String,
  ID:String,          //ID
  score:number,
  rank:number,
}


const gridData :evaItem[]=[]

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


/**
 * 提交分数
 */
const utlsubmitStyle=ref([])
 const submitTaskcore=()=>{
  ElMessageBox.confirm(
    '是否确认提交?',
    'Warning',
    {
      confirmButtonText: 'OK',
      cancelButtonText: 'Cancel',
      type: 'warning',
    }
    )
    .then(async() => {
      ElMessage({
        type: 'success',
        message: 'Submit completed',
      })
      subscoreloading.value=true;
      
      try {
        utlsubmitStyle.value=[];
        gridData.forEach(ele=>{
            const{ID,score}=ele;
            utlsubmitStyle.value.push({
              evaluated_id:ID,
              score:score
            })
        })
        const response = await request({
          url: getBaseURL() + 'api/system/evaluate_task/submit_evaluate_task/',
          method: 'post',
          data:{
            evaluate_id:Cookies.get('staff_id'),
            task_id:props.task_id,
            scores:utlsubmitStyle.value
          }
        })
        const data = await response.data;
        if(response.code===2000){
          subscoreloading.value=false;
          ElMessageBox.alert('Success', '成功提交', {
            confirmButtonText: 'OK',
            callback: (action: Action) => {
              location.reload()
            },
          })
        }else{
          ElMessage({
          type: 'error',
          message: response.msg,
          })
          subscoreloading.value=false;
        }

        
      } catch (error) {
        ElMessage({
        type: 'error',
        message: error.message,
        })
        subscoreloading.value=false;
      }
      



      
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: 'Submit canceled',
      })
    })
}



</script>





<template>

<div class="scorelistCon"  v-loading="subscoreloading">

  <el-dialog
      v-model="dialogVisible"
      v-bind="errmessage"
      title="tips"
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





  <div class="prescore">
    <p class="scorelistTitle">{{ $props.title }}</p>
    <el-text size="large"> {{ $props.discribe }}</el-text>
  </div>
  <el-form
    ref="formRef"
    label-width="auto"
    class="demo-ruleForm"
    >
    <el-table   ref="thistable" :key="loadingData" :data="gridData" :row-class-name="tableRowClassName" :row-style="changestyle">
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
  <div class="submitscored">
    <el-col :span="12"></el-col>
    <el-col :span="10"></el-col>
    <el-col :span="8"><el-button size="large" type="danger" @click="submitTaskcore"> 提交</el-button></el-col>
    
  </div>
</div>
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
.prescore{
  flex:block;
  text-align: center; /* horizontally center */
}

.scorelistTitle{
    font-size: 3rem;
    line-height: 1.33333;
    font-weight: 400;
    color: #4a4a4a;
    top: 0;
    left: 0;
    padding: 13px;
    margin: 0;
}

.submitscored{
  margin: 20px;
  display: flex;
}
</style>