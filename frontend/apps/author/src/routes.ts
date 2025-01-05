import type { RouteRecordRaw } from 'vue-router';
import { PortalLayout } from '@kwai/ui';
import HomePage from '@root/pages/HomePage.vue';
import AuthorToolbar from '@root/components/AuthorToolbar.vue';
import NewsPage from '@root/pages/news/NewsPage.vue';
import NewsCreatePage from '@root/pages/news/NewsCreatePage.vue';
import NewsEditPage from '@root/pages/news/NewsEditPage.vue';
import PagesPage from '@root/pages/pages/PagesPage.vue';
import ApplicationsPage from '@root/pages/applications/ApplicationsPage.vue';
import ApplicationEditPage from '@root/pages/applications/ApplicationEditPage.vue';
import PageCreatePage from '@root/pages/pages/PageCreatePage.vue';
import PageEditPage from '@root/pages/pages/PageEditPage.vue';
import NotAllowedPage from '@root/pages/not_allowed/NotAllowedPage.vue';

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
        meta: { title: 'Home' },
      },
      {
        name: 'author.now_allowed',
        path: '/not_allowed',
        components: {
          toolbar: AuthorToolbar,
          main: NotAllowedPage,
        },
        meta: { requiresAuth: false },
      },
      {
        name: 'author.news',
        path: '/news',
        components: {
          toolbar: AuthorToolbar,
          main: NewsPage,
        },
        meta: { title: 'Nieuws' },
      },
      {
        name: 'author.news.create',
        path: '/news/create',
        props: {
          toolbar: false,
          main: true,
        },
        components: {
          toolbar: AuthorToolbar,
          main: NewsCreatePage,
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
        meta: { title: 'Pagina\'s' },
      },
      {
        name: 'author.pages.create',
        path: '/pages/create',
        components: {
          toolbar: AuthorToolbar,
          main: PageCreatePage,
        },
      },
      {
        name: 'author.pages.edit',
        path: '/pages/edit/:id(\\d+)',
        props: {
          toolbar: false,
          main: true,
        },
        components: {
          toolbar: AuthorToolbar,
          main: PageEditPage,
        },
      },
      {
        name: 'author.applications',
        path: '/applications',
        components: {
          toolbar: AuthorToolbar,
          main: ApplicationsPage,
        },
        meta: { title: 'Applicaties' },
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
