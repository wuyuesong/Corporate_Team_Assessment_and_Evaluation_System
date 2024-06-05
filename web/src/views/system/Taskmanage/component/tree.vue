<script lang="ts" setup>
import { onMounted,ref , getCurrentInstance} from 'vue';
import { ElMessageBox , ElMessage} from 'element-plus';
import { request } from '/@/utils/service';
import { getBaseURL } from '/@/utils/baseUrl';


const defaultProps = {
  children: 'children',
  label: 'value',
}

const Treedata =ref([]);


onMounted(()=>{
    fetchAddingTreeInfo();
});
const fetchAddingTreeInfo=async()=>{
    try {
        // 发送请求并获取数据
        const response = await request({
        url: 'api/system/rank/tree_rank_list/',
        method: 'get',})
        const data = await response.data;
        // 更新选项列表
        Treedata.value = data;
    } catch (error) {
        ElMessage({
        showClose: true,
        message: error.value,
        type: 'error',
        })
    }

}
const { proxy } = getCurrentInstance();
const treeclick =()=>{
  const ourtree =proxy.$refs.addingtree;
  const res=[];
  const target=[];
  res.push(...ourtree.getCheckedNodes())
  res.forEach(element => {
    if(element.id.charAt(0)==='c'){
      const temp=element.id.split('-')
      target.push({
        staff_department:temp[1],
        staff_rank:temp[2]
      })
    }
  });
  return target;
}

defineExpose({
  treeclick
})


const checked = ref(false)
</script>



<template>
    <el-tree
      ref="addingtree"
      :data="Treedata"
      :props="defaultProps"
      :height="300"
      highlight-current="true"
      show-checkbox
    >
      <template #default="{ node }">
        <span class="prefix" :class="{ 'is-leaf': node.isLeaf }">
          <el-icon >
            <SuitcaseLine />
          </el-icon>
            [系统组织]
        </span>
        <span>{{ node.label }}</span>

        <div class="addtag">
          <!-- <el-check-tag  v-if="node.isLeaf" :checked="checked" @change="checked=!checked"  >评价-优秀</el-check-tag> -->
        </div>
      </template>
    </el-tree>
</template>

<style scoped>
.prefix {
  color: var(--el-color-primary);
  margin-right: 10px;
}
.prefix.is-leaf {
  color: var(--el-color-success);
}
.el-tree{
    background-color: #fcf9f9;
    margin-top: 50px;
    margin-left: 200px;
    margin-right: 200px;
    margin-bottom: 20px;
    font-size: large;
    letter-spacing: 1px; /* 增加1像素的间距 */
    line-height: 150%;
}
.addtag{
  width: max-content;
  text-align: right;
  margin-left: 50px;
}
</style>