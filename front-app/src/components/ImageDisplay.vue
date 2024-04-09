<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from "vue";
import { useStore, getCaptioning } from "../store";
import ImageCaptation from "./ImageCaptation.vue";

const { file } = useStore();
const imgUrl = ref("");
const aspectRatio = ref({ ratio: 4 / 3, name: "4/3" });

const img = new Image();

const calculateAspectRatio = (width: number, height: number) => {
  return width / height;
};

const selectBestAspectRatio = (ratio: number) => {
  const availableRatios = [
    { ratio: 16 / 9, name: "16/9" },
    { ratio: 4 / 3, name: "4/3" },
    { ratio: 1, name: "1/1" },
  ];

  let closestOption = aspectRatio.value;
  let minDifference = Math.abs(ratio - closestOption.ratio);
  for (const option of availableRatios) {
    const difference = Math.abs(ratio - option.ratio);
    if (difference < minDifference) {
      closestOption = option;
      minDifference = difference;
    }
  }

  return closestOption;
};

img.onload = function () {
  const ratio = calculateAspectRatio(img.naturalWidth, img.naturalHeight);
  aspectRatio.value = selectBestAspectRatio(ratio);
};

const fileToDataURL: (file: File) => Promise<string> = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
};

const loadImage = async () => {
  try {
    if (file.value && file.value instanceof File) {
      imgUrl.value = await fileToDataURL(file.value);
      img.src = imgUrl.value;
    } else {
      imgUrl.value = "";
      img.src = "";
    }
  } catch (error) {
    console.error(error);
  }
};

watch(
  file,
  async () => {
    await loadImage();
  },
  { immediate: true }
);
</script>

<template>
  <v-img
    :src="imgUrl"
    cover
    :aspect-ratio="aspectRatio.name"
    max-height="900"
    v-if="imgUrl"
  ></v-img>
</template>
