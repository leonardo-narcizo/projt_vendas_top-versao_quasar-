import { data } from 'autoprefixer';
import io from 'socket.io-client'

let socket = null
const baseURL = 'http://localhost:5000'

export async function connectSocket({ state, commit }) {
  if (!socket) {
    socket = io(baseURL, {
      autoConnect: false,
    });

    socket.on('connect', () => {
      console.log('Conexão com o servidor Socket.IO estabelecida.');
    });

    // Conectar manualmente após configurar o socket
    socket.connect();
  }
}

export async function disconnectSocket({ state, commit }) {
  if (socket) {
    socket = null
    
    console.log('Desconectado do servidor Socket.IO.');
  }
}


export async function searchUserChats({ state, commit }, { username, situation }) {
  try {
    if (situation === 'chat_venda') {
      commit('setSeller', true);
      socket.emit('show_seller_chats', { username });

      return new Promise((resolve, reject) => {
        socket.on('found_chats', (response) => {
          console.log('Chegou na API de seller e emitiu o evento de found_chats');
          console.log('chats retornados: ', response.chats);
        
          commit('setSellerChats', response.chats);
          resolve(response.chats); 
        });
    
        socket.on('error', (error) => {
          console.error('Erro:', error.message);
          reject(error); 
        });
    
        socket.on('data_error', (data_error) => {
          console.error('Erro de dados:', data_error.message);
          reject(data_error); 
        });
      });
    }

    else if (situation === 'chat_compra') {
      commit('setBuyer', true);
      socket.emit('show_buyer_chats', { username });

      return new Promise((resolve, reject) => {
        socket.on('found_chats', (response) => {
          console.log('Chegou na API de buyer e emitiu o evento de found_chats');
          console.log('chats retornados: ', response.chats);
        
          commit('setBuyerChats', response.chats);
          resolve(response.chats); 
        });
    
        socket.on('error', (error) => {
          console.error('Erro:', error.message);
          reject(error); 
        });
    
        socket.on('data_error', (data_error) => {
          console.error('Erro de dados:', data_error.message);
          reject(data_error); 
        });
      });
    }
  } catch (err) {
    console.error('Erro ao tentar buscar chats da API', err);
    throw err; 
  }
}


export async function searchChatMessages({ commit }, { id_chat }) {
  try {
    socket.emit('show_chat_messages', { id_chat });

      return new Promise((resolve, reject) => {
        socket.on('found_messages', (response) => {
          console.log('mensagens desse chat: ', response.messages);
        
          commit('setChatMessages', response.messages);
          resolve(response.messages)
        });
    
        socket.on('error', (error) => {
          console.error('Erro:', error.message);
          reject(error);
        });
    
        socket.on('data_error', (data_error) => {
          console.error('Erro de dados:', data_error.message);
          reject(data_error); 
        });
      });
  }
  catch (err) {
      console.error('Erro ao tentar buscar chats da API', err);
      throw err
  }
}


export async function sendMessage({ commit }, messageData) {
  return new Promise((resolve, reject) => {
    socket.emit('send_message', messageData);
    

    socket.once('sent_message', (message) => {
      commit('setNewMessageTrue', true)
      resolve(message);
    });

    socket.on('error', (error) => {
      console.error('Erro:', error.message);
      reject(error); // Rejeita a promessa em caso de erro
    });

    socket.on('data_error', (data_error) => {
      console.error('Erro de dados:', data_error.message);
      reject(data_error); // Rejeita a promessa em caso de erro de dados
    });
  });
}


// Function extremamente importante q ficará ouvindo uma nova mensagem chegando em tmepo real
export async function listenForMessages({ commit }, id_chat) {
  socket.off('sent_message'); // Remove qualquer escuta existente

  socket.on('sent_message', (message) => {
      commit('addChatMessage', message);
      console.log('esaa: ', message)
  });
}

export async function removeMessagesListener() {
  socket.off('sent_message')
}


export async function criarNovoChat({ commit }, { proprietarioUsername, compradorUsername, idCarro }) {
  try {
    const data = {
      proprietario_username: proprietarioUsername,
      comprador_username: compradorUsername,
      id_carro: idCarro
    }

    // Emitindo o evento 'create_chat' para o servidor
    socket.emit('create_chat', data);

    return new Promise((resolve, reject) => {
      // Ouvindo pela resposta do servidor após emitir o evento
      socket.on('chat_created', (response) => {
        console.log(response.message); // Mensagem de sucesso
        console.log(response.new_chat_id); // ID do novo chat criado
        commit('setNewChatId', response.new_chat_id)
        resolve(response); // Resolve a promessa com os dados recebidos
      });

      // Ouvindo por erros, caso ocorram
      socket.on('error', (error) => {
        console.error(error.message); // Mensagem de erro do servidor
        reject(error); // Rejeita a promessa com o erro recebido
      });

      // Ouvindo emissão de erro de dados enviados
      socket.on('data_error', (data_error) => {
        console.error(data_error.message)
        reject(data_error)
      })
    });
  } catch (error) {
    console.error('Erro ao criar chat:', error);
    throw error;
  }
}


export async function listenSoldCar() {
  socket.on('new_sold_car', (new_sold_car) => {
    console.log(new_sold_car.carro_vendido)
  })
}












