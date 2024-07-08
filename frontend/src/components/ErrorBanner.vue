<template>
    <q-banner class="error-banner">
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
.error-banner {
    background-color: $negative;
    border: 2px solid red;
    border-radius: 8px;
}
</style>
  