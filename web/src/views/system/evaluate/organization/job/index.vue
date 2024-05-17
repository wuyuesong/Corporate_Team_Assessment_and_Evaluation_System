<script setup lang="ts">
import { request, downloadFile } from '/@/utils/service';
import { useFs } from '@fast-crud/fast-crud';
import { createCrudOptions } from './crud';
import { Session } from '/@/utils/storage';
import { onMounted,inject,ref} from 'vue';
import { getBaseURL } from '/@/utils/baseUrl';
const { crudBinding, crudRef,crudExpose } = useFs({ createCrudOptions });
import type { Action } from 'element-plus'
const uploadRef = ref()
const refreshView = inject('refreshView')
import { ElMessage, ElMessageBox } from 'element-plus'

onMounted(() => {
	crudExpose.doRefresh();
});


let props = defineProps({
  upload: {
    type: Object,
    default () {
      return {
        // 是否显示弹出层
        open: true,
        // 弹出层标题
        title: '',
        // 是否禁用上传
        isUploading: false,
        // 是否更新已经存在的用户数据
        updateSupport: 0,
        // 设置上传的请求头部
        headers: { Authorization: 'JWT ' + Session.get('token') },
        // 上传的地址
        url: getBaseURL()+ 'api/system/file/'
      }
    }
  },
  api: { // 导入接口地址
    type: String,
    default () {
      return undefined
    }
  }
})



// 文件上传成功处理
const handleFileSuccess=function (response:any, file:any, fileList:any) {
  uploadRef.value.clearFiles()
  // 是否更新已经存在的用户数据
  return request({
    url: 'api/system/rank/import_data/',
    method: 'post',
    data: {
      url: response.data.url
    }
  }).then((response:any) => {
    ElMessageBox.alert('导入成功', '导入完成', {
      confirmButtonText: 'OK',
      callback: (action: Action) => {
        refreshView()
      },
    })
  }).catch(()=>{

  })
}

</script>


<template>
    <div class="container"  style="padding-top: 20px; padding-bottom: 30px;padding-left: 50px; padding-right: 50px; height: 900px;">


        <fs-crud ref="crudRef" v-bind="crudBinding" > </fs-crud>
        
        <div class="upload" style="min-height: 20%; padding-top: 0px;padding-left: 100px;padding-right: 100px;">
                <el-upload
                    ref="uploadRef"
                    :limit="1"
                    accept=".xlsx, .xls"
                    :headers="props.upload.headers"
                    :action="props.upload.url"
                    :on-success="handleFileSuccess"
                    drag>
                  <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                  <div class="el-upload__text">
                    Drop file here or <em>click to upload</em>
                  </div>
                  <template #tip>
                    <div class="el-upload__tip">
                      请上传excel文件，不要超过500mb
                    </div>
                  </template>
                </el-upload>
             </div>
    </div>


</template>

<style>

.container{
    display: flex;
    flex-direction: column;

}
.upload{
    padding-top: 20px;
}
</style>