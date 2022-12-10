// axios.ts

import axios, { AxiosRequestConfig } from 'axios'
import type { App } from 'vue'

interface AxiosOptions {
  baseUrl?: string
  token?: string
}

export default {
  install: (app: App, options: AxiosOptions) => {
    const defaults = {} as AxiosRequestConfig

    defaults['baseURL'] = options.baseUrl
    defaults['headers'] = {}
    defaults['headers']['Content-Type'] = 'application/json'

    const axiosInstance = axios.create(defaults)
    app.config.globalProperties.$axios = axiosInstance

    app.provide('axios', axiosInstance)
    app.provide('axiosConfig', defaults)
  },
}
