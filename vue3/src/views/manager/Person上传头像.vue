<template>
  <div>
    <input type="file" @change="uploads">  
    <p></p>
    <img :src="imgUrl" v-if="imgUrl">
  </div>
</template>

<script>
import axios from 'axios';
import request from '../../utils/request';

export default {
  data() {
    return {
      imgUrl: null,
      file: null,
      token: null,
    };
  },
  created() {
    const user = JSON.parse(localStorage.getItem('student-user') || '{}');
    request.post('/auth/jwt/create/', { 
      username: user.username,
      password: user.password
    }).then(res => {
      if (res.status === 200) {
        this.token = res.data.access;
      }
    }).catch(err => {
      console.error('Error fetching token:', err);
    });
  },
  methods: {
    uploads(e) {
      const file = e.target.files[0];
      this.file = file;
      this.imgUrl = URL.createObjectURL(file);

      if (this.file) {
        const formData = new FormData();
        formData.append('image', this.file);

        axios.put('http://localhost:8000/user/update/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `JWT ${this.token}`,
          }
        }).then(res => {
          console.log('上传文件');
          console.log(res);
          alert('更新成功!');
        }).catch(err => {
          console.error(err);
          alert('更新失败: ' + err.message);
        });
      }
    },
  },
};
</script>

<style scoped>
/* Add any necessary styles here */
</style>
