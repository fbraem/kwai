import { JsonApiData } from '@kwai/api';
import { z } from 'zod';

export const CountryResourceSchema = JsonApiData.extend({
  type: z.literal('countries'),
  attributes: z.object({
    iso_2: z.string(),
    iso_3: z.string(),
    name: z.string(),
  }),
});
export type CountryResource = z.infer<typeof CountryResourceSchema>;
