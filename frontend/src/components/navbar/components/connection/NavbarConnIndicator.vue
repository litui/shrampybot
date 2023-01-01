<template>
  <div v-if="connected" class="color-dropdown">
    <va-icon name="fa-link" color="#00FF00" stick-to-edges size="large"></va-icon>
  </div>
  <div v-else>
    <va-icon name="fa-unlink" color="#FF0000" stick-to-edges size="large"></va-icon>
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
