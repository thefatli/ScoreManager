<template>
  <div>
    <div class="card" style="margin-bottom: 10px">
      <el-input style="width: 260px; margin-right: 10px" v-model="data.name" placeholder="请输入课程名称查询"
                :prefix-icon="Search"/>
      <el-button type="primary" style="margin-left: 10px" @click=search()>查询</el-button>
      <el-button type="info" @click="reset">重置</el-button>
    </div>

    <div class="card" style="margin-bottom: 10px">

      <div>
        <el-table :data="data.tableData" style="width: 100%"
        :default-sort="{ prop: 'score', order: 'descending' }">
          <!-- <el-table-column prop="id" label="序号" width="70"/> -->
          <el-table-column prop="course_name" label="课程名称" v-if="data.user.role=='S'"/>
          <el-table-column prop="name" label="课程名称" v-if="data.user.role=='T'"/>
          <el-table-column prop="id" label="课程编号" v-if="data.user.role=='T'"/>
          <el-table-column prop="course" label="课程编号" v-if="data.user.role=='S'"/>
          <el-table-column label="课堂成员" v-if="data.user.role=='T'">
            <template #default="scope">
              <el-button :type="info" text @click="Seesl(scope.row)" v-if="data.user.role === 'T'">查看学生名单</el-button>
            </template>
          </el-table-column>
          <el-table-column prop="grade" label="开设年级" v-if="data.user.role=='T'"/>
          <el-table-column prop="avg_score" label="平均成绩" v-if="data.user.role=='T'"/>
          <el-table-column prop="score" label="课程成绩" v-if="data.user.role=='S'" sortable/>
          <el-table-column label="操作" width="180">
            <template #default="scope">
              <el-button type="danger" @click="del(scope.row)" v-if="data.user.role === 'S'">退选</el-button>
              <el-button type="primary" @click="addstudent(scope.row)" v-if="data.user.role === 'T'">添加</el-button>
              <el-button type="danger" @click="del(scope.row)" v-if="data.user.role === 'T'">删除</el-button>
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

    <el-dialog width="35%" v-model="data.formVisible2" title="课堂学生名单">
      <el-table :data="data.slist.items" style="width: 100%">
          <el-table-column prop="student" label="学生学号"/>
          <el-table-column prop="student_name" label="学生姓名"/>
          <el-table-column prop="score" label="学生成绩"/>
          <el-table-column label="操作" width="100">
            <template #default="scope">
              <el-button type="danger" @click="delstudent(scope.row)">删除</el-button>
            </template>
          </el-table-column>
      </el-table>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="data.formVisible2 = false">取 消</el-button>
          <el-button type="primary" @click="save">保 存</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog width="35%" v-model="data.formVisible" title="添加学生">
      <el-form :model="data.gradeForm" label-width="100px" label-position="right" style="padding-right: 40px">
        <el-form-item label="课程名称">
          <el-input v-model="data.gradeForm.name" autocomplete="off" disabled />
        </el-form-item>
        <el-form-item label="添加学生">
          <el-select v-model="data.gradeForm.student" clearable=""  filterable  placeholder="请搜索或下拉选择学生">
            <el-option v-for="item in Students" :label="item.name" :value="item.id" :key="item.id"></el-option>
          </el-select>
        </el-form-item>
        <!-- <el-form-item label="分数">
          <el-input v-model="data.gradeForm.score" autocomplete="off" />
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

 let Students=[]
 request.get('/studentlist/').then(res=>{
  if(res.status==200) {
    console.log('获取学生信息成功')
    Students=res.data
    console.log(Students)
  }
 })

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

let add=0   //设置保存按钮的类型
//add=1 新建课程

const data = reactive({
  name: '',
  no: '',
  tableData: [],
  total: 0,
  pageNum: 1,  // 当前的页码
  pageSize: 6,  // 每页的个数
  user: JSON.parse(localStorage.getItem('student-user') || '{}'),
  gradeForm: {},
  slist:{},
  formVisible: false
})

const load = () => {
  if (data.user.role === 'S') {  // 如果当前登录的是学生，那就查询自己的选课记录
  request.get('/students/'+ me.id +'/courses/',{
    params: {
      page: data.pageNum,
      //'results.id' :'data.name'
    }
    }).then(res => {
    if(res.status==200) {
      console.log('获取数据成功')
      console.log(res.data.results)
      data.tableData = res.data.results
      data.total=res.data.count}
  })
}
  else{
    request.get('/teachers/'+ me.id +'/courses/',{
    params: {
      page: data.pageNum,
      //'results.id' :'data.name'
    }
    }).then(res => {
    if(res.status==200) {
      console.log('获取数据成功')
      console.log(res.data.results)
      data.tableData = res.data.results
      data.total=res.data.count}
  })
  }
}
// 调用方法获取后台数据
// load()


const search=()=>{
  if(data.user.role=='T') {
   console.log(data.name)
   request.get('/teachers/'+me.id+'/courses/'+'?search='+ data.name).then(res => {
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
  else{ 
    console.log(data.name)
   request.get('/students/'+me.id+'/courses/'+'?search='+ data.name).then(res => {
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
  }


const handelCurrentChange = () => {
  // 当翻页的时候重新加载数据即可
  load()
}

const reset = () => {
  data.name = ''
  data.no = ''
  load()
}

const del = (row) => {
  console.log(row)
  ElMessageBox.confirm('删除数据后无法恢复，您确认删除吗？', '删除确认', { type: 'warning' }).then(res => {
    if(data.user.role === 'S'){
      console.log('学生删除')
      if(row.score==null){
      request.delete('/students/' + me.id + '/courses/' + row.id + '/').then(res => {
      if (res.status === 204) {
        load()    // 重新获取数据
        ElMessage.success("退选课程成功")
      } else {
        ElMessage.error(res.msg)
      }
    })
    }
    else{
      ElMessage.error('已有成绩的课程无法退课')
    }
    }
    else{
      console.log('老师删除')
      if(row.avg_score==null){
      request.delete('/teachers/' + me.id + '/courses/' + row.id +'/').then(res => {
      if (res.status === 204) {
        load()    // 重新获取数据
        ElMessage.success("删除课程成功")
      } else {
        ElMessage.error(res.msg)
      }
    })
    }
    else{
      ElMessage.error('已有成绩的课程无法删除')
    }
    }
  }).catch(res => {})
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
        data.formVisible2=false
        load()
      } else {
        ElMessage.error(res.msg)
      }})
    }
    else{
      ElMessage.error('已有成绩的学生无法删除')
    }
  }).catch(res=>{})
}


const addstudent = (row) => {
  // 添加学生
  add=1
  data.formVisible = true
  console.log(row)
  data.gradeForm.name = row.name
  data.gradeForm.id = row.id
}

const Seesl = (row) => {
  // 学生名单
  data.formVisible2 = true
  data.slist.name = row.name
  data.slist.items = row.items
}

const save = () => {
  if(add==0) { } //查看学生名单中的保存 无任何操作
  if(add==1) {  //为课程添加学生，也可同时添加分数
  request.post('/students/'+data.gradeForm.student+'/courses/', 
  {course:data.gradeForm.id}).then(res => {
    if (res.status == 201) {
      ElMessage.success("添加学生成功")
      // if(score!=null)  {
      //   request.post('/students/'+data.gradeForm.student+'/courses/'+data.form.course+'/', {
      //   score:data.form.score
      //   }).then(res => {
      //   if (res.status === '201') {
      //   } else {
      //     ElMessage.error('打分失败')
      //   }})
      // }
      load()  // 重新获取数据
      data.formVisible = false  // 关闭弹窗
    }
  }).catch(err=>{
    ElMessage.error('该学生已在课堂中')
  })
   } 
  // request.post('/grade/add', data.gradeForm).then(res => {
  //   if (res.code === '200') {
  //     data.formVisible = false  // 关闭弹窗
  //     ElMessage.success("操作成功")
  //   } else {
  //     ElMessage.error(res.msg)
  //   }
  // })
}
</script>