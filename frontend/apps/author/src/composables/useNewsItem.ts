import { useQuery } from '@tanstack/vue-query';
import { JsonApiDocument, useHttpApi } from '@kwai/api';
import { z } from 'zod';
import { createDateTimeFromUTC } from '@kwai/date';
import { ref, toValue } from 'vue';
import type { Ref } from 'vue';
import { TextSchema, NewsItemSchema, ApplicationSchema } from '@kwai/types';
import type { NewsItemText, NewsItem, ApplicationResource } from '@kwai/types';

interface NewsItemForAuthorText extends NewsItemText {
  format: string,
  original_summary: string,
  original_content?: string | null
}

export interface NewsItemForAuthor extends NewsItem {
  enabled: boolean,
  texts: NewsItemForAuthorText[]
}

interface NewsItemsForAuthor {
  meta: { count: number, offset: number, limit: number },
  items: NewsItemForAuthor[]
}

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
type NewsItemForAuthorResource = z.infer<typeof NewsItemAuthorSchema>;

const NewsItemDocumentSchema = JsonApiDocument.extend({
  data: z.union([NewsItemAuthorSchema, z.array(NewsItemAuthorSchema).default([])]),
  included: z.array(ApplicationSchema).default([]),
}).transform(doc => {
  const mapModel = (newsItemResource: NewsItemForAuthorResource): NewsItemForAuthor => {
    const application = doc.included.find(
      included => included.type === ApplicationSchema.shape.type.value && included.id === newsItemResource.relationships.application.data.id
    ) as ApplicationResource;

    return {
      id: newsItemResource.id,
      enabled: newsItemResource.attributes.enabled,
      priority: newsItemResource.attributes.priority,
      publishDate: createDateTimeFromUTC(newsItemResource.attributes.publish_date),
      texts: newsItemResource.attributes.texts.map(text => ({
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

  if (Array.isArray(doc.data)) {
    return {
      meta: {
        count: doc.meta?.count || 0,
        offset: doc.meta?.offset || 0,
        limit: doc.meta?.limit || 0,
      },
      items: doc.data.map(mapModel),
    };
  } else {
    return mapModel(doc.data);
  }
});

const getNewsItem = (id: string) : Promise<NewsItemForAuthor> => {
  const url = `/v1/news_items/${id}`;
  const api = useHttpApi().url(url);
  return api.get().json().then(json => {
    const result = NewsItemDocumentSchema.safeParse(json);
    if (result.success) {
      return result.data as NewsItemForAuthor;
    }
    throw result.error;
  });
};

export const useNewsItem = (id: Ref<string>) => {
  return useQuery({
    queryKey: ['author/news_items', id],
    queryFn: () => getNewsItem(toValue(id)),
  });
};

const getNewsItems = async({
  offset = null,
  limit = null,
  application = null,
} : {
    offset?: number | null,
    limit?: number | null,
    application?: string | null
  }) : Promise<NewsItemsForAuthor> => {
  let api = useHttpApi()
    .url('/v1/news_items')
    .query({ 'filter[enabled]': false })
  ;
  if (application) {
    api = api.query({ 'filter[application]': application });
  }
  if (offset) {
    api = api.query({ 'page[offset]': offset });
  }
  if (limit) {
    api = api.query({ 'page[limit]': limit });
  }
  return api.get().json().then(json => {
    const result = NewsItemDocumentSchema.safeParse(json);
    if (result.success) {
      return result.data as NewsItemsForAuthor;
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
    queryFn: () => getNewsItems({
      offset: toValue(offset),
      limit: toValue(limit),
      application: toValue(application),
    }),
  });
};
