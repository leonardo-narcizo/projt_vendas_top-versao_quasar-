<template>
    <q-menu v-model="menu" anchor="top right" self="bottom right">
      <q-list>
        <q-item clickable v-ripple @click="goToProfile">
          <q-item-section>Perfil</q-item-section>
        </q-item>
        <q-item clickable v-ripple @click="logout">
          <q-item-section>Sair</q-item-section>
        </q-item>
      </q-list>
    </q-menu>
  </template>
  
  <script>
  import { ref } from 'vue'
  import { useStore } from 'vuex'
  import { useRouter } from 'vue-router'
  
  export default {
    name: 'AvatarMenu',
    setup() {
      const menu = ref(false)
      const store = useStore()
      const router = useRouter()
  
      const goToProfile = () => {
        router.push('/profile')
      }
  
      const logout = () => {
        store.commit('user/logout')
        router.push('/')
      }
  
      return {
        menu,
        goToProfile,
        logout,
      }
    }
  }
  </script>
  
  <style scoped>
  /* Adicione estilos específicos do menu aqui, se necessário */
  </style>
  