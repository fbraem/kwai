<template>
  <div class="container mx-auto">
    <h2 class="text-4xl mb-4">
      {{ page.texts[0].title }}
    </h2>
    <blockquote class="italic mb-4">
      <div v-html="page.texts[0].summary" />
    </blockquote>
    <div
      class="markdown"
      v-html="page.texts[0].content"
    />
  </div>
</template>

<script setup lang="ts">
import type { Page } from '@root/composables/usePage';

interface PageProperty {
  page: Page
}
defineProps<PageProperty>();
</script>

<style>
.markdown h1 {
  @apply text-2xl font-bold mb-2;
}

.markdown h2 {
  @apply text-xl font-bold mb-2;
}

.markdown h3 {
  @apply text-lg font-bold mb-2;
}

.markdown h4 {
  @apply font-bold mb-2;
}

.markdown p {
  @apply leading-8 mb-4;
}

.markdown ul {
  @apply list-disc list-inside pl-1 mb-4;
}

.markdown li {
  @apply mb-4;
}

.markdown li p {
  @apply inline;
}

.markdown a {
  @apply text-blue-600;
}

.markdown a:hover {
  @apply underline;
}
.markdown blockquote {
  @apply p-3 mb-4 border-l-4 border-gray-300 bg-gray-200;
}
.markdown blockquote p {
  @apply mb-0;
}
.markdown table {
  @apply divide-y divide-gray-200 shadow overflow-x-auto border-b border-gray-200 sm:rounded-lg mb-5;
}
.markdown table thead {
  @apply bg-gray-50;
}
.markdown table th {
  @apply px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider;
}
.markdown table td {
  @apply px-6 py-4 whitespace-nowrap;
}
.markdown table tbody {
  @apply bg-white divide-y divide-gray-200;
}
</style>
