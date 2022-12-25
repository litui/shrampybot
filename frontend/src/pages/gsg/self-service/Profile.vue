<template service="">
  <va-card color="background-element" style="padding: 0.75rem">
    <div class="row">
      <div v-for="i in integrationData" :key="i.identity" class="flex lg4">
        <integration-card :integration-item="i"></integration-card>
      </div>
    </div>
  </va-card>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import IntegrationCard from './cards/IntegrationCard.vue'

  const integrationData = ref([
    {
      identity: 'Twitch',
      icon: 'fa-twitch',
      brandColor: '#7742EA',
      primaryLogin: true,
      linked: false,
    },
    {
      identity: 'Mastodon',
      icon: 'fa-mastodon',
      brandColor: '#6359F3',
      primaryLogin: false,
      linked: false,
    },
    {
      identity: 'Discord',
      icon: 'fa-discord',
      brandColor: '#5B5AE6',
      primaryLogin: false,
      linked: false,
    },
  ])
</script>
