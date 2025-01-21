<script setup lang="ts">
import clubImage from '/club.jpg';
</script>

<template>
  <section class="bg-zinc-50">
    <div class="container mx-auto">
      <div class="grid grid-cols-12">
        <div class="grid col-span-12 xl:col-span-7 mt-5 p-10 gap-8">
          <div>
            <h2 class="text-4xl mb-2 font-medium">
              Wat heeft onze club te bieden?
            </h2>
            <p class="text-gray-700 leading-8">
              Judokwai Kemzeke biedt in de gemeente Stekene judo aan op
              recreatief en competitief niveau, voor 5- tot plus 60- jarigen.
            </p>
          </div>
          <div class="flex gap-8 mt-12">
            <img
              src="/jeugdsport.png"
              alt="jeugdsport"
              class="object-contain w-32"
            >
            <div class="flex flex-col pl-3">
              <h3 class="text-2xl">
                Jeudgvriendelijke Judoclub
              </h3>
              <p class="leading-8 text-gray-700">
                Voor het zevende jaar op rij verdient onze club goud bij de
                proclamatie van het jeugdjudofonds!
              </p>
            </div>
          </div>
          <div class="flex gap-8">
            <img
              src="/judo_vlaanderen.svg"
              alt="Judo Vlaanderen"
              class="object-contain w-32"
            >
            <div class="flex flex-col pl-3">
              <h3 class="text-2xl">
                Eens proberen?
              </h3>
              <p class="leading-8 text-gray-700">
                Judo Vlaanderen en Judokwai Kemzeke bieden u een volledige maand
                gratis proeflessen aan.
              </p>
            </div>
          </div>
          <div class="flex gap-8">
            <img
              src="/hartveilig.jpg"
              alt="Hartveilig"
              class="object-contain w-32"
            >
            <div class="flex flex-col pl-3">
              <h3 class="text-2xl">
                Hartveilig
              </h3>
              <p class="leading-8 text-gray-700">
                Onze club is hartveilig. 10% van onze medewerkers zijn getraind
                in reanimatie.
              </p>
            </div>
          </div>
          <div class="flex gap-8">
            <img
              src="/gezond.jpg"
              alt="Gezond Sporten"
              class="object-contain w-32"
            >
            <div class="flex flex-col pl-3">
              <h3 class="text-2xl">
                Gezond Sporten
              </h3>
              <p class="leading-8 text-gray-700">
                Wij dragen Gezond Sporten hoog in het het vaandel.
              </p>
            </div>
          </div>
          <div class="flex gap-8 pb-12 xl:pb-24">
            <img
              src="/panathlon.jpg"
              alt="Panathlon"
              class="object-contain w-32"
            >
            <div class="flex flex-col pl-3">
              <h3 class="text-2xl">
                Panathlon Verklaring
              </h3>
              <p class="leading-8 text-gray-700">
                Onze club onderschrijft de Panathlon verklaring.
              </p>
            </div>
          </div>
        </div>
        <div
          class="col-span-0 xl:col-span-5 bg-cover bg-center bg-no-repeat"
          :style="{ 'background-image': `url(${clubImage})` }"
        />
      </div>
    </div>
  </section>
</template>

<style scoped></style>
