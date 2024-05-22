<template>
  <!-- by 张羽佳 -->
  <div>
    <div class="card" style="width: 50%; padding: 40px">
      <el-form :model="data.form" ref="formRef" label-width="100px" label-position="right"
               style="padding-right: 40px">
        <el-form-item label="学生头像">
          <el-upload class="avatar-uploader" action="http://localhost:8000/user/update/" :show-file-list="false"
                     :on-success="handleImgUploadSuccess" method="put">
            <img v-if="data.form.avatar" :src="data.form.avatar" class="avatar">
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="学生账号" prop="username">
          <el-input v-model="data.form.username" autocomplete="off" disabled />
        </el-form-item>
        <el-form-item label="学生名称">
          <el-input v-model="data.form.name" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="data.form.gender">
            <el-radio label="男"></el-radio>
            <el-radio label="女"></el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="年级">
          <el-input v-model="data.form.grade" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="学院">
          <el-input v-model="data.form.college" autocomplete="off"/>
        </el-form-item>
        <!-- <el-form-item label="联系方式">
          <el-input v-model="data.form.phone" autocomplete="off"/>
        </el-form-item> -->
        <el-form-item label="生日">
          <el-date-picker style="width: 100%" format="YYYY-MM-DD" value-format="birth_date"
                          v-model="data.form.birth"></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="update">保 存</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import {reactive} from "vue";
import request from "@/utils/request";
import {ElMessage} from "element-plus";
import router from "@/router";
import {Plus} from "@element-plus/icons-vue"

let me
  request.get('/me/').then(res => {
    if (res.status === 200) {
      console.log('person2获取个人信息成功')
      console.log(res.data)
      me=res.data
    } else {
      ElMessage.error('获取个人信息失败')
      console.log(res.status)
    }
  })

const data = reactive({
  form: JSON.parse(localStorage.getItem('student-user') || "{}")
})

const handleImgUploadSuccess = (res) => {
  data.form.avatar = res.data
}

const update = () => {
  request.put('/me/', data.form).then(res => {
    if (res.status === 200) {
      ElMessage.success("操作成功")
      //router.push('/login')
    } else {
      ElMessage.error(res.msg)
    }
  })
}
</script>

<style>
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
</style>