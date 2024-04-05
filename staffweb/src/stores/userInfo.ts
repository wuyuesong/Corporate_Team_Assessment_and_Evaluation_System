import { defineStore } from 'pinia';
import { UserInfosStates } from './interface';
import { Session } from '/@/utils/storage';
import { request } from '../utils/service';
/**
 * 用户信息
 * @methods setUserInfos 设置用户信息
 */
export const useUserInfo = defineStore('userInfo', {
	state: (): UserInfosStates => ({
		userInfos: {
			username: '',
			name: '',
			tasks: [
				{
					taskID:'',
					title: '',
					Btime: '',
					Etime: '',
					state: true,
				},
			],
		},
	}),
	actions: {
		async updateUserInfos() {
			let userInfos: any = await this.getApiUserInfo();
			this.userInfos.username = userInfos.data.name;
			this.userInfos.name = userInfos.data.name;
			this.userInfos.tasks = userInfos.data.tasks;
			Session.set('userInfo', this.userInfos);
		},
		async setUserInfos() {
			// 存储用户信息到浏览器缓存
			if (Session.get('userInfo')) {
				this.userInfos = Session.get('userInfo');
			} else {
				let userInfos: any = await this.getApiUserInfo();
				this.userInfos.username = userInfos.data.name;
				this.userInfos.name = userInfos.data.name;
				this.userInfos.tasks = userInfos.data.tasks;
				Session.set('userInfo', this.userInfos);
			}
		},
		async getApiUserInfo() {
			return request({
				url: '/api/system/user/user_info/',
				method: 'get',
			});
		},
	},
});
