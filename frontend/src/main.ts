import { createApp } from 'vue'
import i18n from './i18n'
import { createVuestic } from 'vuestic-ui'
import { createGtm } from '@gtm-support/vue-gtm'
import vueKonva from 'vue-konva'

import pinia from './stores/index'
import router from './router'
import axiosPlugin from './plugins/axios'
import vuesticGlobalConfig from './services/vuestic-ui/global-config'
import App from './App.vue'

const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(i18n)
app.use(axiosPlugin, {
  baseUrl: '/api',
})
app.use(vueKonva)
app.use(createVuestic({ config: vuesticGlobalConfig }))

if (import.meta.env.VITE_APP_GTM_ENABLED) {
  app.use(
    createGtm({
      id: import.meta.env.VITE_APP_GTM_KEY,
      debug: false,
      vueRouter: router,
    }),
  )
}

app.mount('#app')
