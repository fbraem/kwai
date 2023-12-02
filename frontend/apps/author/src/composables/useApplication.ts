import { JsonApiDocument, JsonResourceIdentifier, useHttpApi } from '@kwai/api';
import { z } from 'zod';
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query';
import type { Ref } from 'vue';
import type { LocationAsRelativeRaw } from 'vue-router';
import { useRouter } from 'vue-router';
import type { Application } from '@kwai/types';

export interface ApplicationForAuthor extends Application {
  short_description: string,
  description: string
  events: boolean,
  news: boolean,
  pages: boolean,
  remark: string,
  weight: number,
}

const ApplicationSchema = JsonResourceIdentifier.extend({
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
type ApplicationResource = z.infer<typeof ApplicationSchema>;

const ApplicationDocumentSchema = JsonApiDocument.extend({
  data: z.union([ApplicationSchema, z.array(ApplicationSchema).default([])]),
}).transform(doc => {
  const mapModel = (applicationResource: ApplicationResource): ApplicationForAuthor => {
    return {
      id: applicationResource.id,
      title: applicationResource.attributes.title,
      name: applicationResource.attributes.name,
      short_description: applicationResource.attributes.short_description,
      description: applicationResource.attributes.description,
      events: applicationResource.attributes.events,
      news: applicationResource.attributes.news,
      pages: applicationResource.attributes.pages,
      remark: applicationResource.attributes.remark,
      weight: applicationResource.attributes.weight,
    };
  };
  if (Array.isArray(doc.data)) {
    return doc.data.map(mapModel);
  }
  return mapModel(doc.data);
});
type ApplicationDocument = z.input<typeof ApplicationDocumentSchema>;

const getApplications = () : Promise<ApplicationForAuthor[]> => {
  const url = '/v1/portal/applications';
  const api = useHttpApi().url(url);
  return api.get().json().then(json => {
    const result = ApplicationDocumentSchema.safeParse(json);
    if (result.success) {
      return result.data as ApplicationForAuthor[];
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

const getApplication = (id: string) : Promise<ApplicationForAuthor> => {
  const url = `/v1/portal/applications/${id}`;
  const api = useHttpApi().url(url);
  return api.get().json().then(json => {
    const result = ApplicationDocumentSchema.safeParse(json);
    if (result.success) {
      return result.data as ApplicationForAuthor;
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

const updateApplication = (application: ApplicationForAuthor): Promise<ApplicationForAuthor> => {
  const payload: ApplicationDocument = {
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
      const result = ApplicationDocumentSchema.safeParse(json);
      if (result.success) {
        return result.data as ApplicationForAuthor;
      }
      throw result.error;
    })
  ;
};

export const useApplicationMutation = (route?: LocationAsRelativeRaw) => {
  const queryClient = useQueryClient();
  const router = useRouter();

  return useMutation({
    mutationFn: (data: ApplicationForAuthor) => updateApplication(data),
    onSuccess: async(data) => {
      queryClient.setQueryData(['author/applications', data.id], data);
      if (route) {
        await router.push(route);
      }
    },
    onSettled: () => queryClient.invalidateQueries({
      queryKey: ['author/applications'],
      exact: true,
    }),
  });
};
