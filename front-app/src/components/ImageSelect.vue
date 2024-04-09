<script setup lang="ts">
import { useStore } from "../store";

const { file } = useStore();

const onFileChange = (e: File | File[] | null) => {
  file.value = Array.isArray(e) ? e[0] : e;
};
</script>

<template>
  <v-card v-bind="$attrs">
    <v-card-item>
      <v-card-title>Make an image into a story</v-card-title>

      <v-card-subtitle>Select an image</v-card-subtitle>
    </v-card-item>

    <v-card-text>
      <v-file-input
        :modelValue="file"
        @update:modelValue="onFileChange"
        accept="image/png, image/jpeg"
        label="Image"
        placeholder="Pick an image"
        prepend-icon="mdi-camera"
      ></v-file-input>
    </v-card-text>
  </v-card>
</template>
