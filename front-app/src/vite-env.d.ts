/// <reference types="vite/client" />

declare module "*.vue" {
  import type { DefineComponent } from "vue";
  const component: DefineComponent<{}, {}, any>;
  export default component;
}

interface ImportMetaEnv {
  readonly VITE_IMAGE_CAPTIONING_BASE_URL: string;
  readonly VITE_STORY_GENERATOR_BASE_URL: string;
  readonly VITE_STORY_TELLER_BASE_URL: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
