<template>
  <div class="main-container">

    <!-- 맵 들어갈 자리 -->
    <div class="map">
      <p>맵</p>
    </div>

    <!-- 사이드 패널 -->
    <SideMenu :visible="menuVisible" @close="menuVisible = false" />
  </div>
</template>

<script>
import SideMenu from '@/components/SideMenu.vue'

export default {
  name: 'MainPage',
  components: { SideMenu },
  data() {
    return {
      menuVisible: false,
    }
  }
}

</script>

<style scoped>
.main-container {
  position: relative;
  height: 100vh;
  background-color: white; /* 배경 흰색 */
  overflow: hidden;
}

/* 맵 자리 */
.map {
  width: calc(100% - 25% - 70px); /* 전체 너비에서 사이드메뉴 너비(25%)와 여유 공간 빼기 */
  height: 90%;
  background-color: #dddddd;
  margin: 45px 20px 20px 60px; /* 상, 우, 하, 좌 */
  border: 2px dashed #aaa;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 30px;
  color: #333;
  box-sizing: border-box;
}

</style>