<template>
  <va-card class="timescale-card user-card" color="#000000" :style="`width: ${hoursWidth}`" square>
    <va-card-content class="d-flex pa-2">
      <div>
        <va-avatar
          :src="imgSrc"
          class="timescale-avatar"
          square
          size="66px"
        />
      </div>
      <div class="pa-2 pl-3 d-flex flex-direction-column justify-begin">
        <h5 class="display-5 ma-0" style="color: inherit">{{ username }}</h5>

        <div class="d-flex">
          <span class="mr-2 text--no-wrap">{{ location }}</span>
        </div>
      </div>
    </va-card-content>
  </va-card>
</template>

<script setup lang="ts">
  import { ref, onMounted } from 'vue'

  const props = defineProps({
    username: {
      type: String,
      default: '',
    },
    location: {
      type: String,
      default: '',
    },
    duration: {
      type: Number,
      default: 2,
    },
    width: {
      type: Number,
      default: 300,
    },
    imgSrc: {
      type: String,
      default: '',
    },
  })

  const hoursWidth = ref<string>('')

  onMounted(() => {
    hoursWidth.value = String(props.duration * props.width - 8) + 'px'
  })
</script>

<style lang="scss" scoped>
  .timescale-card {
    overflow: flex;
    border: 1px solid #ffffff;
    height: 86px;
    margin: 4px;
  }

  .timescale-avatar {
    border: 1px solid #ffffff;
    padding: 0px;
  }
</style>
