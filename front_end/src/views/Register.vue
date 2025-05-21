<template>
  <div>
    <h2>회원가입 페이지</h2> <!--css 하면서 여기도 수정해 주세요-->
    <input v-model="username" placeholder="Your ID" />
    <input v-model="password" placeholder="Your PW" />
    <button @click="SendServer">가입</button>
  </div>
</template>

<script setup>
    import { ref } from 'vue'
    import axios from 'axios'

    const username = ref('')
    const password = ref('')

    const SendServer = async () => {
        
      
      try{
        const res = await axios.post('http://localhost:5000/register', {
            username : username.value,
            password : password.value
        })
        alert(res.data.message)
      } catch(err){
        if(err.response) {
          alert(err.response.data.message)
        } else {
          alert('gone wrong')
        }
      }
    
    
    
    
    }
</script>