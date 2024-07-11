export default function() {
    return {
      sellerChats: [],
      buyerChats: [],
      seller: false,
      buyer: false,
      newChatIsCreated: false,
      currentChat: {
        id_chat: null,
        chatMessages: [],
        newMessage: false
      },
      newChatId: null
    }
  }
  