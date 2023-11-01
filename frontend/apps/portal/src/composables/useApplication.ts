import { JsonApiDocument, useHttpApi } from '@kwai/api';
import { z } from 'zod';
import { useQuery } from '@tanstack/vue-query';

const JsonApiApplication = z.object({
  id: z.string(),
  type: z.literal('applications'),
  attributes: z.object({
    name: z.string(),
    title: z.string(),
    short_description: z.string(),
    description: z.string(),
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
}

const toModel = (json: JsonApiApplicationDocumentType): Application | Application[] => {
  const mapModel = (d: JsonApiApplicationType): Application => {
    return {
      id: d.id,
      title: d.attributes.title,
      name: d.attributes.name,
      short_description: d.attributes.short_description,
      description: d.attributes.description,
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
    queryKey: ['portal/applications'],
    queryFn: () => getApplications(),
    staleTime: 10 * 1000 /* 10 seconds */,
  });
};
