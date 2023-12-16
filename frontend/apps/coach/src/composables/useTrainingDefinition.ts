import { JsonApiData, JsonApiDocument, JsonResourceIdentifier, useHttpApi } from '@kwai/api';
import { z } from 'zod';
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query';
import type { DateType } from '@kwai/date';
import { createDateTimeFromUTC, formatToUTC } from '@kwai/date';
import type { Ref } from 'vue';
import { toValue } from 'vue';
import type { Team } from '@root/composables/useTeam';

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
    }).optional(),
  }).optional(),
});
type TrainingDefinitionResource = z.infer<typeof TrainingDefinitionResourceSchema>;

export type TrainingDefinition = {
  id?: string,
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
    if (trainingDefinitionResource.relationships?.team?.data?.id) {
      const teamResource = doc.included?.find(
        included => included.type === 'teams' && included.id === trainingDefinitionResource.relationships?.team?.data?.id
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

const mutateTrainingDefinition = (trainingDefinition: TrainingDefinition) : Promise<TrainingDefinition> => {
  const payload: TrainingDefinitionDocument = {
    data: {
      id: trainingDefinition.id,
      type: 'training_definitions',
      attributes: {
        name: trainingDefinition.name,
        active: trainingDefinition.active,
        description: trainingDefinition.description,
        start_time: formatToUTC(trainingDefinition.start_time, 'HH:mm')!,
        end_time: formatToUTC(trainingDefinition.end_time, 'HH:mm')!,
        location: trainingDefinition.location,
        remark: trainingDefinition.remark,
        weekday: trainingDefinition.weekday,
      },
      relationships: {
        team: trainingDefinition.team
          ? {
              data: {
                id: trainingDefinition.team.id,
                type: 'teams',
              },
            }
          : { data: null },
      },
    },
  };
  if (trainingDefinition.id) {
    return useHttpApi()
      .url(`/v1/training_definitions/${trainingDefinition.id}`)
      .patch(payload)
      .json()
      .then(json => {
        const result = TrainingDefinitionDocumentSchema.safeParse(json);
        if (result.success) {
          return result.data as TrainingDefinition;
        }
        throw result.error;
      });
  }
  return useHttpApi()
    .url('/v1/training_definitions')
    .post()
    .json()
    .then(json => {
      const result = TrainingDefinitionDocumentSchema.safeParse(json);
      if (result.success) {
        return result.data as TrainingDefinition;
      }
      throw result.error;
    });
};

type OnSuccessCallback = (resource: TrainingDefinition) => void;
type OnSuccessAsyncCallback = (resource: TrainingDefinition) => Promise<void>;
interface MutationOptions {
  onSuccess?: OnSuccessCallback | OnSuccessAsyncCallback
}

export const useTrainingDefinitionMutation = ({ onSuccess } : MutationOptions = {}) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: TrainingDefinition) => mutateTrainingDefinition(data),
    onSuccess: async(data: TrainingDefinition) => {
      queryClient.setQueryData(['coach/training_definitions', data.id], data);
      if (onSuccess) {
        if (onSuccess.constructor.name === 'AsyncFunction') {
          await onSuccess(data);
        } else {
          onSuccess(data);
        }
      }
    },
    onSettled: () => queryClient.invalidateQueries({
      queryKey: ['coach/training_definitions'],
      exact: true,
    }),
  });
};
