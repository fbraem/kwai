import type { Ref } from 'vue';
import type { DateType } from '@kwai/date';
import { createDateTimeFromUTC } from '@kwai/date';
import { z } from 'zod';
import { JsonApiDocument, JsonResourceIdentifier, useHttpApi } from '@kwai/api';
import { useQuery } from '@tanstack/vue-query';

const JsonApiEvent = z.object({
  start_date: z.string(),
  end_date: z.string(),
  location: z.nullable(z.string()).optional(),
  cancelled: z.boolean(),
  active: z.boolean(),
});

const JsonApiContent = z.object({
  locale: z.string(),
  format: z.string(),
  title: z.string(),
  summary: z.string(),
  content: z.nullable(z.string()).optional(),
});

const JsonApiTeam = z.object({
  id: z.string(),
  type: z.literal('teams'),
  attributes: z.object({
    name: z.string(),
  }),
});
type JsonApiTeamType = z.infer<typeof JsonApiTeam>;

const JsonApiCoach = z.object({
  id: z.string(),
  type: z.literal('coaches'),
  attributes: z.object({
    name: z.string(),
  }),
});

const JsonApiDefinition = z.object({
  id: z.string(),
  type: z.literal('training_definitions'),
  attributes: z.object({
    name: z.string(),
  }),
});

const JsonApiTraining = z.object({
  id: z.string(),
  type: z.literal('trainings'),
  attributes: z.object({
    event: JsonApiEvent,
    remark: z.string(),
    texts: z.array(JsonApiContent),
  }),
  relationships: z.object({
    teams: z.object({
      data: z.array(JsonResourceIdentifier),
    }),
  }),
});
type JsonApiTrainingType = z.infer<typeof JsonApiTraining>;

const JsonApiTrainingData = z.object({
  data: z.union([JsonApiTraining, z.array(JsonApiTraining).default([])]),
  included: z.array(z.union([JsonApiTeam, JsonApiCoach, JsonApiDefinition])).default([]),
});

const JsonApiTrainingDocument = JsonApiDocument.extend(JsonApiTrainingData.shape);
type JsonApiTrainingDocumentType = z.infer<typeof JsonApiTrainingDocument>;

type Team = {
  id: string,
  name: string,
}

export type Training = {
  id: string,
  cancelled: boolean,
  start_date: DateType,
  end_date: DateType,
  location?: string | null,
  title: string,
  summary: string,
  content?: string | null,
  teams: Team[],
};

interface TrainingsWithMeta {
  meta: { count: number, offset: number, limit: number },
  items: Training[]
}

const toModel = (json: JsonApiTrainingDocumentType): Training | TrainingsWithMeta => {
  const mapModel = (data: JsonApiTrainingType): Training => {
    const teams: JsonApiTeamType[] = [];
    if (data.relationships?.teams && Array.isArray(data.relationships.teams.data)) {
      data.relationships.teams.data.forEach(t => {
        const includedTeam = json.included?.find(
          included => included.type === 'teams' && included.id === t.id
        );
        if (includedTeam) {
          teams.push(includedTeam as JsonApiTeamType);
        }
      });
    }
    return {
      id: data.id,
      cancelled: data.attributes.event.cancelled,
      start_date: createDateTimeFromUTC(data.attributes.event.start_date),
      end_date: createDateTimeFromUTC(data.attributes.event.end_date),
      location: data.attributes.event.location,
      title: data.attributes.texts[0].title,
      summary: data.attributes.texts[0].summary,
      content: data.attributes.texts[0].content,
      teams: teams.map(team => ({
        id: team.id,
        name: team.attributes.name,
      })),
    };
  };
  if (Array.isArray(json.data)) {
    return {
      meta: {
        count: json.meta?.count || 0,
        offset: json.meta?.offset || 0,
        limit: json.meta?.limit || 0,
      },
      items: json.data.map(mapModel),
    };
  }
  return mapModel(json.data);
};

export interface TrainingPeriod {
  start: DateType,
  end: DateType
}

const getTrainings = (period: TrainingPeriod) : Promise<TrainingsWithMeta> => {
  return useHttpApi().url('/v1/trainings')
    .query({
      'filter[start]': period.start.format() + ' 00:00:00',
      'filter[end]': period.end.format() + ' 00:00:00',
    })
    .get()
    .json()
    .then(json => {
      const result = JsonApiTrainingDocument.safeParse(json);
      if (result.success) {
        return toModel(result.data) as TrainingsWithMeta;
      }
      console.log(result.error);
      throw result.error;
    });
};

export const useTrainings = (period : Ref<TrainingPeriod>) => {
  return useQuery({
    queryKey: ['portal/trainings', period],
    queryFn: () => getTrainings(period.value),
  });
};

export type TrainingDays = {[key: string] : Training[]};

/**
 * Returns an object will all trainings per day. The day is used as property.
 * @param trainings
 */
export const useTrainingDays = (trainings: Training[]) : TrainingDays => {
  const result : TrainingDays = {};
  trainings.forEach(training => {
    const date = training.start_date.format('YYYY-MM-DD');
    if (!result[date]) {
      result[date] = [];
    }
    result[date].push(training);
  });
  return result;
};
