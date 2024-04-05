import type { RouteRecordRaw } from 'vue-router';
import { PortalLayout } from '@kwai/ui';
import HomePage from '@root/pages/home/HomePage.vue';
import ClubToolbar from '@root/components/ClubToolbar.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: PortalLayout,
    children: [
      {
        name: 'club.home',
        path: '/',
        components: {
          toolbar: ClubToolbar,
          main: HomePage,
        },
        meta: {
          title: 'Home',
        },
      },
    ],
  },
];

export default routes;
