import { JsonApiData, JsonApiDocument, useHttpApi } from '@kwai/api';
import { useQuery } from '@tanstack/vue-query';
import { z } from 'zod';

export interface Coach {
  id?: string
  name: string
}

export const CoachResourceSchema = JsonApiData.extend({
  type: z.literal('coaches'),
  attributes: z.object({
    name: z.string(),
  }),
});
export type CoachResource = z.infer<typeof CoachResourceSchema>;

const CoachDocumentSchema = JsonApiDocument.extend({
  data: z.union([
    CoachResourceSchema,
    z.array(CoachResourceSchema).default([]),
  ]),
}).transform(doc => {
  const mapModel = (data: CoachResource): Coach => {
    return {
      id: data.id,
      name: data.attributes.name,
    };
  };
  if (Array.isArray(doc.data)) {
    return doc.data.map(mapModel);
  }
  return mapModel(doc.data);
});
type CoachDocument = z.input<typeof CoachDocumentSchema>;

const getCoaches = () : Promise<Coach[]> => {
  return useHttpApi().url('/v1/trainings/coaches')
    .get()
    .json()
    .then(json => {
      const result = CoachDocumentSchema.safeParse(json);
      if (result.success) {
        return result.data as Coach[];
      }
      console.log(result.error);
      throw result.error;
    });
};

export const useCoaches = () => {
  return useQuery({
    queryKey: ['portal/coaches'],
    queryFn: () => getCoaches(),
  });
};
