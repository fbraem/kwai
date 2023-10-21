import { defineStore } from 'pinia';
import type { Ref } from 'vue';
import { ref, watch } from 'vue';
import type { JsonApiDataType } from '@kwai/api';
import { JsonApiDocument, JsonResourceIdentifier, useHttpApi } from '@kwai/api';
import type { DateType } from '@kwai/date';
import { createDateTimeFromUTC } from '@kwai/date';
import { z } from 'zod';
import useSWRV from 'swrv';

const JsonApiText = z.object({
  locale: z.string(),
  format: z.string(),
  title: z.string(),
  summary: z.string(),
  content: z.nullable(z.string()),
});

const JsonApiNewsItem = z.object({
  id: z.string(),
  type: z.literal('news_items'),
  attributes: z.object({
    priority: z.number(),
    publish_date: z.string(),
    texts: z.array(JsonApiText),
  }),
  relationships: z.object({
    application: z.object({
      data: JsonResourceIdentifier,
    }),
  }),
});
type JsonApiNewsItemType = z.infer<typeof JsonApiNewsItem>;

const JsonApiApplication = z.object({
  id: z.string(),
  type: z.literal('applications'),
  attributes: z.object({
    name: z.string(),
    title: z.string(),
  }),
});

const JsonApiNewsItemData = z.object({
  data: z.union([JsonApiNewsItem, z.array(JsonApiNewsItem).default([])]),
  included: z.array(JsonApiApplication).default([]),
});
const JsonApiNewsItemDocument = JsonApiDocument.extend(JsonApiNewsItemData.shape);
type JSONApiNewsItemDocumentType = z.infer<typeof JsonApiNewsItemData>;

interface NewsItemText {
  locale: string,
  title: string,
  summary: string,
  content?: string | null
}

export interface NewsItem {
  id: string,
  priority: number,
  publish_date: DateType,
  texts: NewsItemText[]
}

const toModel = (json: JSONApiNewsItemDocumentType): NewsItem | NewsItem[] => {
  const mapModel = (d: JsonApiDataType): NewsItem => {
    const newsItem = <JsonApiNewsItemType> d;
    return {
      id: newsItem.id,
      priority: newsItem.attributes.priority,
      publish_date: createDateTimeFromUTC(newsItem.attributes.publish_date, d.attributes.timezone),
      texts: newsItem.attributes.texts.map(text => ({
        locale: text.locale,
        title: text.title,
        summary: text.summary,
        content: text.content,
      })),
    };
  };
  if (Array.isArray(json.data)) {
    return json.data.map(mapModel);
  }
  return mapModel(json.data);
};

export const useNewsStore = defineStore('news', () => {
  const items = ref<NewsItem[]>([]);

  const load = ({
    offset = ref(0),
    limit = ref(0),
  }: {
    offset?: Ref<number>,
    limit?: Ref<number>
  } = {}) => {
    const { data, isValidating, error } = useSWRV<JSONApiNewsItemDocumentType>(
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
        const result = JsonApiNewsItemDocument.safeParse(nv);
        if (result.success) {
          items.value = <NewsItem[]>toModel(result.data);
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
