import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import axios from 'axios'

createApp(App).use(router).mount('#app')
// 예: Vue 프로젝트의 main.js 또는 axios.js
axios.defaults.withCredentials = true;

