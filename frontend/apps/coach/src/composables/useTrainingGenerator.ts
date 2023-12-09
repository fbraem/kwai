import type { TrainingDefinition } from '@root/composables/useTrainingDefinition';
import type { DateType } from '@kwai/date';
import type { Training } from '@root/composables/useTraining';

/**
 * Generate trainings for the given period based on the training definition.
 * @param definition
 * @param start
 * @param end
 */
export const generateTrainings = (
  definition: TrainingDefinition,
  start: DateType,
  end: DateType
): Training[] => {
  const trainings = [];

  let next = start.set('day', definition.weekday);
  if (next.isBefore(start)) {
    next = next.add(1, 'week');
  }
  while (next.isBefore(end)) {
    const training: Training = {
      start_date: next.copy(definition.start_time, ['hour', 'minute']),
      end_date: next.copy(definition.end_time, ['hour', 'minute']),
      texts: [
        {
          locale: 'nl',
          format: 'md',
          title: definition.name,
          summary: '',
          originalSummary: definition.description,
          content: null,
          originalContent: null,
        },
      ],
      enabled: true,
      location: definition.location,
      remark: '',
      teams: definition.team ? [] : [definition.team!],
      cancelled: false,
      definition,
    };
    trainings.push(training);
    next = next.add(7, 'd');
  }
  return trainings;
};
