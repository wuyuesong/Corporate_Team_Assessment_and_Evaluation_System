import * as api from './api';
import { UserPageQuery, AddReq, DelReq, EditReq, CreateCrudOptionsProps, CreateCrudOptionsRet, dict } from '@fast-crud/fast-crud';
import {commonCrudConfig} from "/@/utils/commonCrud";
import { downloadFile } from '/@/utils/service';
import { getBaseURL } from '/@/utils/baseUrl';
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

					customButton: {
						show: true,
						label: "导出信息",
						text:"导出信息",
						onClick:() => {
							// 在这里执行您想要的操作
							downloadFile({
								url: getBaseURL() + 'api/system/staff/export_data/',
								params: {},
								method: 'get'
							})
						},
						order:2,
					}	
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
						show:true,
						disabled: false,
					},
					type: 'input',
					column:{
						minWidth: 120,
					},
					form: {
						disabled: false,
						component: {
		
							placeholder: '请输入编号',
						},
					},
				},
				staff_id: {
					title: '员工系统编号',
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
							placeholder: '请输入系统编号',
						},
					},
				},
				staff_firm_id: {
					title: '员工企业编号',
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
							placeholder: '请输入企业编号',
						},
					},
				},
                staff_name: {
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
                staff_department: {
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
                staff_rank: {
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
                staff_job: {
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
                staff_telephone: {
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
                staff_email: {
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
                staff_status: {
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
                staff_excellence: {
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
                staff_kpi: {
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
			
		},
	};
};