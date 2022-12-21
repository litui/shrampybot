<template>
  <va-card :color="integrationItem?.brandColor" gradient>
    <va-card-title>
      <div class="row align-baseline">
        <div class="flex md6">
          <va-icon size="large" :name="integrationItem?.icon" />
          <span class="title-text">{{ integrationItem?.identity }}</span>
        </div>
        <!-- <v-spacer /> -->
        <div v-if="integrationItem?.primaryLogin && oauth_service.linked === true" class="flex md6 chip-holder">
          <va-chip icon="fa-link" size="small" color="info" square shadow>{{ t('user.primaryLink') }}</va-chip>
        </div>
        <div v-else-if="!integrationItem?.primaryLogin && oauth_service.linked === true" class="flex md6 chip-holder">
          <va-chip size="small" color="success" square shadow>{{ t('user.linked') }}</va-chip>
        </div>
        <div v-else-if="oauth_service.linked === false" class="flex md6 chip-holder">
          <va-chip icon="fa-unlink" color="danger" size="small" square shadow>{{ t('user.notLinked') }}</va-chip>
        </div>
      </div>
    </va-card-title>
    <va-card-content>
      <div v-if="oauth_service.linked === true" class="row">
        <div class="flex md12">
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
      <div class="row">

        <!-- <div v-if="service_name === 'twitch' && user.self.streamer.twitch_account" class="flex xs12">
          <va-avatar src="https://randomuser.me/api/portraits/women/5.jpg" class="mr-4" />
        </div> -->
      </div>
    </va-card-content>
    <va-card-actions>
      <div class="row">
        <div class="flex lg12 xs12">
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
  import { defineProps, ref, onMounted } from 'vue'
  import { useI18n } from 'vue-i18n'
  import { useWSStore } from '../../../../stores/ws'
  import { useAuthStore } from '../../../../stores/auth'
  // import { useUserStore } from '../../../../stores/user'
  import moment from 'moment'
  
  const t = useI18n().t

  const props = defineProps({
    integrationItem: { type: Object, required: true },
  })
  props.integrationItem

  var service_name = props.integrationItem?.identity.toLowerCase()

  const oauth_service = ref({} as Record<string, any>)

  const auth = useAuthStore()
  // const user = useUserStore()
  const ws = useWSStore()

  const checked = ref(true)

  auth.$subscribe((mutation, state) => {
    const uss = state.userServicesStatus
    if (service_name in uss) {
      oauth_service.value = uss[service_name]
    }

    // if (oauth_service.value.linked && !oauth_service.value.verified) {
    //   ws.sendData({
    //     class: 'vue.verify.users.services',
    //     service: service_name,
    //   })
    // }
  })

  ws.$onAction((event) => {
    if (event.name === 'connectSocket') {
      event.after(() => {
        event.store.sendData({
          class: 'vue.get.users.services.status',
          service: service_name,
        })
      })
    }
  })

  onMounted(() => {
    if (ws.connected && ws.socket.readyState === ws.socket.OPEN) {
      ws.sendData({
        class: 'vue.get.users.services.status',
        service: service_name,
      })
    }
  })
</script>

<style>
  .chip-holder {
    text-align: right;
  }

</style>