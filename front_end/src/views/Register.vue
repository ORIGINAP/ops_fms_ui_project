<template>
  <div class="login-container"> <!--로그인 css 재사용-->
    <h2>회원가입 페이지</h2> 
    <input v-model="username" placeholder="Your ID" />
    <input v-model="password" placeholder="Your PW" />
    <button @click="SendServer">가입</button>
  </div>
</template>

<script setup>
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'
    import axios from 'axios'

    const username = ref('')
    const password = ref('')
    const router = useRouter()

    const SendServer = async () => {
        
      
      try{
        const res = await axios.post('http://localhost:5000/register', {
            username : username.value,
            password : password.value
        })
        alert(res.data.message)
        router.push('/');
      } catch(err){
        if(err.response) {
          alert(err.response.data.message)
        } else {
          alert('gone wrong')
        }
      }
    
    
    
    
    }
</script>

<style scoped>
.login-container {
  width: 300px;
  margin: 100px auto;
  padding: 24px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f9f9f9;
  box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
}

.login-container h1 {
  text-align: center;
  margin-bottom: 20px;
}

.login-container label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.login-container input {
  width: 100%;
  padding: 8px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.login-container button {
  width: 100%;
  padding: 10px;
  background-color: #254081;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.login-container button:hover {
  background-color: #1e305d;
}
</style>