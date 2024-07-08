<template>
  <q-item clickable tag="router-link" :to="to" class="essential-link">
    <q-item-section v-if="icon" avatar>
      <q-icon :name="icon" class="icon-label"/>
    </q-item-section>
    <q-item-section>
      <q-item-label class="link-label">{{ title }}</q-item-label>
    </q-item-section>
  </q-item>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'EssentialLink',
  props: {
    title: {
      type: String,
      required: true
    },
    to: {
      type: String,
      required: true
    },
    icon: {
      type: String,
      default: ''
    }
  }
})
</script>

<style scoped>
.essential-link {
  text-decoration: none;
  color: inherit;
}
</style>
