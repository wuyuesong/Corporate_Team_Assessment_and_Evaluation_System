<script setup lang="ts">
import { ref, onMounted ,reactive,inject} from 'vue';
import { ElMessageBox , ElMessage ,ElSegmented } from 'element-plus';
import { request } from '/@/utils/service';
import { getBaseURL } from '/@/utils/baseUrl';
import evablock from '../component/evaluatorBlock.vue'
import { CaretLeft } from '@element-plus/icons-vue';
import { successMessage } from '/@/utils/message';
import relationtree from '../component/tree.vue'
const refreshView = inject('refreshView')

onMounted(() => {
      fetchDepatOptions();
      fetchRankOptions ();
});
const pageloading = ref(false)
const loading = ref(false)
const dialogvisable=ref(false);
const addDrawvisable=ref(false);
const judge=ref(true);
const evaluatingbutton=ref(true);
//单选框变量
const noticeradio = ref('1')

//起止时间响应变量
const startendTime=ref('');
//任务标题
const TaskTitle=ref('');
//任务描述
const TaskDescription=ref('');


//使用map查重
const allevaluatemap=ref(new Map());

//发布任务按钮
const taskpresentbutton=ref(true);


const evaluatedrevert=async()=>{

    ElMessageBox.confirm('确认提交?',{
        confirmButtonText: '确认',
        cancelButtonText: '取消'
    })
    .then(async () => {
      loading.value = true;
      const response=await request({
        url: 'api/system/staff/',
        method: 'get',
        params:{
            staff_department:form.department,
            staff_rank:form.staff_rank,
            
            "limit":500
        }
      })
      if(response.code===2000){
            griddata.value.push(...response.data)
            dialogvisable.value=false;
            judge.value=false;
            loading.value = false;
            evaluatingbutton.value=false;

            //去除重复
            griddata.value=griddata.value.filter((item:any,index:any)=>{
                return griddata.value.findIndex((item2:any)=>item2.staff_id===item.staff_id)===index
            })

            //evaedoptions加入
            griddata.value.forEach(item=>{
                //判断是否已经加入
                if(!evaedoptions.value.includes(item.staff_job)){
                    evaedoptions.value.push(item.staff_job)
                    weight.value[item.staff_job]={}
                }
            })
            evavalue.value=evaedoptions.value[0]
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
  ElMessageBox.confirm('确定要关闭吗',{
    confirmButtonText: '确认',
    cancelButtonText: '取消'
  })
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
        url: 'api/system/department/',
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
        url: 'api/system/rank/unique_rank_list/',
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

const feach_rank_of_deparrtment=async(department:any)=>{

    form.staff_rank='';
    if(department===''){
        try {
            // 发送请求并获取数据
            const response = await request({
            url: 'api/system/rank/unique_rank_list/',
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
    }else{
        try {
                // 发送请求并获取数据
                const response = await request({
                url: 'api/system/rank/department_get_rank/',
                method: 'post',
                data:{
                    department:form.department
                }
                })
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
    
}





const reset=()=>{
    ElMessageBox.confirm('你确认要重置?',{
        confirmButtonText: '确认',
        cancelButtonText: '取消'

    })
    .then(() => {
        griddata.value=[]
        evaluatingGroup.value = [];
        judge.value=true;
        evaluatingbutton.value=true;
        evaedoptions.value=[];
        weight.value={};

    })
    .catch(() => {
        ElMessage({
        showClose: true,
        message: error.value,
        type: 'error',
        })
    })
    
}


const evaluatingGroup=ref([])
const reltree:any=ref(null);
const addevaluatinggroup=async()=>{
    loading.value = true;
    const evaluatingTabledata=ref([]);
    const addtarget=reltree.value.treeclick();
    console.log(addtarget)

    try {
        // 发送请求并获取数据
        addtarget.forEach(async targetelement => {
            const response=await request({
                url:  'api/system/staff/',
                method: 'get',
                params:{
                    staff_department:targetelement.staff_department,
                    staff_rank:targetelement.staff_rank,
                    "limit":500
                }
            })
            if(response.code==2000){
                const data = await response.data;
                let flag=true
                for(const item of data){
                    if(allevaluatemap.value.has(item.staff_id)){
                        flag=false;
                        ElMessage({
                            showClose: true,
                            message: allevaluatemap.value.get(item.staff_id)+'已经存在，请不要重复添加',
                            type: 'error',
                        })
                        return 
                    }
                }
                if(flag){
                    evaluatingTabledata.value.push(...data)
                    evaluatingTabledata.value.forEach(item=>{
                        allevaluatemap.value.set(item.staff_id,item.staff_name)

                        if(!evaoptions.value.includes(item.staff_job)){
                            evaoptions.value.push(item.staff_job)
                            for (const eva in weight.value) {
                                weight.value[eva][item.staff_job]=0
                            }
                        }
                    })
                }
            } else{
                ElMessageBox.alert(response.message)
                return
           }
            
        });
        evaluatingGroup.value.push({
            tableData:evaluatingTabledata,
            task_weight:null
        });
        loading.value = false;
        addDrawvisable.value=false;
        //判断当前有无group
        if(evaluatingGroup.value.length>0){
            taskpresentbutton.value=false;
        }else{
            taskpresentbutton.value=true;
        }
        
        // 更新选项列表
    } catch (error) {
        ElMessage({
        showClose: true,
        message: error.value,
        type: 'error',
        })
    }
    
}

//子组件给出删除项
const removeAllMapOne=(staffid)=>{
    allevaluatemap.value.delete(staffid)
}
const removeChild=(index)=>{

    evaluatingGroup.value[index].tableData.forEach(element => {
        allevaluatemap.value.delete(element.staff_id)
    });
    evaluatingGroup.value.splice(index, 1);
    if(evaluatingGroup.value.length>0){
        taskpresentbutton.value=false;
    }else{
        taskpresentbutton.value=true;
    }
    refreshevaoptions()
}

const refreshevaoptions = ()=>{
    evaoptions.value=[]
    for (const eva in weight.value) {
        weight.value[eva]={}
    }
    for(const item of evaluatingGroup.value){
        for (const ele of item.tableData) {
            if(!evaoptions.value.includes(ele.staff_job)){
                evaoptions.value.push(ele.staff_job)
                for (const eva in weight.value) {
                    weight.value[eva][ele.staff_job]=0
                }
            }
        }
    }
}


//请求负载的标准数据
const torequestEvaluate =ref([])
const toEvaluatedTotal =ref([])
const torequestEvaluated =ref([])
const weighttable=ref({})
/**
 * 请求负载处理
 */
const processtoRequestData=()=>{
    torequestEvaluate.value=[];
    torequestEvaluated.value=[];
    toEvaluatedTotal.value=[];
    
    
    evaluatingGroup.value.forEach(element => {
        // let total=element.tableData.length;
        // if(element.task_weight===null){
        //     totalweight=-1;
        //     return;
        // }
        // totalweight=totalweight+parseFloat(element.task_weight);
        // let avaweight=parseFloat(element.task_weight)/total;
        element.tableData.forEach(ele=>{
            const {staff_id,staff_job} =ele;
            if(toEvaluatedTotal[staff_job]===undefined){
                toEvaluatedTotal[staff_job]=1;
            }else{
                toEvaluatedTotal[staff_job]=toEvaluatedTotal[staff_job]+1;
            }

            torequestEvaluate.value.push({
                evaluate_id:staff_id,
                staff_job:staff_job
                // task_weight:avaweight
            })
        })
    });
    // if(totalweight<0){
    //     ElMessage({
    //             showClose: true,
    //             message: "存在权重没填",
    //             type: 'error',
    //     })
    //     return true;
    // }
    // if(!(totalweight===100)){
    //     ElMessage({
    //             showClose: true,
    //             message: "权重总和不为100",
    //             type: 'error',
    //         })
    //     return true;
    // }

    //遍历evaluatedGroup数据
    griddata.value.forEach(element=>{
        const {staff_id,staff_job} =element;
        torequestEvaluated.value.push({
            evaluated_id:staff_id,
            staff_job:staff_job
        })
    })
    //遍历weight
    for(const evaed in weight.value){
        let evaedtotal=0
        for(const eva in weight.value[evaed]){
            evaedtotal+=weight.value[evaed][eva]
            weight.value[evaed][eva]=weight.value[evaed][eva]/toEvaluatedTotal[eva]
        }
        if(!( evaedtotal === 100 || evaedtotal ===0)){
            ElMessage({
                showClose: true,
                message: evaed+'权重总和不为100',
                type: 'error',
            })
            return true;
        }

    }

    
    return false;
}



/**
 * 发布任务
 * @async  发布接口
 * 
 */

const TaskPreSubmit=async(type:number)=>{
    if (evaluatingGroup.value.length === 0|| griddata.value.length===0) {
        ElMessage({
        showClose: true,
        message: "评价组或被评价组尚未填入，请重试",
        type: 'error',
        })
        return;
    } 
    if(processtoRequestData()){
        return;
    }
    if(TaskTitle.value.length<=0){
        ElMessage({
            showClose: true,
            message: "请输入任务标题",
            type: 'error',
        })
        return;
    }
    if(startendTime.value.length<2){
        ElMessage({
            showClose: true,
            message: "请输入起止时间",
            type: 'error',
        })
        return;
    }
    
    pageloading.value=true;
    weighttable.value={};
    for(const item of torequestEvaluate.value){
        //遍历torequestEvaluated
        if (!weighttable.value[item.evaluate_id]) {
            weighttable.value[item.evaluate_id] = {};
        }
        for(const item2 of torequestEvaluated.value){
            weighttable.value[item.evaluate_id][item2.evaluated_id] = weight.value[item2.staff_job][item.staff_job]
        }
    }
    try {
        const response=await request({
                url: 'api/system/evaluate_task/evaluate_task_create/',
                method: 'post',
                data:{
                    task_name: TaskTitle.value,
                    task_describe:TaskDescription.value,
                    task_start_date:startendTime.value[0],
                    task_end_date:startendTime.value[1],
                    evaluate:torequestEvaluate.value,
                    evaluated:torequestEvaluated.value,
                    weight_to_evaluated:weighttable.value,
                    task_type:type,
                    //已完成
                    inform_type:noticeradio.value,
                }
        })
        if(response.code==2000){
            pageloading.value=false;
            ElMessage({
                showClose: true,
                message: "任务成功发布",
                type: 'success',
            })
            refreshView()

        } else{
            ElMessageBox.alert(response.message);
            torequestEvaluate.value=[];
            torequestEvaluated.value=[];
            pageloading.value=false;
        }
    } catch (error) {
        ElMessage({
        showClose: true,
        message: error.value,
        type: 'error',
        })
        pageloading.value=false;
    }

}

const swiftsubmitstyle=ref(true)



const transfertoevaluate=()=>{
    const evaluatingTabledata=griddata.value
    //查找数据中有没有重复，没有加入map 有就报错
    let flag=true;
    for( const item of evaluatingTabledata){
        if(allevaluatemap.value.has(item.staff_id)){
            flag=false;
            ElMessage({
                showClose: true,
                message: allevaluatemap.value.get(item.staff_id)+'已经存在，请不要重复添加',
                type: 'error',
            })
            return
        }
    }
    if(flag){
        evaluatingGroup.value.push({
            tableData:evaluatingTabledata,
            task_weight:null
        });
        evaluatingTabledata.forEach(item=>{
            allevaluatemap.value.set(item.staff_id,item.staff_name)

            if(!evaoptions.value.includes(item.staff_job)){
                evaoptions.value.push(item.staff_job)
                for (const eva in weight.value) {
                    weight.value[eva][item.staff_job]=0
                }
            }
        })
    }
    if(evaluatingGroup.value.length>0){
        taskpresentbutton.value=false;
    }else{
        taskpresentbutton.value=true;
    }
}

const evaoptions = ref([])
const evaedoptions = ref([])


const weight=ref({
    // '总监':{
    //     '总监':0,
    //     '部门正职':0,
    //     '部门副职':0,
    // },
    // '部门正职':{
    //     '总监':0,
    //     '部门正职':0,
    //     '部门副职':0,
    // },
    // '部门副职':{
    //     '总监':0,
    //     '部门正职':0,
    //     '部门副职':0,
    // },
})


const evavalue = ref()

</script>


<template>
    

<div v-loading="pageloading">
    <div class="TaskPresntHeader">
        <div class="TitleAndDes">
            <div>
                <input type="text" aria-label="标题" v-model="TaskTitle" placeholder="标题" class="TasktitleInput"/>
            </div>
            <div>
                <el-input
                    class="desArea"
                    v-model="TaskDescription"
                    maxlength="300"
                    rows="6"
                    placeholder="请对任务进行必须的描述"
                    show-word-limit
                    type="textarea"
                />
            </div>

        </div>
        <div class="ArrangeTime">
            <span class="titlefont">
                任务时间设置
            </span>

            <div>
                <el-date-picker 
                class="timepicker"
                size="large"
                v-model="startendTime"
                type="datetimerange"
                range-separator="To"
                start-placeholder="Start date"
                end-placeholder="End date"
                value-format="YYYY-MM-DD HH:mm:ss"
                />
            </div>
            <div class="SubmitTaskButton" style="margin-top: 70px;">
                <div class="mb-2 text-sm">
                    <el-radio-group v-model="noticeradio">
                        <el-radio value="1" size="large" border>邮件通知</el-radio>
                        <el-radio value="2" size="large" border>匿名通知</el-radio>
                    </el-radio-group>
                </div>
                <el-button class="evaTaskPresent_relname" :disabled="taskpresentbutton" @click="TaskPreSubmit(0)" size="large" type="danger" >发布任务</el-button>
            </div>
            
        </div>

    </div>



    <div class="eva_container">
        <div class="evaluating_container">
            <div class="evatag">
                <h4 class="evaluated_title">评价组</h4>
                <div class="addgrouo_container">
                    <el-button class="addgroup" @click="addDrawvisable=true" :disabled="evaluatingbutton">
                        <h4 class="evaluated_title">加入评价组</h4>
                    </el-button>
                </div>
          
            </div> 
            <el-drawer v-model="addDrawvisable" title="添加评价组"  direction="btt" size="70%" :before-close="handleClose">
                <div class="Evaluating_add__content">
                   <relationtree ref="reltree"></relationtree>
                    <div class="demo-drawer__footer">
                        <el-button type="primary" :loading="loading" @click="addevaluatinggroup">{{
                            loading ? '确认 ...' : '确认'
                            }}</el-button>                    
                    </div>
                </div>
            </el-drawer>
            <el-scrollbar max-height="85vh">
            <div v-for=" (group,index) in evaluatingGroup"> 
                <evablock v-model="evaluatingGroup[index]"  @remove="removeChild(index)" @removeallmapone="removeAllMapOne"></evablock>
            </div>
            </el-scrollbar>
            
        </div>
        <div class="middle" style="font-size: 50px">
            <el-icon><DArrowRight /></el-icon>
        </div>
        <div class="evaluated_container">
            <div style="display: flex;">
            <p class="evaluated_title">被评价组    
            </p>
            <el-button v-if="!judge"  class="shadow-lg shadow-orange-400/10 ..." @click="transfertoevaluate"  style="background-color: #fc7319;" size="large" :icon="CaretLeft" ><p class="font-mono font-bold antialiased text-slate-50 ... ">移动</p></el-button>
                
            </div>
            
            <el-empty v-if="judge" id="emptyElement" description="Empty" style="width: 100%;" @click="dialogvisable=true"/>
            <el-drawer v-model="dialogvisable" title="添加被评价组"  :before-close="handleClose">
                <div class="Evaadd__content">
                    <el-form :model="form">
                        
                        <el-form-item label="部门" :label-width="'80px'">
                        <el-select
                            v-model="form.department"
                            placeholder="Please select "
                            :change="feach_rank_of_deparrtment(form.department)"
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
                            loading ? '确认 ...' : '确认'
                            }}</el-button>
                        
                    </div>
                </div>
            </el-drawer>


            <el-table v-if="!judge" id="EvaluatedTable"
                    :data="griddata"
                    style="width: 100%" height="600">
                    <el-table-column prop="staff_name" label="名字"/>
                    <el-table-column prop="staff_firm_id" label="编号"/>true
            </el-table>
            <div class="UtlTaskButton" v-if="!judge" >
                <div>
                    <el-button class="transition ease-in-out delay-150 bg-blue-500 hover:-translate-y-1 hover:scale-110 hover:bg-indigo-500 duration-300 ..." @click="reset"  size="large" type="warning" >重置</el-button>
                    <el-button class="transition ease-in-out delay-150 bg-blue-500 hover:-translate-y-1 hover:scale-110 hover:bg-indigo-500 duration-300 ..." size="large" type="primary" @click="dialogvisable=true">
                        增加
                    </el-button>
                </div>
              
            </div>

            
        </div>
        
    </div>
    <div class="rounded-lg shadow-xl hover:shadow-2xl ..." style="margin: 30px; padding: 20px; min-height: 500px;box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.3); ">
        <div class="ContentBody" v-if=true>
            <h1 class="text-3xl font-extrabold text-center text-gray-700 bg-clip-text">
                评价人权重配置
            </h1>
            <!-- <div>
                <el-segmented class="segment" v-model="evavalue" :options="evaedoptions" block />
            </div> -->

            <el-segmented class="segment" v-model="evavalue" :options="evaedoptions" block >
                <template #default="{ item }">
                    <div class="text-1xl font-bold text-center bg-clip-text">{{ item }}</div>
                </template>
            </el-segmented>
<!-- 
            <el-radio-group v-model="evavalue" size="large" style="display: flex;">
                <el-radio-button
                    v-for="item in evaedoptions"
                    :key="item"
                    :label="item"
                >
                    {{ item }}
                </el-radio-button>
            </el-radio-group> -->
            
            <div v-for="item in evaedoptions">
                <div class="evacontent" v-if="item==evavalue">
                    <span class="text-xl  text-center text-gray-700 bg-clip-text">被评价对象层级 / {{ item }}</span>
                    <div class="wightFillblock" v-for="evaitem in evaoptions">
                        <span class="text-xl  text-center text-gray-700 bg-clip-text"style="width: 300px;">{{ evaitem }}(权重%)</span>
                        <el-input-number class="weight_input" v-model="weight[item][evaitem]" :min="0" :max="100"  placeholder="权重(总和100)"  controls-position="right"/>
                    </div>
                </div>
            </div>
        </div>
        <div class="ContentBody" v-else>
            <el-empty description="请选择任务进行配置" />
        </div>

    </div>
    
</div>
    
</template>
<style>

.TaskPresntHeader{
    margin-left: 30px;
    margin-right: 30px;
    margin-top:20px;
    box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.3); /* 添加一个 10px 的模糊黑色阴影 */
    padding: 20px; /* 可选：为了美观，添加一些内边距 */
    border-radius: 10px;
    display: Flex;
    height: 300px;
}
.TitleAndDes{
    padding: 10px;
    width: 70%;
    height: auto
}

.ArrangeTime{
    padding: 10px;
    width: 30%;
    height: auto;
    display: flex;
    flex-direction: column;
}
.titlefont{
    color: rgba(0, 0, 0, .54);
    font-size: 20px;
    font-weight: 400;
    line-height: 24px;
    margin-bottom: 20px;
}
.TasktitleInput{
    padding-inline: 8px;
    background-color: transparent;
    border-bottom: 3px solid #fc7319; /* 添加下边框线，2px宽，灰色 */
    display: block;
    font: 400 20px Helvetica, Arial, sans-serif;
    width: 70%;
    transition: border-bottom 0.2s; 
}
.TasktitleInput:focus{
    border-bottom: 5px solid #fc7319; /* 添加下边框线，2px宽，灰色 */
}
.desArea{
    margin-top: 30px;
    font-size: 18px;
    width: 70%;
}
.eva_container{
    display: flex; /* 使用 Flexbox 布局 */
    width: 100%;
}

.evatag{
    display: flex;
    align-items: center;
    width: 100%;
    margin-bottom: 20px;
   
}
.addgrouo_container{
    transition: transform 0.3s ease; 
    width: 25%;
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
    width: 65%;
    max-height: 120vh;
    box-sizing: border-box; /* 让 padding 和 border 不会增加元素的宽度和高度 */
    box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.3); /* 添加一个 10px 的模糊黑色阴影 */
    padding: 20px; /* 可选：为了美观，添加一些内边距 */
    border-radius: 10px;
}
.evaluated_container{
    max-height: 120vh;
    margin: 30px;
    padding: 20px;
    width:30%;
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
    width: auto;
}

.Evaadd__content{
    padding: 20px;
}
.el-empty{
    /* border: 1px solid rgb(100, 100, 100); 添加一个 2px 宽度的黑色边框 */
    /* background-color: lightgray; 当鼠标悬停时，改变背景色为浅灰色 */
}

.el-empty:hover{
    background-color: lightgray; /* 当鼠标悬停时，改变边框颜色为深灰色 */
}


.evaluated_title{
    font-size: large;
    font-weight: bold; /* 鼠标悬停时的字体粗细 */
    padding: 10px;
    width: 75%;

}


.Evaluating_add__content{
    text-align: center;
}
.UtlTaskButton{
    display: flex;
    align-items: center;
    margin-top: 10px;
}

.SubmitTaskButton{
}
.evablock{
    width: 100%;
}
.ml-2{
    margin-right: 20px;
}


.evaTaskPresent_relname {
    width: 255px;  
}

.OTheaderBlank{
    display: flex;
    align-items: center;
    padding-left: 30px;
    width: 80%;
}
.ContentBody{
    display: flex;
    width: 100%;
    padding-top: 20px;   
    flex-direction: column;
}
.segment{
    margin-top: 20px;
    background-color: #dadada; /* 白色背景 */
}
.evacontent{
    margin-top: 20px;
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;

}
.wightFillblock{
    display: flex;
    flex-direction: row;
    align-items: center; 
    background-color: #ffffff; /* 白色背景 */
    border-radius: 10px;        /* 圆角5px */
    border: 1px solid #cccccc; /* 灰色边框 */
    width: 600px;               /* 宽度300px */
    height: 50px;              /* 高度100px */
    margin: 10px;
    padding: 10px;
}
.submitbutton{
    width: 80%;
    display: flex;
    justify-content: right;
    align-items: right; 
    text-align: right;
}
.weight_input{
    width: 300px;
}
</style>