
<script setup lang="ts">
import * as api from './api';
import { request, downloadFile } from '/@/utils/service';
import {inject,ref} from "vue";
import type { Action } from 'element-plus'
import { getBaseURL } from '/@/utils/baseUrl';
import { Session } from '/@/utils/storage';
import {  ElMessageBox } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import { defineAsyncComponent, onMounted, reactive, computed } from 'vue';
import { FsActionbar } from '@fast-crud/fast-crud';

import { useFs } from '@fast-crud/fast-crud';
import { createCrudOptions } from './crud';
const { crudBinding, crudRef, crudExpose } = useFs({ createCrudOptions });
const uploadRef = ref()
const refreshView = inject('refreshView')
// 页面打开后获取列表数据
onMounted(() => {
	crudExpose.doRefresh();
});

const asideSettings = ref({
    isCollapse:true,
    width:'50'
})



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
        url: getBaseURL() + 'api/system/file/'
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
    url: getBaseURL() + 'api/system/staff/import_data/',
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
    <div class="common-layout" style=" background-color: #f2f2f2;">
          <el-main>
            <div class="container"  style="padding-top: 20px; padding-bottom: 30px;padding-left: 50px; padding-right: 50px; height: 800px">
                    <div style="font-size: 30px; text-align:center">
                            <b>组织人员信息</b>
                    </div>
                    <fs-crud ref="crudRef" v-bind="crudBinding" > </fs-crud>
            </div>

            <div style="padding: 10px;"></div>
            <div style="background:linear-gradient(to left,#FFFFFF,#b6b6b6,#FFFFFF);height:10px;"></div>
            <div class="container" style="padding-top: 50px; text-align: center;">
                <div div-lc-mark style="font-size: 30px;">
                    <b>请上传人员信息文件以供分析</b>
                </div>
            </div>
            <div class="container" style="min-height: 20%; padding-top: 0px;padding-left: 100px;padding-right: 100px;">
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
            
            
          </el-main>
    </div>
  </template>
  
      
  <style>
  body{
    background-color: #ffffff;
    max-width: 100vw;
    overflow: hidden;
  }
  .el-main {
    width: 100%;
    padding: 0;
    height: 200vh;
    overflow-x: hidden;
  }
  .el-upload{
    background-color: #4d0f0f; /* 设置上传区域的背景颜色 */
  }
  </style>