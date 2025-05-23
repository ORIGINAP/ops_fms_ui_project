<template>
  <div class="menu-bar">
    <!-- 글씨 -->
    <div class="str">
      <p>WELCOME TO OUR FACTORY!</p>
    </div>
  </div>
</template>

<script>
export default {

};
</script>

<style scoped>
.menu-bar {
  position: fixed;
  top: 30px;
  right: 40px;
  width: 120px;
  height: calc(100vh - 60px);

  background-color: rgba(21,100,191,100);
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);

  display: flex;
  border-radius: 20px;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.str {
  position: fixed;
  top: 50px;
  right: 11%;
  height: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 40px;
  font-weight: bold;
  color: rgba(0,63,136,100);
}

</style>
