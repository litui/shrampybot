<template>
  <div class="markup-tables flex">
    <va-card class="flex mb-4">
      <va-card-title>{{ t('staff.masterList') }}</va-card-title>
      <va-card-content>
        <div class="table-wrapper">
          <table class="va-table">
            <thead>
              <tr>
                <th>{{ t('staff.tables.visualName') }}</th>
                <th>{{ t('staff.tables.twitch') }}</th>
                <th>{{ t('staff.tables.location') }}</th>
                <th>{{ t('staff.tables.email') }}</th>
                <th>{{ t('staff.tables.now') }}</th>
                <th>{{ t('staff.tables.next') }}</th>
                <th>{{ t('staff.tables.later') }}</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="user in users" :key="user.guid">
                <td>{{ user.visual_name }}</td>
                <!-- <td>{{ user.twitch_url }}</td> -->
                <td>{{ user.twitch_account.display_name }}</td>
                <td>{{ user.irl_location }}</td>
                <td>{{ user.e_mail }}</td>
                <td>{{ user.now }}</td>
                <td>{{ user.next }}</td>
                <td>{{ user.later }}</td>
                <!-- <td>
                  <va-badge :text="user.status" :color="getStatusColor(user.status)" />
                </td> -->
              </tr>
            </tbody>
          </table>
        </div>
      </va-card-content>
    </va-card>

    <!-- <va-card>
      <va-card-title>{{ t('tables.stripedHoverable') }}</va-card-title>
      <va-card-content>
        <div class="table-wrapper">
          <table class="va-table va-table--striped va-table--hoverable">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Country</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.name }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.country }}</td>
                <td>
                  <va-badge :text="user.status" :color="getStatusColor(user.status)" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </va-card-content>
    </va-card> -->
  </div>
</template>

<script setup lang="ts">
  import { ref, onBeforeMount, watchEffect } from 'vue'
  import { useI18n } from 'vue-i18n'
  import { useAuthStore } from '../../../stores/auth'
  import { useUserStore } from '../../../stores/user'
  import { useRouter } from 'vue-router'
  import { validateAndFetchRoute } from '../../../router'
  import { useTimer } from 'vue-timer-hook'
  import axios from 'axios'

  const router = useRouter()
  const AuthStore = useAuthStore()
  const UserStore = useUserStore()

  const { t } = useI18n()

  interface MasterListUser {
    guid: string
    visual_name: string
    irl_location: string
    twitch_url: string
    twitch_account: any
    e_mail: string
    now: string
    next: string
    later: string
  }

  const users = ref({} as Record<string, MasterListUser>)

  function getStatusColor(status: string) {
    if (status === 'paid') {
      return 'success'
    }

    if (status === 'processing') {
      return 'info'
    }

    return 'danger'
  }

  onBeforeMount(() => {
    // heartbeatTimerRestart()
    // watchEffect(async () => {
    //   if (timer.isExpired.value) {
    //     heartbeatTimerRestart()
    //   }
    // })
  })

  const time = Date.now()
  const timer = useTimer(time + 60000)
  const heartbeatTimerRestart = async () => {
    // Reload streams
    router.push(await validateAndFetchRoute(router.currentRoute))
    axios
      .get('/streamers/acts/', AuthStore.getAxiosConfig())
      .then((response) => {
        updateActsData(response.data)
      })
      .catch((error) => {
        console.log(error)
      })
    const time = Date.now()
    timer.restart(time + 60000)
  }

  function updateActsData(newData: Array<MasterListUser>) {
    newData.forEach((element: MasterListUser) => {
      let guid = element.guid
      if (!users.value[guid]) {
        users.value[guid] = element
      }
    })
  }
</script>

<style lang="scss">
  .markup-tables {
    .table-wrapper {
      overflow: auto;
    }

    .va-table {
      width: 100%;
    }
  }
</style>
