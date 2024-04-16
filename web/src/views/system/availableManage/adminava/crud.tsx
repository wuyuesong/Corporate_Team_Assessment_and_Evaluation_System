import * as api from './api';
import {
    dict,
    UserPageQuery,
    AddReq,
    DelReq,
    EditReq,
    CreateCrudOptionsProps,
    CreateCrudOptionsRet
} from '@fast-crud/fast-crud';
import {commonCrudConfig} from "/@/utils/commonCrud";
import { Md5 } from 'ts-md5';
export const createCrudOptions = function ({ crudExpose }: CreateCrudOptionsProps): CreateCrudOptionsRet {
    const pageRequest = async (query: UserPageQuery) => {
        return await api.GetList(query);
    };
    const editRequest = async ({form, row}: EditReq) => {
        form.id = row.id;
        return await api.UpdateObj(form);
    };
    const delRequest = async ({row}: DelReq) => {
        return await api.DelObj(row.id);
    };
    const addRequest = async ({form}: AddReq) => {
        return await api.AddObj(form);
    };

    const exportRequest = async (query: UserPageQuery) => {
        return await api.exportData(query)
    }

    
	
	return {
        crudOptions: {
            container:{
				is:'fs-layout-card',
			},
            form: { 
				labelWidth: "120px", //标签宽度
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
                }
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
                    form: {show: false},
                    column: {
                        type: 'index',
                        align: 'center',
                        width: '70px',
                        columnSetDisabled: true, //禁止在列设置中选择
                    },
                },
                username: {
                    title: '账号',
                    type: 'input',
                    column: {
                        minWidth: 100, //最小列宽
                    },
                    form: {
                        rules: [
                            // 表单校验规则
                            {
                                required: true,
                                message: '账号必填项',
                            },
                        ],
                        component: {
                            placeholder: '请输入账号',
                        },
                    },
                },
                password: {
                    title: '密码',
                    type: 'password',
                    column: {
                        show: false,
                    },
                    editForm: {
                        show: false,
                    },
                    form: {
                        rules: [
                            // 表单校验规则
                            {
                                required: true,
                                message: '密码必填项',
                            },
                        ],
                        component: {
                            span: 12,
                            showPassword: true,
                            placeholder: '请输入密码',
                        },
                    },
                    valueResolve({form}) {
                        if (form.password) {
                            form.password = Md5.hashStr(form.password)
                        }
                    }
                },
                name: {
                    title: '姓名',
                    search: {
                        show: true,
                    },
                    type: 'input',
                    column: {
                        minWidth: 100, //最小列宽
                    },
                    form: {
                        rules: [
                            // 表单校验规则
                            {
                                required: true,
                                message: '姓名必填项',
                            },
                        ],
                        component: {
                            span: 12,
                            placeholder: '请输入姓名',
                        },
                    },
                },
                mobile: {
                    title: '手机号码',
                    search: {
                        show: true,
                    },
                    type: 'input',
                    column: {
                        minWidth: 120, //最小列宽
                    },
                    form: {
                        rules: [
                            {
                                max: 20,
                                message: '请输入正确的手机号码',
                                trigger: 'blur',
                            },
                            {
                                pattern: /^1[3-9]\d{9}$/,
                                message: '请输入正确的手机号码',
                            },
                        ],
                        component: {
                            placeholder: '请输入手机号码',
                        },
                    },
                },
                email: {
                    title: '邮箱',
                    column: {
                        width: 260,
                    },
                    form: {
                        rules: [
                            {
                                type: 'email',
                                message: '请输入正确的邮箱地址',
                                trigger: ['blur', 'change'],
                            },
                        ],
                        component: {
                            placeholder: '请输入邮箱',
                        },
                    },
                },
                
            },
        },
    };
};