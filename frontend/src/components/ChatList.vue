<template>
  <div>
    <div class="div-header text-h6 q-mb-lg q-px-xs">
      <div>{{ currentFilterLabel }}</div>
      <div class="filtros"> 
        <q-btn 
          dense flat round icon="filter_alt" 
          label="Filtros"
          color="secondary"
          @click="menu = true"
        />
        <filter-menu :onSelect="updateFilter" currentTab="chats" />
      </div>
    </div>

    <q-list bordered v-if="chats.length > 0">
      <q-item v-for="chat in chats" :key="chat.id_chat" clickable @click="openChat(chat)">
        <q-item-section>
          <q-item-label v-if="currentFilter == 'chat_venda'" class="text-bold">
             {{ chat.username_comprador }} (Comprador)
          </q-item-label>
          <q-item-label v-if="currentFilter == 'chat_compra'" class="text-bold">
             {{ chat.username_proprietario }} (Proprietário) 
          </q-item-label>
          <q-item-label caption>{{ chat.marca }}, {{ chat.modelo }}</q-item-label>
        </q-item-section>
      </q-item>
    </q-list>

    <div v-else class="q-pa-md text-h6 text-center">
      Não há conversas
    </div>
    <Conversation v-if="selectedChat" :chat="selectedChat" @fechar-conversa="selectedChat = null" />
  </div>
</template>

<script>
import { ref, watch, onMounted, onBeforeMount, onBeforeUnmount, computed } from 'vue'
import { useStore } from 'vuex'
import FilterMenu from './FilterMenu.vue'
import Conversation from './dialogs/Conversation.vue'

export default {
  name: 'ChatList',
  components: {
    FilterMenu,
    Conversation
  },
  setup() {
    const store = useStore();
    const username = sessionStorage.getItem('username');
    const chats = ref([]);
    const selectedChat = ref(null)
    const newChatId = computed(() => store.getters['socket/getNewChatId']);

    // Configuração do header com os filtros
    const currentFilterLabel = ref('Chats de venda');
    const currentFilter = ref('chat_venda');

    const updateFilter = ({ filter, label }) => {
      currentFilter.value = filter;
      currentFilterLabel.value = label;
      handleSearchChats(username, filter);
    }

    

    const handleSearchChats = async (username, situation) => {
      try {
        const fetchedChats = await store.dispatch('socket/searchUserChats', { username, situation });
        chats.value = fetchedChats;
      } catch (err) {
        console.error('Erro ao buscar conversas:', err);
      }
    }

    watch(currentFilter, (newVal) => {
      if (newVal === 'chat_compra') {
        handleSearchChats(username, newVal);
      } else if (newVal === 'chat_venda') {
        handleSearchChats(username, newVal);
      }
    })

    watch(newChatId, async (newVal) => {
      if (newVal) {
        console.log('mudouu: ', newVal)
        await handleSearchChats(username, currentFilter.value)
        const chat = chats.value.find(chat => chat.id_chat == newVal);
        if (chat) {
          await openChat(chat);
          store.commit('socket/setNewChatId', null)
        } else {
          // Se o chat ainda não estiver na lista, buscar do servidor (opcional)
          const fetchedChat = store.dispatch('socket/fetchChatById', newVal);
          if (fetchedChat) {
            chats.value.push(fetchedChat);
            openChat(fetchedChat);
          }
        }
      }
    });




    onMounted(async () => {
      await handleSearchChats(username, currentFilter.value);
    });

    onBeforeUnmount(() => {
      // Remover listener ao desmontar o componente
      store.dispatch('socket/removeMessagesListener')
    });

    const openChat = async  (chat) => {
      console.log('Abrindo chat:', chat);
      selectedChat.value = chat
    };

    const fecharConversa = () => {
      selectedChat.value = null;
    };

    return {
      currentFilter,
      currentFilterLabel,
      updateFilter,
      chats,
      selectedChat,
      openChat,
      fecharConversa
    };
  }
};
</script>

<style scoped>
.chat-list {
  max-width: 1100px;
  margin: 0 auto;
}

.div-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 2px solid black;
  border-radius: 5px;
}
</style>
