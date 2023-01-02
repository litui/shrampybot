<template>
  <canvas ref="hCanvas"></canvas>
</template>

<script setup lang="ts">
  import { computed, ref, onMounted } from 'vue'

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

  const hCanvas = ref<HTMLCanvasElement | null>(null)

  async function drawTick(drawContext: any, x: number, length: number, tickWidth: number) {
    drawContext.beginPath()
    drawContext.lineWidth = tickWidth
    drawContext.moveTo(x, tickMaxLength.value - length / 2)
    drawContext.lineTo(x, tickMaxLength.value + length / 2)
    drawContext.stroke()
  }

  async function drawScale(drawContext: any) {
    var tickCount = Math.floor(props.width / (props.spacing - props.tickWidth))
    var tickLength = tickMaxLength.value

    for (var i = 0; i < tickCount; i++) {
      drawContext.strokeStyle = props.tickColor
      tickLength = Math.floor(tickMaxLength.value / 2)

      var firstModI = i % props.divisions[0]
      var secondModI = i % props.divisions[1]

      if (firstModI === 0) {
        drawContext.strokeStyle = props.firstDivisionColor
        tickLength = tickMaxLength.value
      } else if (secondModI === 0) {
        drawContext.strokeStyle = props.secondDivisionColor
        tickLength = Math.floor(tickMaxLength.value / 1.25)
      }
      var xPos = props.xOffset + i * props.spacing - props.tickWidth
      await drawTick(drawContext, xPos, tickLength, props.tickWidth)
    }
  }

  function resizeCanvas() {
    if (hCanvas.value) {
      hCanvas.value.width = props.width
      hCanvas.value.height = tickMaxLength.value * 2
    }
  }

  onMounted(async () => {
    var drawContext = hCanvas.value?.getContext('2d')
    resizeCanvas()
    await drawScale(drawContext)
  })
</script>

<style lang="scss" scoped></style>
