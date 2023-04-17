import { reactive, Ref, toRefs } from "vue"

interface State {
    isOpen: Boolean
}

const state: State = reactive({
    isOpen: false
})

export function useSidebar() {
    return {
        ...toRefs(state)
    }
}
