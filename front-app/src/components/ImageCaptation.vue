<script setup lang="ts">
import { computed, watch } from "vue";
import { useStore, getCaptioning } from "../store";

const { file, loading, image_captations } = useStore();
const loading_captation = computed(() => {
  return loading.captioning;
});

watch(
  file,
  async () => {
    if (file.value instanceof File) {
      await getCaptioning(file.value as File);
    }
  },
  { immediate: true }
);
</script>

<template>
  <v-skeleton-loader
    v-if="loading_captation"
    class="mx-auto border"
    width="100%"
    type="heading"
  ></v-skeleton-loader>

  <v-card-title
    v-else-if="image_captations?.result === 'success'"
    style="white-space: pre-wrap"
    class="capitalize"
  >
    {{ image_captations.generated_text }}
  </v-card-title>
  <v-card-title style="white-space: pre-wrap" v-else
    >Could not load captioning for the provided image</v-card-title
  >
</template>

<style scoped>
.capitalize::first-letter {
  text-transform: uppercase;
}
</style>
