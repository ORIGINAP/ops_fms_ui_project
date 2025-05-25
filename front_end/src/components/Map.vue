<template>
  <div class="map">
    <p>맵 자리</p>
  </div>

</template>

<script>
export default {
  name: 'Map',
};
</script>

<style scoped>

.map {
  position: fixed;
  top: 40px;
  left: 40px;

  width: 1205px;
  height: 870px;
  box-shadow: 3px 3px 7px rgba(21,100,191, 0.13);
  background-color: white;
  display: flex;


  justify-content: center;
  align-items: center;
  border-radius: 30px;
  font-size: 30px;
  color: #333;
  box-sizing: border-box;
}

</style>
