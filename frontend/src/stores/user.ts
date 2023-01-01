import { defineStore } from 'pinia'
import { UserSerializer, StreamerSerializer } from '../../model-ts/all'

export const useUserStore = defineStore('user', {
  state: () => {
    return {
      self: {
        username: '',
        is_authenticated: false,
        is_superuser: false,
        is_staff: false,
        streamer: {} as StreamerSerializer,
        password: '',
      } as UserSerializer,
    }
  },
  actions: {
    setSelf(selfData: UserSerializer) {
      this.$state.self = selfData
    },
  },
})
