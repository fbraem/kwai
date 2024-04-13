import type { RouteRecordRaw } from 'vue-router';
import { PortalLayout } from '@kwai/ui';
import HomePage from '@root/pages/home/HomePage.vue';
import NotAllowedPage from '@root/pages/not_allowed/NotAllowedPage.vue';
import MembersPage from '@root/pages/members/MembersPage.vue';
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
      {
        name: 'club.not_allowed',
        path: '/not_allowed',
        components: {
          toolbar: ClubToolbar,
          main: NotAllowedPage,
        },
        meta: {
          requiresAuth: false,
        },
      },
      {
        name: 'club.members',
        path: '/members',
        components: {
          toolbar: ClubToolbar,
          main: MembersPage,
        },
      },
    ],
  },
];

export default routes;
