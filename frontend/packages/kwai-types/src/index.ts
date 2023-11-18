import { z } from 'zod';

export const JsonApiText = z.object({
  locale: z.string(),
  format: z.string(),
  title: z.string(),
  summary: z.string(),
  content: z.nullable(z.string()),
});
