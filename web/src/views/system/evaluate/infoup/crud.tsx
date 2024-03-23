import * as api from './api';
import { UserPageQuery, AddReq, DelReq, EditReq, CreateCrudOptionsProps, CreateCrudOptionsRet, dict } from '@fast-crud/fast-crud';
import {commonCrudConfig} from "/@/utils/commonCrud";

export const createCrudOptions = function ({ crudExpose }: CreateCrudOptionsProps): CreateCrudOptionsRet {
	const pageRequest = async (query: UserPageQuery) => {
		return await api.GetList(query);
	};
	const editRequest = async ({ form, row }: EditReq) => {
		form.id = row.id;
		return await api.UpdateObj(form);
	};
	const delRequest = async ({ row }: DelReq) => {
		return await api.DelObj(row.id);
	};
	const addRequest = async ({ form }: AddReq) => {
		return await api.AddObj(form);
	};
	return {
		crudOptions: {

			container:{
				is:'fs-layout-card',
			},
			request: {
				pageRequest,
				addRequest,
				editRequest,
				delRequest,
			},
			actionbar: {
				buttons: {
					add: {
						show: true,
					},
				},
			},
			rowHandle: {
				fixed:'right',
				width: 250,
				buttons: {
					view: {
						type: 'text',
					},
					edit: {
						show: true,
					},
					remove: {
						show: true,
					},
				},
			},
			toolbar:{
				show:false
			},
			columns: {
				_index: {
					title: '序号',
					form: { show: false },
                    disabled:true,
					column: {
						//type: 'index',
						align: 'center',
						width: '70px',
						fixed: 'left', //固定列
						columnSetDisabled: true, //禁止在列设置中选择
						formatter: (context) => {
							//计算序号,你可以自定义计算规则，此处为翻页累加
							let index = context.index ?? 1;
							let pagination = crudExpose!.crudBinding.value.pagination;
							return ((pagination!.currentPage ?? 1) - 1) * pagination!.pageSize + index + 1;
						},
					},
				},
				id: {
					title: '编号',
					search: {
						disabled: false,
					},
					type: 'input',
					column:{
						minWidth: 120,
					},
					form: {
						disabled: true,
						component: {
		
							placeholder: '请输入编号',
						},
					},
				},
				stuff_id: {
					title: '员工系统编号',
					search: {
						disabled: false,
					},
					type: 'input',
					column:{
						minWidth: 100,
					},
					form: {
						disabled: true,
						component: {
							placeholder: '请输入系统编号',
						},
					},
				},
				stuff_firm_id: {
					title: '员工企业编号',
					search: {
						disabled: false,
					},
					type: 'input',
					column:{
						minWidth: 100,
					},
					form: {
						disabled: true,
						component: {
							placeholder: '请输入企业编号',
						},
					},
				},
                stuff_name: {
					title: '员工姓名',
					search: {
						disabled: false,
					},
					type: 'input',
					column:{
						minWidth: 100,
					},
					form: {
						disabled: true,
						component: {
							placeholder: '请输入用户姓名',
						},
					},
				},
                stuff_department: {
					title: '员工部门',
					search: {
						disabled: false,
					},
					type: 'input',
					column:{
						minWidth: 100,
					},
					form: {
						disabled: true,
						component: {
							placeholder: '请输入员工部门',
						},
					},
				},
                stuff_rank: {
					title: '员工职级',
					search: {
						disabled: false,
					},
					type: 'input',
					column:{
						minWidth: 100,
					},
					form: {
						
						disabled: true,
						component: {
							placeholder: '请输入员工职级',
						},
					},
				},
                stuff_job: {
					title: '员工职务',
					search: {
						disabled: false,
					},
					type: 'input',
					column:{
						minWidth: 100,
					},
					form: {
						disabled: true,
						component: {
							placeholder: '请输入员工职务',
						},
					},
				},
                stuff_telephone: {
					title: '员工电话',
					search: {
						disabled: false,
					},
					type: 'input',
					column:{
						minWidth: 100,
					},
					form: {
						disabled: true,
						component: {
							placeholder: '请输入员工电话',
						},
					},
				},
                stuff_email: {
					title: '员工邮箱',
					search: {
						disabled: false,
					},
					type: 'input',
					column:{
						minWidth: 100,
					},
					form: {
						disabled: true,
						component: {
							placeholder: '请输入员工电话',
						},
					},
				},
                stuff_status: {
					title: '政治面貌',
					search: {
						disabled: false,
					},
					type: 'input',
					column:{
						minWidth: 100,
					},
					form: {
						disabled: true,
						component: {
							placeholder: '请输入员工电话',
						},
					},
				},
                stuff_excellence: {
					title: '评奖评优',
					search: {
						disabled: false,
					},
					type: 'input',
					column:{
						minWidth: 100,
					},
					form: {
						disabled: true,
						component: {
							placeholder: '请输入评奖评优',
						},
					},
				},
                stuff_kpi: {
					title: 'KPI',
					search: {
						disabled: false,
					},
					type: 'input',
					column:{
						minWidth: 100,
					},
					form: {
						disabled: true,
						component: {
							placeholder: '请输入KPI',
						},
					},
				},
				...commonCrudConfig({
					create_datetime: {
						search: true
					}
				})
			},
			FsFileUploader:{

			},
		},
	};
};