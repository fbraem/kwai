import { useQuery } from '@tanstack/vue-query';
import type { JsonApiDataType } from '@kwai/api';
import { JsonApiDocument, JsonResourceIdentifier, useHttpApi } from '@kwai/api';
import { z } from 'zod';
import { createDateTimeFromUTC } from '@kwai/date';
import type { DateType } from '@kwai/date';
import { ref } from 'vue';
import type { Ref } from 'vue';

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
type JsonApiApplicationType = z.infer<typeof JsonApiApplication>;

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

interface Application {
  title: string,
  name: string
}

export interface NewsItem {
  id: string,
  priority: number,
  publishDate: DateType,
  texts: NewsItemText[],
  application: Application
}

interface NewsItemsWithMeta {
  meta: { count: number, offset: number, limit: number },
  items: NewsItem[]
}

const toModel = (json: JSONApiNewsItemDocumentType): NewsItem | NewsItemsWithMeta => {
  const mapModel = (d: JsonApiDataType): NewsItem => {
    const newsItem = <JsonApiNewsItemType> d;
    const application = <JsonApiApplicationType> json.included.find(
      included => included.type === JsonApiApplication.shape.type.value && included.id === newsItem.relationships.application.data.id
    );

    return {
      id: newsItem.id,
      priority: newsItem.attributes.priority,
      publishDate: createDateTimeFromUTC(newsItem.attributes.publish_date),
      texts: newsItem.attributes.texts.map(text => ({
        locale: text.locale,
        title: text.title,
        summary: text.summary,
        content: text.content,
      })),
      application: {
        title: application.attributes.title,
        name: application.attributes.name,
      },
    };
  };
  if (Array.isArray(json.data)) {
    return {
      meta: {
        count: json.meta.count,
        offset: json.meta.offset,
        limit: json.meta.offset,
      },
      items: json.data.map(mapModel),
    };
  }
  return mapModel(json.data);
};

const getNewsItem = (id: string) : Promise<NewsItem> => {
  const url = `/v1/news_items/${id}`;
  const api = useHttpApi().url(url);
  return api.get().json(json => {
    const result = JsonApiNewsItemDocument.safeParse(json);
    if (result.success) {
      return <NewsItem> toModel(result.data);
    }
    throw result.error;
  });
};

export const useNewsItem = (id: string) => {
  return useQuery<NewsItem>({
    queryKey: ['portal/news_items', id],
    queryFn: () => getNewsItem(id),
  });
};

const getNewsItems = (options: {
    offset: Ref<number>,
    limit: Ref<number>,
  }) : Promise<NewsItemsWithMeta> => {
  const api = useHttpApi().url('/v1/news_items');
  return api.get().json(json => {
    const result = JsonApiNewsItemDocument.safeParse(json);
    if (result.success) {
      return toModel(result.data);
    }
    throw result.error;
  });
};

const getPromotedNewsItems = () : Promise<NewsItemsWithMeta> => {
  const api = useHttpApi().url('/v1/portal/news');
  return api.get().json(json => {
    const result = JsonApiNewsItemDocument.safeParse(json);
    if (result.success) {
      return toModel(result.data);
    }
    throw result.error;
  });
};

export const useNewsItems = ({ promoted = false, offset = ref(0), limit = ref(0) } : {promoted?: boolean, offset?: Ref<number>, limit?: Ref<number>}) => {
  if (promoted) {
    return useQuery<NewsItemsWithMeta>({
      queryKey: ['portal/promoted_news_items'],
      queryFn: () => getPromotedNewsItems(),
    });
  } else {
    return useQuery<NewsItemsWithMeta>({
      queryKey: ['portal/news_items'],
      queryFn: () => getNewsItems({ offset, limit }),
    });
  }
};
