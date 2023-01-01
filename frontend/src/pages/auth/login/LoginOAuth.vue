<template>
  <div class="row">
    <div class="flex xs12">
      <div class="login-area">
        <va-button color="#9146FF" gradient size="large" :onclick="redirect_func">
          <span>
            <span class="vuestic-icon mb-3 pt-3">
              <va-icon name="ion-logo-twitch" size="20px" />
            </span>
            {{ t('auth.loginWithTwitch') }}
          </span>
        </va-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  // import MastodonLogo from '../../../components/logos/MastodonLogo.vue'
  import { onBeforeMount, onMounted } from 'vue'
  // import { useRouter } from 'vue-router'
  import { useI18n } from 'vue-i18n'
  import { useAuthStore } from '../../../stores/auth'
  import { useUserStore } from '../../../stores/user'
  import { useToast } from 'vuestic-ui'
  import axios from 'axios'
  import { VWAP } from '@amcharts/amcharts5/.internal/charts/stock/indicators/VWAP'

  const AuthStore = useAuthStore()
  const UserStore = useUserStore()

  const { t } = useI18n()

  async function redirect_func() {
    const response = await axios.get('/api/services/twitch', {
      headers: {
        'Content-Type': 'application/json',
      },
    })
    if (response.status === 200) {
      let target_url = response.data.oauth_login_url

      let return_path = window.location.origin
      let return_endpoint = '/auth/validate_oauth'
      let return_encoded = encodeURIComponent(return_path + return_endpoint)
      let scope = response.data.broad_scope.replace(/ /g, '+')
      let client_id = response.data.api_client_id

      let final_url = `${target_url}?redirect_uri=${return_encoded}&client_id=${client_id}&response_type=code&force_login=true&scope=${scope}`

      window.location.href = final_url
    }
  }

  onBeforeMount(() => {
    AuthStore.$state.accessToken = ''
    AuthStore.$state.refreshToken = ''
    UserStore.$state.self = {
      username: '',
      password: '',
      is_authenticated: false,
    }
  })

  onMounted(() => {
    const { init, close, closeAll } = useToast()

    init({
      title: 'Cookie Agreement',
      message: `
        <p>ShrampyBot only makes minimal use of browser cookies for some of its core functionality but does use third party features (notably Twitch and Discord) that may involve cookies for tracking and other purposes.</p>
        <p>By continuing to log in to ShrampyBot you agree to the terms of our cookie usage as well as the terms of those third parties.</p>
      `,
      dangerouslyUseHtmlString: true,
      closeable: false,
      customClass: 'cookie-agreement',
      duration: 0,
      position: 'bottom-left',
    })
  })
</script>

<style lang="scss">
  .cookie-agreement {
    margin: 0 0 0 0;
    bottom: 16px;
    left: 16px;
  }
  .cookie-agreement p {
    margin-block-end: 1em;
  }
  .login-area {
    text-align: center;
    align-items: center;
    justify-items: center;
    width: 100%;
  }
</style>
