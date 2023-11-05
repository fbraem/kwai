<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';
import IntroSection from '@root/components/IntroSection.vue';
import { useApplications } from '@root/composables/useApplication';
import { computed, ref, toRef } from 'vue';
import { usePages } from '@root/composables/usePage';
import FullArticle from '@root/components/FullArticle.vue';
const route = useRoute();
const applicationName = route.meta.application as string;
const heroImageUrl = route.meta.heroImageUrl as string;

// Application
const { data: applications } = useApplications();
const application = computed(() => {
  if (applications.value) {
    return applications.value.find(application => application.name === applicationName);
  }
  return null;
});

// Pages
const { data: pages } = usePages(toRef(applicationName));
const sortedPages = computed(() => {
  return [...pages.value || []].sort((a, b) => b.priority - a.priority);
});
const backgroundClassPages = computed(() => {
  return sortedPages.value.map((page, index) => {
    return {
      'bg-black': index % 2,
      'hover:bg-gray-900': index % 2,
      'bg-red-600': !(index % 2),
      'hover:bg-red-500': !(index % 2),
    };
  });
});

const articleSection = ref<HTMLInputElement | null>(null);
const currentPage = computed(() => {
  if (route.query.page) {
    if (articleSection.value) articleSection.value.scrollIntoView(true);
    return sortedPages.value.find(page => page.id === route.query.page);
  }
  return sortedPages.value[0];
});
const router = useRouter();

const gotoPage = (id: string) => {
  router.replace({ query: { ...route.query, page: id } });
};
</script>

<template>
  <IntroSection
    :hero-image-url="heroImageUrl"
  >
    <div class="container lg:max-w-5xl relative mx-auto flex h-full items-center">
      <div
        v-if="application"
        class="flex flex-col space-y-5 p-4"
      >
        <h1 class="text-4xl font-semibold text-white">
          {{ application.title }}
        </h1>
        <p
          class="text-white leading-8 text-xl"
        >
          {{ application.short_description }}
        </p>
      </div>
    </div>
  </IntroSection>
  <section class="grid grid-flow-row auto-rows-fr md:grid-flow-col md:auto-cols-fr">
    <template
      v-for="(page, index) in sortedPages"
      :key="page.id"
    >
      <a
        class="cursor-pointer"
        @click="gotoPage(page.id)"
      >
        <div
          class="text-center text-white p-8 h-full"
          :class="backgroundClassPages[index]"
        >
          <h2 class="text-2xl mb-2 font-medium">
            {{ page.texts[0].title }}
          </h2>
          <div
            class="text-gray-200"
            v-html="page.texts[0].summary"
          />
        </div>
      </a>
    </template>
  </section>
  <section
    ref="articleSection"
    class="py-12"
  >
    <FullArticle
      v-if="currentPage"
      :page="currentPage"
    />
  </section>
</template>
