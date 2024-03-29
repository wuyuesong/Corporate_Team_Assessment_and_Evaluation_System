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
			toolbar:{
				show:false
			},
			search:{
				show:false
			},
			form: { // crudOptions.form
				labelWidth: "120px", //标签宽度

			},
            columns: {
				_index: {
					title: '序号',
					form: { show: false },
                    disabled:true,
					column: {
						//type: 'index',
						show:false,
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
					title: '用户部门',
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
							placeholder: '请输入用户部门',
						},
					},
				},
				normal_department: {
					title: '用户标准化部门',
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
							placeholder: '请输入标准化部门',
						},
					},
				},
            }
        }
    }
}