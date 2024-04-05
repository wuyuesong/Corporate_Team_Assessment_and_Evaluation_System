<script setup lang="ts">
import { ref, onMounted ,reactive} from 'vue';
import { ElMessageBox , ElMessage} from 'element-plus';
import { request } from '/@/utils/service';
import { getBaseURL } from '/@/utils/baseUrl';
import evablock from '../component/evaluatorBlock.vue'
import { successMessage } from '/@/utils/message';
import relationtree from '../component/tree.vue'
import { forEach } from 'lodash';


onMounted(() => {
      fetchDepatOptions();
      fetchRankOptions ();
});
const loading = ref(false)
const dialogvisable=ref(false);
const addDrawvisable=ref(false);
const judge=ref(true);
const evaluatingbutton=ref(true);



const evaluatedrevert=async()=>{

    ElMessageBox.confirm('Do you want to submit?')
    .then(async () => {
      loading.value = true;
      const response=await request({
        url: getBaseURL() + 'api/system/staff/',
        method: 'get',
        params:{
            staff_department:form.department,
            staff_rank:form.staff_rank,
            
            "limit":500
        }
      })
      if(response.code===2000){
            griddata.value=response.data
            dialogvisable.value=false;
            judge.value=false;
            loading.value = false;
            evaluatingbutton.value=false;
      }else{
        loading.value = false;
        ElMessage({
        showClose: true,
        message: response.msg,
        type: 'error',
        })
      }
    })
    .catch((error) => {
        ElMessage({
        showClose: true,
        message: error.value,
        type: 'error',
        })
    })
}



// form内容
const form = reactive({
  department: '',
  staff_rank:''
})

/**
 * 关闭抽屉取消行为
 * @param done 
 */
const handleClose = (done: () => void) => {
  ElMessageBox.confirm('Are you sure you want to close this?')
    .then(() => {
      done()
    })
    .catch(() => {
        ElMessage({
        showClose: true,
        message: error.value,
        type: 'error',
        })
    })
}



const Departoptions = ref([]); // 用于存储选项列表
const Rankoptions = ref([]); // 用于存储选项列表
const griddata  =ref([])
// 异步请求获取选项列表
const fetchDepatOptions = async () => {
    try {
        // 发送请求并获取数据
        const response = await request({
        url: getBaseURL() + 'api/system/department/',
        method: 'get',})
        const data = await response.data;
        // 更新选项列表
        Departoptions.value = data;
    } catch (error) {
        ElMessage({
        showClose: true,
        message: error.value,
        type: 'error',
        })
    }
}

// 异步请求获取选项列表
const fetchRankOptions = async () => {
    try {
        // 发送请求并获取数据
        const response = await request({
        url: getBaseURL() + 'api/system/rank/unique_rank_list',
        method: 'get',})
        const data = await response.data;
        // 更新选项列表
        Rankoptions.value = data;
    } catch (error) {
        ElMessage({
        showClose: true,
        message: error.value,
        type: 'error',
        })
    }
}





const reset=()=>{
    ElMessageBox.confirm('Are you sure you want to reset this?')
    .then(() => {
        griddata.value=[]
        judge.value=true;
        evaluatingbutton.value=true;

    })
    .catch(() => {
        ElMessage({
        showClose: true,
        message: error.value,
        type: 'error',
        })
    })
    
}


/**
 * 根据页面提交信息增加对应组
 */

 async function fetchgroupData(targetElement) {
    try {
        const response = await request({
            url: getBaseURL() + 'api/system/staff/',
            method: 'get',
            params: {
                staff_department: targetElement.staff_department,
                staff_rank: targetElement.staff_rank,
                "limit": 500
            }
        });
        return response.data; // 直接返回数据
    } catch (error) {
        console.error("获取数据时出错:", error);
        return []; // 如果出现错误，则返回空数组
    }
}

const evaluatingGroup=ref([])
const reltree:any=ref(null);
const addevaluatinggroup=async()=>{
    loading.value = true;
    const evaluatingTabledata=ref([]);
    const addtarget=reltree.value.treeclick();
 
    


    try {
        // 发送请求并获取数据
        addtarget.forEach(async targetelement => {
            const response=await request({
                url: getBaseURL() + 'api/system/staff/',
                method: 'get',
                params:{
                    staff_department:targetelement.staff_department,
                    staff_rank:targetelement.staff_rank,
                    "limit":500
                }
            })
            const data = await response.data;
            evaluatingTabledata.value.push(...data)
        });

        evaluatingGroup.value.push({
            tableData:evaluatingTabledata,
            weight:null
        });
        loading.value = false;
        addDrawvisable.value=false;
        // 更新选项列表
    } catch (error) {
        ElMessage({
        showClose: true,
        message: error.value,
        type: 'error',
        })
    }
    
}

const removeChild=(index)=>{
      evaluatingGroup.value.splice(index, 1);
}


</script>


<template>


    <div class="eva_container">
        <div class="evaluating_container">
            <div class="evatag">
                <h4 class="evaluated_title">评价组</h4>
                <div class="addgrouo_container">
                    <el-button class="addgroup" @click="addDrawvisable=true" :disabled="evaluatingbutton">
                        <h4 class="evaluated_title">加入新的评价组</h4>
                    </el-button>
                </div>
          
            </div> 
            <el-drawer v-model="addDrawvisable" title="添加评价组"  direction="btt" size="70%" :before-close="handleClose">
                <div class="Evaluating_add__content">
                   <relationtree ref="reltree"></relationtree>
                    <div class="demo-drawer__footer">
                        <el-button type="primary" :loading="loading" @click="addevaluatinggroup">{{
                            loading ? 'Submitting ...' : 'Submit'
                            }}</el-button>                    
                    </div>
                </div>
            </el-drawer>
            <el-scrollbar max-height="85vh">
            <div v-for=" (group,index) in evaluatingGroup">
                <evablock v-model="evaluatingGroup[index]"  @remove="removeChild(index)"></evablock>
            </div>

            </el-scrollbar>
            
        </div>
        <div class="middle" style="font-size: 50px">
            <el-icon><DArrowRight /></el-icon>
        </div>
        <div class="evaluated_container">
            <p>
                <h4 class="evaluated_title">被评价组</h4>
            </p>
            <el-empty v-if="judge" id="emptyElement" description="Empty" style="width: 100%;" @click="dialogvisable=true"/>
            <el-drawer v-model="dialogvisable" title="添加被评价组"  :before-close="handleClose">
                <div class="Evaadd__content">
                    <el-form :model="form">
                        
                        <el-form-item label="部门" :label-width="'80px'">
                        <el-select
                            v-model="form.department"
                            placeholder="Please select "
                        >
                            <el-option label="" value=""/>
                            <el-option
                                v-for="item in Departoptions"
                                :key="item.staff_department"
                                :value="item.staff_department"
                            />
                            
                        </el-select>
                        </el-form-item>


                        <el-form-item label="职级" :label-width="'80px'">
                        <el-select
                            v-model="form.staff_rank"
                            placeholder="Please select "
                        >   
                            <el-option label="" value=""/>
                            <el-option
                                v-for="item in Rankoptions"
                                :key="item.name"
                                :value="item.name"
                            />
                            
                        </el-select>
                        </el-form-item>

                    </el-form>
                    <div class="demo-drawer__footer">
                        <el-button type="primary" :loading="loading" @click="evaluatedrevert">{{
                            loading ? 'Submitting ...' : 'Submit'
                            }}</el-button>
                        
                    </div>
                </div>
            </el-drawer>


            <el-table v-if="!judge" id="EvaluatedTable"
                    :data="griddata"
                    style="width: 100%" height="500">
                    <el-table-column prop="staff_name" label="名字"/>
                    <el-table-column prop="staff_firm_id" label="编号"/>true
            </el-table>
            <el-button class="evaluatedreset"  v-if="!judge" @click="reset" type="warning">reset</el-button>
        </div>
    </div>
    
</template>
<style>


.eva_container{
    display: flex; /* 使用 Flexbox 布局 */
}

.evatag{
    display: flex;
    align-items: center;
    margin-bottom: 20px;
   
}
.addgrouo_container{
    transition: transform 0.3s ease; 
    margin-left: 500px;
}
.addgrouo_container:hover{
    transform: scale(1.2); /* 按钮容器放大 */
}
.addgroup{
    background: #ededed;
    border-radius: 8px;
    color: #00050d;
    min-height: 20px;
    padding: 20px;
    
}
.evaluating_container{
    margin: 30px;
    padding: 20px;
    width: 800px;
    max-height: 100vh;
    box-sizing: border-box; /* 让 padding 和 border 不会增加元素的宽度和高度 */
    box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.3); /* 添加一个 10px 的模糊黑色阴影 */
    padding: 20px; /* 可选：为了美观，添加一些内边距 */
    border-radius: 10px;
}
.evaluated_container{
    max-height: 100vh;
    margin: 30px;
    padding: 20px;
    width: 500px;
    height:auto;
    box-sizing: border-box; /* 让 padding 和 border 不会增加元素的宽度和高度 */
    box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.3); /* 添加一个 10px 的模糊黑色阴影 */
    padding: 20px; /* 可选：为了美观，添加一些内边距 */
    border-radius: 10px;
}
.middle{
    display: flex; /* 使用 Flexbox 布局 */
    margin-top: 30px;
    margin-bottom: 30px;
    align-items: center;
}

.Evaadd__content{
    padding: 20px;
}
.el-empty{
    /* border: 1px solid rgb(100, 100, 100); 添加一个 2px 宽度的黑色边框 */
    /* background-color: lightgray; 当鼠标悬停时，改变背景色为浅灰色 */
}
/* .el-table{
    display: none;
} */

.el-empty:hover{
    background-color: lightgray; /* 当鼠标悬停时，改变边框颜色为深灰色 */
}


.evaluated_title{
    font-size: large;
    font-weight: bold; /* 鼠标悬停时的字体粗细 */

}
.evaluatedreset{
    margin-top: 10px;
}

.Evaluating_add__content{
    text-align: center;
}
</style>