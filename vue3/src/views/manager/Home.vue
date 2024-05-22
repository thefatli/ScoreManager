<template>
  <el-container class="card2">
    <!-- style="height: 98%;background-color: white;" -->
   <el-aside :class="clty1">
        <div :class="clty2" @click=xiugai()>
          <!-- 首页user信息 -->
          <el-card shadow= 'hover' style="background-color: rgba(0,0,0,0.1);">
            <div style="height: 400px;margin-top: auto;">
              <el-avatar :size="100" :src="circleUrl" style="position: relative;margin-top: 25%;margin-left: 28%;">
                <div style="margin-top: 40px;">
                  <img v-if="user.role=='A'" :src="'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); max-width: 100%; max-height: 100%;">
                  <img v-if="user.role=='T'"  :src="useravatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); max-width: 100%; max-height: 100%;">
                  <img v-if="user.role=='S'" :src="useravatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); max-width: 100%; max-height: 100%;">
                </div>
          </el-avatar>

              <div style="height: 20px;margin-left: 30%;margin-top: 15%;">
                <p><el-icon><User /></el-icon> _{{ user.username }}_</p>
                <p v-if="user.role=='T'" underline>
                  <el-icon><UserFilled /></el-icon> _老师_</p>
                <p v-if="user.role=='S'">
                  <el-icon><UserFilled :size="1"/></el-icon> _学生_</p>
                <p v-if="user.role=='A'">
                  <el-icon><UserFilled /></el-icon> _管理员_</p>
              </div>
            </div>
          </el-card>
        </div>        
  </el-aside>

  <el-card style="margin-top:0;margin-left: 0;height: 97%;">
      <el-calendar style="width: 90%;border: 0cap;box-shadow: 0cap;"  v-model="value" />
  </el-card>
      
</el-container>
</template>

<style scoped>
.card2 {
    background-color: white;
    border-radius: 5px;
    height: 100%;
    position: fixed;
    margin-right: 10px;
    margin-bottom: 10px;
    padding-bottom: 10px;
    /* padding-right: 10px; */
    box-shadow: 0 0 10px rgba(0,0,0,.1);
}

.asideA{
  width: 35%;height: 97%;
  background-image: url(/src/assets/imgs/home1.jpg);
  background-repeat: no-repeat;
  background-attachment: fixed;
}

.divasideA{
  margin-left: 10%;
  margin-top: 25%;
  margin-right: 5%;
  background-image: url(/src/assets/imgs/home1.jpg);
  background-repeat: no-repeat;
  background-attachment: fixed;
  border-style: solid;
  border-color: white;

}

.asideS{
  width: 35%;height: 97%;
  background-image: url(/src/assets/imgs/home2.jpg);
  background-repeat: no-repeat;
  background-attachment: fixed;
}

.divasideS{
  margin-left: 10%;
  margin-top: 25%;
  margin-right: 5%;
  background-image: url(/src/assets/imgs/home2.jpg);
  background-repeat: no-repeat;
  background-attachment: fixed;
  border-style: solid;
  border-color: white;

}

.asideT{
  width: 35%;height: 97%;
  background-image: url(/src/assets/imgs/home3.jpg);
  background-repeat: no-repeat;
  background-attachment: fixed;
}

.divasideT{
  margin-left: 10%;
  margin-top: 25%;
  margin-right: 5%;
  background-image: url(/src/assets/imgs/home3.jpg);
  background-repeat: no-repeat;
  background-attachment: fixed;
  border-style: solid;
  border-color: white;

}


</style>


<script setup>
import request from "@/utils/request";
import {reactive} from "vue";
import {ElMessageBox} from "element-plus";
// import router from "vue-router";
import { useRoute } from 'vue-router'
const useravatar = localStorage.getItem('useravatar') || '{}'
const me = JSON.parse(localStorage.getItem('me') || '{}')
const user = JSON.parse(localStorage.getItem('student-user') || '{}')
console.log('头像数据：'+useravatar)
console.log(me)
  const xiugai=()=>{
    //跳转到修改个人资料
    window.location.href = 'http://localhost:5173/person';
  }

let clty1,clty2
if(user.role=='A') {clty1="asideA"; clty2="divasideA"}
if(user.role=='T') {clty1="asideT"; clty2="divasideT"}
if(user.role=='S') {clty1="asideS"; clty2="divasideS"}

request.get('/').then(res => {
  console.log(res)
})

</script>

  





