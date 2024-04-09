<script setup lang="ts">
import ImageSelect from "./components/ImageSelect.vue";
import StoryCard from "./components/StoryCard.vue";
import { useStore } from "./store";

const { file } = useStore();
</script>

<template>
  <v-container style="min-height: 100vh">
    <v-sheet
      class="d-flex flex-column align-content-center flex-wrap gap-2"
      min-height="100%"
    >
      <ImageSelect class="mb-6" width="60%" />
      <StoryCard class="mb-6" width="60%" v-show="file" />
    </v-sheet>
  </v-container>
</template>
