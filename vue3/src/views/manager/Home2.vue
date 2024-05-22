<template>
  <!-- 初始版本 -->
  <div>
    <div class="card" style="line-height: 30px">
      <div>欢迎您，<span style="color: dodgerblue;">{{ user.username }}</span> 祝您今天过得开心！</div>
    </div>

  </div>
</template>

<script setup>
  import request from "@/utils/request";
  const user = JSON.parse(localStorage.getItem('student-user') || '{}')
  request.get('/me/').then(res => {
    if (res.status === 200) {
      console.log('获取个人信息成功')
      console.log(res.data)
    } else {
      ElMessage.error('获取个人信息失败')
      console.log(res.status)
    }
  })
</script>