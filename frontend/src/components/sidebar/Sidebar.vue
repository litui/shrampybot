<template>
  <va-sidebar :width="width" :minimized="minimized" :minimized-width="minimizedWidth" :animated="animated">
    <menu-minimized v-if="minimized" :items="items" />
    <menu-accordion v-else :items="items" />
  </va-sidebar>
</template>

<script setup lang="ts">
  import { ref, onBeforeMount } from 'vue'
  import { routes, INavigationRoute } from '../../router'
  import MenuAccordion from './menu/MenuAccordion.vue'
  import MenuMinimized from './menu/MenuMinimized.vue'
  import { useUserStore } from '../../stores/user'

  withDefaults(
    defineProps<{
      width?: string
      color?: string
      animated?: boolean
      minimized?: boolean
      minimizedWidth?: string
    }>(),
    {
      width: '16rem',
      color: 'secondary',
      animated: true,
      minimized: true,
      minimizedWidth: undefined,
    },
  )

  const UserStore = useUserStore()

  const items = ref([] as Array<INavigationRoute>)

  function getNavRoutes() {
    routes.forEach((item) => {
      let route = item as INavigationRoute
      let nav: any = item.meta?.nav
      let perms: any = item.meta?.perms
      if (nav.hidden === false) {
        if (perms.requiresStaff === true && UserStore.$state.self.is_staff) {
          items.value.push(route)
        } else if (perms.requiresAdmin === true && UserStore.$state.self.is_superuser) {
          items.value.push(route)
        } else if (perms.requiresAuth === true && UserStore.$state.self.is_authenticated) {
          items.value.push(route)
        } else {
          items.value.push(route)
        }
      }
    })
  }

  onBeforeMount(() => {
    getNavRoutes()
  })
</script>

<style lang="scss">
  .va-sidebar {
    &__menu {
      padding: 2rem 0;
    }

    &-item {
      &__icon {
        width: 1.5rem;
        height: 1.5rem;
        display: flex;
        justify-content: center;
        align-items: center;
      }
    }

    &__title {
      font-family: 'Revalia';
    }
  }
</style>
