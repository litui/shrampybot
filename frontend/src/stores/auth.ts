import { defineStore } from 'pinia'
import { AxiosRequestConfig } from 'axios'
import { useLocalStorage } from '@vueuse/core'

export const useAuthStore = defineStore('auth', {
  state: () => {
    const accessToken = useLocalStorage('accessToken', '')
    const refreshToken = useLocalStorage('refreshToken', '')

    return { accessToken, refreshToken }
  },
  actions: {
    getAxiosConfig() {
      return {
        baseURL: '/api',
        headers: {
          Authorization: `Bearer ${this.accessToken}`,
          'Content-Type': 'application/json',
        },
      } as AxiosRequestConfig
    },
  },
})
