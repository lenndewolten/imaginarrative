<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useStore, generateAudio } from "../store";

const { loading, generated_story } = useStore();

const loading_audio = computed(() => {
  return loading.audio || loading.story || loading.captioning;
});

const audioPlayer = ref();
watch(
  generated_story,
  async () => {
    if (generated_story.value?.story) {
      const url = await generateAudio(generated_story.value.story);

      const audio = new Audio(url);
      audio.controls = true;
      if (audioPlayer.value) {
        audioPlayer.value.src = audio.src;
      }
    } else {
      if (audioPlayer.value) {
        audioPlayer.value.src = "";
      }
    }
  },
  { immediate: true }
);
</script>

<template>
  <v-skeleton-loader
    class="mx-auto border"
    v-if="loading_audio"
    width="100%"
    type="heading"
  ></v-skeleton-loader>
  <v-card-text v-else class="audio-container">
    <audio ref="audioPlayer" controls>
      Your browser does not support the audio element.
    </audio>
  </v-card-text>
</template>

<style scoped>
.audio-container {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
