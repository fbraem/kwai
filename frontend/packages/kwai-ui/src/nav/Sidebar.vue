<template>
  <div class="flex">
    <div
        class="fixed z-20 inset-0 opacity-50 transition-opacity lg:hidden"
        :class="[isOpen ? 'block' : 'hidden', bgColor]"
        @click="isOpen = false"
    />
    <div
        :class="[isOpen ? 'translate-x-0 ease-out' : '-translate-x-full ease-in', bgOverlayColor]"
        class="fixed z-30 inset-y-0 left-0 w-64 transition duration-300 transform overflow-y-auto lg:translate-x-0 lg:static lg:inset-0"
    >
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSidebar } from "./useSidebar.js"

export interface Props {
  bgColor?: string,
  bgOverlayColor?: string
}

const props = withDefaults(
    defineProps<Props>(),
    {
      bgColor: 'bg-black',
      bgOverlayColor: 'bg-gray-900'
    }
)

const { isOpen } = useSidebar()
</script>
