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
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const email = ref('');
const password = ref('');

const handleLogin = () => {
  console.log('로그인 시도:', email.value, password.value);

  if (!email.value || !password.value) {
    alert('이메일과 비밀번호를 입력하세요.');
    return;
  }

  if (email.value === 'admin@example.com' && password.value === '1234') {
    console.log('로그인 성공!');
  } else {
    alert('로그인 실패!');
  }
};
</script>