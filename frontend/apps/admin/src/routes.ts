import type { RouteRecordRaw } from 'vue-router';
import { PortalLayout } from '@kwai/ui';
import HomePage from '@root/pages/home/HomePage.vue';
import NotAllowedPage from '@root/pages/not_allowed/NotAllowedPage.vue';
import AdminToolbar from '@root/components/AdminToolbar.vue';
import UsersPage from '@root/pages/users/UsersPage.vue';
import UserInvitationsPage from '@root/pages/users/UserInvitationsPage.vue';
import CreateUserInvitationPage from '@root/pages/users/CreateUserInvitationPage.vue';

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
        path: '/users',
        components: {
          toolbar: AdminToolbar,
          main: UsersPage,
        },
      },
      {
        name: 'admin.user_invitations',
        path: '/user_invitations',
        components: {
          toolbar: AdminToolbar,
          main: UserInvitationsPage,
        },
      },
      {
        name: 'admin.user_invitations.create',
        path: '/user_invitations/create',
        components: {
          toolbar: AdminToolbar,
          main: CreateUserInvitationPage,
        },
      },
    ],
  },
];

export default routes;
