import { JsonApiData, JsonApiDocument, useHttpApi } from '@kwai/api';
import { useQuery } from '@tanstack/vue-query';
import { z } from 'zod';

export interface Team {
  id?: string
  name: string
}

export const TeamResourceSchema = JsonApiData.extend({
  type: z.literal('teams'),
  attributes: z.object({
    name: z.string(),
  }),
});
export type TeamResource = z.infer<typeof TeamResourceSchema>;

const TeamDocumentSchema = JsonApiDocument.extend({
  data: z.union([
    TeamResourceSchema,
    z.array(TeamResourceSchema).default([]),
  ]),
}).transform(doc => {
  const mapModel = (data: TeamResource): Team => {
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
type TeamDocument = z.input<typeof TeamDocumentSchema>;

const getTeams = () : Promise<Team[]> => {
  return useHttpApi().url('/v1/trainings/teams')
    .get()
    .json()
    .then(json => {
      const result = TeamDocumentSchema.safeParse(json);
      if (result.success) {
        return result.data as Team[];
      }
      console.log(result.error);
      throw result.error;
    });
};

export const useTeams = () => {
  return useQuery({
    queryKey: ['coach/teams'],
    queryFn: () => getTeams(),
  });
};
