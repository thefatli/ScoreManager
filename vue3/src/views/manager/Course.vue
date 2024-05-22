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
      <div style="margin-bottom: 10px">
        <el-button type="primary" @click="handleAdd">新增</el-button>
      </div>

      <div>
        <el-table :data="data.tableData" style="width: 100%">
          <el-table-column prop="name" label="课程名称"/>
          <el-table-column prop='id' label="课程编号"/>
          <!-- <el-table-column prop="id" label="课程编号"/> -->
          <el-table-column prop="point" label="课程学分"/>
          <el-table-column prop="time" label="课时"/>
          <el-table-column prop="grade" label="开设年级"/>
          <el-table-column prop="teacher_name" label="任课老师"/>
          <el-table-column prop="college_name" label="开设学院"/>
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

    <el-dialog width="35%" v-model="data.formVisible" title="课程信息">
      <el-form :model="data.form" label-width="100px" label-position="right" style="padding-right: 40px">
        <el-form-item label="课程名称">
          <el-input v-model="data.form.name" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="课程学分">
          <el-input v-model="data.form.point" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="课时">
          <el-input v-model="data.form.time" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="开设年级">
          <el-input v-model="data.form.grade" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="任课老师">
          <el-select v-model="data.form.teacher" clearable="" filterable>
            <el-option v-for="item in Teachers" :label="item.name" :value="item.id" :key="item.id"></el-option>
          </el-select>
         </el-form-item>
        <el-form-item label="开设学院">
          <el-select v-model="data.form.college" clearable="" filterable>
            <el-option v-for="item in Colleges" :label="item.name" :value="item.id" :key="item.id"></el-option>
          </el-select>
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
import {reactive} from "vue"
import {Search} from '@element-plus/icons-vue'
import request from "@/utils/request";
import {ElMessage, ElMessageBox} from "element-plus";
 
 let Colleges=[]
  request.get('/collegelist/').then(res=>{
  if(res.status==200) {
    console.log('获取学院信息成功')
    Colleges = res.data
  }
 })

 let Teachers=[]
 request.get('/teacherlist/').then(res=>{
  if(res.status==200) {
    console.log('获取老师信息成功')
    Teachers=res.data
    console.log(Teachers)
  }
 })

const data = reactive({
  name: '',
  // id: '',
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
      //id: data.id,
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

const handleAdd = () => {
  data.form = {}
  data.formVisible = true
}

//保存数据到后台
const save = () => {
  console.log(data.form)
  console.log(data.form.id)
       request.request({
         url: data.form.id ? '/courses/' + data.form.id + '/' : '/courses/',
         method: data.form.id ? 'PUT' : 'POST',
         data: {
          'name':data.form.name,
          'grade':data.form.grade,
          'time':data.form.time,
          'point':data.form.point,
          'college':data.form.college,
          'teacher':data.form.teacher,
         }
       }).then(res => {
         if (res.status === 200 || res.status==201) {
          console.log(data.tableData)
           load()    // 重新获取数据
           data.formVisible = false  // 关闭弹窗
           ElMessage.success("操作成功")
         } else {
           ElMessage.error(res.msg)
         }
       })
 }



const handleEdit = (row) => {
  data.form = JSON.parse(JSON.stringify(row))
  data.formVisible = true
}

const del = (id) => {
  ElMessageBox.confirm('删除数据后无法恢复，您确认删除吗？', '删除确认', { type: 'warning' }).then(res => {
    request.delete('/courses/' + id + '/').then(res => {
      if (res.status === 204) {
        load()    // 重新获取数据
        ElMessage.success("操作成功")
      } else {
        ElMessage.error('操作失败')
      }
    })
  }).catch(res => {})
}
</script>