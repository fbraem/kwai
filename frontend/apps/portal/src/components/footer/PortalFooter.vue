<script setup lang="ts">
import HouseIcon from '@root/components/icons/HouseIcon.vue';
import MailIcon from '@root/components/icons/MailIcon.vue';

import config, { portal } from '@kwai/config';
import { defineAsyncComponent } from 'vue';

const loadIcon = (name: string) => {
  return defineAsyncComponent(() => import(`@root/components/icons/${name}.vue`));
};
</script>

<template>
  <section class="bg-gray-800 text-white pt-12">
    <div class="container mx-auto flex flex-col">
      <div class="relative flex flex-col self-center max-w-3xl sm:rounded-lg sm:shadow-lg sm:shadow-gray-600 bg-red-600 text-white -mt-20 px-2">
        <p
          v-for="(text, index) in config.portal.promotion_footer"
          :key="`promotion_footer_${index}`"
          class="first:pt-10 last:pb-10"
        >
          {{ text }}
        </p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 pt-12 px-12">
        <div>
          <h2 class="text-xl pb-2">
            Contact
          </h2>
          <ul class="grid grid-row-3">
            <li class="font-bold">
              {{ config.website.title }}
            </li>
            <li class="flex items-center">
              <HouseIcon class="w-4 h-4 fill-current mr-2" />{{ config.contact.street }}
            </li>
            <li>{{ config.contact.city }}</li>
          </ul>
          <div class="flex items-center">
            <MailIcon class="w-4 h-4 fill-current mr-2" />
            <a
              :href="`mailto:${config.contact.email}`"
              class="text-blue-300"
            >
              {{ config.contact.email }}
            </a>
          </div>
        </div>
        <div>
          <h2 class="text-xl pb-2">
            Links
          </h2>
          <div
            v-for="link in config.portal.links"
            :key="link.title"
          >
            <a
              :href="link.url"
              target="_blank"
              class="text-blue-400"
            >{{ link.title }}</a>
          </div>
        </div>
        <div>
          <h2 class="text-xl pb-2">
            Sociale Media
          </h2>
          <div class="flex flex-col gap-4">
            <div
              v-for="socialMedia in config.portal.social_media"
              :key="socialMedia.title"
            >
              <a
                :href="socialMedia.url"
                target="_blank"
              >
                <h3 class="flex items-center font-semibold pb-2">
                  <component
                    :is="loadIcon(socialMedia.icon)"
                    class="w-4 fill-current mr-2"
                  />
                  {{ socialMedia.title }}
                </h3>
                <p class="text-sm">
                  {{ socialMedia.text }}
                </p>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="container mx-auto flex justify-center py-12 px-2">
      <div class="text-xs text-center">
        &copy; {{ config.website.copyright }}<br>
        Zumuta - <a
          :href="`mailto:${config.website.email}`"
          class="text-blue-400"
        >Franky Braem</a>
      </div>
    </div>
  </section>
</template>

<style scoped>

</style>
