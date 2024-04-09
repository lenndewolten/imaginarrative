import { Ref, computed, reactive, ref } from "vue";
import { ImageCaptions } from "./models/ImageCaptions";
import { GeneratedStory } from "./models/GeneratedStory";

const state: {
  loading: { captioning: boolean; story: boolean; audio: boolean };
  file: Ref<File | null>;
  image_captations: Ref<ImageCaptions | null>;
  generated_story: Ref<GeneratedStory | null>;
} = {
  loading: reactive({
    captioning: false,
    story: false,
    audio: false,
  }),
  file: ref(null),
  image_captations: ref(null),
  generated_story: ref(null),
};

export const getCaptioning = async (file: File) => {
  try {
    state.loading.captioning = true;
    state.image_captations.value = null;
    const formData = new FormData();

    formData.append("file", file);
    formData.append("image_text_input", "A photograph of");
    formData.append("num_return_sequences", "1");

    // const res = await fetch(
    //   `${import.meta.env.VITE_IMAGE_CAPTIONING_BASE_URL}/generate-by-file`,
    //   {
    //     method: "POST",
    //     body: formData,
    //   }
    // );

    // if (!res.ok) {
    //   if (res.status === 400) {
    //     console.error(res.json());
    //   } else {
    //     throw new Error(res.statusText);
    //   }
    // }
    // state.image_captations.value = (await res.json()) as ImageCaptions;

    state.image_captations.value = {
      result: "success",
      warnings: [],
      captions: [
        {
          generated_text: "test",
        },
      ],
    };
  } catch (error) {
    console.error(error);
    state.image_captations.value = null;
  } finally {
    state.loading.captioning = false;
  }
};

export const generateStory = async (image_captation: string) => {
  try {
    state.loading.story = true;
    state.generated_story.value = null;
    const body = {
      prompt: image_captation,
    };

    const res = await fetch(
      `${import.meta.env.VITE_STORY_GENERATOR_BASE_URL}/generate`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }
    );

    if (!res.ok) {
      if (res.status === 400) {
        console.error(res.json());
      } else {
        throw new Error(res.statusText);
      }
    }

    state.generated_story.value = (await res.json()) as GeneratedStory;
  } catch (error) {
    console.error(error);
    state.generated_story.value = null;
  } finally {
    state.loading.story = false;
  }
};

export const generateAudio = async (story: string) => {
  try {
    state.loading.audio = true;
    const body = {
      text: story,
    };

    const res = await fetch(
      `${import.meta.env.VITE_STORY_TELLER_BASE_URL}/generate`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }
    );

    if (res.ok) {
      const blob = await res.blob();
      return window.URL.createObjectURL(blob);
    }
  } catch (error) {
    console.error(error);
  } finally {
    state.loading.audio = false;
  }
};

export const useStore = () => {
  return {
    file: state.file,
    loading: state.loading,
    image_captations: computed(() => {
      return {
        result: state.image_captations.value?.result,
        generated_text:
          state.image_captations.value?.captions[0].generated_text ?? "",
      };
    }),
    generated_story: state.generated_story,
  };
};
