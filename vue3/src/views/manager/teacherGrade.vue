<template>
  <div>
    <div class="card" style="margin-bottom: 10px">
      <el-input style="width: 260px; margin-right: 10px" v-model="data.courseName" placeholder="请输入课程名称查询"
                :prefix-icon="Search"/>
      <el-button type="primary" style="margin-left: 10px" @click=search()>查询</el-button>
      <el-button type="info" @click="reset">重置</el-button>
    </div>
    <div class="card" style="margin-bottom: 10px">

      <div>
        <el-table :data="data.tableData" style="width: 100%" height="350">
    <el-table-column type="expand">
      <template #default="props">
        <div m="4">
          <el-table :data="props.row.items" :default-sort="{ prop: 'score', order: 'descending' }" >
            <el-table-column label="学生姓名" prop="student_name" />
            <el-table-column label="学生学号" prop="student" />
            <el-table-column label="学生成绩" prop="score" sortable width="180"/>
            <el-table-column label="操作" width="180">
            <template #default="scope">
              <el-button type="primary" @click="handleEdit(scope.row)" >打分</el-button>
              <el-button type="danger" @click="delstudent(scope.row)" >删除</el-button>
            </template>
            </el-table-column>
          </el-table>
        </div>
        </template>
        </el-table-column>
        <el-table-column label="课程名称" prop="name" />
        <el-table-column label="课程编号" prop="id" />
        <el-table-column label="平均成绩" prop="avg_score" />
        </el-table>
      </div>

    </div>

    <div class="card">
      <el-pagination v-model:current-page="data.pageNum" v-model:page-size="data.pageSize"
                     @current-change="handelCurrentChange"
                     background layout="prev, pager, next" :total="data.total"/>
    </div>

    <el-dialog width="35%" v-model="data.formVisible" title="打分">
      <el-form :model="data.form" label-width="100px" label-position="right" style="padding-right: 40px">
        <el-form-item label="课程名称">
          <el-input v-model="data.form.course_name" autocomplete="off" disabled/>
        </el-form-item>
        <el-form-item label="学生姓名">
          <el-input v-model="data.form.student_name" autocomplete="off" disabled/>
        </el-form-item>
        <el-form-item label="成绩">
          <el-input v-model="data.form.score" autocomplete="off" placeholder="请输入分数" />
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

let me = {
  id:0,
  name:' ',
}

  request.get('/me/').then(res => {
  if (res.status === 200) {
    console.log('获取个人信息成功')
    me.id=res.data.id
    me.name=res.data.name
    console.log(me.name)
    console.log(me.id)
    load()
  } else {
    ElMessage.error('获取个人信息失败')
    console.log(res.status)
  }
})

const data = reactive({
  form: {},
  courseName: '',
  studentName: '',
  tableData: [],
  tableData2: [],
  total: 0,
  pageNum: 1,  // 当前的页码
  pageSize: 6,  // 每页的个数
  user: JSON.parse(localStorage.getItem('student-user') || '{}'),
  formVisible: false
})

const load = () => {
  request.get('/teachers/'+ me.id +'/courses/',{
    params: {
      page: data.pageNum,
      //'results.id' :'data.name'
    }
    }).then(res => {
    if(res.status==200) {
      console.log('获取老师课程数据成功')
      console.log(res.data.results)
      console.log(res.data.results[0].items)
      data.tableData=res.data.results
      data.total=res.data.count
      let a=res.data.count
      let j=0
      for(let i=0;i<a;i++)
      {
        for(let k=0;k<res.data.results[i].items.length;k++){
          data.tableData2[j] = res.data.results[i].items[k]
          j++}
      }
      data.total=res.data.count
      console.log(data.tableData)
      console.log(data.tableData[0].items)
      console.log(data.tableData2)
    }
  })
}

const search = () => {
    console.log(data.name)
          request.get('teachers/'+me.id+'/courses/?search='+ data.courseName).then(res=>{
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
  data.courseName = ''
  data.studentName = ''
  load()
}

const del = (id) => {
  ElMessageBox.confirm('删除数据后无法恢复，您确认删除吗？', '删除确认', { type: 'warning' }).then(res => {
    request.delete('/grade/delete/' + id).then(res => {
      if (res.code === '200') {
        load()    // 重新获取数据
        ElMessage.success("操作成功")
      } else {
        ElMessage.error(res.msg)
      }
    })
  }).catch(res => {})
}

// 打分
const handleEdit = (row) => {
  data.form = JSON.parse(JSON.stringify(row))  // 拷贝行数据到表单对象
  data.formVisible = true
}

const save = () => {
  request.put('/students/'+data.form.student+'/courses/'+data.form.id+'/', {
    score:data.form.score
  }).then(res => {
    if (res.status === 200) {
      load()
      data.formVisible = false  // 关闭弹窗
      ElMessage.success("打分成功")
    } else {
      ElMessage.error(res.msg)
    }
  })
}

const delstudent=(row)=>{
  ElMessageBox.confirm('删除数据后无法恢复，您确认删除吗？', '删除确认', { type: 'warning' }).then(res => {
    console.log('删除学生')
      if(row.score==null){
        console.log(row)
      request.delete('/students/' + row.student + '/courses/' + row.id +'/').then(res => {
      if (res.status === 204) {
        load()    // 重新获取数据
        ElMessage.success("删除学生成功")
      } else {
        ElMessage.error(res.msg)
      }})
    }
    else{
      ElMessage.error('已有成绩的学生无法删除')
    }
  }).catch(res=>{})
}
</script>