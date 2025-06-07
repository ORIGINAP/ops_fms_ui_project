<template>
  <div class="login-container">
    <h1>{{ $t('login.title') }}</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label>{{ $t('login.email') }}:</label>
        <input v-model="email" type="email" required />
      </div>
      <div>
        <label>{{ $t('login.password') }}:</label>
        <input v-model="password" type="password" required />
      </div>
      <button type="submit">{{ $t('login.loginButton') }}</button>
      <button @click="GotoRegister">{{ $t('login.registerButton') }}</button>
    </form>
  </div>

</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import axios from 'axios';

const { t } = useI18n();
const email = ref('');
const password = ref('');
const router = useRouter();

const handleLogin = async () => {
  console.log('로그인 시도:', email.value, password.value);

  if (!email.value || !password.value) {
    alert(t('login.emailRequired'));
    return;
  }
  try {
    const res = await axios.post('http://localhost:5000/login', {
      email: email.value,
      password: password.value,
    }, 
    {
      withCredentials: true
    });
    alert(t('login.loginSuccess')); 
    router.push('/main');
  } catch (err) {
    if (err.response) {
      alert(err.response.data.message);
    } else {
      alert(t('login.error'));
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