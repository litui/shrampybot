<template>
  <svg class="htsi-segment" :height="tickMaxLength * 1.5" :width="width">
    <line
      v-for="index in Array(4).keys()"
      :key="index"
      :x1="xOffset + index * spacing - tickWidth"
      :y1="tickMaxLength - lengthOfTickAtIndex(index)"
      :x2="xOffset + index * spacing - tickWidth"
      :y2="lengthOfTickAtIndex(index)"
      :style="`stroke: ${colorOfTickAtIndex(index)}; stroke-width: ${tickWidth}px`"
    />
  </svg>
</template>

<script setup lang="ts">
  import { computed, onMounted } from 'vue'

  const props = defineProps({
    width: {
      type: Number,
      default: 216,
    },
    spacing: {
      type: Number,
      default: 54,
    },
    xOffset: {
      type: Number,
      default: 840 + 54,
    },
    divisions: {
      type: Array<number>,
      default: [4, 2],
    },
    tickColor: {
      type: String,
      default: '#FFFFFF',
    },
    firstDivisionColor: {
      type: String,
      default: '#FFBB22',
    },
    secondDivisionColor: {
      type: String,
      default: '#FFFFFF',
    },
    tickWidth: {
      type: Number,
      default: 4,
    },
    scaleFactor: {
      type: Number,
      default: window.innerWidth / 1920,
    },
  })

  const tickMaxLength = computed(() => {
    return 18 * props.scaleFactor
  })

  function lengthOfTickAtIndex(index: number) {
    var firstModI = index % props.divisions[0]
    var secondModI = index % props.divisions[1]

    if (firstModI === 0) {
      return tickMaxLength.value
    } else if (secondModI === 0) {
      return Math.floor(tickMaxLength.value / 1.05)
    } else {
      return Math.floor(tickMaxLength.value / 1.2)
    }
  }

  function colorOfTickAtIndex(index: number) {
    var firstModI = index % props.divisions[0]
    var secondModI = index % props.divisions[1]

    if (firstModI === 0) {
      return props.firstDivisionColor
    } else if (secondModI === 0) {
      return props.secondDivisionColor
    } else {
      return props.tickColor
    }
  }

  function resizeCanvas() {
    // if (hCanvas.value) {
    //   hCanvas.value.width = props.width
    //   hCanvas.value.height = tickMaxLength.value * 2
    // }
  }

  onMounted(async () => {
    // var drawContext = hCanvas.value?.getContext('2d')
    // resizeCanvas()
    // await drawScale(drawContext)
  })
</script>

<style lang="scss" scoped></style>
