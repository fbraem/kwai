import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query';
import { JsonApiDocument, useHttpApi } from '@kwai/api';
import { z } from 'zod';
import { ref, toValue } from 'vue';
import type { Ref } from 'vue';
import { TextSchema, PageSchema, ApplicationSchema } from '@kwai/types';
import type { PageText, Page, ApplicationResource } from '@kwai/types';

interface PageForAuthorText extends PageText {
  format: string,
  originalSummary: string,
  originalContent: string | null
}

export interface PageForAuthor extends Page {
  enabled: boolean,
  texts: PageForAuthorText[]
  remark: string
}

interface PagesForAuthor {
  meta: { count: number, offset: number, limit: number },
  items: PageForAuthor[]
}

const TextAuthorSchema = TextSchema.extend({
  format: z.string(),
  original_summary: z.string(),
  original_content: z.nullable(z.string()),
});

const PageAuthorSchema = PageSchema.extend({
  attributes: z.object({
    enabled: z.boolean(),
    priority: z.number(),
    texts: z.array(TextAuthorSchema),
    remark: z.string(),
  }),
});
type PageForAuthorResource = z.infer<typeof PageAuthorSchema>;

const PageDocumentSchema = JsonApiDocument.extend({
  data: z.union([PageAuthorSchema, z.array(PageAuthorSchema).default([])]),
  included: z.array(ApplicationSchema).default([]),
}).transform(doc => {
  const mapModel = (pageResource: PageForAuthorResource): PageForAuthor => {
    const application = doc.included.find(
      included => included.type === ApplicationSchema.shape.type.value && included.id === pageResource.relationships.application.data.id
    ) as ApplicationResource;

    return {
      id: pageResource.id,
      enabled: pageResource.attributes.enabled,
      priority: pageResource.attributes.priority,
      texts: pageResource.attributes.texts.map(text => ({
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
      remark: pageResource.attributes.remark,
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
type PageDocument = z.input<typeof PageDocumentSchema>;

const getPage = (id: string) : Promise<PageForAuthor> => {
  const url = `/v1/pages/${id}`;
  const api = useHttpApi().url(url);
  return api.get().json().then(json => {
    const result = PageDocumentSchema.safeParse(json);
    if (result.success) {
      return result.data as PageForAuthor;
    }
    throw result.error;
  });
};

export const usePage = (id: Ref<string>, { enabled } : {enabled: Ref<boolean> } = { enabled: ref(true) }) => {
  return useQuery({
    queryKey: ['author/pages', id],
    queryFn: () => getPage(toValue(id)),
    enabled,
  });
};

const getPages = async({
  offset = null,
  limit = null,
  application = null,
} : {
    offset?: number | null,
    limit?: number | null,
    application?: string | null
  }) : Promise<PagesForAuthor> => {
  let api = useHttpApi()
    .url('/v1/pages')
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
    const result = PageDocumentSchema.safeParse(json);
    if (result.success) {
      return result.data as PagesForAuthor;
    }
    console.log(result.error);
    throw result.error;
  });
};

export const usePages = ({ application = null, offset = ref(0), limit = ref(0) } : {application?: Ref<string> | null, offset?: Ref<number>, limit?: Ref<number>}) => {
  const queryKey : { offset: Ref<number>, limit: Ref<number>, application?: Ref<string> | null} = { offset, limit };
  if (application) {
    queryKey.application = application;
  }
  return useQuery({
    queryKey: ['author/pages', queryKey],
    queryFn: () => getPages({
      offset: toValue(offset),
      limit: toValue(limit),
      application: toValue(application),
    }),
  });
};

const mutatePage = (page: PageForAuthor): Promise<PageForAuthor> => {
  const payload: PageDocument = {
    data: {
      id: page.id,
      type: 'pages',
      attributes: {
        enabled: page.enabled,
        priority: page.priority,
        remark: page.remark,
        texts: [
          {
            locale: page.texts[0].locale,
            format: page.texts[0].format,
            title: page.texts[0].title,
            summary: page.texts[0].summary,
            original_summary: page.texts[0].originalSummary,
            content: page.texts[0].content,
            original_content: page.texts[0].originalContent,
          },
        ],
      },
      relationships: {
        application: {
          data: {
            id: page.application.id,
            type: 'applications',
          },
        },
      },
    },
  };
  if (page.id) { // Update
    return useHttpApi()
      .url(`/v1/pages/${page.id}`)
      .patch(payload)
      .json(json => {
        const result = PageDocumentSchema.safeParse(json);
        if (result.success) {
          return result.data as PageForAuthor;
        }
        throw result.error;
      })
    ;
  }
  // Create
  return useHttpApi()
    .url('/v1/pages')
    .post(payload)
    .json(json => {
      const result = PageDocumentSchema.safeParse(json);
      if (result.success) {
        return result.data as PageForAuthor;
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

export const usePageMutation = ({ onSuccess } : MutationOptions = {}) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: PageForAuthor) => mutatePage(data),
    onSuccess: async(data) => {
      queryClient.setQueryData(['author/pages', data.id], data);
      if (onSuccess) {
        if (onSuccess.constructor.name === 'AsyncFunction') {
          await onSuccess();
        } else {
          onSuccess();
        }
      }
    },
    onSettled: () => queryClient.invalidateQueries({
      queryKey: ['author/pages'],
      exact: true,
    }),
  });
};
