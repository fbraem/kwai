import { defineComponent } from 'vue';
import { mount } from '@vue/test-utils';
import { VueQueryPlugin } from '@tanstack/vue-query';
import { expect, vi } from 'vitest';
import { useTeamMembers } from '@root/composables/useTeamMember';

describe('useTeamMembers e2e tests', () => {
  it('can get team members', async() => {
    const TestComponent = defineComponent({
      setup() {
        return useTeamMembers({});
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
    const teamMembers = wrapper.vm.data;
    expect(teamMembers).toBeDefined();
  });
});
