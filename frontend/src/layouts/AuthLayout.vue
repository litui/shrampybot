<template>
  <div class="auth-layout row align-content-center">
    <div class="flex xs12 pa-3 justify-center">
      <router-link class="py-2 justify-center d-flex" to="/">
        <g-s-g-live-logo class="logo" />
      </router-link>
    </div>

    <div class="flex xs12 pa-3">
      <div class="d-flex justify-center">
        <va-card class="flex auth-layout__card justify-center">
          <!-- <va-card-title class="justify-center">{{ t('auth.login_oauth') }}</va-card-title> -->
          <va-card-content class="justify-center">
            <div class="flex pa-3 justify-center">
              <router-view />
            </div>
          </va-card-content>
        </va-card>
      </div>
    </div>
  </div>
</template>

<script>
  import GSGLiveLogo from '../components/logos/GSGLiveLogo.vue'
  import { useI18n } from 'vue-i18n'
  import { watchEffect } from 'vue'
  /* Set default colour scheme to dark */
  import { useColors } from 'vuestic-ui'

  export default {
    name: 'AuthLayout',
    components: { GSGLiveLogo },
    setup() {
      const { applyPreset, setColors } = useColors()
      watchEffect(() => {
        applyPreset('dark')
        setColors({
          primary: '#FFBB22',
        })
      })

      const { t } = useI18n()
      return { t }
    },
    data() {
      return {
        selectedTabIndex: 0,
        login: {
          email: '',
          password: '',
        },
      }
    },
    computed: {
      tabIndex: {
        set(tabName) {
          this.$router.push({ name: tabName })
        },
        get() {
          return this.$route.name
        },
      },
    },
    methods: {
      async loginUser() {
        try {
          let response = await this.$axios.post('/api/token', this.login)
          let token = response.data.data.token
          localStorage.setItem('user', token)
        } catch (err) {
          console.log(err.response)
        }
      },
    },
  }
</script>

<style lang="scss">
  .auth-layout {
    min-height: 100vh;
    background-image: linear-gradient(to right, var(--va-background-primary), var(--va-white));

    &__card {
      width: 100%;
      max-width: 600px;
    }
  }

  a {
    span.logo {
      font-family: 'Revalia';
      font-size: 32pt;
      color: #ffbb22;
      #dot_text {
        font-family: 'Revalia';
        font-size: 32pt;
        color: #e42222;
      }
      #bot_text {
        font-family: 'Revalia';
        font-size: 32pt;
        color: #ffffff;
      }
    }
  }
</style>
