
<script setup lang="ts">
import * as api from './api';
import { request, downloadFile } from '/@/utils/service';
import {inject,ref} from "vue";
import type { Action } from 'element-plus'
import { getBaseURL } from '/@/utils/baseUrl';
import { Session } from '/@/utils/storage';
import { UploadFilled } from '@element-plus/icons-vue'
import { defineAsyncComponent, onMounted, reactive, computed } from 'vue';
import { FsActionbar } from '@fast-crud/fast-crud';
import {Download } from '@element-plus/icons-vue'
import { useFs } from '@fast-crud/fast-crud';
import { createCrudOptions } from './crud';
const { crudBinding, crudRef, crudExpose } = useFs({ createCrudOptions });
const uploadRef = ref()
const refreshView = inject('refreshView')
import { ElMessage, ElMessageBox } from 'element-plus'
import { Eleme } from '@element-plus/icons-vue'
// 页面打开后获取列表数据
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



// 定义一个处理点击事件的函数
const handleDLClick = () => {
  downloadFile({
    url: getBaseURL() + 'api/system/staff/import_data/',
    params: {},
    method: 'get'
  })
}


const subloading = ref(false); // 使用ref创建响应式变量
const resetloading = ref(false); // 使用ref创建响应式变量
const handleSubmmitClick = () => {
  ElMessageBox.confirm(
    '提交员工信息至系统之后无法修改，确定你的操作?',
    'Warning',
    {
      confirmButtonText: 'OK',
      cancelButtonText: 'Cancel',
      type: 'warning',
    }
  )
    .then(() => {
      SubmmitInfo()
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '操作取消',
      })
    })
}
const handleResetClick = () => {
  ElMessageBox.confirm(
    '确定重置?',
    'Warning',
    {
      confirmButtonText: 'OK',
      cancelButtonText: 'Cancel',
      type: 'warning',
    }
  )
    .then(() => {
      ResetInfo()
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '操作取消',
      })
    })
}

//定义提交信息的函数
const SubmmitInfo = async() => {
      //loading.value = true; // 开始加载状态
      // request({
      //   // url: getBaseURL() + 'api/system/staff/import_data/',
      //   method: 'post',
      //   // data: {
      //   //   url: response.data.url
      //   // }
      // }).then((response:any) => {
      //   if(response.code==200){
      //       ElMessageBox.alert('提交成功', {
      //       })
      //       loading.value = false; // 结束加载状态vv
      //     } 
      // })
      //loading.value = false; // 结束加载状态vv
};
const ResetInfo = async() => {
      resetloading.value = true; // 开始加载状态
       request({
          url: getBaseURL() + 'api/system/staff/delete_all/',
         method: 'get',
       }).then((response:any) => {
         if(response.code==2000){
             ElMessageBox.alert('重置成功', {
              
             })
             resetloading.value = false; // 结束加载状态vv
             refreshView()
           } else{
            ElMessageBox.alert(response.message)
            resetloading.value = false;
           }
       })
      //loading.value = false; // 结束加载状态vv
};
</script>



<template>
    <div class="common-layout" style=" background-color: #f2f2f2;">
          <el-main>
            <div class="container"  style="padding-top: 20px; padding-bottom: 30px;padding-left: 50px; padding-right: 50px; height: 800px">
                    <div style="font-size: 30px; text-align:center">
                            <b>组织人员信息</b>
                    </div>
                    <fs-crud ref="crudRef" v-bind="crudBinding" > </fs-crud>
                    <div style="padding: 10px;">
                      <el-button id="staffsubmit" type="danger" :loading="subloading" @click="handleSubmmitClick" size="large">
                      <template #loading>
                        <div class="custom-loading">
                          <svg class="circular" viewBox="-10, -10, 50, 50">
                            <path
                              class="path"
                              d="
                              M 30 15
                              L 28 17
                              M 25.61 25.61
                              A 15 15, 0, 0, 1, 15 30
                              A 15 15, 0, 1, 1, 27.99 7.5
                              L 15 15
                            "
                              style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"
                            />
                          </svg>
                        </div>
                      </template>
                      提交员工信息
                      </el-button>   
                      
                      <el-button id="staffreset" type="warning" :loading="resetloading" @click="handleResetClick" size="large">
                      <template #loading>
                        <div class="custom-loading">
                          <svg class="circular" viewBox="-10, -10, 50, 50">
                            <path
                              class="path"
                              d="
                              M 30 15
                              L 28 17
                              M 25.61 25.61
                              A 15 15, 0, 0, 1, 15 30
                              A 15 15, 0, 1, 1, 27.99 7.5
                              L 15 15
                            "
                              style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"
                            />
                          </svg>
                        </div>
                      </template>
                      重置
                      </el-button>     
                    </div>
                    
            </div>
                   
            <div style="padding: 40px;"></div>
            <div style="background:linear-gradient(to left,#FFFFFF,#b6b6b6,#FFFFFF);height:10px;"></div>
            <div class="container" style="padding-top: 50px; text-align: center;">
                <div style="text-align: left; padding-left: 100px">
                  <el-button type="primary" size="large" @click="handleDLClick">
                    下载模板<el-icon class="el-icon--right"><Download/></el-icon>
                  </el-button>
                </div>
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

  .el-button .custom-loading .circular {
  margin-right: 6px;
  width: 18px;
  height: 18px;
  animation: loading-rotate 2s linear infinite;
}
.el-button .custom-loading .circular .path {
  animation: loading-dash 1.5s ease-in-out infinite;
  stroke-dasharray: 90, 150;
  stroke-dashoffset: 0;
  stroke-width: 2;
  stroke: var(--el-button-text-color);
  stroke-linecap: round;
}
  </style>