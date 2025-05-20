<template>
  <div>
    <h2>회원가입 페이지</h2> <!--css 하면서 여기도 수정해 주세요-->
    <input v-model="username" placeholder="Your ID" />
    <input v-model="password" placeholder="Your PW" />
    <button @click="register">가입</button>
  </div>
</template>

<script setup>
</script>