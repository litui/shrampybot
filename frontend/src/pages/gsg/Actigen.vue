<template>
  <div class="overlay-relativizer">
    <span class="overlay-now-bar-title">Now:</span>
    <svg class="overlay-now-bar" height="25.9vh" width="0.52vw">
      <line x1="0" y1="0" x2="0" y2="25.9vh" />
      <line x1="0.52vw" y1="0" x2="0.52vw" y2="25.9vh" />
    </svg>
    <div class="overlay-base">
      <va-virtual-scroller
        v-slot="{ item }"
        ref="timescaleScroller"
        :items="hugeArray.slice(0, 1000)"
        :bench="38"
        :wrapper-size="windowWidth"
        :item-size="fixedWidth"
        horizontal
        class="timescale-scroller"
      >
        <horizontal-time-scale
          :id="`hts_${item}`"
          :width="fixedWidth"
          :spacing="fixedSpacing"
          :x-offset="fixedSpacing"
          :tick-width="tickWidth"
          :scale-factor="scaleFactor"
        />
      </va-virtual-scroller>
      <div
        v-for="stIndex in eventData.stages.keys()"
        :key="stIndex"
        class="tsci-row"
      >
        <va-virtual-scroller
          :id="`stage-row-${stIndex}`"
          v-slot="{ item }"
          ref="stageScrollers"
          :items="hugeArray.slice(0, 1000)"
          :bench="20"
          :wrapper-size="windowWidth"
          :item-size="fixedWidth"
          horizontal
          :class="`stage-scroller-${eventData.stages.length}`"
        >
          <time-scale-card
            :id="`tsci-${stIndex}-${item}`"
            :width="fixedWidth"
            :username="eventData.stages[stIndex][item]?.act"
            :location="eventData.stages[stIndex][item]?.location + `[${item}]`"
            :img-src="eventData.stages[stIndex][item]?.img_src"
            :scale-factor="scaleFactor"
          ></time-scale-card>
        </va-virtual-scroller>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { computed, ref, onBeforeUnmount, onMounted, watchEffect, watch } from 'vue'
  import HorizontalTimeScale from './actigen/HorizontalTimeScaleSVG.vue'
  import TimeScaleCard from './actigen/TimeScaleCard.vue'
  import { VaVirtualScroller } from 'vuestic-ui'
  import { useRoute } from 'vue-router'

  const timescaleScroller = ref<typeof VaVirtualScroller | null>(null)
  const stageScrollers = ref<Array<typeof VaVirtualScroller | null>>([null, null, null, null])

  const currentDate = ref<Date | null>(null)

  const viewPortWidth = computed(() => {
    return `${window.innerWidth}px`
  })
  const viewPortHeight = computed(() => {
    return `${window.innerHeight}px`
  })
  const windowWidth = computed(() => {
    return window.innerWidth
  })
  const scaleFactor = computed(() => {
    return window.innerWidth / 1920
  })
  const fixedWidth = computed(() => {
    return 198 * scaleFactor.value
  })
  const fixedSpacing = computed(() => {
    // spacing for 15 minute blocks
    return fixedWidth.value / 4
  })
  const fixedLeft = computed(() => {
    return 110 * scaleFactor.value
  })
  const tickWidth = computed(() => {
    return 5 * scaleFactor.value
  })
  const minsInPixels = computed(() => {
    return (fixedWidth.value * 24) / 1440
  })

  const startDate = new Date()

  // Mock data for the schedule
  const eventData = ref({
    stages: [
      [
        {
          time: new Date(startDate.valueOf() - 120000000),
          duration: '2',
          act: 'SynthCore',
          location: 'Tokyo, Japan',
          img_src: 'http://cdn.shrampybot.live/misc/image_0.jpg',
        },
        {
          time: startDate,
          duration: '2',
          act: 'ModularMan',
          location: 'Istanbul, Turkey',
          img_src: 'http://cdn.shrampybot.live/misc/image_1.jpg',
        },
      ],
      [
        {
          time: new Date(startDate.valueOf() - 60000000),
          duration: '1',
          act: 'Musikator',
          location: 'Bangkok, Thailand',
          img_src: 'http://cdn.shrampybot.live/misc/image_2.jpg',
        },
        {
          time: new Date(startDate.valueOf() + 60000000),
          duration: '1',
          act: 'SynthSynth',
          location: 'Johannesburg, South Africa',
          img_src: 'http://cdn.shrampybot.live/misc/image_3.jpg',
        },
      ],
    ],
  })

  const hugeArrayBase = new Array(10000)
  const hugeArray = hugeArrayBase.fill(null).map((_, index) => index)

  const route = useRoute()

  var olTimer = null as any

  function setPosition(value: number) {
    console.log(value)
    for (var i = 0; i < eventData.value.stages.length; i++) {
      const ssVal = eventData.value.stages[i]
      const stageScroller = stageScrollers.value[i]
      if (ssVal && stageScroller) {
        console.log(ssVal[0])
        stageScroller.$el.scrollLeft = value
      }
    }
    if (timescaleScroller.value) {
      timescaleScroller.value.$el.scrollLeft = value + 45 * scaleFactor.value
    }
  }

  function calcPosition() {
    currentDate.value = new Date()
    const cd_mins = currentDate.value.getUTCHours() * 60 + currentDate.value.getUTCMinutes()
    const now = minsInPixels.value * cd_mins
    console.log(now)
    setPosition(fixedLeft.value + now)
  }

  onMounted(() => {
    calcPosition()

    olTimer = setInterval(() => {
      calcPosition()
    }, 15000)
  })

  onBeforeUnmount(() => {
    clearInterval(olTimer)
  })
</script>

<style lang="scss">
  body {
    background-color: transparent;
  }

  .overlay-relativizer {
    position: relative;
    width: 100vw;
    height: 100vh;
  }

  .overlay-base {
    position: absolute;
    bottom: 0px;
    left: 0px;
    margin: 0px;
    padding: 0px;
    z-index: 1;
  }

  .tsci-row:nth-child(2) {
    position: absolute;
    bottom: 8.8vh;
  }

  .overlay-now-bar {
    position: absolute;
    left: 24.375vw;
    bottom: 0px;
    stroke: #ffbb22;
    stroke-width: 0.1vw;
    z-index: 2;

    &-title {
      position: absolute;
      font-family: 'Revalia';
      text-transform: uppercase;
      font-size: 1.4vw;
      text-align: center;
      color: #ffffff;
      bottom: 26.48vh;
      left: 22.656vw;
      z-index: 3;
    }
  }

  .timescale-scroller {
    overflow: hidden;
    position: absolute;
    bottom: 21.2vh;
    padding: 0px;
    margin: 0px;
    z-index: 2;
  }

  .stage-scroller-1 {
    overflow: hidden;
    position: absolute;
  }

  .stage-scroller-2 {
    overflow: hidden;
    position: absolute;
    bottom: 3.7vh;
    // left: 0px;
  }

  .stage-scroller-3 {
    overflow: hidden;
    position: absolute;
  }

  .stage-scroller-4 {
    overflow: hidden;
    position: absolute;
  }
</style>
