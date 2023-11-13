import { JsonApiDocument, JsonResourceIdentifier, useHttpApi } from '@kwai/api';
import { z } from 'zod';
import { useQuery } from '@tanstack/vue-query';
import type { DateType } from '@kwai/date';
import { createDateTimeFromUTC } from '@kwai/date';

const JsonApiApplication = JsonResourceIdentifier.extend({
  type: z.literal('applications'),
  attributes: z.object({
    name: z.string(),
    title: z.string(),
    short_description: z.string(),
    description: z.string(),
    events: z.boolean(),
    news: z.boolean(),
    pages: z.boolean(),
    remark: z.string(),
    weight: z.number(),
    updated_at: z.string(),
    created_at: z.string(),
  }),
});
type JsonApiApplicationType = z.infer<typeof JsonApiApplication>;

const JsonApiApplicationData = z.object({
  data: z.union([JsonApiApplication, z.array(JsonApiApplication).default([])]),
});
const JsonApiApplicationDocument = JsonApiDocument.extend(JsonApiApplicationData.shape);
type JsonApiApplicationDocumentType = z.infer<typeof JsonApiApplicationDocument>;

export interface Application {
  id: string,
  name: string,
  title: string,
  short_description: string,
  description: string
  events: boolean,
  news: boolean,
  pages: boolean,
  remark: string,
  weight: number,
  updated_at: DateType | null,
  created_at: DateType
}

const toModel = (json: JsonApiApplicationDocumentType): Application | Application[] => {
  const mapModel = (d: JsonApiApplicationType): Application => {
    return {
      id: d.id,
      title: d.attributes.title,
      name: d.attributes.name,
      short_description: d.attributes.short_description,
      description: d.attributes.description,
      events: d.attributes.events,
      news: d.attributes.news,
      pages: d.attributes.pages,
      remark: d.attributes.remark,
      weight: d.attributes.weight,
      updated_at: d.attributes.updated_at ? createDateTimeFromUTC(d.attributes.updated_at) : null,
      created_at: createDateTimeFromUTC(d.attributes?.created_at),
    };
  };
  if (Array.isArray(json.data)) {
    return json.data.map(mapModel);
  }
  return mapModel(json.data);
};

const getApplications = () : Promise<Application[]> => {
  const url = '/v1/portal/applications';
  const api = useHttpApi().url(url);
  return api.get().json(json => {
    const result = JsonApiApplicationDocument.safeParse(json);
    if (result.success) {
      return <Application[]> toModel(result.data);
    }
    throw result.error;
  });
};

export const useApplications = () => {
  return useQuery<Application[]>({
    queryKey: ['author/applications'],
    queryFn: () => getApplications(),
  });
};
