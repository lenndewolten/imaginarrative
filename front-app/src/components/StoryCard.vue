<script setup lang="ts">
import { generateAudio, useStore } from "../store";
import ImageCaptation from "./ImageCaptation.vue";
import ImageDisplay from "./ImageDisplay.vue";
import GeneratedStory from "./GeneratedStory.vue";
import StoryTeller from "./StoryTeller.vue";

const { file } = useStore();
</script>

<template>
  <v-card v-bind="$attrs">
    <ImageDisplay />

    <ImageCaptation />

    <v-divider></v-divider>

    <GeneratedStory />

    <StoryTeller />
  </v-card>
</template>
