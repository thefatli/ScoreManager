<template>
  <div>
    <div class="card" style="margin-bottom: 10px">
      <el-input style="width: 260px; margin-right: 10px" v-model="data.name" placeholder="请输入课程名称/学院/老师查询"
                :prefix-icon="Search"/>
      <!-- <el-input style="width: 260px; margin-right: 10px" v-model="data.college_name" placeholder="请输入开设学院查询"
                :prefix-icon="Search"/>
      <el-input style="width: 260px" v-model="data.teacher_name" placeholder="请输入任课老师查询" :prefix-icon="Search"/> -->
      <el-button type="primary" style="margin-left: 10px" @click=search()>查询</el-button>
      <el-button type="info" @click="reset">重置</el-button>
    </div>

    <div class="card" style="margin-bottom: 10px">
      <div>
        <el-table :data="data.tableData" style="width: 100%">
          <el-table-column prop='id' label="序号" width="70"/>
          <el-table-column prop="name" label="课程名称"/>
          <!-- <el-table-column prop="id" label="课程编号"/> -->
          <el-table-column prop="point" label="课程学分"/>
          <el-table-column prop="time" label="课时"/>
          <el-table-column prop="grade" label="开设年级"/>
          <el-table-column prop="teacher_name" label="任课老师"/>
          <el-table-column prop="college_name" label="开设学院"/>
          <el-table-column label="操作" width="180">
            <template #default="scope">
            <el-button type="primary" @click="selectCourse(scope.row)">选课</el-button>
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
  </div>
</template>

<script setup>
import {reactive} from "vue"
import {Search} from '@element-plus/icons-vue'
import request from "@/utils/request";
import {ElMessage, ElMessageBox} from "element-plus";

const datac = reactive({
   name: '',
   tableData: [],
   total: 0,
   pageNum: 1,  // 当前的页码
   pageSize: 6,  // 每页的个数
 })
 

 let Teachers=[]
 request.get('/teachers/').then(res=>{
  if(res.status==200) {
    console.log('获取老师信息成功')
    Teachers=res.data.results
    console.log(Teachers)
  }
 })

let me={ }

  request.get('/me/').then(res => {
    if (res.status === 200) {
      console.log('获取个人信息成功')
      console.log(res.data)
      me=res.data
      console.log(me)
    } else {
      ElMessage.error('获取个人信息失败')
      console.log(res.status)
    }
  })

const data = reactive({
  name: '',
  id: '',
  teacher_name: '',
  college_name: '',
  tableData: [],
  total: 0,
  pageNum: 1,  // 当前的页码
  pageSize: 6,  // 每页的个数
  formVisible: false,
  form: {}
})

const load = () => {
  request.get('/courses/',{
    params: {
      page: data.pageNum,
      // count: data.pageSize,
      name: data.name,
      id: data.id,
      teacher_name: data.teacher_name,
    }
  }).then(res => {
    if(res.status==200) {
      console.log(res.data)
      console.log(res.status)
      data.tableData = res.data.results
      data.total = res.data.count
      console.log(data.tableData)
      console.log(data.total)
    }
    else console.log(res.msg)
  })
}

load()

const search = () => {
    console.log(data.name)
          request.get('/courses/?search='+ data.name).then(res=>{
          if(res.status==200){
          console.log('查询成功')
          data.tableData = res.data.results
          data.total = res.data.results.length}})
}


const handelCurrentChange = () => {
  // 当翻页的时候重新加载数据即可
  load()
}

const reset = () => {
  data.name = ''
  // data.id = ''
  data.teacher_name = ''
  data.college_name = ''
  load()
}

const selectCourse = (row) => {
  console.log(row)
  if(row.grade==me.grade){
  request.post('/students/'+me.id+'/courses/', {course:row.id}).then(res => {
    if (res.status === 201) {
      ElMessage.success("选课成功")
    } else {
      ElMessage.error('请勿重复选课')
    }
  }).catch(err=>{
    ElMessage.error('请勿重复选课')
  })
}
else{
  ElMessage.error('该课程只能'+row.grade+'年级学生选择')
}
}
</script>

