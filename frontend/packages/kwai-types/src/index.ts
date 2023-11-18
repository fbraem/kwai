import { z } from 'zod';
import { DateType } from '@kwai/date';

export const JsonApiText = z.object({
  locale: z.string(),
  title: z.string(),
  summary: z.string(),
  content: z.nullable(z.string()),
});

export interface NewsItemText {
  locale: string,
  title: string,
  summary: string,
  content?: string | null
}

export interface Application {
  title: string,
  name: string
}

export interface NewsItem {
  id: string,
  priority: number,
  publishDate: DateType,
  texts: NewsItemText[],
  application: Application
}
