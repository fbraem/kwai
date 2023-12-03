import { JsonApiData, JsonApiDocument, useHttpApi } from '@kwai/api';
import { z } from 'zod';
import { useQuery } from '@tanstack/vue-query';
import type { DateType } from '@kwai/date';
import { createDateTimeFromUTC } from '@kwai/date';

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
});
type TrainingDefinitionResource = z.infer<typeof TrainingDefinitionResourceSchema>;

export type TrainingDefinition = {
  id: string,
  active: boolean,
  description: string,
  end_time: DateType,
  location: string,
  name: string,
  remark: string,
  start_time: DateType,
  weekday: number,
}

const TrainingDefinitionDocumentSchema = JsonApiDocument.extend({
  data: z.union([TrainingDefinitionResourceSchema, z.array(TrainingDefinitionResourceSchema).default([])]),
}).transform(doc => {
  const mapModel = (trainingDefinitionResource: TrainingDefinitionResource): TrainingDefinition => {
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
    };
  };
  if (Array.isArray(doc.data)) {
    return doc.data.map(mapModel);
  } else {
    return mapModel(doc.data);
  }
});

type TrainingDefinitionDocument = z.input<typeof TrainingDefinitionDocumentSchema>;

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
