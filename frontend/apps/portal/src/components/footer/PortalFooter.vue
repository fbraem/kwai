<script setup lang="ts">
import HouseIcon from '@root/components/icons/HouseIcon.vue';
import MailIcon from '@root/components/icons/MailIcon.vue';

import config from '@kwai/config';
import { defineAsyncComponent } from 'vue';

const loadIcon = (name: string) => {
  return defineAsyncComponent(() => import(`@root/components/icons/${name}.vue`));
};
</script>

<template>
  <section class="bg-gray-800 text-white pt-12">
    <div class="container mx-auto flex flex-col">
      <div class="relative flex self-center max-w-3xl sm:rounded-lg bg-red-600 text-white -mt-20 py-3 px-2">
        <p class="p-10">
          Wil jij ook beginnen met judo? Vanaf de leeftijd van <span class="font-bold">5 jaar</span>
          ben je welkom. Spring gewoon eens binnen op een training. Een judopak is nog niet nodig,
          sportieve kledij is voldoende. De eerste 4 lessen zijn
          trouwens gratis zodat je zonder verplichting kan zien of judo iets voor jou is.
        </p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 pt-12 px-12">
        <div>
          <h2 class="text-xl pb-2">
            Contact
          </h2>
          <ul class="grid grid-row-3">
            <li class="font-bold">
              Judokwai Kemzeke vzw
            </li>
            <li class="flex items-center">
              <HouseIcon class="w-4 h-4 fill-current mr-2" />Polderstraat 10
            </li>
            <li>9190 Stekene</li>
          </ul>
          <div class="flex items-center">
            <MailIcon class="w-4 h-4 fill-current mr-2" />
            <a
              :href="`mailto:${config.website.email}`"
              class="text-blue-300"
            >
              {{ config.website.email }}
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
        Zumuta - Franky Braem
      </div>
    </div>
  </section>
</template>

<style scoped>

</style>
