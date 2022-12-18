<template>
  <div v-if="connected">
    <va-icon name="material-icons-link" color="#00FF00" size="large"></va-icon>
  </div>
  <div v-else>
    <va-icon name="material-icons-link_off" color="#FF0000" size="large"></va-icon>
  </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { useWSStore } from '../../../../stores/ws'

  const WSStore = useWSStore()

  const connected = ref(false)

  WSStore.$subscribe((mutation, state) => {
    connected.value = state.connected
  })
</script>
