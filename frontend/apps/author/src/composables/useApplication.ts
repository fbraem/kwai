import { JsonApiDocument, JsonResourceIdentifier, useHttpApi } from '@kwai/api';
import { z } from 'zod';
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query';
import type { Ref } from 'vue';

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
      return toModel(result.data) as Application[];
    }
    throw result.error;
  });
};

export const useApplications = () => {
  return useQuery({
    queryKey: ['author/applications'],
    queryFn: () => getApplications(),
  });
};

const getApplication = (id: string) : Promise<Application> => {
  const url = `/v1/portal/applications/${id}`;
  const api = useHttpApi().url(url);
  return api.get().json(json => {
    const result = JsonApiApplicationDocument.safeParse(json);
    if (result.success) {
      return toModel(result.data) as Application;
    }
    throw result.error;
  });
};

export const useApplication = (id: Ref<string>) => {
  return useQuery({
    queryKey: ['author/applications', id],
    queryFn: () => getApplication(id.value),
  });
};

const updateApplication = (application: Application): Promise<Application> => {
  const payload: JsonApiApplicationDocumentType = {
    data: {
      id: application.id,
      type: 'applications',
      attributes: {
        name: application.name,
        title: application.title,
        short_description: application.short_description,
        description: application.description,
        events: application.events,
        news: application.news,
        pages: application.pages,
        remark: application.remark,
        weight: application.weight,
      },
    },
  };
  return useHttpApi()
    .url(`/v1/portal/applications/${application.id}`)
    .patch(payload)
    .json(json => {
      const result = JsonApiApplicationDocument.safeParse(json);
      if (result.success) {
        return toModel(result.data) as Application;
      }
      throw result.error;
    })
  ;
};

export const useApplicationMutation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: Application) => updateApplication(data),
    onSuccess: (data, variables) => {
      queryClient.setQueryData(['author/applications', data.id], data);
    },
    onSettled: () => queryClient.invalidateQueries({
      queryKey: ['author/applications'],
      exact: true,
    }),
  });
};
