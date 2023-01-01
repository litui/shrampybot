<template>
  <div class="overlay-relativizer">
    <span class="overlay-now-bar-title">Now:</span>
    <svg class="overlay-now-bar" height="280" width="10">
      <line x1="0" y1="0" x2="0" y2="300" />
      <line x1="10" y1="0" x2="10" y2="300" />
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
          ></time-scale-card>
        </va-virtual-scroller>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, onBeforeUnmount, onMounted, watchEffect, watch } from 'vue'
  import HorizontalTimeScale from './actigen/HorizontalTimeScale.vue'
  import TimeScaleCard from './actigen/TimeScaleCard.vue'
  import { VaVirtualScroller } from 'vuestic-ui'
  import { useRoute } from 'vue-router'

  const timescaleScroller = ref<typeof VaVirtualScroller | null>(null)
  const stageScrollers = ref<Array<typeof VaVirtualScroller | null>>([null, null, null, null])

  const currentDate = ref<Date | null>(null)

  const viewPortWidth = ref('1920px')
  const viewPortHeight = ref('1080px')
  const windowWidth = ref(window.innerWidth)
  const fixedWidth = 198
  const fixedSpacing = fixedWidth / 4
  const fixedDefault = 180
  const tickWidth = 5

  const minsInPixels = (fixedWidth * 24) / 1440

  // Mock data for the schedule
  const eventData = ref({
    stages: [
      [
        {
          time: new Date(new Date().valueOf() - 120000000),
          duration: '2',
          act: 'SynthCore',
          location: 'Tokyo, Japan',
          img_src: 'http://cdn.shrampybot.live/misc/image_0.jpg',
        },
        {
          time: new Date(),
          duration: '2',
          act: 'ModularMan',
          location: 'Istanbul, Turkey',
          img_src: 'http://cdn.shrampybot.live/misc/image_1.jpg',
        },
      ],
      [
        {
          time: new Date(new Date().valueOf() - 60000000),
          duration: '1',
          act: 'Musikator',
          location: 'Bangkok, Thailand',
          img_src: 'http://cdn.shrampybot.live/misc/image_2.jpg',
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
        stageScroller.$el.scrollLeft = value - 45 + 1585
      }
    }
    if (timescaleScroller.value) {
      timescaleScroller.value.$el.scrollLeft = value
    }
  }

  function calcPosition() {
    currentDate.value = new Date()
    const cd_mins = currentDate.value.getUTCHours() * 60 + currentDate.value.getUTCMinutes()
    const now = minsInPixels * cd_mins
    console.log(now)
    setPosition(fixedDefault + now)
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
    width: v-bind(viewPortWidth);
    height: v-bind(viewPortHeight);
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
    bottom: 95px;
  }

  .overlay-now-bar {
    position: absolute;
    left: 468px;
    bottom: 0px;
    stroke: #ffbb22;
    stroke-width: 3px;
    z-index: 2;

    &-title {
      position: absolute;
      font-family: 'Revalia';
      text-transform: uppercase;
      font-size: 26px;
      text-align: center;
      color: #ffffff;
      bottom: 286px;
      left: 435px;
    }
  }

  .timescale-scroller {
    overflow: hidden;
    position: absolute;
    bottom: 229px;
    padding: 0px;
    margin: 0px;
  }

  .stage-scroller-1 {
    overflow: hidden;
    position: absolute;
  }

  .stage-scroller-2 {
    overflow: hidden;
    position: absolute;
    bottom: 40px;
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
