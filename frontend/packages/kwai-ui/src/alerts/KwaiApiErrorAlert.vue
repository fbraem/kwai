<script setup lang="ts">
import Button from 'primevue/button';
import KwaiErrorAlert from './KwaiErrorAlert.vue';
import ExpandIcon from '../icons/ExpandIcon.vue';
import CollapseIcon from '../icons/CollapseIcon.vue';
import { ref } from 'vue';

interface ApiError {
  status: string
  message: string
  url: string
}

interface Props {
  error: ApiError
}
defineProps<Props>();

const showDetails = ref(false);
const toggleDetails = () => {
  showDetails.value = !showDetails.value;
};
</script>

<template>
  <KwaiErrorAlert>
    <div class="p-2 flex flex-col">
      <div>
        <slot />
      </div>
      <div>
        <Button
          @click="() => toggleDetails()"
          variant="link"
          :pt="{ root: () => 'px-0 py-0' }"
        >
          <slot name="details_button">
            Show Details
          </slot>
          <ExpandIcon
            v-show="!showDetails"
            class="w-4 fill-current"
          />
          <CollapseIcon
            v-show="showDetails"
            class="w-4 fill-current"
          />
        </Button>
      </div>
    </div>
    <dl
      v-show="showDetails"
      class="border-1 rounded px-2 bg-white divide-y divide-gray-100 mb-2"
    >
      <div class="px-2 py-3 sm:grid sm:grid-cols-4 sm:gap-4 sm:px-0">
        <dt class="text-sm font-bold text-gray-900">
          Status
        </dt>
        <dd class="mt-1 text-sm/6 text-gray-700 sm:col-span-3 sm:mt-0">
          {{ error.status }}
        </dd>
      </div>
      <div class="px-2 py-3 sm:grid sm:grid-cols-4 sm:gap-4 sm:px-0">
        <dt class="text-sm font-bold text-gray-900">
          Error
        </dt>
        <dd class="mt-1 text-sm text-gray-700 sm:col-span-3 sm:mt-0">
          {{ error.message }}
        </dd>
      </div>
      <div class="px-2 py-3 sm:grid sm:grid-cols-4 sm:gap-4 sm:px-0">
        <dt class="text-sm font-bold text-gray-900">
          URL
        </dt>
        <dd class="mt-1 text-sm text-gray-700 sm:col-span-3 sm:mt-0">
          {{ error.url }}
        </dd>
      </div>
    </dl>
  </KwaiErrorAlert>
</template>

<style scoped>

</style>
