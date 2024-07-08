<template>
    <q-banner class="success-banner">
      {{ message }}
    </q-banner>
</template>
  
<script>
export default {
    props: {
      message: {
        type: String,
        required: true
      }
    }
}
</script>
  
<style lang="scss" scoped>
.success-banner {
    background-color: $positive;
    border: 2px solid green;
    border-radius: 8px;
}
</style>
  