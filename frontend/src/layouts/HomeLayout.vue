<template>
  <q-layout :style="backgroundStyle" view="hhr LpR lFf">
    <q-header elevated class="header bg-primary text-white">
      <q-toolbar class="toolbar">
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />
        <q-toolbar-title class="toolbar-title">
          <div class="name-page">{{ namePage }}</div>
          <div class="right-side">
            <q-btn flat icon="notifications" class="notifications" />
            <q-btn flat no-caps class="avatar" @click="toggleAvatarMenu">{{ avatar }}</q-btn>
            <AvatarMenu :menu="avatarMenu" />
          </div>
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer class="bg-secondary" v-model="leftDrawerOpen" side="left">
      <q-list>
        <essential-link
          v-for="item in items"
          :key="item.to"
          :title="item.title"
          :to="item.to"
          :icon="item.icon"
        />
        <essential-link
          title="Sair"
          icon="logout"
          :to="logout"
          @click="logout"
        />
      </q-list>
    </q-drawer>

    <status-on-footer 
      :showFooter="showFooter"
      status="confirmed"
      message="Deslogado com sucesso"
    />

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import foto1 from 'src/assets/imgs/foto_1.jpg'
import EssentialLink from 'src/components/EssentialLink.vue'
import StatusOnFooter from 'src/components/StatusOnFooter.vue'
import AvatarMenu from 'src/components/AvatarMenu.vue'
import { ref, computed, onBeforeMount, onBeforeUnmount } from 'vue'

export default {
  components: { 
    EssentialLink,
    StatusOnFooter,
    AvatarMenu
   },
   props: {
    namePage: {
      type: String,
      required: true
    }
   },
  setup () {
    const leftDrawerOpen = ref(false)
    const avatarMenu = ref(false)
    const store = useStore()
    const router = useRouter()
    const isAuthenticated = computed(() => store.getters['user/getIsAuthenticated'])
    const showFooter = ref(false)
    const loginPage = ref('/')

    const items = [
      { title: 'Home', to: '/home', icon: 'home' },
      { title: 'Colocar um carro à venda', to: '/postCar', icon: 'add_circle'},
      { title: 'Propostas de compra', to: '/proposals', icon: 'mail' },
      { title: 'Comprar carro', to: '/buyCar', icon: 'shopping_cart'},
      { title: 'Meus insights', to: '/insights', icon: 'bar_chart'}
    ]

    const logout = () => {
      store.commit('user/logout')
      showFooter.value = true

      const redirect = setTimeout(() => {
                        router.push(loginPage.value)
                      }, 1250)
      return redirect
    }
    
    const backgroundStyle = {
      backgroundImage: `url(${foto1})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundAttachment: 'fixed'
    }

    const avatar = sessionStorage.getItem('username')

    onBeforeMount(async () => {
        try {
          await store.dispatch('chat/connectSocket');
        } catch (error) {
          console.error('Erro ao conectar ao servidor Socket.IO:', error);
        }
    })

    onBeforeUnmount(async () => {
        try {
          await store.dispatch('chat/disconnectSocket');
        } catch (error) {
          console.error('Erro ao desconectar ao servidor Socket.IO:', error);
        }
    })

    return {
      leftDrawerOpen,
      avatarMenu,
      items,
      backgroundStyle,
      showFooter,
      logout,
      isAuthenticated,
      avatar,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      },
      toggleAvatarMenu () {
        avatarMenu.value = !avatarMenu.value
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.header {
  position: fixed;
}

.toolbar {
  color: black;
}

.toolbar-title {
  display: flex;
  justify-content: space-between;
  width: 100%;
  align-items: center;
}

.name-page {
  flex-shrink: 0;
}

.right-side {
  display: flex;
  align-items: center;
  margin-left: auto;
}

.notifications {
  margin-right: 10px;
}

.avatar {
  background-color: $secondary;
  border: 2px solid black;
  border-radius: 5px;
  padding: 3px;
}
</style>
