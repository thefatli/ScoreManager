<template>
  <div>
    <div class="login-container">
      <div style="width: 350px" class="login-box">
        <div style="font-weight: bold; font-size: 24px; text-align: center; margin-bottom: 30px">登 录</div>
        <el-form :model="data.form" ref="formRef" :rules="rules">
          <el-form-item prop="username">
            <el-input prefix-icon="User" v-model="data.form.username" placeholder="请输入账号" />
          </el-form-item>
          <el-form-item prop="password">
            <el-input show-password prefix-icon="Lock" v-model="data.form.password"  placeholder="请输入密码" />
          </el-form-item>
          <el-form-item prop="role">
            <el-select style="width: 100%" v-model="data.form.role">
              <el-option value="A" label="管理员"></el-option>
              <el-option value="S" label="学生"></el-option>
              <el-option value="T" label="教师"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" style="width: 100%" @click="login">登 录</el-button>
          </el-form-item>
        </el-form>
        <div style="margin-top: 30px; text-align: right">
          还没有账号？请 <a href="/register">注册</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {reactive, ref} from "vue"
import request from "@/utils/request";
import {ElMessage} from "element-plus";
import router from "@/router";
import axios from "axios";


const data = reactive({
  form: { role: 'A' }
})

const rules = reactive({
  username: [
    { required: true, message: '请输入账号', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
  ],
})

const formRef = ref()

function changerole(label){
  data.form.role = label
}

const login = () => {
  formRef.value.validate((valid) => {
    if (valid) {
      console.log(data.form)
      request.post('/auth/jwt/create/', { 
        username: data.form.username,
        password: data.form.password}).then(res => {
        console.log(res.data)
        console.log(res.status)
        if (res.status === 200) {
          localStorage.setItem('student-user', JSON.stringify(data.form))
          localStorage.setItem('token', res.data.access)
          localStorage.setItem('refresh', res.data.refresh)
          console.log(localStorage.getItem('token'))
          request.get('/identified_check/').then(res=>{
            console.log(res)
            if(res.status==200){
              console.log('正确身份'+res.data.identified_check)
              console.log(data.form.role)
              if(res.data.identified_check === data.form.role){
                ElMessage.success('登录成功')
                request.get('/user/update/').then(res=>{
                if(res.status==200){
                  console.log('header获取头像成功')
                  console.log(res.data)
                  localStorage.setItem('useravatar', res.data.image)
                }
              })
              request.get('/me/').then(res => {
                if (res.status === 200) {
                  console.log('获取个人信息成功')
                  console.log(res.data)
                  localStorage.setItem('me', JSON.stringify(res.data))
                } else {
                  ElMessage.error('获取个人信息失败')
                  console.log(res.status)
                }
              })
                console.log(res.data)
                router.push('/home') // 跳转到主页
              }
              else ElMessage.error('请检查身份')
            }
          }).catch(err=>{
            ElMessage.error('账号未选择身份')
          })
          //ElMessage.success('登录成功')
          //console.log(res.data)
          //router.push('/home') // 跳转到主页
        }
      }).catch(err=>{
        ElMessage.error('账号或密码错误!')
      })
    }
  })
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background-image: url("@/assets/imgs/bg.jpg");
  background-size: cover;
}
.login-box {
  /* background-color: #fff; */
  background-color:rgba(255,255,255,0.8);
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  padding: 30px;
  border-radius: 5px;
}
</style>