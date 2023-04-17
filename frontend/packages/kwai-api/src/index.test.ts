import { describe, expect, it } from 'vitest';
import { useHttp, useHttpAuth } from './index';
import { ref } from 'vue';

describe('http tests', () => {
  it('can use a simple http', async() => {
    const res = await useHttp({
      baseUrl: 'https://www.example.com',
    })
      .get()
      .text();
    expect(res).toBeDefined();
  });

  it('can use an authenticated http', async() => {
    const accessToken = ref('TEST');
    const text = await useHttpAuth({
      baseUrl: 'https://www.example.com',
      accessToken,
    })
      .get()
      .text();
    expect(text).toBeDefined();
  });
});
