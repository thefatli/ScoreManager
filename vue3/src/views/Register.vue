<template>
  <div>
    <div class="login-container">
      <div style="width: 350px" class="login-box">
        <div style="font-weight: bold; font-size: 24px; text-align: center; margin-bottom: 30px">注 册</div>
        <el-form :model="data.form" ref="formRef" :rules="rules">
          <el-form-item prop="username">
            <el-input prefix-icon="User" v-model="data.form.username" placeholder="请输入账号" />
          </el-form-item>
          <el-form-item prop="password">
            <el-input show-password prefix-icon="Lock" v-model="data.form.password"  placeholder="请输入密码" />
          </el-form-item>
          <el-form-item prop="role">
            <el-select style="width: 100%" v-model="data.form.role">
              <!-- <el-option value="ADMIN" label="管理员"></el-option> -->
              <el-option value="S" label="学生"></el-option>
              <el-option value="T" label="教师"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" style="width: 100%" @click="register">注 册</el-button>
          </el-form-item>
        </el-form>
        <div style="margin-top: 30px; text-align: right">
          已有账号？请 <a href="/login">登录</a>
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
  form: {}
})

const rules = reactive({
  username: [
    { required: true, message: '请输入账号', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
  ],
  role: [
    { required: true, message: '请选择身份', trigger: 'blur' },
  ]
})

const formRef = ref()

const register = () => {
  formRef.value.validate((valid) => {
    if (valid) {
      axios.post('http://127.0.0.1:8000/auth/users/', {
        username:data.form.username,
        password:data.form.password,
        identified_check:data.form.role
      }).then(res => {
        if (res.status === 201) {
          ElMessage.success('注册成功')
          console.log(res.data)
          let tempid=res.data.id
          if(data.form.role=="S"){
            axios.post('http://127.0.0.1:8000/students/',{
              user:tempid,
              gender:'女'
            }).then(res=>{
              if(res.status==201) console.log('学生账号创建成功')
            })}
          if(data.form.role=="T"){
            request.post('http://127.0.0.1:8000/teachers/',{
              user:tempid,
              gender:'女'
            }).then(res=>{
              if(res.status==201) console.log('老师账号创建成功')
            })}
          // router.push('/login/') // 跳转到主页
        } else {
          ElMessage.error(res.msg)
        }
      }).catch(err=>{
        ElMessage.error('请检查账号或密码')
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