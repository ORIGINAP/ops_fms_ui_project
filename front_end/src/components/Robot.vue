<template>
  <div class="black-box"></div>
</template>

<script setup>
    import { ref, onMounted } from 'vue'
    import axios from 'axios'
    import { io } from 'socket.io-client'

    const socke = io('http://localhost:5002')
    const robots = ref({})


    onMounted(() => {
      // 소켓 연결
      socke.on('connect', () => {
        console.log('소켓 연결 성공:', socke.id)
      })

      // 서버로부터 'robot' 이벤트 수신
      socke.on('robot', (data) => {
        robots.value = data
        console.log('로봇 데이터 수신:', data)
      })

      // 에러 핸들링
      socke.on('error', (error) => {
        console.error('소켓 에러:', error)
      })
    })

    onBeforeUnmount(() => {
      // 컴포넌트 언마운트 시 소켓 연결 해제
      socke.disconnect()
      console.log('소켓 연결 해제')
    })

onMounted(async () => {
  try {
    // field 쿼리 파라미터로 name/version/description/robot 중 하나를 지정
    const response = await axios.get('http://localhost:5001/robotB', {
      params: {
        field: 'name'  // 또는 'version', 'description', 'robot'
      }
    })

    // text/plain 응답일 경우
    alert(response.data)

    // console로 응답 전체 확인
    console.log('응답 상태:', response.status)
    console.log('응답 헤더:', response.headers)
    console.log('응답 데이터:', response.data)

    } catch (error) {
        console.error('API 요청 실패:', error)
    }
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
