<template>
  <va-card :color="integrationItem?.brandColor" gradient>
    <va-card-title>
      <div class="row flex align-baseline">
        <div class="flex xs6">
          <va-icon size="large" :name="integrationItem?.icon" />
          <span class="xs3 title-text">{{ integrationItem?.identity }}</span>
        </div>
        <div v-if="integrationItem?.primaryLogin && oauth_service.linked === true" class="flex xs6 chip-holder">
          <va-chip icon="fa-link" size="small" color="info" square shadow>{{ t('user.primaryLink') }}</va-chip>
        </div>
        <div v-else-if="!integrationItem?.primaryLogin && oauth_service.linked === true" class="flex xs6 chip-holder">
          <va-chip size="small" color="success" square shadow>{{ t('user.linked') }}</va-chip>
        </div>
        <div v-else-if="oauth_service.linked === false" class="flex xs6 chip-holder">
          <va-chip icon="fa-unlink" color="danger" size="small" square shadow>{{ t('user.notLinked') }}</va-chip>
        </div>
      </div>
    </va-card-title>
    <va-card-content>
      <div v-if="oauth_service.linked === true" class="row">
        <div class="flex xs12">
          <va-input
            v-model="oauth_service.identity"
            :label="t('user.linkedAccount')"
            placeholder="none"
            readonly
          />
        </div>
        <div class="flex d-flex flex-direction-column">
          <h5 class="mb-2">{{ t('user.scopes') }}</h5>
          <!-- <va-checkbox
            v-if="!oauth_service.scopes || oauth_service.scopes[0] === ''"
            v-model="checked"
            readonly
            color="success"
            class="mb-1"
            label="Authentication & Identity"
          /> -->
          <va-checkbox
            v-for="scope in oauth_service.scopes"
            :key="scope"
            v-model="checked"
            class="mb-1"
            color="primary"
            readonly
            :label="scope === '' ? t('scopes.basicAuth') : t(`scopes.$(service_name).$(scope)`)"
          />
        </div>
      </div>
    </va-card-content>
    <va-card-actions>
      <div class="row">
        <div class="flex lg12 xs12">
          <va-button 
            v-if="'linked' in oauth_service && !oauth_service.linked"
            :href="oauth_uri"
          >
            {{ t('user.linkAccount') }}
          </va-button>
          <va-progress-bar
            v-if="!('linked' in oauth_service) || (oauth_service.linked && !oauth_service.verified)"
            indeterminate
            size="small"
          />
        </div>
      </div>
      <!-- <va-button>Test</va-button> -->
    </va-card-actions>
  </va-card>
</template>

<script setup lang="ts">
  import { defineProps, ref, onMounted, onBeforeMount } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useI18n } from 'vue-i18n'
  import { useWSStore } from '../../../../stores/ws'
  import { useAuthStore } from '../../../../stores/auth'
  // import { useUserStore } from '../../../../stores/user'

  const t = useI18n().t

  const props = defineProps({
    integrationItem: { type: Object, required: true },
  })
  props.integrationItem

  var service_name = props.integrationItem?.identity.toLowerCase()

  const oauth_service = ref({} as Record<string, any>)
  const oauth_uri = ref('')

  const auth = useAuthStore()
  // const user = useUserStore()
  const ws = useWSStore()

  const route = useRoute()
  const router = useRouter()

  const checked = ref(true)

  auth.$subscribe((mutation, state) => {
    const uss = state.userServicesStatus
    if (service_name in uss) {
      oauth_service.value = uss[service_name]

      oauth_uri.value = oauth_service.value.oauth_url
      oauth_uri.value += '?response_type=code'
      oauth_uri.value += `&client_id=${encodeURIComponent(oauth_service.value.client_id)}`
      oauth_uri.value += `&redirect_uri=${encodeURIComponent(window.location.href + '/' + service_name)}`
      oauth_uri.value += `&scope=${encodeURIComponent(oauth_service.value.request_scopes?.join(' '))}`
    }

    // if (oauth_service.value.linked && !oauth_service.value.verified) {
    //   ws.sendData({
    //     class: 'vue.verify.users.services',
    //     service: service_name,
    //   })
    // }
  })

  async function handleOAuthFlow() {
    const baseURL = window.location.origin + window.location.pathname

    if (route.params.service && route.query.code && route.params.service === service_name) {
      console.log(route.query)
      ws.sendData({
        class: 'vue.users.services.oauth.flow',
        service: service_name,
        code: route.query.code,
        redirect_uri: baseURL,
      })
      router.replace('profile')
    }
  }

  ws.$onAction((event) => {
    if (event.name === 'connectSocket') {
      event.after(async () => {
        await event.store.sendData({
          class: 'vue.get.users.services.status',
          service: service_name,
        })
        await handleOAuthFlow()
      })
    }
  })

  onMounted(async () => {
    if (ws.connected && ws.socket.readyState === ws.socket.OPEN) {
      await ws.sendData({
        class: 'vue.get.users.services.status',
        service: service_name,
      })
      await handleOAuthFlow()
    }
  })
</script>

<style>
  .chip-holder {
    text-align: right;
  }
  .chip-holder {
    flex: content;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .va-card__title div div {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
</style>
