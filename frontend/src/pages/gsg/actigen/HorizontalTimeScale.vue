<template>
  <canvas ref="hCanvas"></canvas>
</template>

<script setup lang="ts">
  import { ref, onMounted } from 'vue'

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
    tickMaxLength: {
      type: Number,
      default: 18,
    },
  })

  const hCanvas = ref<HTMLCanvasElement | null>(null)

  async function drawTick(drawContext: any, x: number, length: number, tickWidth: number) {
    drawContext.beginPath()
    drawContext.lineWidth = tickWidth
    drawContext.moveTo(x, props.tickMaxLength - length / 2)
    drawContext.lineTo(x, props.tickMaxLength + length / 2)
    drawContext.stroke()
  }

  async function drawScale(drawContext: any) {
    var tickCount = Math.floor(props.width / (props.spacing - props.tickWidth))
    var tickLength = props.tickMaxLength

    for (var i = 0; i < tickCount; i++) {
      drawContext.strokeStyle = props.tickColor
      tickLength = Math.floor(props.tickMaxLength / 2)

      var firstModI = i % props.divisions[0]
      var secondModI = i % props.divisions[1]

      if (firstModI === 0) {
        drawContext.strokeStyle = props.firstDivisionColor
        tickLength = props.tickMaxLength
      } else if (secondModI === 0) {
        drawContext.strokeStyle = props.secondDivisionColor
        tickLength = Math.floor(props.tickMaxLength / 1.25)
      }
      var xPos = props.xOffset + i * props.spacing - props.tickWidth
      await drawTick(drawContext, xPos, tickLength, props.tickWidth)
    }
  }

  function resizeCanvas() {
    if (hCanvas.value) {
      hCanvas.value.width = props.width
      hCanvas.value.height = props.tickMaxLength * 2
    }
  }

  onMounted(async () => {
    var drawContext = hCanvas.value?.getContext('2d')
    resizeCanvas()
    await drawScale(drawContext)
  })
</script>

<style lang="scss" scoped></style>
