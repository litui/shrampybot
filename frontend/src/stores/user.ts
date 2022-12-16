import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => {
    return {
      self: {
        username: '',
        isLoggedIn: false,
      },
    }
  },
})
