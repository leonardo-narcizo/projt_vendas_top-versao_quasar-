<template>
  <q-dialog v-model="showDialog" @hide="$emit('fechar-conversa')">
    <q-card style="width: 1000px;">
      <q-card-actions align="right" class="btn-close">
        <q-btn icon="close" color="negative" @click="$emit('fechar-conversa')" />
      </q-card-actions>
      <q-card-section class="header-section">
        <h4 class="text-h6">{{ chat.username_proprietario }} <q-avatar icon="arrow_forward"/>{{ chat.username_comprador }}</h4>
        <p class="data-car text-subtitle1">Carro tratado: {{ chat.marca }}, {{ chat.modelo }}</p>
      </q-card-section>

      <q-separator />

      <!-- Exibição das mensagens do chat -->
      <q-card-section style="max-height: 300px; overflow-y: auto" ref="messagesContainer">
        <q-list>
          <q-item v-if="chatMessages.length === 0" class="empty-chat text-center">
            <q-item-section >
              Sem Mensagens até agora...<br>
              Começe agora e mande uma mensagem!
            </q-item-section>
          </q-item>
          <q-item v-for="message in chatMessages" :key="message.id_mensagem">
            <q-item-section v-if="message.username != username" class="guest-container">
              <q-item-label>{{ message.username }}</q-item-label>
              <q-item-label caption>{{ message.conteudo }}</q-item-label><br>
              <q-item-label caption class="message-date">{{ message.data_envio }}</q-item-label>
            </q-item-section>
            <q-item-section v-else class="user-container">
              <q-item-label class="text-left">Você</q-item-label>
              <q-item-label caption class="text-left">{{ message.conteudo }}</q-item-label><br>
              <q-item-label caption class="message-date">{{ message.data_envio }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>

      <q-card-actions>
        <div class="send-message-box">
          <q-input
            v-model="newMessage"
            filled
            dense
            placeholder="Digite sua mensagem..."
            clearable
          >
            <template v-slot:append>
              <q-btn icon="send" @click="sendMessage" color="primary" flat />
            </template>
          </q-input>
        </div>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue';
import { useStore } from 'vuex';

export default {
  name: 'Conversation',
  props: {
    chat: Object, // Recebe o objeto chat como propriedade
  },
  setup(props, { emit }) {
    const username = sessionStorage.getItem('username');
    const store = useStore();
    const showDialog = ref(true); // Controle do diálogo
    const chatMessages = ref([]); // Usando ref para armazenar as mensagens do chat
    const newMessage = ref('');
    const messagesContainer = ref(null)
    const newMessageReceived = computed(() => store.getters['socket/getNewMessageTrue'])


    const fetchChatMessages = async () => {
      try {
        await store.dispatch('socket/searchChatMessages', { id_chat: props.chat.id_chat });
        chatMessages.value = store.getters['socket/getChatMessages'];
      } catch (error) {
        console.error('Erro ao buscar mensagens do chat:', error);
      }
    };

    const sendMessage = async () => {
      if (newMessage.value.trim() === '') {
        return;
      }

      const messageData = {
        id_chat: props.chat.id_chat,
        username_participante: username,
        conteudo: newMessage.value,
      };

      try {
        await store.dispatch('socket/sendMessage', messageData);
        newMessage.value = ''; // Limpando o input após o envio
        await fetchChatMessages(); // Atualizar mensagens após enviar uma nova
        scrollToBottom(); // Rolando para o final após enviar mensagem
        console.log('array de mensagens: ', chatMessages.value)
      } catch (err) {
        console.error('Erro ao enviar mensagem: ', err);
      }
    };

    // Função para rolar para o final da lista de mensagens
    const scrollToBottom = () => {
      nextTick(() => {
        if (messagesContainer.value && messagesContainer.value.$el) {
          messagesContainer.value.$el.style.scrollBehavior = 'smooth'
          messagesContainer.value.$el.scrollTop = messagesContainer.value.$el.scrollHeight;
        }
      });
    };


    // Rolar para o final quando as mensagens são atualizadas do usuario q envia a nova mensagem
    watch(chatMessages, (newMessages) => {
      console.log('usou o watcher!')
      if (newMessages.length > 0) {
        scrollToBottom();
      }
    });

    // Watcher para atualizar o scroll do destinátario da mensagem
    watch(newMessageReceived, (newVal) => {
      
      if (newVal) {
        console.log('identificou nova mesagem')
        scrollToBottom()
      }
    })

    // Assim que o componente é montado, busca as mensagens do chat
    onMounted(async () => {
      await fetchChatMessages();

      // Ouvir evento de nova mensagem enviada
      await store.dispatch('socket/listenForMessages', props.chat.id_chat);

      scrollToBottom();
    });

    onBeforeUnmount(() => {
      // Remover listener ao desmontar o componente
      store.dispatch('socket/removeMessagesListener');
    });

    return {
      chatMessages,
      showDialog,
      username,
      newMessage,
      sendMessage,
      messagesContainer
    };
  },
};
</script>

<style lang="scss" scoped>
.user-container, .guest-container {
  word-wrap: break-word; /* Força a quebra de linha quando o texto excede a largura */
}

.user-container {
  background-color: $secondary; // Cor de fundo para mensagens do usuário atual
  color: white; // Texto branco para melhor contraste
  margin-left: auto; // Alinha as mensagens do usuário atual à direita
  padding: 8px;
  border-radius: 8px;
  margin-left: 300px;
}

.guest-container {
  background-color: lightgrey; // Cor de fundo para mensagens de outros usuários
  padding: 8px;
  border-radius: 8px;
  margin-right: 300px;
}

.message-date {
  align-self: flex-end; // Alinha a data no final de cada mensagem
  color: rgb(172, 172, 172); // Cor cinza para a data
  font-size: 0.70rem; // Tamanho menor para a data
}

.btn-close {
  margin-bottom: -10%;
}

.send-message-box {
  width: 100%;
}

.data-car {
  margin-top: -5%;
  margin-bottom: -2%;
}

.header-section {
  background-color: #f5f5f5; // Cor de fundo para a seção do cabeçalho
  padding: 20px; // Espaçamento interno para a seção do cabeçalho
  border-bottom: 1px solid #e0e0e0; // Linha de divisão na parte inferior
  border-radius: 8px 8px 0 0; // Bordas arredondadas na parte superior
}

.header-section h4 {
  margin: 0; // Remove margem do título
  color: #333; // Cor do texto do título
}

.header-section .data-car {
  margin: 5px 0 0; // Margem superior e inferior para a descrição do carro
  color: #777; // Cor do texto da descrição do carro
}

.empty-chat {
  background-color: $warning;
}
</style>
