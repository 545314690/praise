<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps({
  count: {
    default: 0,
  },
})

const counter = ref(props.count)
</script>

<template>
  <iframe allow="camera; microphone; fullscreen; display-capture; autoplay" src="https://lb.ysaw.top:8443/112" style="height: 100%; width: 100%; border: 0px;"></iframe>
</template>
