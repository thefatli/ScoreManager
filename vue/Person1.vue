<template>
<el-container class="card2">
    <!-- style="height: 98%;background-color: white;" -->
   <el-aside :class="clty1">
        <div :class="clty2" @click=xiugai()>
          <!-- 首页user信息 -->
          <el-card shadow= 'hover' style="background-color: rgba(0,0,0,0.1);">
            <div style="height: 400px;margin-top: auto;">
              <el-avatar :size="100" :src="circleUrl" style="position: relative;margin-top: 25%;margin-left: 28%;">
                <div style="margin-top: 40px;" @click="shangchuan()">
                  <img :src="useravatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); max-width: 100%; max-height: 100%;">
                </div>
          </el-avatar>
              <div style="height: 20px;margin-left: 29%;margin-top: 15%;">
                <p><el-icon><User /></el-icon> _{{user.username}}_</p>
                <p v-if="user.role=='T'"><el-icon><UserFilled /></el-icon> _老师_</p>
                <p v-if="user.role=='S'"><el-icon><UserFilled /></el-icon> _学生_</p>
                <p v-if="user.role=='A'"><el-icon><UserFilled /></el-icon> _管理员_</p>
              </div>
            </div>
          </el-card>
        </div>        
  </el-aside>
  <el-container class="card3">
  <!-- <el-form :model="data.form" ref="formRef" label-width="100px" label-position="right"
               style="padding-right: 40px;width: 650px;padding-left: 80px;padding-top: 0px;"> -->

        <!-- <el-form-item><h1 style="font-size: 200%;font-family: '黑体';">个人信息</h1></el-form-item>
        <p style="font-family:'黑体';font-size: 18px;">
        <span style="margin-left: 80px;">学号： {{ me.id }} </span>
        </p>
        <p style="font-family:'黑体';font-size: 18px;">
        <span style="margin-left: 80px;">姓名： {{ me.name }}</span>
        </p>
        <p style="font-family:'黑体';font-size: 18px;margin-top: 20px">
          <span style="margin-left: 80px;">性别：</span>
          <el-radio-group v-model="me.gender" aria-disabled="ture">
                <el-radio label="男"></el-radio>
                <el-radio label="女"></el-radio>
              </el-radio-group>
        </p>
        <p style="font-family:'黑体';font-size: 18px;margin-top: 20px">
          <span style="margin-left: 80px;">学院：</span>
          <span style="margin-left: 10px;">{{ me.college_name }}</span>
        </p>
        <p v-if="data.user.role=='S'"  style="font-family:'黑体';font-size: 18px;margin-top: 20px">
          <span style="margin-left: 80px;">年级：</span>
          <span style="margin-left: 10px;">{{ me.grade }}</span>
        </p>
        <p style="font-family:'黑体';font-size: 18px;margin-top: 20px">
          <span style="margin-left: 80px;">联系方式：</span>
          <span style="margin-left: 10px;">{{ me.email }}</span>
        </p>
        <p style="font-family:'黑体';font-size: 18px;margin-top: 20px">
          <span style="margin-left: 80px;">生日：</span>
          <span style="margin-left: 10px;">{{ me.birth_date }}</span>
        </p>
        <p style="font-family:'黑体';font-size: 18px;margin-top: 20px">
          <span style="margin-left: 80px;">个人简介：</span>
          <span style="margin-left: 10px;">{{ me.info }}</span>
        </p> -->

        <el-form label-width="100px" label-position="right"
               style="padding-right: 100px;width: 650px;padding-left: 80px;padding-top: 0px;">
        <el-form-item><h1 style="font-family: '黑体';">个人信息</h1></el-form-item>
        <el-form-item label="姓名" disabled>
          <el-input v-model=me.name />
        </el-form-item>
        <el-form-item v-if="user.role=='S'"  label="学号" disabled>
          <el-input v-model=me.id />
        </el-form-item>
        <el-form-item v-if="user.role=='T'"  label="学工号" disabled>
          <el-input v-model=me.id />
        </el-form-item>
        <el-form-item label="性别" disabled>
          <el-radio-group v-model="me.gender">
            <el-radio label="男"></el-radio>
            <el-radio label="女"></el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="学院" disabled>
          <el-input v-model=me.college_name />
        </el-form-item>
        <el-form-item label="年级" v-if="data.user.role=='S'" disabled>
          <el-input v-model=me.grade />
        </el-form-item>
        <el-form-item label="邮箱" disabled>
          <el-input v-model="me.email" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="生日" disabled>
          <el-date-picker style="width: 100%" format="YYYY-MM-DD" value-format="YYYY-MM-DD"
                          v-model="me.birth_date"></el-date-picker>
        </el-form-item>
        <el-form-item label="个人简介" disabled>
          <el-input v-model="me.info" autocomplete="off"/>
        </el-form-item>

      <p style="margin-top: 10px;margin-left: 100px;">
        <el-button type="primary" @click="updatea">上传头像</el-button>
        <el-button type="primary" @click="update">修改资料</el-button>
      </p>
  </el-form>
  </el-container>
</el-container>

<el-dialog width="35%" height="50%" v-model="data.formVisible" title="个人信息">
      <el-form :model="data.form" ref="formRef" label-width="100px" label-position="right"
               style="padding-right: 40px">
        <el-form-item label="姓名" prop="username">
          <el-input v-model="data.form.name" autocomplete="off" disabled />
        </el-form-item>
        <el-form-item v-if="user.role=='S'" label="学号">
          <el-input v-model="data.form.id" autocomplete="off" disabled/>
        </el-form-item>
        <el-form-item v-if="user.role=='T'" label="学工号">
          <el-input v-model="data.form.id" autocomplete="off" disabled/>
        </el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="data.form.gender">
            <el-radio label="男"></el-radio>
            <el-radio label="女"></el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="学院">
          <el-select v-model="data.form.college" clearable="" filterable>
            <el-option v-for="item in Colleges" :label="item.name" :value="item.id" :key="item.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="年级" v-if="data.user.role=='S'">
          <el-select style="width: 100%" v-model="data.form.grade">
              <el-option value="1" label="1"></el-option>
              <el-option value="2" label="2"></el-option>
              <el-option value="3" label="3"></el-option>
              <el-option value="4" label="4"></el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="data.form.email" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="生日">
          <el-date-picker style="width: 100%" format="YYYY-MM-DD" value-format="YYYY-MM-DD"
                          v-model="data.form.birth_date"></el-date-picker>
        </el-form-item>
        <el-form-item label="个人简介">
          <el-input v-model="data.form.info" autocomplete="off"/>
        </el-form-item>
        <el-form-item>
          <el-button @click="data.formVisible = false">取 消</el-button>
          <el-button type="primary" @click="save">保 存</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog width="35%" height="50%" v-model="data.formVisible2" title="上传头像">
    <el-form :model="data.form" ref="formRef" label-width="100px" label-position="right"
              style="padding-right: 40px">
      <el-form-item>
        <!-- <el-upload class="avatar-uploader" action="http://localhost:8000/user/update/" method="put" headers=token
        :show-file-list="false" :on-success="handleImgUploadSuccess">
          <img v-if="data.avatar" :src="data.avatar" class="avatar">
          <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
        </el-upload> -->
        <div class="card">
        <div>
          <input style="position:absolute;opacity:0;" type="file" @change="uploads"/>
          <img style="width: 120px;height: 120px;" src="../../assets/imgs/上传头像.png"> 
          <!-- <el-icon class="avatar-uploader-icon" :size="130"><Plus /></el-icon> -->
        </div>
      </div>
      </el-form-item>
      <el-form-item style="margin-left: 40%;margin-top: 15%;">
          <el-button @click="data.formVisible2 = false">取 消</el-button>
        </el-form-item>
      </el-form>
      </el-dialog>
</template>

<script setup>
import {reactive} from "vue";
import request from "@/utils/request";
import {ElMessage} from "element-plus";
import router from "@/router";
import axios from 'axios';
import {Plus} from "@element-plus/icons-vue"
const user = JSON.parse(localStorage.getItem('student-user') || '{}')
const useravatar = localStorage.getItem('useravatar') || '{}'
const me = JSON.parse(localStorage.getItem('me') || '{}')
const token = localStorage.getItem('token') || '{}'

console.log(me)

let Colleges=[]
  request.get('/collegelist/').then(res=>{
  if(res.status==200) {
    console.log('获取学院信息成功')
    Colleges = res.data
  }
 })

const data = reactive({
  user: JSON.parse(localStorage.getItem('student-user') || "{}"),
  // avatar:
})

let clty1,clty2
if(user.role=='A') {clty1="asideA"; clty2="divasideA"}
if(user.role=='T') {clty1="asideT"; clty2="divasideT"}
if(user.role=='S') {clty1="asideS"; clty2="divasideS"}

const handleImgUploadSuccess = (res) => {
  data.avatar = res.data.image
  console.log(data.avatar)
}

const save = () => {
  request.put('/me/', data.form).then(res => {
    console.log(data.form)
    if (res.status === 200) {
      ElMessage.success("修改资料成功，请重新登录")
      router.push('/login')
    } else {
      ElMessage.error(res.msg)
    }
  })
}

const update = () => {
  data.form=me;
  data.formVisible=true;
}

const updatea = () => {
  // data.avatar=useravatar;
  data.formVisible2=true;
}

const uploads=(e)=>{
    const file = e.target.files[0];
    // this.file = file;
    if (file) {
      const formData = new FormData();
      formData.append('image', file);

      axios.put('http://localhost:8000/user/update/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `JWT ${token}`,
        }
      }).then(res => {
        console.log('上传文件');
        console.log(res);
        ElMessage.success('上传成功，请重新登陆查看！');
        data.formVisible2=false;
        router.push('/login')
      }).catch(err => {
        console.error(err);
        ElMessage.error('更新失败: ' + err.message);
      });
    }
}


</script>

<style>
.card2 {
    /* background-color: white; */
    background-image: url(/src/assets/imgs/home2.jpg);
    background-repeat: no-repeat;
    background-attachment: fixed;
    border-radius: 5px;
    height: 100%;
    position: fixed;
    margin-right: 10px;
    margin-bottom: 10px;
    padding-bottom: 10px;
    /* padding-right: 10px; */
    box-shadow: 0 0 10px rgba(0,0,0,.1);
}

.card3 {
    /* background-color: #fff; */
    margin:20px;
    margin-right: 10%;
    background-color: rgba(250,250,250,0.99);
    border-radius: 5px;
    padding: 10px;
    box-shadow: 0 0 10px rgba(0,0,0,.1);
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  line-height: 100px;
  text-align: center;
}
.avatar {
  width: 100px;
  height: 100px;
  display: block;
}

.asideS{
  width: 380px;
  height: 97%;
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
  border-color: white;border-style: solid;
}

.asideT{
  width: 380px;
  height: 97%;
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
  border-color: white;border-style: solid;
}
</style>