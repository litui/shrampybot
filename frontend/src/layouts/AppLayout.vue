<template>
  <div class="app-layout">
    <navbar />
    <div class="app-layout__content">
      <div class="app-layout__sidebar-wrapper" :class="{ minimized: isSidebarMinimized }">
        <div v-if="isFullScreenSidebar" class="d-flex justify-end">
          <va-button class="px-4 py-4" icon="md_close" preset="plain" color="dark" @click="onCloseSidebarButtonClick" />
        </div>
        <sidebar
          :width="sidebarWidth"
          :minimized="isSidebarMinimized"
          :minimized-width="sidebarMinimizedWidth"
          :animated="!isMobile"
        />
      </div>
      <div class="app-layout__page">
        <div class="layout fluid va-gutter-5">
          <router-view />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { computed, onBeforeMount, onBeforeUnmount, onMounted, watchEffect, ref } from 'vue'
  import { onBeforeRouteUpdate } from 'vue-router'
  import { storeToRefs } from 'pinia'

  import { useGlobalStore } from '../stores/global-store'
  import { useTimer } from 'vue-timer-hook'

  import Navbar from '../components/navbar/Navbar.vue'
  import Sidebar from '../components/sidebar/Sidebar.vue'

  /* Set default colour scheme to dark */
  import { useColors } from 'vuestic-ui'
  import { useAuthStore } from '../stores/auth'
  import { useWSStore } from '../stores/ws'

  const { applyPreset, setColors } = useColors()

  watchEffect(() => {
    applyPreset('dark')
    setColors({
      primary: '#FFBB22',
      secondary: '#FFFFFF',
      danger: '#E42222',
    })
  })

  const GlobalStore = useGlobalStore()
  const AuthStore = useAuthStore()
  const WSStore = useWSStore()

  const mobileBreakPointPX = 640
  const tabletBreakPointPX = 768

  const sidebarWidth = ref('16rem')
  const sidebarMinimizedWidth = ref('')

  const time = Date.now()
  const timer = useTimer(time + 60000)
  const heartbeatTimerRestart = async () => {
    // Monitor the current state of the websocket connection and refresh if it needs it
    await AuthStore.testAndRefreshToken()

    if (WSStore.connected !== true) {
      WSStore.connectSocket(AuthStore.accessToken)
    }
    const time = Date.now()
    timer.restart(time + 60000)
  }

  const isMobile = ref(false)
  const isTablet = ref(false)
  const { isSidebarMinimized } = storeToRefs(GlobalStore)
  const checkIsTablet = () => window.innerWidth <= tabletBreakPointPX
  const checkIsMobile = () => window.innerWidth <= mobileBreakPointPX

  const onResize = () => {
    isSidebarMinimized.value = checkIsTablet()

    isMobile.value = checkIsMobile()
    isTablet.value = checkIsTablet()
    sidebarMinimizedWidth.value = isMobile.value ? '0' : '4.5rem'
    sidebarWidth.value = isTablet.value ? '100%' : '16rem'
  }

  onMounted(async () => {
    watchEffect(async () => {
      if (timer.isExpired.value) {
        await heartbeatTimerRestart()
      }
    })

    window.addEventListener('resize', onResize)
  })

  onBeforeMount(async () => {
    await heartbeatTimerRestart()
    // WSStore.connectSocket(AuthStore.accessToken)
  })

  onBeforeUnmount(() => {
    window.removeEventListener('resize', onResize)
  })

  onBeforeRouteUpdate(() => {
    if (checkIsTablet()) {
      // Collapse sidebar after route change for Mobile
      isSidebarMinimized.value = true
    }
  })

  onResize()

  const isFullScreenSidebar = computed(() => isTablet.value && !isSidebarMinimized.value)

  const onCloseSidebarButtonClick = () => {
    isSidebarMinimized.value = true
  }
</script>

<style lang="scss">
  $mobileBreakPointPX: 640px;
  $tabletBreakPointPX: 768px;

  .app-layout {
    height: 100vh;
    display: flex;
    flex-direction: column;
    &__navbar {
      min-height: 4rem;
    }

    &__content {
      display: flex;
      height: calc(100vh - 4rem);
      flex: 1;

      @media screen and (max-width: $tabletBreakPointPX) {
        height: calc(100vh - 6.5rem);
      }

      .app-layout__sidebar-wrapper {
        position: relative;
        height: 100%;
        background: var(--va-white);

        @media screen and (max-width: $tabletBreakPointPX) {
          &:not(.minimized) {
            width: 100%;
            height: 100%;
            position: fixed;
            top: 0;
            z-index: 999;
          }

          .va-sidebar:not(.va-sidebar--minimized) {
            // Z-index fix for preventing overflow for close button
            z-index: -1;
            .va-sidebar__menu {
              padding: 0;
            }
          }
        }
      }
    }
    &__page {
      flex-grow: 2;
      overflow-y: scroll;
    }
  }
</style>
