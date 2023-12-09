import { JsonApiData, JsonApiDocument, JsonResourceIdentifier, useHttpApi } from '@kwai/api';
import { z } from 'zod';
import { useQuery } from '@tanstack/vue-query';
import type { DateType } from '@kwai/date';
import { createDateTimeFromUTC } from '@kwai/date';
import type { Ref } from 'vue';
import { toValue } from 'vue';

const TeamResourceSchema = JsonApiData.extend({
  type: z.literal('teams'),
  attributes: z.object({
    name: z.string(),
  }),
});
type TeamResource = z.infer<typeof TeamResourceSchema>;

const TrainingDefinitionResourceSchema = JsonApiData.extend({
  type: z.literal('training_definitions'),
  attributes: z.object({
    name: z.string(),
    active: z.boolean(),
    description: z.string(),
    end_time: z.string(),
    location: z.string(),
    remark: z.string(),
    start_time: z.string(),
    weekday: z.number(),
  }),
  relationships: z.object({
    team: z.object({
      data: JsonResourceIdentifier.nullable(),
    }),
  }),
});
type TrainingDefinitionResource = z.infer<typeof TrainingDefinitionResourceSchema>;

type Team = {
  id: string,
  name: string,
}

export type TrainingDefinition = {
  id: string,
  active: boolean,
  description: string,
  end_time: DateType,
  location: string,
  name: string,
  remark: string,
  team: Team | null,
  start_time: DateType,
  weekday: number,
}

const TrainingDefinitionDocumentSchema = JsonApiDocument.extend({
  data: z.union([TrainingDefinitionResourceSchema, z.array(TrainingDefinitionResourceSchema).default([])]),
}).transform(doc => {
  const mapModel = (trainingDefinitionResource: TrainingDefinitionResource): TrainingDefinition => {
    let team: Team | null = null;
    if (trainingDefinitionResource.relationships.team.data?.id) {
      const teamResource = doc.included?.find(
        included => included.type === 'teams' && included.id === trainingDefinitionResource.relationships.team.data?.id
      ) as TeamResource;
      if (teamResource) {
        team = {
          id: teamResource.id!,
          name: teamResource.attributes.name,
        };
      }
    }
    return {
      id: trainingDefinitionResource.id!,
      name: trainingDefinitionResource.attributes.name,
      description: trainingDefinitionResource.attributes.description,
      end_time: createDateTimeFromUTC(trainingDefinitionResource.attributes.end_time, 'HH:mm'),
      active: trainingDefinitionResource.attributes.active,
      start_time: createDateTimeFromUTC(trainingDefinitionResource.attributes.start_time, 'HH:mm'),
      weekday: trainingDefinitionResource.attributes.weekday,
      location: trainingDefinitionResource.attributes.location,
      remark: trainingDefinitionResource.attributes.remark,
      team,
    };
  };
  if (Array.isArray(doc.data)) {
    return doc.data.map(mapModel);
  } else {
    return mapModel(doc.data);
  }
});

type TrainingDefinitionDocument = z.input<typeof TrainingDefinitionDocumentSchema>;

const getTrainingDefinition = (id: string): Promise<TrainingDefinition> => {
  return useHttpApi()
    .url(`/v1/training_definitions/${id}`)
    .get()
    .json()
    .then(json => {
      const result = TrainingDefinitionDocumentSchema.safeParse(json);
      if (result.success) {
        return result.data as TrainingDefinition;
      }
      throw result.error;
    });
};

export const useTrainingDefinition = (id: Ref<string>) => {
  return useQuery({
    queryKey: ['coach/training_definitions', id],
    queryFn: () => getTrainingDefinition(toValue(id)),
  });
};

const getTrainingDefinitions = () : Promise<TrainingDefinition[]> => {
  return useHttpApi()
    .url('/v1/training_definitions')
    .get()
    .json()
    .then(json => {
      const result = TrainingDefinitionDocumentSchema.safeParse(json);
      if (result.success) {
        return result.data as TrainingDefinition[];
      }
      throw result.error;
    });
};

export const useTrainingDefinitions = () => {
  return useQuery({
    queryKey: ['coach/training_definitions'],
    queryFn: () => getTrainingDefinitions(),
  });
};
