<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template>
  <div class="page"><h1>记录</h1><ul><li v-for="r in items" :key="r.id">{{ r.wall_name }} → {{ r.result?.rolls }} 卷<template v-if="r.result"> · {{ r.result.match_pattern === undefined ? '旧记录' : (r.result.match_pattern ? '对花' : '不对花') }} · 每条 {{ r.result.drop_len_m }}m</template></li></ul></div>
</template>
