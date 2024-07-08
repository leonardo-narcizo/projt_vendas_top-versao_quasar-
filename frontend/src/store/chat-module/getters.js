export function getSellerChats(state) {
    return state.sellerChats
}

export function getBuyerChats(state) {
    return state.buyerChats
}

export function getChatMessages(state) {
    return state.currentChat.chatMessages
}

export function getNewChatId(state) {
    return state.newChatId
}

export function getNewMessageTrue(state) {
    return state.currentChat.newMessage
}