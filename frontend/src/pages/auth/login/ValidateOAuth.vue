<template>
  <div class="row">
    <div class="flex" width="100%">
      <div class="item">
        <va-button color="info" gradient size="large">
          <mastodon-logo class="logo"></mastodon-logo>
        </va-button>
        <va-modal v-model="show_modal" hide-default-actions no-dismiss blur>
          <template #default>
            <va-card-title>{{ progress_title }}</va-card-title>
            <va-card-content>
              <div class="va-spacer"></div>
              <va-progress-bar :model-value="oauth_progress" size="large" class="oauth_progress" />
            </va-card-content>
          </template>
        </va-modal>
        <va-modal v-model="show_error_modal" hide-default-actions no-dismiss blur>
          <template #default>
            <va-card-title>{{ t('auth.error') }}</va-card-title>
            <va-card-content>
              <va-progress-bar
                :model-value="error_timeout"
                size="large"
                class="oauth_progress"
                color="danger"
                content-inside
              >
                {{ error_timeout_seconds }}
              </va-progress-bar>
            </va-card-content>
          </template>
        </va-modal>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  // import MastodonLogo from '../../../Components/logos/MastodonLogo.vue'
  import MastodonLogo from '../../../Components/logos/MastodonLogo.vue'
  import { computed, ref, inject, onMounted, App, getCurrentInstance } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import { useI18n } from 'vue-i18n'
  import router from '../../../router'
  import type { AxiosInstance } from 'axios'
  import { useAuthStore } from '../../../stores/auth'
  import { useUserStore } from '../../../stores/user'

  const AuthStore = useAuthStore()
  const UserStore = useUserStore()

  const axios = inject('axios') as AxiosInstance

  const { t } = useI18n()

  const route = useRoute()
  const show_modal = ref(true)
  const show_error_modal = ref(false)
  const error_timeout = ref(0)
  const error_timeout_seconds = ref(10)

  const oauth_progress = ref(0)
  const progress_title = ref(t('auth.title_oauth_validating'))

  onMounted(() => {
    getQueryParams()
  })

  const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms))

  const getQueryParams = async () => {
    await router.isReady()
    let code = route.query.code
    if (!code) {
      console.log(route.redirectedFrom)
      return false
    }
    let path = '/services/mastodon-gsglive?action=verify_user'

    console.log(document.URL.split('?')[0])

    await axios
      .post(path, {
        code: code,
      })
      .then(async (response) => {
        oauth_progress.value = 33
        progress_title.value = t('auth.title_oauth_generating')
        console.log(response.data)
        await jwt_authenticate(response.data.username, response.data.temp_password)
      })
      .catch((reason) => {
        encountered_error(reason)
      })
  }

  const encountered_error = async (reason: any) => {
    show_modal.value = false
    show_error_modal.value = true

    while (error_timeout_seconds.value > 0) {
      error_timeout_seconds.value -= 1
      error_timeout.value += 100 / 10
      await sleep(1000)
    }

    show_error_modal.value = false
    router.push({ name: 'login' })
  }

  const jwt_authenticate = async (user: string, password: string) => {
    let path = '/token/'
    await axios
      .post(path, {
        username: user,
        password: password,
      })
      .then((response) => {
        oauth_progress.value = 66
        progress_title.value = t('auth.title_oauth_synchronizing')
        AuthStore.$state.accessToken = response.data.access
        AuthStore.$state.refreshToken = response.data.refresh
        // TODO: Write data sync
        router.push({ name: 'dashboard' })
      })
      .catch((reason) => {
        encountered_error(reason)
      })
  }
</script>

<style>
  .oauth_progress {
    --va-progress-bar-width: 300px;
  }

  .oauth_runner {
    --va-progress-bar-width: 290px;
    align-self: right;
  }
</style>