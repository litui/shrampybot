<template>
  <div class="dashboard">
    <div class="row">
      <div v-for="stream in streamInfo" :key="stream.guid" class="flex xs4">
        <va-card>
          <va-image :src="stream.twitch_stream.thumbnail_image" style="height: 250px" />
          <va-card-title>
            <va-icon class="mr-3" color="#8f4ed6" name="ion-logo-twitch" />
            {{ stream.main_streamer.identity }}
            <va-spacer />
            <span>Started {{ streamTimes[stream.guid].fromNow() }}</span>
          </va-card-title>
          <va-card-content>{{ stream.twitch_stream.title }}</va-card-content>
        </va-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted, watchEffect } from 'vue'
  import { useRouter } from 'vue-router'
  import { validateAndFetchRoute } from '../../router'

  import { useTimer } from 'vue-timer-hook'
  import { useAuthStore } from '../../stores/auth'
  import axios from 'axios'
  import moment, { Moment } from 'moment'

  const AuthStore = useAuthStore()
  const router = useRouter()

  interface StreamDataType {
    guid: string
    twitch_stream?: any
    main_streamer?: any
  }

  const streamInfo = ref({} as Record<string, StreamDataType>)
  const streamTimes = ref({} as Record<string, Moment>)

  const time = Date.now()
  const timer = useTimer(time + 10000)
  const heartbeatTimerRestart = async () => {
    // Reload streams
    router.push(await validateAndFetchRoute(router.currentRoute))
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

  function updateStreamData(newData: Array<StreamDataType>) {
    newData.forEach((element: StreamDataType) => {
      let guid = element.guid
      if (!streamInfo.value[guid]) {
        streamInfo.value[guid] = element
        streamTimes.value[guid] = moment(element.twitch_stream.started_at)
      }
    })
  }

  onMounted(() => {
    // heartbeatTimerRestart()
    // watchEffect(async () => {
    //   if (timer.isExpired.value) {
    //     heartbeatTimerRestart()
    //   }
    // })
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
