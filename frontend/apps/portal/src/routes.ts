import type { RouteRecordRaw } from 'vue-router';
import HomePage from '@theme/pages/HomePage.vue';
import TrainingsPage from '@theme/pages/TrainingsPage.vue';
import NewsPage from '@theme/pages/NewsPage.vue';
import TrainingsArticlePage from '@theme/pages/trainings/TrainingsArticlePage.vue';
import ApplicationPage from '@theme/pages/ApplicationPage.vue';
import PortalToolbar from './components/toolbar/PortalToolbar.vue';
import { PortalLayout } from '@kwai/ui';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: PortalLayout,
    children: [
      {
        name: 'home',
        path: '/',
        components: {
          toolbar: PortalToolbar,
          main: HomePage,
        },
      },
      {
        name: 'portal.news',
        path: '/news',
        components: {
          toolbar: PortalToolbar,
          main: NewsPage,
        },
      },
      {
        name: 'portal.club',
        path: '/club',
        components: {
          toolbar: PortalToolbar,
          main: ApplicationPage,
        },
      },
      {
        name: 'portal.trainings',
        path: '/trainings',
        components: {
          toolbar: PortalToolbar,
          main: TrainingsPage,
        },
        children: [
          {
            name: 'portal.trainings.article',
            path: ':id(\\d+)',
            props: true,
            component: TrainingsArticlePage,
          },
        ],
      },
    ],
  },
];
export default routes;
