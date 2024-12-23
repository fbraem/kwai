<!-- A wrapper around PrimeVue ButtonGroup -->
<script setup lang="ts">
import ButtonGroup from 'primevue/buttongroup';
defineOptions({
  inheritAttrs: false,
});

</script>

<template>
  <ButtonGroup>
    <slot />
  </Buttongroup>
</template>

<style>
span[data-pc-name="buttongroup"] > *:first-child > button[data-pc-name="button"]:first-child {
  border-bottom-right-radius: 0;
  border-top-right-radius: 0;
}
span[data-pc-name="buttongroup"] > *:not(:first-child, :last-child) > button[data-pc-name="button"] {
  border-radius: 0;
}
span[data-pc-name="buttongroup"] > *:last-child > button[data-pc-name="button"] {
  border-bottom-left-radius: 0;
  border-top-left-radius: 0;
}
</style>
