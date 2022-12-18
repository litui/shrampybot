<template>
  <v-stage ref="stage" :config="stageSize">
    <v-layer v-if="ready" ref="layer">
      <v-image
        ref="imageElement"
        :config="{
          image: image,
          x: 50,
          y: 50,
        }"
      />
    </v-layer>
  </v-stage>
</template>

<script setup lang="ts">
  import { ref, onBeforeMount, onMounted, watchEffect } from 'vue'
  import konva from 'konva'

  const width = window.innerWidth
  const height = window.innerHeight

  const stageSize = ref({
    width: width,
    height: height,
  })

  const ready = ref(false)
  const image = ref({} as HTMLImageElement)
  const imageElement = ref(null)
  const layer = ref(null)
  const stage = ref(null)

  // const anim = new konva.Animation(function(frame) {
  //   image.value.setAttribute('x', '20px')
  // })

  onMounted(() => {
    const localImage = new ImageData(100, 100)
    localImage.src = 'https://konvajs.org/assets/yoda.jpg'
    localImage.className = 'wombrimage'
    localImage.onload = () => {
      // set image only when it is loaded
      image.value = localImage
      ready.value = true

      const centreX = stage.value.getNode().getWidth()

      const anim = new konva.Animation(function (frame: any) {
        image.value.setInterval(100 * Math.sin((frame.time * 2 * Math.PI) / 5000) + centreX)
      }, layer)

      if (ready.value === true) {
        anim.start()
      }
    }
  })
</script>
