import { useRouter } from 'vue-router';

export const useGoBack = (defaultRouteName: string) => {
  const router = useRouter();

  return async() => {
    if (router.options.history.state.back) {
      router.go(-1);
    }
    await router.replace({ name: defaultRouteName });
  };
};
