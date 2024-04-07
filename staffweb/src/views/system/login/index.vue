<script lang="ts" setup>
import * as loginApi from './api';
import {Md5}  from 'ts-md5';
import { useRoute, useRouter } from 'vue-router';
import { Session } from '/@/utils/storage';
import Cookies from 'js-cookie';
import { ref } from 'vue';
import { defineAsyncComponent, onMounted, reactive, computed } from 'vue';
import { NextLoading } from '/@/utils/loading';
import { storeToRefs } from 'pinia';
import { useUserInfo } from '/@/stores/userInfo';
const input = ref('')
const password = ref('')
const errors = ref('')
const { userInfos } = storeToRefs(useUserInfo());
const route = useRoute();
const router = useRouter();
import { message } from '/@/utils/message';



  

// 页面加载时
onMounted(() => {
	NextLoading.done();
});



const loginClick = async () => {
    errors.value='';
    if (!input.value||!password.value){
      errors.value = 'Please enter your username or password';
      Session.clear();
      Cookies.clear();
      return;
    }

    // Md5.hashStr(password.value),
     loginApi.login({ username:input.value, password: password.value,login_type:"2"}).then((res: any) => {
        if (res.code === 2000) {
          Session.set('token', res.data.access);
          Cookies.set('staff_id',input.value)
          Cookies.set('username', res.data.name);
          loginSuccess();
        }else{  
        }
      }).catch((err: any) => {
       
      });
};

//获取登陆人的信息
const getUserInfo = () => {
			useUserInfo().setUserInfos();
	};

		// 登录成功后的跳转
const loginSuccess = () => {

      router.push('/home');
      NextLoading.start();
      // if (route.query?.redirect) {
      //     router.push({
      //         path: <string>route.query?.redirect,
      //         query: Object.keys(<string>route.query?.params).length > 0 ? JSON.parse(<string>route.query?.params) : '',
      //     });
      // } else {
      //     router.push('/');
      // }
};

</script>
<template>
  <div class="app_container">
    <header>
      <a class="logo" href="/" >
      <li-icon type="logo" size="50dp"  color="brand" role="banner">
        <svg width="40" height="32" viewBox="0 0 102 26" fill="none" id="logo">
          
        </svg>
      </li-icon>
    </a>
    </header>
    <main class="loginmainpage">
      <div style="height: 120px; width: 100%"/>
      <div class="card">
          <div class="organ">
              <div class="headercontent">
                <h1 class="header__content__heading ">登录</h1>
                <br>
                <p class="header__content__subheading ">使用评估系统</p>
              </div>
            <div style="height: 10px;"/>
              <form  class="login__form"  novalidate="true"  @submit.prevent="loginClick">
                <div class="l-1">
                  <input id="username" v-model="input" name="session_key" type="text" required  autofocus aria-label="账号" autocomplete="off">
                  <label class="form__label--floating" for="username" aria-hidden="true">账号</label>
                </div>
                <div class="l-1">
                  <input id="password" v-model="password" name="session_key" type="password" required  autofocus aria-label="密码" autocomplete="off">
                  <label class="form__label--floating" for="password" aria-hidden="true">密码</label>
                  <span id="passwordVisable" class="tabbutton" role="button" tabindex="0"></span>
                </div>
                <div class="l-1">
                  <span v-if="errors" class="error-message" >{{ errors}}</span>
                </div>
                <div class="l-1">
                  <button class="submitbutton" type="submit">登录</button>
                </div>
              </form>
              
          </div>
      </div>
      <div style="height: 120px; width: 100%"/>

    </main>
  </div>


</template>




<style>

@font-face {
  font-family: "钉钉进步体 Regular";font-weight: 400;src: url("//at.alicdn.com/wf/webfont/iSq66waD0Wdh/hJRqEK6c6oM1.woff2") format("woff2"),
  url("//at.alicdn.com/wf/webfont/iSq66waD0Wdh/it8Mekj0bBph.woff") format("woff");
  font-display: swap;
}

#app__container {

    display: flex;
    min-height: 100vh;
    background-color: var(--color-background-canvas, #ffffff);
}

.loginmainpage{
  background-image: url('../../../assets/login_add.png');
  background-position: right; /* 将背景图像居中 */
  background-repeat: no-repeat; /* 禁止背景图像重复 */
  text-align: left;

}
.card{
    width: 500px;
    padding: 40px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    border-radius:50px;
    margin-left: 300px;
    background: var(--color-background-container, #fff);
    display: flex;
    justify-content: center;
}
.app__content {
    display: flex;
    flex: 1;
    float: none;
    flex-direction: column;
    justify-content: center;
    margin: 0 auto;
}
.header{
    margin: 0;
    padding: 0;
    border: 0;
    font-size: 100%;
    vertical-align: baseline;
    background: transparent;
}


.headercontent .header__content__heading {
    font-family: '钉钉进步体 Regular';
    font-size: 3.2rem;
    line-height: 1.25;
    font-weight: 600;
    color: rgba(0, 0, 0, 0.9);
    padding: 0 0 4px 0;
}

.headercontent .header__content__subheading {
    font-family: '钉钉进步体 Regular';
    font-size: 1.4rem;
    line-height: 1.42857;
    font-weight: 400;
    color: rgba(0, 0, 0, 0.9);
}


.logo {
    display: block;
    margin: 32px 0 0 56px;
    background-image: url('../../../assets/logo.svg');
    -webkit-box-reflect: below 1px linear-gradient(transparent,transparent,#005);
}

.l-1 {
    margin-top: 24px;
    position: relative;
    background-color: #fff;
}



.l-1>input {
    font-size: 1.6rem;
    line-height: 1.33333;
    font-weight: 400;
    color: rgba(0, 0, 0, 0.9);
    position: relative;
    z-index: 1;
    border: 2px solid #ccc; /* 设置边框为1像素宽，实线，颜色为灰色 */
    height: 60px;
    padding: 28px 15px 6px;
    border-radius: 4px !important;
}

.l-1>label {
    font-size: 1.8rem;
    line-height: 1.33333;
    font-weight: 400;
    color: #ccc;
    position: absolute;
    z-index: 1;
    top: 0;
    left: 0;
    padding: 13px;
    margin: 0;
    -webkit-transition: .2s all;
    transition: .2s all;
}

input:focus + .form__label--floating,
input:valid + .form__label--floating {
    transform: translateY(-9px); /* 使标签向上移动 */
    font-size: 16px; /* 缩小标签字体大小 */
    color: #007bff; /* 修改标签颜色 */
}
input:focus {
    border-color: #007bff; /* 修改输入框边框颜色为蓝色 */
    /* 其他样式可以根据需要添加 */
}


  /* 登录按钮样式 */
.submitbutton {
    display: block;
    width: 100%;
    height: 60px;
    margin-top: 30px;
    font: 900 30px 'Arial', sans-serif;
    text-decoration: none;
    line-height: 60px;
    border-radius: 30px;
    background-image: linear-gradient(to left, #3cadeb, #3cadeb);
    text-align: center;
    color: white;
    border: none;
    cursor: pointer;
}
  
  /* 鼠标悬停时登录按钮样式 */
.submitbutton:hover {
    background-image: linear-gradient(to left, #3cadeb, #9c88ff);
}
  



.login__form .tabbutton {
    background-color: rgba(0, 0, 0, 0);
    border: 0;
    border-radius: 2px;
}

.error-message {
  color: red; /* 设置为红色 */
}

</style>
