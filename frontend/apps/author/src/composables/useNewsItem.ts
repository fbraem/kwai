import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query';
import { JsonApiDocument, useHttpApi } from '@kwai/api';
import { z } from 'zod';
import { createDateTimeFromUTC, formatToUTC } from '@kwai/date';
import type { DateType } from '@kwai/date';
import { ref, toValue } from 'vue';
import type { Ref } from 'vue';
import { TextSchema, NewsItemSchema, ApplicationSchema } from '@kwai/types';
import type { NewsItemText, NewsItem, ApplicationResource } from '@kwai/types';

interface NewsItemForAuthorText extends NewsItemText {
  format: string,
  originalSummary: string,
  originalContent: string | null
}

export interface NewsItemForAuthor extends NewsItem {
  endDate: DateType | null,
  enabled: boolean,
  promotionEndDate: DateType | null,
  texts: NewsItemForAuthorText[]
  remark: string
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
    promotion_end_date: z.nullable(z.string()),
    publish_date: z.string(),
    end_date: z.nullable(z.string()),
    texts: z.array(TextAuthorSchema),
    remark: z.string(),
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
      endDate: newsItemResource.attributes.end_date ? createDateTimeFromUTC(newsItemResource.attributes.end_date) : null,
      promotionEndDate: newsItemResource.attributes.promotion_end_date ? createDateTimeFromUTC(newsItemResource.attributes.promotion_end_date) : null,
      texts: newsItemResource.attributes.texts.map(text => ({
        locale: text.locale,
        format: text.format,
        title: text.title,
        summary: text.summary,
        originalSummary: text.original_summary,
        content: text.content,
        originalContent: text.original_content,
      })),
      application: {
        id: application.id,
        title: application.attributes.title,
        name: application.attributes.name,
      },
      remark: newsItemResource.attributes.remark,
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
type NewsItemDocument = z.input<typeof NewsItemDocumentSchema>;

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

export const useNewsItem = (id: Ref<string>, { enabled } : {enabled: Ref<boolean> } = { enabled: ref(true) }) => {
  return useQuery({
    queryKey: ['author/news_items', id],
    queryFn: () => getNewsItem(toValue(id)),
    enabled,
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

const mutateNewsItem = (newsItem: NewsItemForAuthor): Promise<NewsItemForAuthor> => {
  const payload: NewsItemDocument = {
    data: {
      id: newsItem.id,
      type: 'news_items',
      attributes: {
        enabled: newsItem.enabled,
        end_date: formatToUTC(newsItem.endDate),
        priority: newsItem.priority,
        promotion_end_date: formatToUTC(newsItem.promotionEndDate),
        publish_date: formatToUTC(newsItem.publishDate) as string,
        remark: newsItem.remark,
        texts: [
          {
            locale: newsItem.texts[0].locale,
            format: newsItem.texts[0].format,
            title: newsItem.texts[0].title,
            summary: newsItem.texts[0].summary,
            original_summary: newsItem.texts[0].originalSummary,
            content: newsItem.texts[0].content,
            original_content: newsItem.texts[0].originalContent,
          },
        ],
      },
      relationships: {
        application: {
          data: {
            id: newsItem.application.id,
            type: 'applications',
          },
        },
      },
    },
  };
  if (newsItem.id) { // Update
    return useHttpApi()
      .url(`/v1/news_items/${newsItem.id}`)
      .patch(payload)
      .json(json => {
        const result = NewsItemDocumentSchema.safeParse(json);
        if (result.success) {
          return result.data as NewsItemForAuthor;
        }
        throw result.error;
      })
    ;
  }
  // Create
  return useHttpApi()
    .url('/v1/news_items')
    .post(payload)
    .json(json => {
      const result = NewsItemDocumentSchema.safeParse(json);
      if (result.success) {
        return result.data as NewsItemForAuthor;
      }
      throw result.error;
    })
  ;
};

type OnSuccessCallback = () => void;
type OnSuccessAsyncCallback = () => Promise<void>;
interface MutationOptions {
  onSuccess?: OnSuccessCallback | OnSuccessAsyncCallback
}

export const useNewsItemMutation = ({ onSuccess } : MutationOptions = {}) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: NewsItemForAuthor) => mutateNewsItem(data),
    onSuccess: async(data) => {
      queryClient.setQueryData(['author/news_items', data.id], data);
      if (onSuccess) {
        if (onSuccess.constructor.name === 'AsyncFunction') {
          await onSuccess();
        } else {
          onSuccess();
        }
      }
    },
    onSettled: () => queryClient.invalidateQueries({
      queryKey: ['author/news_items'],
      exact: true,
    }),
  });
};
