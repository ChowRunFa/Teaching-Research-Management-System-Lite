<template>
  <div class="main-box">
    <div
      :class="['container', 'container-login', { 'is-txl is-z200': isLogin }]"
    >
      <form>
        <h2 class="title">教学科研管理系统</h2>
        <span class="text">开启高效管理教学科研信息之旅！</span>
        <input class="form__input"  placeholder="请输入工号" type="text" v-model="user.workno">
        <input class="form__input"  placeholder="请输入姓名" type="password" v-model="user.name" show-password>
        <div class="primary-btn" @click="login">登录</div>
        <br>

          <div class="flex justify-space-between mb-4 flex-wrap gap-4">
    <el-button
      v-for="button in buttons"
      :key="button.text"
      :type="button.type"
      @click="button.click"
      text
      >{{ button.text }}</el-button
    >
  </div>

      </form>
    </div>
    <div :class="['switch']">
<!--       { login: isLogin }-->
              <div class="top">
                <h1 class="title4"> AcademiaPro</h1>

              </div>
<!--      <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>-->

          <div class="demo-image__preview">
<!--            :src="srcList[currentIndex]"-->
            <!--        :src="url"-->
    <el-image

      :src="srcList[currentIndex]"
      :zoom-rate="1.2"
      :preview-src-list="srcList"
      :initial-index="0"
      fit="cover"
    />

      </div>

    </div>

  </div>

</template>

<script setup>


//导入引用对象
import { ElMessageBox   } from 'element-plus';
import {ref, onMounted} from 'vue'
import {Login} from '@/api/user'
import {useRouter} from'vue-router'
//创建一个用户
const user = ref({workno:"",name:""})
const router = useRouter();

const buttons = ref([
  { type: 'primary', text: '快速体验AcademiaPro', click: handleClick },
  // { type: 'info', text: 'Gay Hub'ick, click: handleCl }
  { type: 'plain', text: '访问我的GitHub', click: toGitHub }

])
function toGitHub(){
      window.location.href
          = 'https://github.com/ChowRunFa/Teaching_Research_Registration_System';
}


function handleClick(){
         ElMessageBox({
    title: '登录成功',
    message: `欢迎您体验AcademiaPro！`,
    type: 'success',
    showCancelButton: false,
    closeOnClickModal: false,
    closeOnPressEscape: false,
    confirmButtonText: '谢谢',
    callback: action => {
      if (action === 'confirm') {
        router.push('/admin')
      }
    }
  });
}
  // { type: 'info', text: 'info', click: handleClick },
  // { type: 'warning', text: 'warning', link: 'https://example.com' },
  // { type: 'danger', text: 'danger', click: handleClick },
function login(){
//实现登录
  Login(user.value)
  .then(res=>{
    if(res.data.code===200){
      const user = res.data.data.user
         ElMessageBox({
    title: '登录成功',
    message: `欢迎您，${user.name} ${user.level}！`,
    type: 'success',
    showCancelButton: false,
    closeOnClickModal: false,
    closeOnPressEscape: false,
    confirmButtonText: '确定',
    callback: action => {
      if (action === 'confirm') {
        // 保存token与用户信息
        localStorage.setItem("token",res.data.token);
        localStorage.setItem("UserInfo",JSON.stringify(user));
        router.push('/admin')
      }
    }
  });
    }else {
      //弹出失败
          ElMessageBox.alert(res.data.msg, '提示', {
            confirmButtonText: '确定',
            type: 'error'
          }).then(() => {
          })
    }
  })
}

const currentIndex = ref(0);
// const url =
//   'https://pic3.zhimg.com/80/v2-a3babe36b1790cef49dfacf3b94f4086_1440w.webp'


const srcList = [
  'https://pic3.zhimg.com/80/v2-a3babe36b1790cef49dfacf3b94f4086_1440w.webp',
  'https://pic2.zhimg.com/80/v2-243d6b9c9c02de9624cded584b4c039d_1440w.webp',
  'https://pic1.zhimg.com/80/v2-28487bee6ed6b86aa413c4b80485b6ec_1440w.webp',
  'https://pic3.zhimg.com/80/v2-aa3c3a02b7bd2126be4d2ca41e00e31a_1440w.webp',
  'https://pic4.zhimg.com/80/v2-59c2b277972a9acbb1b5832a693c53f3_1440w.webp',
  'https://pic2.zhimg.com/80/v2-945e3fbcb5f6cfe4da857e7181a217ad_1440w.webp',
  'https://pic2.zhimg.com/80/v2-72952d7b52c00576c5cbd3e52f7bd83d_1440w.webp',
]

onMounted(() => {
  setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % srcList.length;
  }, 2000);
});


</script>

<style lang="scss" scoped>
body {
  background-color: #ecf0f3;
}
.main-box {
 position: fixed;
  top: 50%;
  left: 50%;
    width: 50%;
  height: 50%;
  transform: translate(-50%, -50%);
  min-width: 1000px;
  min-height: 600px;
  padding: 25px;
  background-color: #ecf0f3;
  box-shadow: 10px 10px 10px #d1d9e6, -10px -10px 10px #f9f9f9;
  border-radius: 12px;
  overflow: hidden;
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 0;
    width: 600px;
    height: 100%;
    padding: 25px;
    background-color: #ecf0f3;
    transition: all 1.25s;
    form {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      width: 100%;
      height: 100%;
      color: #a0a5a8;
      .title {
        font-size: 34px;
        font-weight: 700;
        line-height: 3;
        color: #181818;
      }
      .text {
        margin-top: 30px;
        margin-bottom: 12px;
      }
      .form__input {
        width: 350px;
        height: 40px;
        margin: 4px 0;
        padding-left: 25px;
        font-size: 13px;
        letter-spacing: 0.15px;
        border: none;
        outline: none;
        // font-family: 'Montserrat', sans-serif;
        background-color: #ecf0f3;
        transition: 0.25s ease;
        border-radius: 8px;
        box-shadow: inset 2px 2px 4px #d1d9e6, inset -2px -2px 4px #f9f9f9;
        &::placeholder {
          color: #a0a5a8;
        }
      }
    }
  }
  .container-register {
    z-index: 100;
    left: calc(100% - 600px);
  }
  .container-login {
    left: calc(100% - 600px);
    z-index: 0;
  }
  .is-txl {
    left: 0;
    transition: 1.25s;
    transform-origin: right;
  }
  .is-z200 {
    z-index: 200;
    transition: 1.25s;
  }
  .switch {
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 400px;
    padding: 50px;
    z-index: 200;
    transition: 1.25s;
    background-color: #ecf0f3;
    overflow: hidden;
    box-shadow: 4px 4px 10px #d1d9e6, -4px -4px 10px #f9f9f9;
    color: #a0a5a8;
    .switch__circle {
      position: absolute;
      width: 500px;
      height: 500px;
      border-radius: 50%;
      background-color: #ecf0f3;
      box-shadow: inset 8px 8px 12px #d1d9e6, inset -8px -8px 12px #f9f9f9;
      bottom: -60%;
      left: -60%;
      transition: 1.25s;
    }
    .switch__circle_top {
      top: -30%;
      left: 60%;
      width: 300px;
      height: 300px;
    }
    .switch__container {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      position: absolute;
      width: 400px;
      padding: 50px 55px;
      transition: 1.25s;
      h2 {
        font-size: 34px;
        font-weight: 700;
        line-height: 3;
        color: #181818;
      }
      p {
        font-size: 14px;
        letter-spacing: 0.25px;
        text-align: center;
        line-height: 1.6;
      }
    }
  }
  .login {
    left: calc(100% - 400px);
    .switch__circle {
      left: 0;
    }
  }
  .primary-btn {
    width: 180px;
    height: 50px;
    border-radius: 25px;
    margin-top: 50px;
    text-align: center;
    line-height: 50px;
    font-size: 14px;
    letter-spacing: 2px;
    background-color: #4b70e2;
    color: #f9f9f9;
    cursor: pointer;
    box-shadow: 8px 8px 16px #d1d9e6, -8px -8px 16px #f9f9f9;
    &:hover {
      box-shadow: 4px 4px 6px 0 rgb(255 255 255 / 50%),
        -4px -4px 6px 0 rgb(116 125 136 / 50%),
        inset -4px -4px 6px 0 rgb(255 255 255 / 20%),
        inset 4px 4px 6px 0 rgb(0 0 0 / 40%);
    }
  }
}

.demo-progress .el-progress--line {
  margin-bottom: 15px;
  width: 350px;
}

.title4{
  font-size: 48px;
color: #052d3a;
letter-spacing: 0;
text-shadow: 0px 1px 0px #999, 0px 2px 0px #888, 0px 3px 0px #777, 0px 4px 0px #666, 0px 5px 0px #555, 0px 6px 0px #444, 0px 7px 0px #333, 0px 8px 7px #001135;

}


.time {
  font-size: 12px;
  color: #999;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.demo-image__error .image-slot {
  font-size: 30px;
}
.demo-image__error .image-slot .el-icon {
  font-size: 30px;
}
.demo-image__error .el-image {
  width: 100%;
  height: 500px;
}

.top {
  position: absolute;
  top: 0%;
  left: 20%;
  //transform: translateY(-50%) translateX(-50%);
}


.bottom {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
}

html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

.parent {
  position: relative;
  height: 100%;
}
.image {
  width: 100%;
  height: 100%;
  transition: opacity 0.5s ease-in-out;
  opacity: 0;
}

.image.show {
  opacity: 1;
}
</style>
