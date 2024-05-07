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

const thistable = ref<HTMLTableElement | null>(null)
onMounted(() => {
	  fetchscoreList()
   
});
const subscoreloading=ref(false)
const loadingData=ref(false)

const gridrowflag=ref([])
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
              if(element.score===0.0){
                element.score=NaN
              }
              let item: evaItem = {
                department: element.evaluated_department,
                office: element.evaluated_rank,
                name: element.evaluated_name,
                ID: element.evaluated_id,
                score:element.score,             
                rank:-1
              };
              gridData.push(item);
              //@ts-ignore
              gridrowflag.value.push({
                state:false
              })
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
  same:{
    name:'',
    score:''
  },
  last:{
    name:'',
    score:''
  },
  next:{
    name:'',
    score:''
  }
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
  tips:number
}


const gridData :evaItem[]=[]

function hasDuplicateScores(gridData:any) {

//查重
    let i=0,j=0;
    for (i=0;i<gridData.length;i++) {
        for(j=i+1;j<gridData.length;j++){
          if(gridData[i].score===gridData[j].score&&gridData[i].score!==0){
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



  const filteredData = gridData.filter(item => !(isNaN(item.score)||typeof item.score === 'object'||item.score===0));
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
  
  
  if(row.score<60||row.score>100){
    row.score=NaN;
    row.tips=1;
    return;
  }

  row.tips=0;
  //将所有的tips置为0
  gridData.forEach(item => {
    item.tips = 0;
  });
  const [num1, num2] = hasDuplicateScores(gridData)
  if(!(num1===num2)){ 
    if(gridData[num1].ID===row.ID){
      errmessage.value.same.name=gridData[num2].name.toString();
      errmessage.value.same.score=gridData[num2].score.toString();
    }else{
      errmessage.value.same.name=gridData[num1].name.toString();
      errmessage.value.same.score=gridData[num1].score.toString();
    }
    
    let flag:boolean=false;
    let target:number=gridData[num1].score;
    row.score=NaN;
    const filteredData = gridData.filter((item, index) => {return !(index=== num1);}).filter(item => !(isNaN(item.score)||typeof item.score === 'object'||item.score===0));
    filteredData.sort((a, b) => b.score-a.score);
    errmessage.value.last.name='无'
    errmessage.value.last.score='60'
    errmessage.value.next.name='无'
    errmessage.value.next.score='100'
    for (const item of filteredData) {
        if (target>item.score) {
          errmessage.value.last.name=item.name.toString()
          errmessage.value.last.score=item.score.toString()
          break;
        }
        errmessage.value.next.name=item.name.toString()
        errmessage.value.next.score=item.score.toString()
    }
    row.tips=2;
    dialogVisible.value = true;
  }
}

const handleignore = (row:any)=>{
  row.tips=0;
  row.score=0;
  row.rank=-1;

}

const handlecancelignore=(row:any)=>{
  row.tips=0;
  row.score=NaN;
  row.rank=-1;
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


//未填数据获取焦点
const focusneedtobeWrite=(idx:number)=>{
  //@ts-ignore
  const table=thistable.value.$el.querySelector('.el-table__body-wrapper');
  const rows = table.querySelectorAll('.el-table__row');
  //@ts-ignore
  rows.forEach((row, index) => {
    if (index === idx) {
      const input = row.querySelector('input');
      if (input) {
        input.focus();
      }
    }
  });


  
  

}


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
      subscoreloading.value=true;
      try {
        utlsubmitStyle.value=[];
        for(let idx=0;idx<gridData.length;idx++){
          const{ID,score}=gridData[idx];
            if(typeof score === 'object'||isNaN(score)){
              ElMessage({
                  type: 'error',
                  message: '还有分数未填',
                })
                focusneedtobeWrite(idx)
                subscoreloading.value=false;
              return;
            }
            //@ts-ignore
            utlsubmitStyle.value.push({
              evaluated_id:ID,
              score:score
            })
        }
        const response = await request({
          url: getBaseURL() + 'api/system/evaluate_task/submit_evaluate_task/',
          method: 'post',
          data:{
            evaluate_id:Cookies.get('staff_id'),
            task_id:props.task_id,
            scores:utlsubmitStyle.value,
            submit_type:1,
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



/**
 * 暂存
 */
const tempsaveTaskcore=async()=>{
  try {
    utlsubmitStyle.value=[];
        for(let idx=0;idx<gridData.length;idx++){
          const{ID,score}=gridData[idx];

          let temp=score
          if(typeof score === 'object'||isNaN(score)){
            temp=0;
          }
          //@ts-ignore
          utlsubmitStyle.value.push({
            evaluated_id:ID,
            score:temp
          })
    }
    const response = await request({
          url: getBaseURL() + 'api/system/evaluate_task/submit_evaluate_task/',
          method: 'post',
          data:{
            evaluate_id:Cookies.get('staff_id'),
            task_id:props.task_id,
            scores:utlsubmitStyle.value,
            submit_type:0,
          }
        })
        const data = await response.data;
        if(response.code===2000){
          ElMessage({
            type: 'success',
            message: "保存成功",
          })
        }else{
          ElMessage({
          type: 'error',
          message: response.msg,
          })
        }
  } catch (error) {
    
  }
}


const handleenter=(row:any,event)=>{
  event.target.blur();
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
    <span>输入重复，请重新输入</span><br>
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
    <!-- <el-text size="large"  class="Scorediscription">
      <textarea readonly cols="100" rows="5"> {{ $props.discribe }}</textarea>
    </el-text> -->
    <el-input class="Scorediscription" v-model="$props.discribe" type="textarea"  disabled="true" autosize="true" />
  </div>
  <el-scrollbar height="450px" >
  <el-form
    ref="formRef"
    label-width="auto"
    class="demo-ruleForm"
    >
    <el-table   ref="thistable" :key="loadingData" :data="gridData" :row-class-name="tableRowClassName" :row-style="changestyle">
      <el-table-column type="index" width="70" />
      <el-table-column property="department" label="部门" width="150" />
      <el-table-column property="office" label="职位" width="200" />
      <el-table-column property="name" label="姓名" width="200" />
      <el-table-column label="得分" width="300">
        <template v-slot:default="{ row }">
              <el-input-number v-model="row.score" controls-position="right" :precision="2" :step="0.01" :controls="false"  @keyup.enter.native="handleenter(row,$event)" @blur="handlesame(row)" v-if="row.score!==0"/>
              <el-tag  style="width: 150px;" v-if="row.score===0" effect="dark" size="large">不了解不予打分</el-tag>
              <el-button  type="info" size="large" style="background-color: cornflowerblue; margin-left: 10px;width: 70px;margin-top:5px;margin-bottom:5px;" @click="handleignore(row)" v-if="row.score!==0">不了解</el-button>
              <el-button type="info"  size="large" style="background-color:firebrick; margin-left: 10px;width: 70px;margin-top:5px;margin-bottom:5px;" v-if="row.score===0" @click="handlecancelignore(row)">撤销</el-button>
        </template>
      </el-table-column>
    <el-table-column  label="排名" property="rank" width="100">
      <template v-slot:default="{ row }">
        <div class="rankandtips">
            <p>{{ row.rank }}</p>
        </div>
        
      </template>
    </el-table-column>
    <el-table-column width="300">
      <template v-slot:default="{ row }">
        <div :key="0" v-if="row.tips === 0"></div>
        <el-alert :key="1" v-if="row.tips === 1" title="分数需要在60和100之间" type="warning" show-icon :closable="false"/>
        <div :key="2" v-show="row.tips === 2">
          <el-alert :title="'上一个人：'+errmessage.last.name+'，分值为'+errmessage.last.score" type="warning" show-icon :closable="false"/>
          <el-alert :title="'与'+ errmessage.same.name+'重复，分值为'+errmessage.same.score" type="error" show-icon :closable="false"/>
          <el-alert :title="'下一个人：'+errmessage.next.name+'，分值为'+errmessage.next.score" type="warning" show-icon :closable="false"/>
        </div>
      </template>
    </el-table-column>
    </el-table>
  </el-form>
  <div class="submitscored">
    <el-col :span="5"></el-col>
    <el-col :span="7"><el-button size="large" type="info" @click="tempsaveTaskcore">保存</el-button></el-col>
    <el-col :span="6"></el-col>
    <el-col :span="6"><el-button  size="large" type="danger" @click="submitTaskcore">提交</el-button></el-col>
    
  </div>
  </el-scrollbar>
</div>
</template>



<style scoped>
.el-form{
    display: flex;
    justify-content: center; /* horizontally center */
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
.Scorediscription{
  margin-top: 10px;
  margin-bottom: 10px;
  font-size: large;
}

.rankandtips{
  display: flex;
  text-align: center;
  align-items: center;
  justify-content: center;
}
</style>

