<template>
  <q-layout :style="backgroundStyle">
    <q-header class="toolbar text-weight-bold q-pa-md bg-primary text-center">
      <q-toolbar class="toolbar">
        <q-toolbar-title>Vendas Top</q-toolbar-title>
      </q-toolbar>
      <div class="text-subtitle2">Encontre o melhor veículo para você! Por meio de filtros personalizados</div>
    </q-header>
    <q-page-container style="text-align: center">
      <!-- Conteúdo da página será inserido aqui -->
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import foto1 from 'src/assets/imgs/foto_1.jpg' // Use alias @

export default {
  data () {
    return {
      backgroundStyle: {
        backgroundImage: `url(${foto1})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundAttachment: 'fixed'
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.toolbar {
  color: black
}
</style>
