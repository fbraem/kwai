<script setup lang="ts">
import { toRef } from 'vue';
import FullArticle from '@root/components/FullArticle.vue';
import { usePage } from '@root/composables/usePage';

interface TrainingsArticleProperty {
  id: string
}
const props = defineProps<TrainingsArticleProperty>();

const { data: page } = usePage(toRef(props.id));
</script>

<template>
  <section
    v-if="page"
    class="bg-zinc-50 py-24"
  >
    <FullArticle :page="page" />
  </section>
</template>
