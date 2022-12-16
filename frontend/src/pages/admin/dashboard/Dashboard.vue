<template>
  <div class="dashboard">
    <div class="row">
      <div v-for="stream in streamInfo" class="flex xs4">
        <va-card>
          <va-image :src="stream.platform_stream.thumbnail_image" style="height: 250px" />
          <va-card-title>
            <a :href="`https://twitch.tv/${stream.main_streamer.twitchaccount.display_name}`">
              {{ stream.platform.name }}
            </a>
            <span>{{ stream.main_streamer.identity }}</span>
          </va-card-title>
          <va-card-content>{{ stream.platform_stream.title }}</va-card-content>
        </va-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted, watchEffect } from 'vue'
  import { useRouter } from 'vue-router'
  import { validateAndFetchUser } from '../../../router'

  import { useTimer } from 'vue-timer-hook'
  import { useAuthStore } from '../../../stores/auth'
  import axios from 'axios'

  const AuthStore = useAuthStore()
  const router = useRouter()

  const dashboardMap = ref()

  const streamInfo = ref({})

  const time = Date.now()
  const timer = useTimer(time + 10000)
  const heartbeatTimerRestart = async () => {
    // Reload streams
    router.push(await validateAndFetchUser(router.currentRoute))
    axios
      .get('/streams/', AuthStore.getAxiosConfig())
      .then((data) => {
        updateStreamData(data.data)
      })
      .catch((error) => {
        console.log(error)
      })
    const time = Date.now()
    timer.restart(time + 10000)
  }

  function updateStreamData(newData) {
    newData.forEach((element) => {
      if (!streamInfo.value[element.guid]) {
        streamInfo.value[element.guid] = element
      }
    })
  }

  function addAddressToMap({ city, country }: { city: { text: string }; country: string }) {
    dashboardMap.value.addAddress({ city: city.text, country })
  }

  onMounted(() => {
    heartbeatTimerRestart()
    watchEffect(async () => {
      if (timer.isExpired.value) {
        heartbeatTimerRestart()
      }
    })
  })
</script>

<style lang="scss">
  .row-equal .flex {
    .va-card {
      height: 100%;
    }
  }

  .dashboard {
    .va-card {
      margin-bottom: 0 !important;
      &__title {
        display: flex;
        justify-content: space-between;
      }
    }
  }
</style>
