export function setBuyer(state, boolean) {
  state.buyer = boolean
}

export function setSeller(state, boolean) {
  state.seller = boolean
}
  
export function setSellerChats(state, chats) {
  state.sellerChats = chats
}

export function setBuyerChats(state, chats) {
  state.buyerChats = chats
}

export function setChatMessages(state, messages) {
  state.currentChat.chatMessages = messages
}

export function addChatMessage(state, message) {
  state.currentChat.chatMessages.push(message)
}

export function setNewChatId(state, chatId) {
  state.newChatId = chatId
}

export function setNewMessageTrue(state, result) {
  state.currentChat.newMessage = result
}