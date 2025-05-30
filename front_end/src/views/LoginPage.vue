<template>
  <div class="login-container">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label>Email:</label>
        <input v-model="email" type="email" required />
      </div>
      <div>
        <label>Password:</label>
        <input v-model="password" type="password" required />
      </div>
      <button type="submit">Login</button>
      <button @click="GotoRegister">Register</button>
    </form>
  </div>

</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const email = ref('');
const password = ref('');
const router = useRouter();

const handleLogin = async () => {
  console.log('로그인 시도:', email.value, password.value);

  if (!email.value || !password.value) {
    alert('이메일과 비밀번호를 입력하세요.');
    return;
  }
  try {
    const res = await axios.post('http://localhost:5000/login', {
      username: email.value,
      password: password.value,
    });
    alert(res.data.message); 
    router.push('/main');
  } catch (err) {
    if (err.response) {
      alert(err.response.data.message);
    } else {
      alert('gone wrong');
    }
  }
  

};

const GotoRegister = () => {
  router.push('/register');
  return;
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
  width: 95%;
  padding: 8px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.login-container button {
  width: 100%;
  margin-top: 15px;
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