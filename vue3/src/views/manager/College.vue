<template>
  <div>
     <div class="card" style="margin-bottom: 10px">
       <!-- <el-input style="width: 260px; margin-right: 10px" v-model="data.username" placeholder="请输入账号查询"
                 :prefix-icon="Search"/> -->
       <el-input style="width: 260px; margin-right: 10px" v-model="data.name" placeholder="请输入名称查询"
                 :prefix-icon="Search"/>
       <el-button type="primary" style="margin-left: 10px" @click=search()>查询</el-button>
       <el-button type="info" @click="reset">重置</el-button>
     </div>
 
     <div class="card" style="margin-bottom: 10px">
       <div style="margin-bottom: 10px">
         <el-button type="primary" @click="handleAdd">新增</el-button>
       </div>
 
       <div>
         <el-table :data="data.tableData" style="width: 100%">
           <el-table-column prop="name" label="学院名称"/>
           <el-table-column prop="id" label="学院编号"/>
           <el-table-column prop="description" label="学院描述"/>
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
 
     <el-dialog width="35%" v-model="data.formVisible" title="学院信息" destroy-on-close>
       <el-form :model="data.form" :rules="rules" ref="formRef" label-width="100px" label-position="right" style="padding-right: 40px">
         <el-form-item label="学院名称">
           <el-input v-model="data.form.name" autocomplete="off"/>
         </el-form-item>
         <el-form-item label="学院描述">
           <el-input v-model="data.form.description" autocomplete="off"/>
         </el-form-item>
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

 const data = reactive({
   name: '',
   tableData: [],
   total: 0,
   pageNum: 1,  // 当前的页码
   pageSize: 6,  // 每页的个数
   formVisible: false,
   form: {}
 })
 
 const load = () => {
   request.get('/colleges/', {
     params: {
       page: data.pageNum,
       //pageSize: data.pageSize,
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
   request.get('/colleges/?search='+ data.name).then(res => {
      // data.tableData = res.data?.list || []
      // data.total = res.data?.total || 0
      console.log(res.data)
      if(res.status==200){
      console.log(res.data)
      data.tableData = res.data.results
      data.total = res.data.count
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
 
 const handleAdd = () => {
   data.form = {}
   // data.form.name=' '
   data.formVisible = true
 }
 
 const save = () => {
   console.log(data.form)
    formRef.value.validate((valid) => {
      if (valid) {
        request.request({
          url: data.form.id ? '/colleges/' + data.form.id + '/' : '/colleges/',
          method: data.form.id ? 'PUT' : 'POST',
          data: {
           'name':data.form.name,
           'description':data.form.description,
          }
        }).then(res => {
          if (res.status === 200) {
           console.log(data.tableData)
            load()    // 重新获取数据
            data.formVisible = false  // 关闭弹窗
            ElMessage.success("编辑成功")
          }
          if (res.status==201) {
           console.log(data.tableData)
            load()    // 重新获取数据
            data.formVisible = false  // 关闭弹窗
            ElMessage.success("新增成功")
          }
        })
      }
    })
  }
 
 
 const handleEdit = (row) => {
   data.form = JSON.parse(JSON.stringify(row))
   data.formVisible = true
 }
 
 const del = (id) => {
   ElMessageBox.confirm('删除数据后无法恢复，您确认删除吗？', '删除确认', { type: 'warning' }).then(res => {
     request.delete('/colleges/' + id + '/').then(res => {
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