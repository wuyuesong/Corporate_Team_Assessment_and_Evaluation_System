<script setup lang="ts">
import { Session, Local } from '/@/utils/storage';
import { ElMessageBox, ElMessage } from 'element-plus';
import screenfull from 'screenfull';
import { useI18n } from 'vue-i18n';
import { storeToRefs } from 'pinia';
const { locale, t } = useI18n();
import Cookies from 'js-cookie';


const  handleCommand= (path: string) => {
	if (path === 'logOut') {
		ElMessageBox({
			closeOnClickModal: false,
			closeOnPressEscape: false,
			title: t('message.user.logOutTitle'),
			message: t('message.user.logOutMessage'),
			showCancelButton: true,
			confirmButtonText: t('message.user.logOutConfirm'),
			cancelButtonText: t('message.user.logOutCancel'),
			buttonSize: 'default',
			beforeClose: (action, instance, done) => {
				if (action === 'confirm') {
					instance.confirmButtonLoading = true;
					instance.confirmButtonText = t('message.user.logOutExit');
					setTimeout(() => {
						done();
						setTimeout(() => {
							instance.confirmButtonLoading = false;
						}, 300);
					}, 700);
				} else {
					done();
				}
			},
		})
			.then(async () => {
				// 清除缓存/token等
                // 只清除Session中的staff_token

                Session.remove('staff_token');
                Cookies.remove('staff_id');
				// 使用 reload 时，不需要调用 resetRoute() 重置路由
				window.location.reload();
			})
			.catch(() => {});
	} 
};
</script>

<template>
<el-header class="background-bar" style="font-size: 25px;">
    <div class="toolbar" >
        <div class="ava">
            <div class="avatar"></div>
            <span style="color: #CCD8E2; font-weight: bold;">用户{{ Cookies.get('staff_id') }}</span>
        </div>
        <div class="setting">
            <el-dropdown trigger="click"  @command="handleCommand">
                <el-icon style="color: #303133" size="30">
                    <setting />
                </el-icon>
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item command="logOut">退出登录</el-dropdown-item>
                    </el-dropdown-menu>
                </template>
            </el-dropdown>
        </div>
    </div>
</el-header> 
</template>




<style scoped>

.background-bar {
  background-color: rgba(238,238,238,0.1); /* 设置背景颜色为透明 */
  /* 其他背景图片样式属性 */
}

.el-header {
    width: 100%;
    color: var(--el-text-color-primary);
    box-shadow: var(--el-box-shadow);
}

.toolbar {
    /* display: inline-flex; */
    align-items: center;
    /* justify-content: center; */
    height: 100%;
    width: 100%;
    text-align: right;
    display: flex;
    justify-content: space-between;
}

.el-dropdown-menu__item {
    width: 120px;
}
.ava{
    display: flex;
    align-items: center;
}
.icon-color {
    color: white;
}

/* 定义头像容器的样式 */
.avatar {
        width: 140px; /* 头像容器的宽度 */
        height: 140px; /* 头像容器的高度 */
        background-image: url('../../../assets/ava.png'); /* 头像图片的URL */
        background-size: cover; /* 让背景图片充满容器 */
        background-position: center; /* 将背景图片居中 */
        border-radius: 50%; /* 将头像容器设置为圆形 */
}
</style>