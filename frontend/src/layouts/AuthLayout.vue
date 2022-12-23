<template>
  <div class="auth-layout row align-content-center">
    <div class="flex xs12 pa-3 justify-center">
      <router-link class="py-5 justify-center d-flex" to="/">
        <vuestic-logo height="32" />
      </router-link>
    </div>

    <div class="flex xs12 pa-3">
      <div class="d-flex justify-center">
        <va-card class="auth-layout__card">
          <va-card-content>
            <va-tabs v-model="tabIndex" center>
              <template #tabs>
                <!-- <va-tab name="login">{{ t('auth.login') }}</va-tab> -->
                <va-tab name="login_oauth">{{ t('auth.login_oauth') }}</va-tab>
                <!-- <va-tab name="signup">{{ t('auth.createNewAccount') }}</va-tab> -->
              </template>
            </va-tabs>

            <va-separator />

            <div class="pa-3">
              <router-view />
            </div>
          </va-card-content>
        </va-card>
      </div>
    </div>
  </div>
</template>

<script>
  import VuesticLogo from '../components/logos/GSGLiveLogo.vue'
  import { useI18n } from 'vue-i18n'
  import { watchEffect } from 'vue'
  /* Set default colour scheme to dark */
  import { useColors } from 'vuestic-ui'

  export default {
    name: 'AuthLayout',
    components: { VuesticLogo },
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
</style>
