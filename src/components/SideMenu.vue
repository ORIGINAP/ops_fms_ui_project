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

      <!-- 세 번째 줄: 로그 저장 페이지 -->
      <div class="menu-row">
        <div class="menu-item menu-log_page">
          <p>로그 저장 설정</p>
        </div>
      </div>

      <!-- 네 번째 줄: 동선 수정 페이지 -->
      <div class="menu-row">
        <div class="menu-item menu-fix_page">
          <p>로봇 동선 수정</p>
        </div>
      </div>

      <!-- 다섯 번째 줄: 시스템 설정 페이지 -->
      <div class="menu-row">
        <div class="menu-item menu-system_page">
          <p>시스템 설정</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SideMenu',
}
</script>

<style scoped>
.side-menu {
  position: fixed;
  top: 0;
  right: 0;
  width: 20%;
  height: 95.8%;
  background-color: rgba(105, 181, 232, 1);
  margin: 0;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
  z-index: 50;
  padding: 20px;
  display: flex;
  flex-direction: column;
  border-top-left-radius: 20px;
  border-bottom-left-radius: 20px;
}

.menu-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.menu-row {
  display: flex;
  gap: 10px;
}

.menu-network {
  background-color: #f0f0f0;
  height: 300px;
  border-radius: 8px;
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  color: darkgray;
}

.menu-temperature {
  background-color: #f0f0f0;
  height: 200px;
  border-radius: 8px;
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  color: darkgray;
}

/* 공통 스타일 */
.menu-item {
  background-color: #f0f0f0;
  height: 50px;
  border-radius: 8px;
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  color: darkgray;
}

/* 개별 */
.menu-log_page {
  margin-top: 60px;
}

.menu-fix_page,
.menu-system_page {
  margin-top: 8px;
}
</style>
