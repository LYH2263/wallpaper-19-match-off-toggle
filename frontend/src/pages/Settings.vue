<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'
const s = ref({})
const matchDefault = ref(true)
const saved = ref(false)
onMounted(async () => {
  s.value = await getJSON('/api/settings')
  matchDefault.value = s.value.match_pattern_default !== '0'
})
async function save() {
  s.value = await putJSON('/api/settings', { values: { match_pattern_default: matchDefault.value ? '1' : '0' } })
  saved.value = true
  setTimeout(() => { saved.value = false }, 1500)
}
</script>
<template>
  <div class="page"><h1>设置</h1>
  <label><input type="checkbox" v-model="matchDefault" /> 默认对花（新测算的初始开关，不影响已保存记录）</label>
  <button @click="save">保存</button><span v-if="saved"> 已保存</span>
  <pre>{{ s }}</pre></div>
</template>
