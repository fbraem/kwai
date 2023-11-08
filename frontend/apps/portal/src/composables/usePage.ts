/**
 * @module
 *
 * Module that defines composable functions for getting pages from the kwai API.
 */
import { z } from 'zod';
import { JsonApiDocument, useHttpApi } from '@kwai/api';
import { JsonApiText } from '@root/composables/types';
import type { Ref } from 'vue';
import { useQuery } from '@tanstack/vue-query';
import { computed } from 'vue';

const JsonApiPage = z.object({
  id: z.string(),
  type: z.literal('pages'),
  attributes: z.object({
    texts: z.array(JsonApiText),
    remark: z.string(),
    priority: z.number(),
    enabled: z.boolean(),
  }),
});
type JsonApiPageType = z.infer<typeof JsonApiPage>;

const JsonApiPageData = z.object({
  data: z.union([JsonApiPage, z.array(JsonApiPage).default([])]),
});
const JsonApiPageDocument = JsonApiDocument.extend(JsonApiPageData.shape);
type JsonApiPageDocumentType = z.infer<typeof JsonApiPageDocument>;

interface PageText {
  locale: string,
  format: string,
  title: string,
  summary: string,
  content: string
}

export type Page = {
  id: string,
  priority: number,
  texts: PageText[]
};

const toModel = (json: JsonApiPageDocumentType): Page | Page[] => {
  const mapModel = (d: JsonApiPageType): Page => {
    return {
      id: d.id,
      priority: d.attributes.priority,
      texts: d.attributes.texts.map(text => ({
        locale: text.locale,
        format: text.format,
        title: text.title,
        summary: text.summary || '',
        content: text.content || '',
      })),
    };
  };
  if (Array.isArray(json.data)) {
    return json.data.map(mapModel);
  }
  return mapModel(json.data);
};

const getPage = (id: string) : Promise<Page> => {
  return useHttpApi().url(`/v1/pages/${id}`)
    .get()
    .json(json => {
      const result = JsonApiPageDocument.safeParse(json);
      if (result.success) {
        return toModel(result.data) as Page;
      }
      throw result.error;
    });
};

/**
 * Fetch a page.
 * @param id
 */
export const usePage = (id: Ref<string>) => {
  return useQuery({
    queryKey: ['portal/page', id],
    queryFn: () => getPage(id.value),
  });
};

const getPages = (application: string) : Promise<Page[]> => {
  const api = useHttpApi().url('/v1/pages').query({ 'filter[application]': application });
  return api.get().json(json => {
    const result = JsonApiPageDocument.safeParse(json);
    if (result.success) {
      return toModel(result.data) as Page[];
    }
    throw result.error;
  });
};

/**
 * Fetch pages for a given application. The query will become active when the application
 * does not contain an empty string.
 *
 * @param application
 */
export const usePages = (application: Ref<string>) => {
  return useQuery({
    queryKey: ['portal/pages', application],
    queryFn: ({ queryKey: [, applicationName] }) => getPages(applicationName),
    enabled: computed(() => application.value !== ''),
  });
};
