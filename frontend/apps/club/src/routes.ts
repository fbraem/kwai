import type { RouteRecordRaw } from 'vue-router';
import { PortalLayout } from '@kwai/ui';
import HomePage from '@root/pages/home/HomePage.vue';
import NotAllowedPage from '@root/pages/not_allowed/NotAllowedPage.vue';
import MembersPage from '@root/pages/members/MembersPage.vue';
import ClubToolbar from '@root/components/ClubToolbar.vue';
import UploadMembersPage from '@root/pages/members/MembersUploadPage.vue';
import TeamsPage from '@root/pages/teams/TeamsPage.vue';
import TeamEditPage from '@root/pages/teams/TeamEditPage.vue';
import TeamCreatePage from '@root/pages/teams/TeamCreatePage.vue';
import TeamMembersPage from '@root/pages/teams/TeamMembersPage.vue';
import TeamMemberButtonAdd from '@root/pages/teams/components/TeamMemberButtonAdd.vue';
import TeamMemberAdd from '@root/pages/teams/components/TeamMemberAdd.vue';

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
      {
        name: 'club.upload',
        path: '/members/upload',
        components: {
          toolbar: ClubToolbar,
          main: UploadMembersPage,
        },
      },
      {
        name: 'club.teams',
        path: '/teams',
        components: {
          toolbar: ClubToolbar,
          main: TeamsPage,
        },
        meta: {
          title: 'Teams',
        },
      },
      {
        name: 'club.teams.edit',
        path: '/teams/edit/:id',
        components: {
          toolbar: ClubToolbar,
          main: TeamEditPage,
        },
        props: {
          toolbar: false,
          main: true,
        },
      },
      {
        name: 'club.teams.create',
        path: '/teams/create',
        components: {
          toolbar: ClubToolbar,
          main: TeamCreatePage,
        },
      },
      {
        path: '/teams/:id/members',
        components: {
          toolbar: ClubToolbar,
          main: TeamMembersPage,
        },
        props: {
          toolbar: false,
          main: true,
        },
        children: [
          {
            name: 'club.teams.members',
            path: '',
            component: TeamMemberButtonAdd,
            props: true,
          },
          {
            name: 'club.teams.members.add',
            path: 'add',
            component: TeamMemberAdd,
            props: true,
          },
        ],
      },
    ],
  },
];

export default routes;
