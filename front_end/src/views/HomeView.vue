<template>
  <div>
    <Status />
    <Map />
    <Menu />
    <AlertOverlay ref="alertOverlay" />
  </div>
</template>

<script>
import Status from '../components/Status.vue';
import Menu from '../components/Menu.vue';
import Map from '../components/Map.vue';
import AlertOverlay from '../components/AlertOverlay.vue';

export default {
  name: 'HomeView',
  components: {
    Status,
    Menu,
    Map,
    AlertOverlay,
  },
  provide() {
    return {
      activateAlert: (message) => {
        this.$refs.alertOverlay.activateAlert(message);
      }
    }
  }
};
</script>

<style>
html, body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: rgb(246,247,249,100);
}
</style>


/*
main-color(mid) : rgba(21,100,191,1)
menu : rgba(8,120,255,1)
중간색 : rgba(178,214,255,1)
제일연한색 : rgba(231,242,255,1)
진한 글씨색 : rgba(0,63,136,1)
중간 글씨색 : rgba(73,135,207,1)
배경색 : rgba(246,247,259,1)
*/