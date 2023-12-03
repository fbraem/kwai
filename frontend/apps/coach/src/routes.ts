import type { RouteRecordRaw } from 'vue-router';
import { PortalLayout } from '@kwai/ui';
import CoachToolbar from '@root/components/CoachToolbar.vue';
import HomePage from '@root/pages/home/HomePage.vue';
import TrainingsPage from '@root/pages/trainings/TrainingsPage.vue';
import TrainingEditPage from '@root/pages/trainings/TrainingEditPage.vue';
import TrainingCreatePage from '@root/pages/trainings/TrainingCreatePage.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: PortalLayout,
    children: [
      {
        name: 'coach.home',
        path: '/',
        components: {
          toolbar: CoachToolbar,
          main: HomePage,
        },
        meta: {
          title: 'Home',
        },
      },
      {
        name: 'coach.trainings',
        path: '/trainings',
        components: {
          toolbar: CoachToolbar,
          main: TrainingsPage,
        },
        meta: {
          title: 'Trainingen',
        },
      },
      {
        name: 'coach.trainings.create',
        path: '/trainings/create',
        components: {
          toolbar: CoachToolbar,
          main: TrainingCreatePage,
        },
      },
      {
        name: 'coach.trainings.edit',
        path: '/trainings/edit/:id(\\d+)',
        props: {
          main: true,
        },
        components: {
          toolbar: CoachToolbar,
          main: TrainingEditPage,
        },
      },
    ],
  },
];

export default routes;
