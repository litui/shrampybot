import { defineStore } from 'pinia'

interface SelfStore {
  username: string
  isLoggedIn: boolean
  is_authenticated?: boolean
  is_superuser?: boolean
  is_staff?: boolean
  streamer?: any
}

export const useUserStore = defineStore('user', {
  state: () => {
    return {
      self: {
        username: '',
        isLoggedIn: false,
        is_authenticated: false,
        is_superuser: false,
        is_staff: false,
        streamer: {},
      } as SelfStore,
    }
  },
  actions: {
    setSelf(selfData: SelfStore) {
      this.$state.self = selfData
    },
  },
})
