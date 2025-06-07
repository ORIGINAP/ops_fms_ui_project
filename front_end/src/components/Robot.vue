<template>
  <div class="black-box"></div>
</template>

<script setup>
    import { ref, onMounted, onBeforeUnmount } from 'vue'
    import axios from 'axios'
    import { io } from 'socket.io-client'

    const socket = io('http://localhost:5002')
    const robots = ref({})


    onMounted(() => {
      // 소켓 연결
      socket.on('connect', () => {
        console.log('소켓 연결 성공:', socket.id)
      })

      // 서버로부터 'robot' 이벤트 수신
      socket.on('robot_status_update', (data) => {
        robots.value = data
        console.log('로봇 데이터 수신:', data)
      })

      // 에러 핸들링
      socket.on('error', (error) => {
        console.error('소켓 에러:', error)
      })
    })

    onBeforeUnmount(() => {
      // 컴포넌트 언마운트 시 소켓 연결 해제
      socket.disconnect()
      console.log('소켓 연결 해제')
    })
    
</script>

<style scoped>
.black-box {
    position: fixed;
    top: 30px;
  right: 40px;
    width: 1000px;
    height: 1000px;
  background-color: black;
}
</style>
