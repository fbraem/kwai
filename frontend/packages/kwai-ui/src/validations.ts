import { GenericValidateFunction } from 'vee-validate';

export const isStringRequired = (message: string): GenericValidateFunction<string> => (value: string): string|boolean => {
  if (value && value.trim()) {
    return true;
  }
  return message;
};
