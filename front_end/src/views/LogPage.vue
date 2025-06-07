<template>
  <div class="body">
    <p>LogPage</p>
    <Menu />
  </div>

</template>

<script>
import Menu from "../components/Menu.vue";

export default {
  name: 'LogPage',
  components: {Menu},
};
</script>

<style scoped>

.body {
  position: fixed;
  top: 35px;
  left: 41px;

  width: 90%;
  height: 92%;
  box-shadow: 2px 0 5px rgba(21,100,191,0.2);
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius:10px;
}

</style>