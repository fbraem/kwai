import type { PrimeVuePTOptions } from 'primevue/config';
import type { PassThrough } from 'primevue/ts-helpers';

declare module 'index.js' {
  export = PassThrough<PrimeVuePTOptions>;
}
