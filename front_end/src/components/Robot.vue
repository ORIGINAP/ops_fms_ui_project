<template>
  <div class="black-box"></div>
</template>

<script setup>
    import { ref, onMounted } from 'vue'
    import axios from 'axios'
// 특별한 JS 로직은 필요 없습니다
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
