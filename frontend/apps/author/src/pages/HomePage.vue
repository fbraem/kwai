<script setup lang="ts">
import {
  KwaiCard,
  KwaiButton,
  ListIcon,
  ContainerSection,
  ContainerSectionContent,
  ContainerSectionTitle,
} from '@kwai/ui';
</script>

<template>
  <ContainerSection>
    <ContainerSectionTitle>
      Beheer applicaties, nieuwsberichten en pagina's.
    </ContainerSectionTitle>
    <ContainerSectionContent>
      <KwaiCard class="w-full">
        <template #title>
          Applicaties
        </template>
        Applicaties zijn de bouwstenen van de website. Wijzig de titel, samenvatting en omschrijving.
        <template #footer>
          <KwaiButton
            :to="{ name: 'author.applications' }"
            small
          >
            <ListIcon class="w-4 mr-2 fill-current" />
            Overzicht
          </KwaiButton>
        </template>
      </KwaiCard>
      <KwaiCard class="w-full">
        <template #title>
          Nieuws
        </template>
        Beheer de nieuwsberichten op de website.
        <template #footer>
          <KwaiButton
            :to="{ name: 'author.news' }"
            small
          >
            <ListIcon class="w-4 mr-2 fill-current" />
            Overzicht
          </KwaiButton>
        </template>
      </KwaiCard>
      <KwaiCard class="w-full">
        <template #title>
          Pagina's
        </template>
        Beheer de pagina's van de website.
        <template #footer>
          <KwaiButton
            :to="{ name: 'author.pages' }"
            small
          >
            <ListIcon class="w-4 mr-2 fill-current" />
            Overzicht
          </KwaiButton>
        </template>
      </KwaiCard>
    </ContainerSectionContent>
  </ContainerSection>
</template>

<style scoped>

</style>
