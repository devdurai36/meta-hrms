<template>
	<!-- Brand wordmark is white on transparent; `invert` renders it in ink on light surfaces -->
	<img :src="wordmark" alt="MetaCarat" class="invert w-auto" />
</template>

<script setup lang="ts">
import wordmark from "../assets/metacarat-wordmark.png";
</script>
