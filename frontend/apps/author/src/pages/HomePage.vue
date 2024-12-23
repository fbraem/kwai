<script setup lang="ts">
import { Card, CardTitle, KwaiButton, ListIcon, ContainerSection, ContainerSectionContent, ContainerSectionTitle } from '@kwai/ui';
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>
      Beheer applicaties, nieuwsberichten en pagina's.
    </ContainerSectionTitle>
    <ContainerSectionContent>
      <Card class="w-full">
        <template #header>
          <CardTitle class="p-3 font-bold text-lg text-gray-900">
            Applicaties
          </CardTitle>
        </template>
        <p class="p-3">
          Applicaties zijn de bouwstenen van de website. Wijzig de titel, samenvatting en omschrijving.
        </p>
        <template #footer>
          <div class="flex justify-between items-center p-3">
            <KwaiButton :to="{ name: 'author.applications' }">
              <ListIcon
                class="w-4 mr-2 fill-current"
              />
              Overzicht
            </KwaiButton>
          </div>
        </template>
      </Card>
      <Card class="w-full">
        <template #header>
          <CardTitle class="p-3 font-bold text-lg text-gray-900">
            Nieuws
          </CardTitle>
        </template>
        <p class="p-3">
          Beheer de nieuwsberichten op de website.
        </p>
        <template #footer>
          <div class="flex justify-between items-center p-3">
            <KwaiButton :to="{ name: 'author.news' }">
              <ListIcon
                class="w-4 mr-2 fill-current"
              />
              Overzicht
            </KwaiButton>
          </div>
        </template>
      </Card>
      <Card class="w-full">
        <template #header>
          <CardTitle class="p-3 font-bold text-lg text-gray-900">
            Pagina's
          </CardTitle>
        </template>
        <p class="p-3">
          Beheer de pagina's van de website.
        </p>
        <template #footer>
          <div class="flex justify-between items-center p-3">
            <KwaiButton :to="{ name: 'author.pages' }">
              <ListIcon
                class="w-4 mr-2 fill-current"
              />
              Overzicht
            </KwaiButton>
          </div>
        </template>
      </Card>
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
