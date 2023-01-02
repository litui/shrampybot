<template>
  <va-card class="timescale-card user-card" color="#000000" :style="`width: ${hoursWidth}`" square>
    <va-card-content class="d-flex pa-0">
      <div>
        <va-avatar
          :src="imgSrc"
          class="timescale-avatar"
          square
          style="height: 6.6vh; width: 3.8vw"
        />
      </div>
      <div class="pa-2 pl-3 d-flex flex-direction-column justify-begin">
        <h5 class="display-5 ma-0" style="color: inherit; font-size: 1.2vw">Test{{ username }}</h5>

        <div class="d-flex">
          <span class="mr-2 text--no-wrap" style="font-size: 1vw">{{ location }}</span>
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
    scaleFactor: {
      type: Number,
      default: 1,
    },
  })

  const hoursWidth = ref<string>('')

  onMounted(() => {
    hoursWidth.value = String(props.duration * props.width - 8 * props.scaleFactor) + 'px'
  })
</script>

<style lang="scss" scoped>
  .timescale-card {
    overflow: flex;
    border: 1px solid #ffffff;
    height: 8.1vh;
    margin-left: 0.208vw;
    margin-right: 0.208vw;
    padding: 0.5vh;
  }

  .timescale-avatar {
    border: 0.1vh solid #ffffff;
    padding: 0px;
    margin: 0.2vh;
  }
</style>
