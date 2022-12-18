import { defineStore } from 'pinia'
import axios, { AxiosRequestConfig } from 'axios'
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
    async testAndRefreshToken() {
      const path = '/token/verify/'
      const axiosConfig = this.getAxiosConfig()

      try {
        const bearerResponse = await axios.post(
          path,
          {
            token: this.$state.accessToken,
          },
          axiosConfig,
        )
        console.log(bearerResponse)
      } catch (error: any) {
        if (error.response.status == 401) {
          const refresh_token = this.$state.refreshToken
          const refresh_path = '/token/refresh/'

          try {
            const refreshResponse = await axios.post(
              refresh_path,
              {
                refresh: refresh_token,
              },
              {
                baseURL: '/api',
                headers: {
                  'Content-Type': 'application/json',
                },
              },
            )
            this.$state.accessToken = refreshResponse.data.access
          } catch (refreshError: any) {
            this.$state.refreshToken = ''
            this.$state.accessToken = ''
          }
        } else if (error.response.status == 500) {
          this.$state.refreshToken = ''
          this.$state.accessToken = ''
        }
      }
    }
  },
})
