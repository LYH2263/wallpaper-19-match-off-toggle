<script setup>
import { computed, onMounted, ref } from 'vue'
import { getJSON } from '../api'
import DropStripBar from '../components/DropStripBar.vue'
const walls = ref([]); const rolls = ref([]); const wallId = ref(null); const rollId = ref(null)
const matchPattern = ref(true); const out = ref(null)
const roll = computed(() => rolls.value.find(r => r.id === rollId.value))
onMounted(async () => {
  walls.value = (await getJSON('/api/walls')).items.filter(w => w.data_quality==='clean')
  rolls.value = (await getJSON('/api/rolls')).items.filter(r => r.data_quality==='clean')
  if (walls.value.length) wallId.value = walls.value[0].id
  if (rolls.value.length) rollId.value = rolls.value[0].id
  const s = await getJSON('/api/settings')
  if (s.match_pattern_default !== undefined) matchPattern.value = s.match_pattern_default === '1'
  await run()
})
async function run() {
  if (!wallId.value || !rollId.value) return
  out.value = await getJSON(`/api/estimate?wall_id=${wallId.value}&roll_id=${rollId.value}&match_pattern=${matchPattern.value}`)
}
</script>
<template>
  <div class="page"><h1>对花说明</h1>
  <p>开启对花时在墙高上加 pattern_cm/100 作为每条长度，再算每卷可裁条数；关闭对花按无花口径，每条长度等于层高、忽略卷材花高。</p>
  <select v-model.number="wallId" @change="run"><option v-for="w in walls" :key="w.id" :value="w.id">{{ w.name }}</option></select>
  <select v-model.number="rollId" @change="run"><option v-for="r in rolls" :key="r.id" :value="r.id">{{ r.name }}</option></select>
  <label><input type="checkbox" v-model="matchPattern" @change="run" /> 对花</label>
  <div v-if="out"><strong>{{ out.rolls }} 卷</strong> · {{ out.drops }} 条 · 每条 {{ out.drop_len_m }}m
  <template v-if="roll"> · 花高 {{ roll.pattern_cm }}cm<template v-if="!out.match_pattern">（已忽略）</template></template>
  <DropStripBar :drops="out.drops" :drop-len="out.drop_len_m" :rolls="out.rolls" /></div>
  </div>
</template>
