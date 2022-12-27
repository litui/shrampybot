<template>
  <va-modal v-model="show_modal" hide-default-actions no-dismiss blur>
    <template #default>
      <va-card-title>{{ t('auth.cookieAgreement') }}</va-card-title>
      <va-card-content>
        <p>Test</p>
      </va-card-content>
    </template>
  </va-modal>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { useI18n } from 'vue-i18n'

  const t = useI18n().t
  const show_modal = ref(true)
</script>

<style lang="scss" scoped></style>
