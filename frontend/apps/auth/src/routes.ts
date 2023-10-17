import type { RouteRecordRaw } from 'vue-router';
import IndexPage from './pages/IndexPage.vue';
import HomePage from './pages/HomePage.vue';
import LoginPage from './pages/LoginPage.vue';
import InvitedPage from './pages/InvitedPage.vue';
import ChangePasswordPage from './pages/ChangePasswordPage.vue';
import RecoverPasswordPage from './pages/RecoverPasswordPage.vue';
import ResetPasswordPage from './pages/ResetPasswordPage.vue';

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: IndexPage,
    children: [
      {
        name: 'home',
        path: '/',
        component: HomePage,
      },
      {
        name: 'change',
        path: '/change',
        component: ChangePasswordPage,
      },
      {
        name: 'login',
        path: '/login',
        component: LoginPage,
      },
      {
        name: 'invited',
        path: '/invited',
        component: InvitedPage,
      },
      {
        name: 'recover',
        path: '/recover',
        component: RecoverPasswordPage,
      },
      {
        name: 'reset',
        path: '/reset',
        component: ResetPasswordPage,
      },
    ],
  },
];
