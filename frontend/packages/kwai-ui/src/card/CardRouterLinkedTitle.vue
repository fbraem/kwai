<template>
  <router-link
    :to="to"
    class="inline-block mb-2"
  >
    <h5>
      <slot></slot>
    </h5>
  </router-link>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import { RouteLocationRaw } from "vue-router"

const props = defineProps<{
  to: RouteLocationRaw
}>()
</script>
