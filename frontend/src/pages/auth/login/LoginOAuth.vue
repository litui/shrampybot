<template>
  <div class="row">
    <div class="flex" width="100%">
      <div class="item">
        <va-button gradient size="large" :onclick="redirect_func">
          <span>
            <span class="vuestic-icon mb-3 pt-3">
              <va-icon name="ion-logo-twitch" size="20px" />
            </span>
            Login with Twitch
          </span>
        </va-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  // import MastodonLogo from '../../../components/logos/MastodonLogo.vue'
  import { onBeforeMount } from 'vue'
  // import { useRouter } from 'vue-router'
  import { useI18n } from 'vue-i18n'
  import { useAuthStore } from '../../../stores/auth'
  import { useUserStore } from '../../../stores/user'
  import axios from 'axios'

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
      isLoggedIn: false,
    }
  })
</script>
