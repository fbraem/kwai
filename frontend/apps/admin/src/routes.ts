import type { RouteRecordRaw } from 'vue-router';
import { PortalLayout } from '@kwai/ui';
import HomePage from '@root/pages/home/HomePage.vue';
import NotAllowedPage from '@root/pages/not_allowed/NotAllowedPage.vue';
import AdminToolbar from '@root/components/AdminToolbar.vue';
import UsersPage from '@root/pages/users/UsersPage.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: PortalLayout,
    children: [
      {
        name: 'admin.home',
        path: '/',
        components: {
          toolbar: AdminToolbar,
          main: HomePage,
        },
        meta: { title: 'Home' },
      },
      {
        name: 'admin.not_allowed',
        path: '/not_allowed',
        components: {
          toolbar: AdminToolbar,
          main: NotAllowedPage,
        },
        meta: { requiresAuth: false },
      },
      {
        name: 'admin.users',
        path: '/',
        components: {
          toolbar: AdminToolbar,
          main: UsersPage,
        },
      },
    ],
  },
];

export default routes;
