import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/LoginPage.vue';
import HomeView from '../views/HomeView.vue'
import Register from '../views/Register.vue';

//여기서 라우터 설정을 하시면 됩니다.
const routes = [
  { path: '/', name: 'Login', component: Login },
  { path: '/main', name: 'home', component: HomeView },
  { path: '/register', name: 'register', component: Register },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
