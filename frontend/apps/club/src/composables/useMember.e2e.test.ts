import { describe, expect, it, vi } from 'vitest';
import { defineComponent } from 'vue';
import { useMembers } from '@root/composables/useMember';
import { mount } from '@vue/test-utils';
import { VueQueryPlugin } from '@tanstack/vue-query';
import { useHttpLogin } from '@kwai/api';
import * as process from 'node:process';

const noUser = process.env.KWAI_USER === undefined;

describe('useMember e2e tests', () => {
  it.skipIf(noUser)('can get members', async() => {
    await useHttpLogin(
      {
        username: process.env.KWAI_USER as string,
        password: process.env.KWAI_PASSWORD as string,
      }
    );

    const TestComponent = defineComponent({
      setup() {
        return useMembers({});
      },
      template: '<span>Test Component</span>',
    });
    const wrapper = mount(TestComponent, {
      global: {
        plugins: [VueQueryPlugin],
      },
    });
    await vi.waitFor(() => {
      expect(wrapper.vm.isPending).toBeFalsy();
    }, { timeout: 1000 });
    const members = wrapper.vm.data;
    expect(members).toBeDefined();
  });
});
