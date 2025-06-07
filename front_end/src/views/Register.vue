<template>
  <div class="login-container">
    <h2>{{ $t('register.title') }}</h2>
    <input v-model="email" :placeholder="$t('register.email')" />
    <input v-model="password" :placeholder="$t('register.password')" />
    <button @click="SendServer">{{ $t('register.registerButton') }}</button>
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

const SendServer = async () => {
  if (!email.value || !password.value) {
    alert(t('register.allFieldsRequired'));
    return;
  }

  // 이메일 형식 검증
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email.value)) {
    alert(t('register.invalidEmail'));
    return;
  }

  try {
    const res = await axios.post('http://localhost:5000/register', {
      email: email.value,
      password: password.value
    });
    alert(res.data.message);
    router.push('/login');
  } catch (err) {
    if (err.response) {
      alert(err.response.data.message);
    } else {
      alert('gone wrong');
    }
  }
};
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