import { useQuery } from '@tanstack/vue-query';
import type { JsonApiDataType } from '@kwai/api';
import { JsonApiDocument, useHttpApi } from '@kwai/api';
import { z } from 'zod';
import { createDateTimeFromUTC } from '@kwai/date';
import { ref } from 'vue';
import type { Ref } from 'vue';
import { TextSchema, NewsItemSchema, ApplicationSchema } from '@kwai/types';
import type { NewsItemText, NewsItem, ApplicationResource } from '@kwai/types';

const TextAuthorSchema = TextSchema.extend({
  format: z.string(),
  original_summary: z.string(),
  original_content: z.nullable(z.string()),
});

const NewsItemAuthorSchema = NewsItemSchema.extend({
  attributes: z.object({
    enabled: z.boolean(),
    priority: z.number(),
    publish_date: z.string(),
    texts: z.array(TextAuthorSchema),
  }),
});
type NewsItemAuthorResource = z.infer<typeof NewsItemAuthorSchema>;

const NewsItemDocumentSchema = JsonApiDocument.extend({
  data: z.union([NewsItemAuthorSchema, z.array(NewsItemAuthorSchema).default([])]),
  included: z.array(ApplicationSchema).default([]),
});
type NewsItemDocument = z.infer<typeof NewsItemDocumentSchema>;

interface NewsItemAuthorText extends NewsItemText {
  format: string,
  original_summary: string,
  original_content?: string | null
}

export interface NewsItemAuthor extends NewsItem {
  enabled: boolean,
  texts: NewsItemAuthorText[]
}

interface NewsItemsAuthorWithMeta {
  meta: { count: number, offset: number, limit: number },
  items: NewsItemAuthor[]
}

const toModel = (json: NewsItemDocument): NewsItemAuthor | NewsItemsAuthorWithMeta => {
  const mapModel = (d: JsonApiDataType): NewsItemAuthor => {
    const newsItem = d as NewsItemAuthorResource;
    const application = json.included.find(
      included => included.type === ApplicationSchema.shape.type.value && included.id === newsItem.relationships.application.data.id
    ) as ApplicationResource;

    return {
      id: newsItem.id,
      enabled: newsItem.attributes.enabled,
      priority: newsItem.attributes.priority,
      publishDate: createDateTimeFromUTC(newsItem.attributes.publish_date),
      texts: newsItem.attributes.texts.map(text => ({
        locale: text.locale,
        format: text.format,
        title: text.title,
        summary: text.summary,
        original_summary: text.original_summary,
        content: text.content,
        original_content: text.original_content,
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
        count: json.meta?.count || 0,
        offset: json.meta?.offset || 0,
        limit: json.meta?.limit || 0,
      },
      items: json.data.map(mapModel),
    };
  }
  return mapModel(json.data);
};

const getNewsItem = (id: string) : Promise<NewsItem> => {
  const url = `/v1/news_items/${id}`;
  const api = useHttpApi().url(url);
  return api.get().json().then(json => {
    const result = NewsItemDocumentSchema.safeParse(json);
    if (result.success) {
      return toModel(result.data) as NewsItem;
    }
    throw result.error;
  });
};

export const useNewsItem = (id: string) => {
  return useQuery({
    queryKey: ['author/news_items', id],
    queryFn: () => getNewsItem(id),
  });
};

const getNewsItems = async({
  offset = null,
  limit = null,
  application = null,
} : {
    offset?: Ref<number> | null,
    limit?: Ref<number> | null,
    application?: Ref<string> | null
  }) : Promise<NewsItemsAuthorWithMeta> => {
  let api = useHttpApi()
    .url('/v1/news_items')
    .query({ 'filter[enabled]': false })
  ;
  if (application) {
    api = api.query({ 'filter[application]': application.value });
  }
  if (offset) {
    api = api.query({ 'page[offset]': offset.value });
  }
  if (limit) {
    api = api.query({ 'page[limit]': limit.value });
  }
  return api.get().json().then(json => {
    const result = NewsItemDocumentSchema.safeParse(json);
    if (result.success) {
      return toModel(result.data) as NewsItemsAuthorWithMeta;
    }
    throw result.error;
  });
};

export const useNewsItems = ({ application = null, offset = ref(0), limit = ref(0) } : {application?: Ref<string> | null, offset?: Ref<number>, limit?: Ref<number>}) => {
  const queryKey : { offset: Ref<number>, limit: Ref<number>, application?: Ref<string> | null} = { offset, limit };
  if (application) {
    queryKey.application = application;
  }
  return useQuery({
    queryKey: ['author/news_items', queryKey],
    queryFn: () => getNewsItems({ offset, limit, application }),
  });
};
