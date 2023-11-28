import { z } from 'zod';
import { DateType } from '@kwai/date';
import { JsonApiData, JsonResourceIdentifier } from '@kwai/api';

export const TextSchema = z.object({
  locale: z.string(),
  title: z.string(),
  summary: z.string(),
  content: z.nullable(z.string()),
});

export interface NewsItemText {
  locale: string;
  title: string;
  summary: string;
  content: string | null;
}

export interface Application {
  id?: string;
  title: string;
  name: string;
}

export interface NewsItem {
  id?: string;
  priority: number;
  publishDate: DateType;
  texts: NewsItemText[];
  application: Application;
}

export const NewsItemSchema = JsonApiData.extend({
  type: z.literal('news_items'),
  attributes: z.object({
    priority: z.number(),
    publish_date: z.string(),
    texts: z.array(TextSchema),
  }),
  relationships: z.object({
    application: z.object({
      data: JsonResourceIdentifier,
    }),
  }),
});

export interface PageText extends NewsItemText {}

export interface Page {
  id?: string;
  priority: number;
  texts: PageText[];
  application: Application;
}

export const PageSchema = JsonApiData.extend({
  type: z.literal('pages'),
  attributes: z.object({
    texts: z.array(TextSchema),
    remark: z.string(),
    priority: z.number(),
    enabled: z.boolean(),
  }),
  relationships: z.object({
    application: z.object({
      data: JsonResourceIdentifier,
    }),
  }),
});
export type PageResource = z.infer<typeof PageSchema>;

export const ApplicationSchema = JsonApiData.extend({
  type: z.literal('applications'),
  attributes: z.object({
    name: z.string(),
    title: z.string(),
  }),
});
export type ApplicationResource = z.infer<typeof ApplicationSchema>;
