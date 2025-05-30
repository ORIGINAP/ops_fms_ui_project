<template>
  <div class="body">
    <p>SystemPage</p>
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
  top: 40px;
  left: 40px;

  width: 89%;
  height: 92%;
  box-shadow: 3px 3px 7px rgba(21,100,191, 0.13);
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 30px;
}

</style>