import { defineStore } from 'pinia';
import type { Ref } from 'vue';
import { ref, watch } from 'vue';
import type { JsonApiDataType } from '@kwai/api';
import { JsonApiDocument, JsonResourceIdentifier, useHttpApi } from '@kwai/api';
import type { DateType } from '@kwai/date';
import { createDateTimeFromUTC } from '@kwai/date';
import { z } from 'zod';
import useSWRV from 'swrv';

const JsonApiContent = z.object({
  locale: z.string(),
  title: z.string(),
  summary: z.string(),
  content: z.nullable(z.string()),
});

const JsonApiNewsStory = z.object({
  id: z.string(),
  type: z.literal('stories'),
  attributes: z.object({
    priority: z.number(),
    publish_date: z.string(),
    content: z.array(JsonApiContent),
  }),
  relationships: z.object({
    application: z.object({
      data: JsonResourceIdentifier,
    }),
  }),
});
type JsonApiNewsStoryType = z.infer<typeof JsonApiNewsStory>;

const JsonApiApplication = z.object({
  id: z.string(),
  type: z.literal('applications'),
  attributes: z.object({
    name: z.string(),
    title: z.string(),
  }),
});

const JsonApiNewsStoryData = z.object({
  data: z.union([JsonApiNewsStory, z.array(JsonApiNewsStory).default([])]),
  included: z.array(JsonApiApplication).default([]),
});
const JsonApiNewsStoryDocument = JsonApiDocument.extend(JsonApiNewsStoryData.shape);
type JSONApiNewsStoryDocumentType = z.infer<typeof JsonApiNewsStoryData>;

interface NewsStoryContent {
  locale: string,
  title: string,
  summary: string,
  content?: string | null
}

export interface NewsStory {
  id: string,
  priority: number,
  publish_date: DateType,
  contents: NewsStoryContent[]
}

const toModel = (json: JSONApiNewsStoryDocumentType): NewsStory | NewsStory[] => {
  const mapModel = (d: JsonApiDataType): NewsStory => {
    const story = <JsonApiNewsStoryType> d;
    return {
      id: story.id,
      priority: story.attributes.priority,
      publish_date: createDateTimeFromUTC(story.attributes.publish_date, d.attributes.timezone),
      contents: story.attributes.content.map(content => ({
        locale: content.locale,
        title: content.title,
        summary: content.summary,
        content: content.content,
      })),
    };
  };
  if (Array.isArray(json.data)) {
    return json.data.map(mapModel);
  }
  return mapModel(json.data);
};

export const useNewsStore = defineStore('news', () => {
  const items = ref<NewsStory[]>([]);

  const load = ({
    offset = ref(0),
    limit = ref(0),
  }: {
    offset?: Ref<number>,
    limit?: Ref<number>
  } = {}) => {
    const { data, isValidating, error } = useSWRV<JSONApiNewsStoryDocumentType>(
      'portal.news',
      () => {
        const api = useHttpApi().url('/v1/portal/news');
        return api
          .get()
          .json()
        ;
      },
      {
        revalidateOnFocus: false,
      }
    );

    watch(
      data,
      (nv) => {
        const result = JsonApiNewsStoryDocument.safeParse(nv);
        if (result.success) {
          items.value = <NewsStory[]>toModel(result.data);
        } else {
          console.log(result);
        }
      }
    );

    return {
      loading: isValidating,
      error,
    };
  };

  return {
    items,
    load,
  };
});
