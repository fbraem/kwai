import type { Ref, MaybeRef } from 'vue';
import type { DateType } from '@kwai/date';
import { createDateTimeFromUTC, formatToUTC, now } from '@kwai/date';
import { z } from 'zod';
import { JsonApiData, JsonApiDocument, JsonResourceIdentifier, useHttpApi } from '@kwai/api';
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query';
import { EventSchema, TextSchema } from '@kwai/types';
import { computed, ref, toValue } from 'vue';

const TeamResourceSchema = JsonApiData.extend({
  type: z.literal('teams'),
  attributes: z.object({
    name: z.string(),
  }),
});
type TeamResource = z.infer<typeof TeamResourceSchema>;

const CoachResourceSchema = JsonApiData.extend({
  type: z.literal('training_coaches'),
  attributes: z.object({
    name: z.string(),
  }),
});

const DefinitionResourceSchema = JsonApiData.extend({
  type: z.literal('training_definitions'),
  attributes: z.object({
    name: z.string(),
  }),
});
type DefinitionResource = z.infer<typeof DefinitionResourceSchema>;

type TrainingDefinition = {
  id: string,
  name: string
};

const TrainingTextSchema = TextSchema.extend({
  format: z.string(),
  original_summary: z.string(),
  original_content: z.nullable(z.string()),
});

const TrainingCoachSchema = z.object({
  id: z.string(),
  head: z.boolean(),
  present: z.boolean(),
  payed: z.boolean(),
});

const TrainingResourceSchema = JsonApiData.extend({
  type: z.literal('trainings'),
  attributes: z.object({
    event: EventSchema,
    remark: z.string(),
    texts: z.array(TrainingTextSchema),
    coaches: z.array(TrainingCoachSchema).default([]),
  }),
  relationships: z.object({
    teams: z.object({
      data: z.array(JsonResourceIdentifier),
    }),
    definition: z.object({
      data: JsonResourceIdentifier.nullable(),
    }),
    coaches: z.object({
      data: z.array(JsonResourceIdentifier),
    }),
  }),
});
type TrainingResource = z.infer<typeof TrainingResourceSchema>;

type Team = {
  id: string,
  name: string,
}

interface TrainingText {
  locale: string,
  format: string,
  title: string,
  summary: string,
  originalSummary: string,
  content: string | null,
  originalContent: string | null
}

export type Training = {
  id?: string,
  cancelled: boolean,
  enabled: boolean,
  start_date: DateType,
  end_date: DateType,
  location: string | null,
  texts: TrainingText[],
  remark: string,
  teams: Team[],
  definition: TrainingDefinition | null
};

interface Trainings {
  meta: { count: number, offset: number, limit: number },
  items: Training[]
}

const TrainingDocumentSchema = JsonApiDocument.extend({
  data: z.union([
    TrainingResourceSchema,
    z.array(TrainingResourceSchema).default([]),
  ]),
  included: z.array(
    z.union([
      TeamResourceSchema,
      CoachResourceSchema,
      DefinitionResourceSchema,
    ])
  ).default([]),
}).transform(doc => {
  const mapModel = (data: TrainingResource): Training => {
    const teams: TeamResource[] = [];
    if (data.relationships?.teams && Array.isArray(data.relationships.teams.data)) {
      data.relationships.teams.data.forEach(t => {
        const includedTeam = doc.included?.find(
          included => included.type === 'teams' && included.id === t.id
        );
        if (includedTeam) {
          teams.push(includedTeam as TeamResource);
        }
      });
    }
    let definition : TrainingDefinition | null = null;
    if (data.relationships.definition.data?.id) {
      const definitionResource = doc.included.find(
        included => included.type === DefinitionResourceSchema.shape.type.value && included.id === data.relationships.definition.data?.id
      ) as DefinitionResource;
      if (definitionResource) {
        definition = {
          id: definitionResource.id!,
          name: definitionResource.attributes.name,
        };
      }
    }
    return {
      id: data.id,
      cancelled: data.attributes.event.cancelled,
      enabled: data.attributes.event.active,
      start_date: createDateTimeFromUTC(data.attributes.event.start_date),
      end_date: createDateTimeFromUTC(data.attributes.event.end_date),
      location: data.attributes.event.location,
      texts: data.attributes.texts.map(text => ({
        locale: text.locale,
        format: text.format,
        title: text.title,
        summary: text.summary,
        originalSummary: text.original_summary,
        content: text.content,
        originalContent: text.original_content,
      })),
      remark: data.attributes.remark,
      teams: teams.map((team) : Team => ({
        id: team.id!,
        name: team.attributes.name,
      })),
      definition,
    };
  };
  if (Array.isArray(doc.data)) {
    return {
      meta: {
        count: doc.meta?.count || 0,
        offset: doc.meta?.offset || 0,
        limit: doc.meta?.limit || 0,
      },
      items: doc.data.map(mapModel),
    };
  }
  return mapModel(doc.data);
});
type TrainingDocument = z.input<typeof TrainingDocumentSchema>;

export const usePeriod = ({ start, end } : {start?: MaybeRef<DateType>, end?: MaybeRef<DateType>} = {}) => {
  const today = now();
  return {
    start: ref(start ?? today.startOf('month')),
    end: ref(end ?? today.endOf('month')),
  };
};

const getTrainings = ({ start, end } : {start: DateType, end: DateType}) : Promise<Trainings> => {
  return useHttpApi().url('/v1/trainings')
    .query({
      'filter[start]': start.format() + ' 00:00:00',
      'filter[end]': end.format() + ' 00:00:00',
      'filter[active]': false,
    })
    .get()
    .json()
    .then(json => {
      const result = TrainingDocumentSchema.safeParse(json);
      if (result.success) {
        return result.data as Trainings;
      }
      console.log(result.error);
      throw result.error;
    });
};

export const useTrainings = ({ start, end } : {start: MaybeRef<DateType>, end: MaybeRef<DateType>}) => {
  return useQuery({
    queryKey: computed(() => [
      'portal/trainings',
      toValue(start)?.format('YYYY-MM-DD'),
      toValue(end)?.format('YYYY-MM-DD'),
    ]),
    queryFn: () => getTrainings({ start: toValue(start), end: toValue(end) }),
  });
};

const getTraining = (id: string) => {
  return useHttpApi()
    .url(`/v1/trainings/${id}`)
    .get()
    .json()
    .then(json => {
      const result = TrainingDocumentSchema.safeParse(json);
      if (result.success) {
        return result.data as Training;
      }
      console.log(result.error);
      throw result.error;
    });
};
export const useTraining = (id: MaybeRef<string>, { enabled } : { enabled: Ref<boolean> } = { enabled: ref(true) }) => {
  return useQuery({
    queryKey: ['coach/trainings', id],
    queryFn: () => getTraining(toValue(id)),
    enabled,
  });
};

const mutateTraining = (training: Training) : Promise<Training> => {
  const payload: TrainingDocument = {
    data: {
      id: training.id,
      type: 'trainings',
      attributes: {
        event: {
          start_date: formatToUTC(training.start_date) as string,
          end_date: formatToUTC(training.end_date) as string,
          cancelled: training.cancelled,
          active: training.enabled,
          location: training.location,
        },
        remark: training.remark,
        texts: [
          {
            locale: training.texts[0].locale,
            format: training.texts[0].format,
            title: training.texts[0].title,
            summary: training.texts[0].summary,
            original_summary: training.texts[0].originalSummary,
            content: training.texts[0].content,
            original_content: training.texts[0].originalContent,
          },
        ],
        coaches: [],
      },
      relationships: {
        teams: {
          data: training.teams.map(team => ({
            id: team.id,
            type: 'teams',
          })),
        },
        definition: training.definition
          ? {
              data: {
                id: training.definition.id,
                type: 'training_definitions',
              },
            }
          : { data: null },
        coaches: {
          data: [],
        },
      },
    },
  };
  if (training.id) { // Update
    return useHttpApi()
      .url(`/v1/trainings/${training.id}`)
      .patch(payload)
      .json(json => {
        const result = TrainingDocumentSchema.safeParse(json);
        if (result.success) {
          return result.data as Training;
        }
        throw result.error;
      });
  }
  // Create
  return useHttpApi()
    .url('/v1/trainings')
    .post(payload)
    .json(json => {
      const result = TrainingDocumentSchema.safeParse(json);
      if (result.success) {
        return result.data as Training;
      }
      throw result.error;
    });
};

type MutationContext = {
  index: number
}
type MutationVariable = {
  training: Training,
  context?: MutationContext
}

type OnSuccessCallback = (resource: Training, context?: MutationContext) => void;
type OnSuccessAsyncCallback = (resource: Training, context?: MutationContext) => Promise<void>;
interface MutationOptions {
  onSuccess?: OnSuccessCallback | OnSuccessAsyncCallback
}

export const useTrainingMutation = ({ onSuccess } : MutationOptions = {}) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: MutationVariable) => mutateTraining(data.training),
    onSuccess: async(data: Training, variables: MutationVariable) => {
      queryClient.setQueryData(['coach/trainings', data.id], data);
      if (onSuccess) {
        if (onSuccess.constructor.name === 'AsyncFunction') {
          await onSuccess(data, variables.context);
        } else {
          onSuccess(data, variables.context);
        }
      }
    },
    onSettled: () => queryClient.invalidateQueries({
      queryKey: ['coach/trainings'],
      exact: true,
    }),
  });
};
