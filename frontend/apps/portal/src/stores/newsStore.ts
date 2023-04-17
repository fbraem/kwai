import { defineStore } from 'pinia';
import type { Ref } from 'vue';
import { ref, watch } from 'vue';
import type { JsonApiDataType } from '@kwai/api';
import { JsonApiDocument, useHttpApi } from '@kwai/api';
import type { DateType } from '@kwai/date';
import { createDateTimeFromUTC } from '@kwai/date';
import { z } from 'zod';
import useSWRV from 'swrv';

const JsonApiContent = z.object({
  locale: z.string(),
  title: z.string(),
  html_summary: z.string(),
  html_content: z.nullable(z.string()),
});

const JsonApiNewsStory = z.object({
  id: z.string(),
  type: z.literal('stories'),
  attributes: z.object({
    enabled: z.boolean(),
    remark: z.nullable(z.string()),
    publish_date: z.string(),
    end_date: z.nullable(z.string()),
    timezone: z.string(),
    promotion: z.number(),
    promotion_end_date: z.nullable(z.string()),
    contents: z.array(JsonApiContent),
  }),
});
type JsonApiNewsStoryType = z.infer<typeof JsonApiNewsStory>;

const JsonApiNewsStoryData = z.object({
  data: z.union([JsonApiNewsStory, z.array(JsonApiNewsStory).default([])]),
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
  enabled: boolean,
  publish_date: DateType,
  contents: NewsStoryContent[]
}

const toModel = (json: JSONApiNewsStoryDocumentType): NewsStory | NewsStory[] => {
  const mapModel = (d: JsonApiDataType): NewsStory => {
    const story = <JsonApiNewsStoryType> d;
    return {
      id: story.id,
      enabled: story.attributes.enabled,
      publish_date: createDateTimeFromUTC(story.attributes.publish_date, d.attributes.timezone),
      contents: story.attributes.contents.map(content => ({
        locale: content.locale,
        title: content.title,
        summary: content.html_summary,
        content: content.html_content,
      })),
    };
  };
  if (Array.isArray(json.data)) {
    return json.data.map(mapModel);
  }
  return mapModel(json.data);
};

const setupNewsStore = () => {
  const items = ref<NewsStory[]>([]);

  const load = ({
    offset = ref(0),
    limit = ref(0),
    year = ref(0),
    month = ref(0),
    application,
    promoted = ref(false),
  } : {
    offset?: Ref<number>,
    limit?: Ref<number>,
    year?: Ref<number>,
    month?: Ref<number>,
    application?: Ref<string>,
    promoted?: Ref<boolean>
  } = {}) => {
    const { data, isValidating, error } = useSWRV<JSONApiNewsStoryDocumentType>(
      () => {
        let key = 'portal.news';
        if (promoted.value) {
          key += '.promoted';
        }
        if (application) {
          return application.value && (key + `.${application.value}`);
        }
        return key;
      },
      () => {
        let api = useHttpApi().url('/news/stories');
        if (promoted.value) {
          api = api.query({ 'filter[promoted]': promoted.value });
        }
        if (application && application.value) {
          api = api.query(({ 'filter[application]': application.value }));
        }
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
          items.value = <NewsStory[]> toModel(result.data);
        } else {
          console.log(result.error);
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
};

export const useNewsStore = defineStore('news', () => setupNewsStore());

export const usePromotedNewsStore = defineStore('promotedNews', () => {
  const store = setupNewsStore();

  return {
    items: store.items,
    load: ({
      application,
    } : {
      application?: Ref<string>
    } = {}) =>
      store.load({
        promoted: ref(true),
        application,
      }),
  };
});
