import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import i18n from './i18n'
import axios from 'axios'

const app = createApp(App)
app.use(router)
app.use(i18n)
app.mount('#app')
// 예: Vue 프로젝트의 main.js 또는 axios.js
axios.defaults.withCredentials = true;

