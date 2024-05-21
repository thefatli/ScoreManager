<template>
  <div>
    <div class="card" style="margin-bottom: 10px">
      <el-input style="width: 260px; margin-right: 10px" v-model="data.name" placeholder="请输入课程名称查询"
                :prefix-icon="Search"/>
      <el-input style="width: 260px; margin-right: 10px" v-model="data.no" placeholder="请输入课程编号查询"
                :prefix-icon="Search"/>
      <el-button type="primary" style="margin-left: 10px" @click="load">查询</el-button>
      <el-button type="info" @click="reset">重置</el-button>
    </div>

    <div class="card" style="margin-bottom: 10px">

      <div>
        <el-table :data="data.tableData" style="width: 100%">
          <el-table-column prop="id" label="序号" width="70"/>
          <el-table-column prop="course_name" label="课程名称"/>
          <el-table-column prop="course" label="课程编号"/>
          <el-table-column prop="score" label="成绩"/>
          <!-- <el-table-column label="操作" width="180">
            <template #default="scope">
              <el-button type="danger" @click="del(scope.row)">退选</el-button>
            </template>
          </el-table-column> -->
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
  name: '',
  no: '',
  tableData: [],
  total: 0,
  pageNum: 1,  // 当前的页码
  pageSize: 6,  // 每页的个数
  user: JSON.parse(localStorage.getItem('student-user') || '{}'),
})

const load = () => {
  request.get('/students/'+ me.id +'/courses/',{
    params: {
      page: data.pageNum,
      'results.id' :'data.name'}
    }).then(res => {
    if(res.status==200) {
      console.log('获取数据成功')
      console.log(res.data.results)
      console.log(res.data.results[0])
      console.log(res.data.results[4].score)
      data.total=res.data.count
      let j=0 
      for(let i=0;i<data.total;i++){
        if(res.data.results[i].score!=null){
          data.tableData[j] = res.data.results[i]
          j = j+1
        }
      }
      }
  })
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

</script>