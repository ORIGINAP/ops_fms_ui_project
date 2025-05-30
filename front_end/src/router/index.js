import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/LoginPage.vue';
import HomeView from '../views/HomeView.vue'
import Register from '../views/Register.vue';
import LogPage from '../views/LogPage.vue';
import RoutePage from '../views/RoutePage.vue';
import SystemPage from '../views/SystemPage.vue';

//여기서 라우터 설정을 하시면 됩니다.
const routes = [
  { path: '/', name: 'Login', component: HomeView },
  { path: '/main', name: 'home', component: HomeView },
  { path: '/register', name: 'register', component: Register },
  { path: '/LogPage', name: 'LogPage', component: LogPage },
  { path: '/RoutePage', name: 'RoutePage', component: RoutePage },
  { path: '/SystemPage', name: 'SystemPage', component: SystemPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
