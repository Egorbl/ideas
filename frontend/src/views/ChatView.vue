<script>
export default {
    name: "app-chat-view",
    data() {
        return {
            chatUrl: "ws://localhost:8000/ws/chat/",
            chatSocket: undefined,
            message: ""
        }
    },
    methods: {
        sendMessage() {
            this.chatSocket.send(JSON.stringify({
                'message': this.message
            }))
        }
    },
    mounted() {
        this.chatSocket = new WebSocket(this.chatUrl);
    }
}
</script>

<template>
    <form @submit.prevent="sendMessage" class="w-100 d-flex flex-row">
        <input type="text" class="form-control" placeholder="Write your message here" aria-describedby="button-addon2"
            v-model="message">
        <button class="btn btn-outline-secondary" type="submit" id="button-addon2">></button>
    </form>
</template>