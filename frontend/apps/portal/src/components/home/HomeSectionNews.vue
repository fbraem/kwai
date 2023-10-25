<template>
  <section class="py-20 bg-zinc-50">
    <div class="container mx-auto px-12 flex flex-col">
      <h2 class="text-4xl font-medium text-center pb-12">
        Nieuws
      </h2>
      <NewsList :promoted="true">
        <template #empty>
          <div class="text-gray-600 text-center mb-6">
            Momenteel zijn er geen hoofdpunten in ons nieuws.
          </div>
        </template>
        <template #default="{ newsItem }">
          <NewsCard :news-item="newsItem" />
        </template>
      </NewsList>
      <div class="mb-12">
        <h2 class="text-4xl font-medium text-center mb-6">
          Meer nieuws
        </h2>
        <p class="text-gray-600 text-center">
          Nog meer nieuws kan je lezen op onze
          <router-link
            to="/news"
            class="hover:underline text-blue-400"
          >
            nieuwspagina
          </router-link>.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import NewsList from '@root/components/news/NewsList.vue';
import NewsCard from '@root/components/news/NewsCard.vue';
</script>
