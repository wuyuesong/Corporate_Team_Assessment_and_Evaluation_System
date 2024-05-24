<script setup lang="ts">
import { useFs,useCrud,useExpose } from '@fast-crud/fast-crud';
import { createCrudOptions } from './crud';
import { onMounted,ref,reactive} from 'vue';

import { warningNotification, successNotification } from '/@/utils/message';
import { Md5 } from 'ts-md5';
import { resetPwd } from './api';
// crud组件的ref
let resetPwdVisible = ref(false);
// crud组件的ref
const crudRef = ref();
// crud 配置的ref
const crudBinding = ref();
// 暴露的方法
const { crudExpose } = useExpose({ crudRef, crudBinding });
// 你的crud配置

// const { crudBinding, crudRef, crudExpose } = useFs({ createCrudOptions });
// 页面打开后获取列表数据
onMounted(() => {
  crudExpose.doRefresh();
});
let resetPwdFormState = reactive({
	id: 0,
	newPassword: '',
	newPassword2: '',
});



const handleResetPwdOpen = ({ id }: { id: number }) => {
	resetPwdFormState.id = id;
	resetPwdVisible.value = true;
};
const handleResetPwdClose = () => {
	resetPwdVisible.value = false;
	resetPwdFormState.id = 0;
	resetPwdFormState.newPassword = '';
	resetPwdFormState.newPassword2 = '';
};


const handleResetPwdSubmit = async () => {
	if (!resetPwdFormState.id) {
		warningNotification('请选择用户！');
		return;
	}
	if (!resetPwdFormState.newPassword || !resetPwdFormState.newPassword2) {
		warningNotification('请输入密码！');
		return;
	}
	if (resetPwdFormState.newPassword !== resetPwdFormState.newPassword2) {
		warningNotification('两次输入密码不一致');
		return;
	}
	const pwdRegex = new RegExp('(?=.*[0-9])(?=.*[a-zA-Z]).{8,30}');
	if (!pwdRegex.test(resetPwdFormState.newPassword) || !pwdRegex.test(resetPwdFormState.newPassword2)) {
		warningNotification('您的密码复杂度太低(密码中必须包含字母、数字)');
		return;
	}
	const res = await resetPwd(resetPwdFormState.id, {
		newPassword: Md5.hashStr(resetPwdFormState.newPassword),
		newPassword2: Md5.hashStr(resetPwdFormState.newPassword2),
	});

	if (res?.code === 2000) {
		successNotification(res.msg || '修改成功！');
		handleResetPwdClose();
	}
};

const { crudOptions } = createCrudOptions({ crudExpose, context: { handleResetPwdOpen } });
// 初始化crud配置
const { resetCrudOptions } = useCrud({
	crudExpose,
	crudOptions,
	context: {},
});
</script>

<template>
    <div class="ava_container"  style="padding-top: 20px; padding-bottom: 30px;padding-left: 50px; padding-right: 50px; height: 800px">
        <fs-crud v-bind="crudBinding" ref="crudRef">
        </fs-crud>
        <el-dialog v-model="resetPwdVisible" title="重设密码" width="400px" draggable :before-close="handleResetPwdClose">
        <div>
          <el-input v-model="resetPwdFormState.newPassword" type="password" placeholder="请输入密码" show-password style="margin-bottom: 20px" />
          <el-input v-model="resetPwdFormState.newPassword2" type="password" placeholder="请再次输入密码" show-password />
        </div>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="handleResetPwdClose">取消</el-button>
            <el-button type="primary" @click="handleResetPwdSubmit"> 保存 </el-button>
          </span>
        </template>
      </el-dialog>
    </div>

    

</template>

<style scoped>

</style>