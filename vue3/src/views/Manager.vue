<template>
  <div>
    <div style="height: 60px; background-color: #fff; display: flex; align-items: center; border-bottom: 1px solid #ddd">
      <div style="flex: 1">
        <div style="padding-left: 20px; display: flex; align-items: center">
          <el-icon :size="40" color=#11A989><Menu></Menu></el-icon>
          <div style="font-weight: bold; font-size: 24px; margin-left: 5px">学生成绩管理系统</div>
        </div>
      </div>
      <div style="width: fit-content; padding-right: 10px; display: flex; align-items: center;">
        <span style="margin-right: 20px;"  v-html="day"></span>
        <img :src="useravatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'" alt="" style="width: 40px; height: 40px; border-radius: 50%">
        <span style="margin-right: 15px; margin-left: 5px">{{ user.username }}</span>
      </div>
    </div>

    <div style="display: flex">
      <div style="width: 200px; border-right: 1px solid #ddd; min-height: calc(100vh - 60px)">
        <el-menu
            router
            style="border: none"
            :default-active="$route.path"
            :default-openeds="['/home', '2', '3','4','/person']"
        >
        <el-menu-item index="/home">
            <el-icon><HomeFilled /></el-icon>
            <span>系统首页</span>
          </el-menu-item>
          <el-sub-menu index="2" v-if="user.role === 'S'">
            <template #title v-if="user.role === 'S'">
              <el-icon><Memo /></el-icon>
              <span>课程管理</span>
            </template>
            <el-menu-item index="/courseList" v-if="user.role === 'S'">
              <el-icon><search /></el-icon>
              <span>学生选课</span>
            </el-menu-item>
            <el-menu-item index="/studentCourse" v-if="user.role === 'S'">
              <el-icon><Document /></el-icon>
              <span>选课记录</span>
            </el-menu-item>
          </el-sub-menu>
          <el-menu-item index="/course" v-if="user.role === 'A'"  >
              <el-icon><memo /></el-icon>
              <span>课程信息</span>
          </el-menu-item>
          <el-sub-menu index="2" v-if="user.role === 'T'">
            <template #title v-if="user.role === 'T'">
              <el-icon><Memo /></el-icon>
              <span>课程管理</span>
            </template>
            <el-menu-item index="/courseteacher" v-if="user.role === 'T'">
              <el-icon><search /></el-icon>
              <span>课程信息</span>
            </el-menu-item>
            <el-menu-item index="/studentCourse" v-if="user.role === 'T'">
              <el-icon><Document /></el-icon>
              <span>开课记录</span>
            </el-menu-item>
          </el-sub-menu>
          <el-menu-item index="/teachergrade" v-if="user.role === 'T'" >
              <el-icon><Document /></el-icon>
              <span>成绩管理</span>
          </el-menu-item>
          <el-menu-item index="/studentgrade" v-if="user.role === 'S'">
              <el-icon><search /></el-icon>
              <span>成绩查询</span>
          </el-menu-item>
          <el-sub-menu index="7" v-if="user.role === 'A'">
            <template #title v-if="user.role === 'A'">
              <el-icon><User /></el-icon>
              <span>用户管理</span>
            </template>
            <el-menu-item index="/teacher" >
              <el-icon><avatar /></el-icon>
              <span>教师信息</span>
            </el-menu-item>
            <el-menu-item index="student">
              <el-icon><UserFilled /></el-icon>
              <span>学生信息</span>
            </el-menu-item>
            <el-menu-item index="college">
              <el-icon><UserFilled /></el-icon>
              <span>学院信息</span>
            </el-menu-item>
          </el-sub-menu>
          <el-menu-item index="/person" v-if="user.role === 'S' || user.role === 'T'" >
            <el-icon><edit /></el-icon>
            <span>个人资料</span>
          </el-menu-item>
          <el-menu-item index="login" @click="logout">
            <el-icon><SwitchButton /></el-icon>
            <span>退出系统</span>
          </el-menu-item>
        </el-menu>
      </div>

      <div style="flex: 1; width: 0; background-color: #f8f8ff; padding: 10px">
        <router-view />
      </div>
    </div>

  </div>
</template>

<script setup>
import { Menu } from '@element-plus/icons-vue';
import { useRoute } from 'vue-router'
const $route = useRoute()
const user = JSON.parse(localStorage.getItem('student-user') || '{}')
const useravatar = localStorage.getItem('useravatar') || '{}'
const me = JSON.parse(localStorage.getItem('me') || '{}')
import request from '../utils/request';

let today = new Date();
let weekday = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
let date = today.getFullYear() + '年 ' + (today.getMonth() + 1) + '月 ' + today.getDate() + '日';
let week = weekday[today.getDay()];
let day = date + "&#x3000;" + week;

console.log('头像数据：'+useravatar)

const logout = () => {
  localStorage.removeItem('student-user')
  localStorage.removeItem('useravatar')
  localStorage.removeItem('me')
}
</script>

<style scoped>
.el-menu-item.is-active {
  background-color: #dcede9 !important;
}
.el-menu-item:hover {
  color: #11A983;
}
:deep(th)  {
  color: #333;
}
</style>