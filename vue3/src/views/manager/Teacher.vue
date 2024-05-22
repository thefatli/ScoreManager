<template>
  <div>
     <div class="card" style="margin-bottom: 10px">
       <el-input style="width: 260px; margin-right: 10px" v-model="data.name" placeholder="请输入姓名/学院查询"
                 :prefix-icon="Search"/>
       <el-button type="primary" style="margin-left: 10px" @click="search()">查询</el-button>
       <el-button type="info" @click="reset">重置</el-button>
     </div>
 
     <div class="card" style="margin-bottom: 10px">
       <div style="margin-bottom: 10px">
         <el-button type="primary" @click="handleAdd">新增</el-button>
       </div>
 
       <div>
         <el-table :data="data.tableData" style="width: 100%">
           <!-- <el-table-column prop="username" label="学生账号"/> -->
           <el-table-column prop="name" label="老师姓名"/>
           <el-table-column prop="id" label="学工号" />
           <!-- <el-table-column prop="phone" label="学生手机号"/> -->
           <el-table-column prop="email" label="邮箱" width="220"/>
           <el-table-column prop="gender" label="性别"/>
           <el-table-column prop="college.name" label="学院"/>
           <!-- <el-table-column prop="birth" label="生日"/> -->
           <el-table-column label="操作" width="180">
             <template #default="scope">
               <el-button type="primary" @click="handleEdit(scope.row)">编辑</el-button>
               <el-button type="danger" @click="del(scope.row.id)">删除</el-button>
             </template>
           </el-table-column>
         </el-table>
       </div>
 
     </div>
 
     <div class="card">
      <el-pagination v-model:current-page="data.pageNum" v-model:page-size="data.pageSize"
                     @current-change="handelCurrentChange"
                     background layout="prev, pager, next" :total="data.total"/>
    </div>

 
     <el-dialog width="35%" v-model="data.formVisible" title="老师信息" destroy-on-close>
       <el-form :model="data.form" :rules="rules" ref="formRef" label-width="100px" label-position="right" style="padding-right: 40px">
         <el-form-item label="老师账号" prop="username" v-if="!add">
           <el-input v-model="data.form.name" autocomplete="off" disabled/>
         </el-form-item>
         <el-form-item label="老师密码" prop="password" v-if="!add">
           <el-input show-password v-model="data.form.password" autocomplete="off"/>
         </el-form-item>
         <el-form-item label="老师姓名">
           <el-input v-model="data.form.name" autocomplete="off"/>
         </el-form-item>
         <!-- <el-form-item label="手机号">
           <el-input v-model="data.form.phone" autocomplete="off"/>
         </el-form-item> -->
         <el-form-item label="邮箱">
           <el-input v-model="data.form.email" autocomplete="off"/>
         </el-form-item>
         <el-form-item label="性别">
           <el-radio-group v-model="data.form.gender">
             <el-radio label="男"></el-radio>
             <el-radio label="女"></el-radio>
           </el-radio-group>
         </el-form-item>
         <el-form-item label="学院">
          <el-select v-model="data.form.college.id" clearable="" filterable>
            <el-option v-for="item in Colleges" :label="item.name" :value="item.id" :key="item.id"></el-option>
          </el-select>
         </el-form-item>
         <!-- <el-form-item label="生日">
           <el-date-picker style="width: 100%" format="YYYY-MM-DD" value-format="YYYY-MM-DD" v-model="data.form.birth"></el-date-picker>
         </el-form-item> -->
       </el-form>
       <template #footer>
         <span class="dialog-footer">
           <el-button @click="data.formVisible = false">取 消</el-button>
           <el-button type="primary" @click="save">保 存</el-button>
         </span>
       </template>
     </el-dialog>
 
   </div>
 </template>
 
 <script setup>
 import {ref, reactive} from "vue"
 import {Search} from '@element-plus/icons-vue'
 import request from "@/utils/request";
 import {ElMessage, ElMessageBox} from "element-plus";
 import axios from "axios";
 
 let Colleges=[]
 request.get('/collegelist/').then(res=>{
  if(res.status==200) {
    console.log('获取学院信息成功')
    Colleges=res.data
    console.log(Colleges)
  }
 })


 const data = reactive({
   username: '',
   name: '',
   tableData: [],
   total: 0,
   pageNum: 1,  // 当前的页码
   pageSize: 6,  // 每页的个数
   formVisible: false,
   form: {}
 })
 
 const load = () => {
   request.get('/teachers/', {
     params: {
       page: data.pageNum,
      //  pageSize: data.pageSize,
       username: data.username,
       name: data.name,
     }
   }).then(res => {
     // data.tableData = res.data?.list || []
     // data.total = res.data?.total || 0
     if(res.status==200){
     data.tableData = res.data.results
     data.total = res.data.count
   }
   })
 }
 // 调用方法获取后台数据
 load()
 
 const search=()=>{
  console.log(data.name)
  request.get('/teachers/?search='+ data.name, {
     params: {
       page: data.pageNum,
       //pageSize: data.pageSize,
       username: data.username,
       name: data.name,
     }
   }).then(res => {
     // data.tableData = res.data?.list || []
     // data.total = res.data?.total || 0
     console.log(res.data)
     if(res.status==200){
     console.log(res.data)
     data.tableData = res.data.results
     data.total = res.data.results.length
   }
   })
 }

 const handelCurrentChange = () => {
   // 当翻页的时候重新加载数据即可
   load()
 }
 
 const reset = () => {
   // data.username = ''
   data.name = ''
   load()
 }
 
 const formRef = ref()
 
 let add=1
 const handleAdd = () => {
  data.form = {}
  data.form.college={}
  // data.form.id=1
   add=0
   data.formVisible = true
 }
 
 //保存数据到后台
 const save = () => {
    //console.log(data.form)
    //console.log(data.form.college.id)
   formRef.value.validate((valid) => {
     if (valid) {
      if(add){
        request.request({
         url: '/teachers/' + data.form.id + '/',
         method:'PUT',
         data: {
          'name':data.form.name,
          'gender':data.form.gender,
          'college':data.form.college.id,
          'email':data.form.email,
         }
       }).then(res => {
         if (res.status === 200) {
          console.log(data.tableData)
           load()    // 重新获取数据
           data.formVisible = false  // 关闭弹窗
           ElMessage.success("编辑成功")
         } else {
           ElMessage.error(res.msg)
         }
       })
      }
      else{
        axios.post('http://127.0.0.1:8000/auth/users/', {
        username:data.form.name,
        password:data.form.password,
        identified_check:"T",
        email:data.form.email
      }).then(res => {
        if (res.status === 201) {
          // ElMessage.success('注册成功')
          console.log(res.data)
          let tempid=res.data.id
            request.post('http://127.0.0.1:8000/teachers/',{
              'user':tempid,
              'gender':data.form.gender,
              'college':data.form.college.id,
            }).then(res=>{
              if(res.status==201) {
                ElMessage.success('新增成功')
                console.log('老师账号创建成功')
                load()    // 重新获取数据
                data.formVisible = false  // 关闭弹窗
              }
            })
        } else {
          ElMessage.error(res.msg)
        }
      }).catch(res=>{
        ElMessage.error(res.msg)
      })
      }
     }
   })
 }
 
 const handleEdit = (row) => {
   data.form = JSON.parse(JSON.stringify(row))
   add=1
   data.formVisible = true
 }
 
 const del = (id) => {
   ElMessageBox.confirm('删除数据后无法恢复，您确认删除吗？', '删除确认', { type: 'warning' }).then(res => {
     request.delete('/teachers/' + id + '/').then(res => {
       if (res.status === 204) {
         load()    // 重新获取数据
         ElMessage.success("删除成功")
       } else {
         ElMessage.error(res.msg)
       }
     })
   }).catch(res => {})
 }
 
 const handleImgUploadSuccess = (res) => {
   data.form.avatar = res.data
 }
 </script>