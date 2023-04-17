<template>
  <ApplicationListModel v-slot="{ applications }">
    <template v-for="application in applications">
      <slot :application="application" />
      <slot
        :name="`app-${application.name}`"
        :application="application"
      />
    </template>
  </ApplicationListModel>
</template>

<script setup lang="ts">
import ApplicationListModel from './ApplicationListModel.vue';
</script>
