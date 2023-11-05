import type { RouteRecordRaw } from 'vue-router';
import HomePage from '@theme/pages/HomePage.vue';
import TrainingsPage from '@theme/pages/TrainingsPage.vue';
import NewsPage from '@theme/pages/news/NewsPage.vue';
import NewsListPage from '@root/pages/news/NewsListPage.vue';
import NewsApplicationListPage from '@root/pages/news/NewsApplicationListPage.vue';
import NewsItemPage from '@theme/pages/news/NewsItemPage.vue';
import ApplicationPage from '@theme/pages/ApplicationPage.vue';
import PortalToolbar from './components/toolbar/PortalToolbar.vue';
import { PortalLayout } from '@kwai/ui';

// eslint-disable-next-line import/no-absolute-path
import heroClubImage from '/hero_club.jpg';
// eslint-disable-next-line import/no-absolute-path
import heroTrainingImage from '/hero_training.jpg';
// eslint-disable-next-line import/no-absolute-path
import heroShopImage from '/hero_shop.jpg';
// eslint-disable-next-line import/no-absolute-path
import heroTournamentsImage from '/hero_tournaments.jpg';
// eslint-disable-next-line import/no-absolute-path
import heroJudoImage from '/hero_judo.jpg';

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
        path: '/news',
        components: {
          toolbar: PortalToolbar,
          main: NewsPage,
        },
        children: [
          {
            name: 'portal.news',
            path: '',
            component: NewsListPage,
          },
          {
            name: 'portal.news.item',
            path: ':id(\\d+)',
            props: true,
            component: NewsItemPage,
          },
          {
            name: 'portal.news.application',
            path: 'application/:application',
            props: true,
            component: NewsApplicationListPage,
          },
        ],
      },
      {
        name: 'portal.club',
        path: '/club',
        components: {
          toolbar: PortalToolbar,
          main: ApplicationPage,
        },
        meta: {
          application: 'club',
          heroImageUrl: heroClubImage,
        },
      },
      {
        name: 'portal.tournaments',
        path: '/tournaments',
        components: {
          toolbar: PortalToolbar,
          main: ApplicationPage,
        },
        meta: {
          application: 'tournaments',
          heroImageUrl: heroTournamentsImage,
        },
      },
      {
        name: 'portal.shop',
        path: '/shop',
        components: {
          toolbar: PortalToolbar,
          main: ApplicationPage,
        },
        meta: {
          application: 'shop',
          heroImageUrl: heroShopImage,
        },
      },
      {
        name: 'portal.trainings',
        path: '/trainings',
        components: {
          toolbar: PortalToolbar,
          main: TrainingsPage,
        },
        meta: {
          application: 'trainings',
          heroImageUrl: heroTrainingImage,
        },
      },
      {
        name: 'portal.judo',
        path: '/judo',
        components: {
          toolbar: PortalToolbar,
          main: ApplicationPage,
        },
        meta: {
          application: 'judo',
          heroImageUrl: heroJudoImage,
        },
      },
    ],
  },
];
export default routes;
