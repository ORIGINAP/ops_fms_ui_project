<template>
  <div class="side-menu">
    <!-- 메뉴 내용 -->
    <div class="menu-body">
      <!-- 첫 번째 줄: 네트워크 -->
      <div class="menu-row">
        <div class="menu-network">
          <p>network</p>
        </div>
      </div>

      <!-- 두 번째 줄: 온도 -->
      <div class="menu-row">
        <div class="menu-temperature">
          <p>외부 온도</p>
        </div>
        <div class="menu-temperature">
          <p>내부 온도</p>
        </div>
      </div>

      <!-- 세 번째 줄: 미정상태 -->
      <div class="menu-row">
        <div class="menu-other">
          <p>other</p>s
        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'Status',
}
</script>

<style scoped>
.side-menu {
  position: fixed;
  top: 80px;
  right: 160px;
  width: 23%;
  height: 93%;
  margin: 0;
  z-index: 50;
  padding: 20px;
  display: flex;
  flex-direction: column;
  border-radius: 20px;
}

.menu-body {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.menu-row {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.menu-network {
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  background-color: white;
  height: 300px;
  border-radius: 20px;
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  color: darkgray;
}

.menu-temperature {
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  background-color: white;
  height: 220px;
  border-radius: 20px;
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  color: darkgray;
}

.menu-other {
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  background-color: white;
  height: 250px;
  border-radius: 20px;
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  color: darkgray;
}
</style>