export interface ImageCaptions {
  result: string;
  warnings: string[];
  captions: { generated_text: string }[];
}
