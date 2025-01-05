import type { RouteRecordRaw } from 'vue-router';
import { PortalLayout } from '@kwai/ui';
import CoachToolbar from '@root/components/CoachToolbar.vue';
import HomePage from '@root/pages/home/HomePage.vue';
import TrainingsPage from '@root/pages/trainings/TrainingsPage.vue';
import TrainingEditPage from '@root/pages/trainings/TrainingEditPage.vue';
import TrainingCreatePage from '@root/pages/trainings/TrainingCreatePage.vue';
import TrainingDefinitionsPage from '@root/pages/training_definitions/TrainingDefinitionsPage.vue';
import GenerateTrainingsPage from '@root/pages/training_definitions/GenerateTrainingsPage.vue';
import TrainingDefinitionEditPage from '@root/pages/training_definitions/TrainingDefinitionEditPage.vue';
import TrainingDefinitionCreatePage from '@root/pages/training_definitions/TrainingDefinitionCreatePage.vue';
import NotAllowedPage from '@root/pages/not_allowed/NotAllowedPage.vue';

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
        meta: { title: 'Home' },
      },
      {
        name: 'club.not_allowed',
        path: '/not_allowed',
        components: {
          toolbar: CoachToolbar,
          main: NotAllowedPage,
        },
        meta: { requiresAuth: false },
      },
      {
        name: 'coach.trainings',
        path: '/trainings',
        components: {
          toolbar: CoachToolbar,
          main: TrainingsPage,
        },
        meta: { title: 'Trainingen' },
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
        props: { main: true },
        components: {
          toolbar: CoachToolbar,
          main: TrainingEditPage,
        },
      },
      {
        name: 'coach.training_definitions',
        path: '/training_definitions',
        components: {
          toolbar: CoachToolbar,
          main: TrainingDefinitionsPage,
        },
        meta: { title: 'Trainingsmomenten' },
      },
      {
        name: 'coach.training_definitions.edit',
        path: '/training_definitions/edit/:id(\\d+)',
        props: { main: true },
        components: {
          toolbar: CoachToolbar,
          main: TrainingDefinitionEditPage,
        },
      },
      {
        name: 'coach.training_definitions.create',
        path: '/training_definitions/create',
        components: {
          toolbar: CoachToolbar,
          main: TrainingDefinitionCreatePage,
        },
      },
      {
        name: 'coach.training_definitions.generate_trainings',
        path: '/training_definitions/generate_trainings/:id(\\d+)',
        props: { main: true },
        components: {
          toolbar: CoachToolbar,
          main: GenerateTrainingsPage,
        },
      },
    ],
  },
];

export default routes;
