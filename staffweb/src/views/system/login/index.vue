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
import jumploading from '../Animate/jumploading.vue';
import VanillaTilt from 'vanilla-tilt';
  
const main=ref()
const temp=ref()
const loginrotaition=ref()
// 页面加载时
onMounted(() => {
	NextLoading.done();
  // VanillaTilt.init(main.value, {
  //   "mouse-event-element":temp.value,
  //   startX:8,
  //   max:8,
  //   axis:'x',
	// });
  // VanillaTilt.init(loginrotaition.value, {
  //   reverse:true,
  //   "mouse-event-element":temp.value,
  //   startX:8,
  //   max:8,
  //   axis:'x',
	// });

});


const loginClick = async () => {

    
    errors.value='';
    if (!input.value||!password.value){
      errors.value = '请输入你的账户和密码';
      Session.remove('staff_token');
      Cookies.remove('staff_id');
      return;
    }
    loading.value=true;
    // Md5.hashStr(password.value),
     loginApi.login({ username:input.value, password: password.value,login_type:"2"}).then((res: any) => {
        if (res.code === 2000) {
          Session.set('staff_token', res.data.access);
          Cookies.set('staff_id',input.value)
          loading.value=false;
          loginSuccess();
        }else{  
          
          loading.value=false;
        }
      }).catch((err: any) => {
        loading.value=false;
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

const loading = ref(false)


</script>
<template>
  <jumploading class="thistop" v-if="true"/>
  <div class="app_container">
    <header>
      <a class="logo">
        <li-icon type="logo" size="10dp" color="brand" role="banner" ref="temp">
          <svg xmlns="http://www.w3.org/2000/svg" width="128" height="86" viewBox="0 0 128 86"><path fill="#ecf5f9" stroke="#ecf5f9" d="M0 48.007v48.008l64.25-.258 64.25-.257.26-47.75.259-47.75H0v48.007m.462.493c.001 26.4.13 37.056.287 23.681.158-13.376.158-34.976 0-48C.591 11.156.462 22.1.462 48.5M56 19.648c-20.754 3.117-35.69 8.818-42.035 16.045-4.251 4.842-3.663 6.391.785 2.068 7.352-7.145 26.26-14.094 42-15.436 5.124-.437 7.25-1.015 7.25-1.972 0-1.329-2.423-1.543-8-.705M88 42.93V57h2.5c2.458 0 2.5-.133 2.5-8v-8h9v8c0 7.333.167 8 2 8 1.839 0 2-.667 2-8.3 0-9.858-.602-10.7-7.643-10.7h-5.242l-.308-4.25c-.255-3.533-.687-4.304-2.557-4.57-2.242-.318-2.25-.268-2.25 13.75m-62.782 6.82c.232 9.653.55 11.75 1.782 11.75 1.103 0 1.58-1.379 1.801-5.205l.3-5.206 6.7-.294L42.5 50.5l.32-3.905c.669-8.179.216-8.595-9.371-8.595h-8.512l.281 11.75m20.994-2.5.288 9.25 8.75.289 8.75.289v-9.539C64 38.735 63.849 38 62.042 38c-1.75 0-1.989.822-2.25 7.75L59.5 53.5h-9l-.292-7.75c-.263-6.98-.49-7.75-2.288-7.75-1.87 0-1.977.578-1.708 9.25m22.846-7.82c-.653.787-1.046 3.149-.873 5.25l.315 3.82 6.25.298c5.944.283 6.25.421 6.25 2.832 0 2.503-.087 2.53-7.002 2.202-6.185-.293-7.002-.123-7 1.457.002 1.604.906 1.759 8.752 1.5l8.75-.289v-10l-6.25-.298c-5.94-.283-6.25-.423-6.25-2.825 0-2.334.326-2.515 4.25-2.36 7.326.29 8.75.043 8.75-1.517 0-2.107-14.199-2.169-15.942-.07M29 44.5v3.61l4.75-.305c4.543-.292 4.75-.435 4.75-3.305s-.207-3.013-4.75-3.305L29 40.89v3.61M12.575 56.847c10.68 18.57 57.969 25.56 88.087 13.021C107.891 66.859 119 57.92 119 55.113c0-.583-1.958.898-4.352 3.292-20.489 20.489-78.715 20.128-99.669-.618-4.226-4.185-4.284-4.207-2.404-.94" fill-rule="evenodd"/><path fill="#f6fcfb" stroke="#f6fcfb" d="M0 48.007v48.008l64.25-.258 64.25-.257.26-47.75.259-47.75H0v48.007m.462.493c.001 26.4.13 37.056.287 23.681.158-13.376.158-34.976 0-48C.591 11.156.462 22.1.462 48.5M50.5 20.109c-17.924 2.585-34.815 10.799-39.051 18.99-2.202 4.258-1.776 4.269 2.033.053C20.836 31.011 46.133 22 61.631 22 63.07 22 64 21.411 64 20.5c0-1.704-3.658-1.81-13.5-.391M88 43.5V58h2.5c2.458 0 2.5-.133 2.5-8v-8h9v8.07c0 7.796.076 8.058 2.25 7.75 2.059-.293 2.275-.922 2.54-7.399.451-10.997-.439-12.421-7.765-12.421H93v-4.5c0-4.133-.204-4.5-2.5-4.5H88v14.5m-63.356 5.218C24.832 62.754 24.698 62 27 62c1.733 0 2-.667 2-5v-5h5.309c7.517 0 8.883-1.29 8.501-8.03l-.31-5.47-9-.282-9-.282.144 10.782M46 46.8c0 10.913.262 11.2 10.2 11.2H64V48c0-9.333-.133-10-2-10-1.822 0-2 .667-2 7.5V53H50v-7.5c0-6.833-.178-7.5-2-7.5-1.848 0-2 .667-2 8.8m21.934-6.126c-2.433 6.4.298 9.285 8.816 9.312 3.105.01 4.25.418 4.25 1.514 0 1.19-1.444 1.5-7 1.5-6.8 0-7 .071-7 2.5 0 2.431.196 2.5 7.066 2.5C83.659 58 85 57.151 85 51.072 85 45.485 84.354 45 76.918 45 73.213 45 72 44.63 72 43.5c0-1.179 1.389-1.5 6.5-1.5 5.833 0 6.5-.205 6.5-2 0-1.834-.667-2-8.025-2-7.778 0-8.056.082-9.041 2.674M29 44.387c0 1.842.627 2.475 2.75 2.777 4.549.645 6.25-.1 6.25-2.737 0-2.21-.403-2.427-4.5-2.427-4.076 0-4.5.225-4.5 2.387m-19 8.322c0 2.488 6.651 9.756 12.225 13.358 27.849 18 84.698 11.942 96.357-10.267 2.182-4.156 1.685-4.551-1.053-.84-17.611 23.87-82.893 24.746-103.454 1.388C11.834 53.802 10 52.164 10 52.709" fill-rule="evenodd"/><path fill="#152c53" stroke="#152c53" d="M0 48.007v48.008l64.25-.258 64.25-.257.26-47.75.259-47.75H0v48.007m.462.493c.001 26.4.13 37.056.287 23.681.158-13.376.158-34.976 0-48C.591 11.156.462 22.1.462 48.5M45 20.962c-15.555 3.332-28.476 9.625-32.716 15.936-3.626 5.394-2.657 6.475 1.805 2.013C21.845 31.155 36.6 25.694 58.922 22.32c2.982-.451 5.607-1.382 5.833-2.07.609-1.851-9.493-1.487-19.755.712M88 43.5V58h2.5c2.458 0 2.5-.133 2.5-8v-8h9v8c0 7.867.042 8 2.5 8 2.478 0 2.5-.077 2.5-8.845C107 38.383 105.996 37 98.171 37H93v-4c0-3.6-.25-4-2.5-4H88v14.5m-63.333-5.833c-.367.366-.667 5.991-.667 12.5V62h2.5c2.333 0 2.5-.333 2.5-5v-5h5.418c8.28 0 8.582-.264 8.582-7.5 0-4.81-.372-6.429-1.582-6.893-2.144-.823-15.918-.774-16.751.06m21.042-.043c-.39.39-.709 4.427-.709 8.971 0 10.98.604 11.575 11.36 11.194l8.14-.289v-20H62c-2.426 0-2.509.228-2.792 7.75L58.916 53h-7.832l-.292-7.75c-.261-6.926-.509-7.781-2.333-8.042-1.123-.161-2.36.027-2.75.416m22.946 1.205C67.745 39.835 67 42.294 67 44.294 67 48.772 68.922 50 75.934 50 79.77 50 81 50.364 81 51.5c0 1.19-1.444 1.5-7 1.5-6.8 0-7 .071-7 2.5 0 2.456.138 2.5 7.929 2.5C84.026 58 86 56.841 86 51.5c0-4.868-2.151-6.5-8.571-6.5C73.27 45 72 44.649 72 43.5c0-1.179 1.389-1.5 6.5-1.5 6.267 0 6.5-.09 6.5-2.5 0-2.44-.177-2.5-7.345-2.5-5.846 0-7.683.373-9 1.829M29 44.5c0 2.296.367 2.5 4.5 2.5s4.5-.204 4.5-2.5-.367-2.5-4.5-2.5-4.5.204-4.5 2.5M9.044 49.282c-.024.43.653 2.455 1.505 4.5 9.798 23.519 67.172 31.176 97.41 12.999 5.986-3.598 12.043-10.697 12.037-14.109-.003-1.935-.207-1.844-1.867.828-11.667 18.785-55.692 25.63-86.915 13.513-8.885-3.448-17.512-9.776-20.158-14.786-1.082-2.05-1.987-3.375-2.012-2.945" fill-rule="evenodd"/><path fill="#152c53" stroke="#152c53" d="M0 48.007v48.008l64.25-.258 64.25-.257.26-47.75.259-47.75H0v48.007m.462.493c.001 26.4.13 37.056.287 23.681.158-13.376.158-34.976 0-48C.591 11.156.462 22.1.462 48.5M52 19.532c-21.015 2.934-37.693 11.092-41.582 20.34-2.324 5.526-1.701 5.428 4.332-.679 8.66-8.766 29.143-16.13 45-16.177 4.929-.015 5.25-.169 5.25-2.516 0-2.875.434-2.843-13-.968m38.25 9.288c-2.215.314-2.25.546-2.25 14.75V58h2.5c2.458 0 2.5-.133 2.5-8v-8h8v16h6v-9.465C107 37.59 106.546 37 98.121 37H93.11l-.305-4.25c-.27-3.764-.562-4.213-2.555-3.93M24 49.5V62h3.044c1.855 0 2.98-.488 2.881-1.25-.089-.687-.109-2.937-.043-5L30 52h6.025C42.659 52 44 50.633 44 43.869 44 37.702 42.872 37 32.965 37H24v12.5m21-3.582C45 58.537 44.529 58 55.607 58H65V37h-6v16h-8V37h-6v8.918m23.571-7.347c-1.625 1.625-2.119 8.019-.782 10.122.418.657 3.341 1.332 6.497 1.5 8.1.433 7.599 2.208-.792 2.807-7.03.502-7.228.636-6.649 4.5.197 1.312 16.234.679 17.904-.706 1.3-1.079 1.702-7.455.644-10.212-.466-1.214-2.093-1.582-7-1.582C73.377 45 72 44.677 72 43.5c0-1.19 1.444-1.5 7-1.5 6.8 0 7-.071 7-2.5 0-2.456-.138-2.5-7.929-2.5-5.874 0-8.335.407-9.5 1.571M30 44.5c0 2.25.4 2.5 4 2.5s4-.25 4-2.5-.4-2.5-4-2.5-4 .25-4 2.5M9.389 50.388c3.314 24.322 59.595 35.29 95.367 18.584 8.113-3.789 15.252-11.835 15.238-17.172-.006-2.101-.14-2.04-1.556.7-10.53 20.392-61.559 27.073-91.938 12.037-8.24-4.078-13.006-8.316-15.693-13.953L8.86 46.5l.529 3.888" fill-rule="evenodd"/></svg>
        </li-icon>
      </a>
    </header>
    <main class="loginmainpage" >
      <div style="height: 120px; width: 100%"/>
      <div class="card" v-loading="loading" ref="loginrotaition" >
          <div class="organ">
              <div class="headercontent">
                <h1 class="header__content__heading ">登录</h1>
                <br>
                <p class="header__content__subheading ">使用评估系统</p>
              </div>
            <div style="height: 10px;"/>
              <form  class="login__form"  novalidate="true"  @submit.prevent="loginClick">
                <div class="l-1">
                  <input  id="username" v-model="input" name="session_key" type="text" required  autofocus aria-label="账号" autocomplete="off">
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




<style scoped>



.app__container {
    display: flex;
    min-height: 100vh;
    background-color: var(--color-background-canvas, #ffffff);
    z-index: 1;

}
.thistop{
  display: relative;
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
    z-index: 1;
}



.l-1>input {
    font-size: 1.6rem;
    line-height: 1.33333;
    font-weight: 400;
    color: rgba(0, 0, 0, 0.9);
    border: 2px solid #ccc; /* 设置边框为1像素宽，实线，颜色为灰色 */
    height: 60px;
    padding: 28px 15px 6px;
    border-radius: 4px !important;
    z-index: 1;
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
    z-index: 1;
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
