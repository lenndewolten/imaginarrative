<script setup lang="ts">
import { computed, watch } from "vue";
import { useStore, generateStory } from "../store";

const { loading, image_captations, generated_story } = useStore();
const loading_story = computed(() => {
  generated_story.value?.result;
  return loading.story || loading.captioning;
});

watch(
  image_captations,
  async () => {
    if (image_captations.value.generated_text) {
      await generateStory(image_captations.value.generated_text);
    }
  },
  { immediate: true }
);
</script>

<template>
  <v-skeleton-loader
    v-if="loading_story"
    class="mx-auto border"
    width="100%"
    type="paragraph"
  ></v-skeleton-loader>
  <v-card-text v-else-if="generated_story?.result === 'success'">
    {{ generated_story?.story }}
  </v-card-text>
  <v-card-text v-else>An error occurred while generating the story</v-card-text>
</template>
