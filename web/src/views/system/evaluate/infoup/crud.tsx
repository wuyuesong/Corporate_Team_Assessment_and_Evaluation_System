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
			form: { // crudOptions.form
				// 以下仅element，其他ui的相关配置请看对应ui的form组件文档
				labelWidth: "120px", //标签宽度
				//... 更多配置请查看对应ui库文档，form表单章节
			},
			toolbar:{
				show:false
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
			
			columns: {
				_index: {
					title: '序号',
					form: { show: false },
                    disabled:true,
					column: {
						show:false,
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
				staff_department: {
					title: '单位名称',
					search: {
						show:true,
						disabled: false,
					},
					column:{
						minWidth: 100,
					},
					type: 'dict-tree',
					dict: dict({
                        isTree: true,
                        url: '/api/system/department',
                        label: 'staff_department',
						value: 'staff_department'
                    }),
					form: {
						disabled: true,
						component: {
                            filterable: true,
                            placeholder: '请选择',
                            props: {
                                checkStrictly:true,
                                props: {
                                    label: 'staff_department',
									value: 'staff_department'
                                },
                            },
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
				staff_rank: {
					title: '职位等级',
					search: {
						show:true,
						disabled: false,
					},
					column:{
						minWidth: 100,
					},
					type: 'dict-tree',
					dict: dict({
                        isTree: true,
                        url: '/api/system/rank',
                        label: 'staff_rank',
						value: 'staff_rank'
                    }),
					form: {
						disabled: true,
						component: {
                            filterable: true,
                            placeholder: '请选择',
                            props: {
                                checkStrictly:true,
                                props: {
                                    label: 'staff_rank',
									value: 'staff_rank'
                                },
                            },
                        },
					},
					
				},
				staff_job: {
					title: '岗位等级',
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
							placeholder: '请输入岗位等级',
						},
					},
				},
				job_title: {
					title: '职称',
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
							placeholder: '职称',
						},
					},
				},
				staff_kpi1: {
					title: '第一年KPI',
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
							placeholder: '请输入第一年KPI',
						},
					},
				},
				staff_kpi2: {
					title: '第二年KPI',
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
							placeholder: '请输入第二年KPI',
						},
					},
				},
				staff_kpi3: {
					title: '第三年KPI',
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
							placeholder: '请输入第三年KPI',
						},
					},
				},
				assessment1: {
					title: '第一年考核结果',
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
							placeholder: '请输入第一年考核结果',
						},
					},
				},
				assessment2: {
					title: '第二年考核结果',
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
							placeholder: '请输入第二年考核结果',
						},
					},
				},
				assessment3: {
					title: '第三年考核结果',
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
							placeholder: '请输入第三年考核结',
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
				staff_firm_id: {
					title: '员工企业ID',
					search: {
						disabled: false,
						show:true,
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
				username:{
					title: '用户名',
					search: {
						disabled: false,
					},
					type: 'text',
					column:{
						minWidth: 100,
					},
					form: {
						show:false
					}

				},
				password:{
					title: '密码',
					search: {
						disabled: false,
					},
					type: 'text',
					column:{
						minWidth: 100,
					},
					form: {
						show:false
					}

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