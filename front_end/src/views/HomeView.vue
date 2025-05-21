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
import SideMenu from '../components/SideMenu.vue'

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
}

/* 맵 자리 */
.map {
  position: absolute;
  inset: 50px; /* top, bottom, left가 20px로 설정됨 */
  right: calc(25%);
  background-color: #dddddd;
  border: 2px dashed #aaa;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 30px;
  color: #333;
  box-sizing: border-box;
  z-index: 1; /* 사이드메뉴보다 아래로 */
}

</style>