<template>
  <section
    v-if="article"
    class="bg-zinc-50 py-24"
  >
    <FullArticle :article="article" />
  </section>
</template>

<script setup lang="ts">
import { useArticleStore } from '@root/stores/articleStore';
import { computed } from 'vue';
import FullArticle from '@root/components/FullArticle.vue';

interface TrainingsArticleProperty {
  id: string
}
const props = defineProps<TrainingsArticleProperty>();
const id = computed(() => props.id);

const articleStore = useArticleStore();
articleStore.get(id);

const article = computed(() => articleStore.article);
</script>
