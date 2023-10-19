<template>
  <section class="py-24 bg-zinc-50">
    <div class="container mx-auto px-12 flex flex-col">
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        <NewsList>
          <template #default="{ story }">
            <NewsCard :story="story" />
          </template>
        </NewsList>
      </div>
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
import NewsList from '@root/components/NewsList.vue';
import NewsCard from '@root/components/NewsCard.vue';
</script>
