<template>
  <div>
    <Status />
    <Menu />
    <Map />
  </div>
</template>

<script>
import Status from '../components/Status.vue';
import Menu from '../components/Menu.vue';
import Map from '../components/Map.vue';

export default {
  name: 'HomeView',
  components: {
    Status,
    Menu,
    Map,
  },
};
</script>

<style>
html, body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: rgba(246,247,249,100);
}
</style>


/*
main-color(mid) : rgba(21,100,191,100)
sub-color(chart) : rgba(178,214,255,100)
제일연한색 : rgba(231,242,255,100)
글씨색 : rgba(73,135,207,100)
진한 글씨색 : rgba(0,63,136,100)
배경색 : rgba(246,247,259,100)

*/