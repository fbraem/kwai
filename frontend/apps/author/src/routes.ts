import type { RouteRecordRaw } from 'vue-router';
import { PortalLayout } from '@kwai/ui';
import HomePage from '@root/pages/HomePage.vue';
import AuthorToolbar from '@root/components/AuthorToolbar.vue';
import NewsPage from '@root/pages/news/NewsPage.vue';
import NewsEditPage from '@root/pages/news/NewsEditPage.vue';
import PagesPage from '@root/pages/PagesPage.vue';
import ApplicationsPage from '@root/pages/applications/ApplicationsPage.vue';
import ApplicationEditPage from '@root/pages/applications/ApplicationEditPage.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: PortalLayout,
    children: [
      {
        name: 'author.home',
        path: '/',
        components: {
          toolbar: AuthorToolbar,
          main: HomePage,
        },
        meta: {
          title: 'Home',
        },
      },
      {
        name: 'author.news',
        path: '/news',
        components: {
          toolbar: AuthorToolbar,
          main: NewsPage,
        },
        meta: {
          title: 'Nieuws',
        },
      },
      {
        name: 'author.news.edit',
        path: '/news/edit/:id(\\d+)',
        props: {
          toolbar: false,
          main: true,
        },
        components: {
          toolbar: AuthorToolbar,
          main: NewsEditPage,
        },
      },
      {
        name: 'author.pages',
        path: '/pages',
        components: {
          toolbar: AuthorToolbar,
          main: PagesPage,
        },
        meta: {
          title: "Pagina's",
        },
      },
      {
        name: 'author.applications',
        path: '/applications',
        components: {
          toolbar: AuthorToolbar,
          main: ApplicationsPage,
        },
        meta: {
          title: 'Applicaties',
        },
      },
      {
        name: 'author.applications.edit',
        path: '/applications/edit/:id(\\d+)',
        props: {
          toolbar: false,
          main: true,
        },
        components: {
          toolbar: AuthorToolbar,
          main: ApplicationEditPage,
        },
      },
    ],
  },
];

export default routes;
