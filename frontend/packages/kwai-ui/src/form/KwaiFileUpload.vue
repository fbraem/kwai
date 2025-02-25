<script setup lang="ts">
import FileUpload, { type FileUploadUploaderEvent } from 'primevue/fileupload';
import { DeleteIcon } from '../icons';
import KwaiButton from './KwaiButton.vue';
import { ref } from 'vue';

interface Props {
  name: string
  maxNumberOfFiles?: number
  uploader: (files: File[]) => void
}
const props = defineProps<Props>();
const fileUpload = ref<typeof FileUpload | null>(null);
const upload = (event: FileUploadUploaderEvent) => {
  // Forward the actual upload to the uploader property.
  if (event.files instanceof File) {
    props.uploader([event.files]);
  } else {
    props.uploader(event.files);
  }
  // @ts-expect-error: primevue
  fileUpload.value!.clear();
  // @ts-expect-error: primevue
  fileUpload.value!.uploadedFileCount = 0;
};
</script>

<template>
  <div class="w-full">
    <FileUpload
      ref="fileUpload"
      :name="props.name"
      accept="text/csv"
      :file-limit="props.maxNumberOfFiles"
      custom-upload
      @uploader="upload"
    >
      <template #empty>
        <slot />
      </template>
      <template #content="{ files, removeFileCallback }">
        <div class="grid grid-rows-1 divide-y">
          <div
            v-for="(file, index) in files"
            :key="file.name + file.type"
            class="grid grid-cols-2 items-center gap-2 py-2"
          >
            <div>
              {{ file.name }}
            </div>
            <div>
              <KwaiButton
                class="bg-primary-500 text-primary-text"
                :small="true"
                @click="() => removeFileCallback(index)"
              >
                <DeleteIcon class="fill-primary-text" />
              </KwaiButton>
            </div>
          </div>
        </div>
      </template>
    </FileUpload>
  </div>
</template>

<style scoped>

</style>
