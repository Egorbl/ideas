<script>
import axios from "axios";

export default {
    name: "app-chat-view",
    data() {
        return {
            baseUrl: "http://sshishigin.space:8765",
            chatsUrl: "http://sshishigin.space:8765/api/chats/",
            usersUrl: "http://sshishigin.space:8765/api/users/",
            chatWsUrl: "ws://sshishigin.space:8765/ws/chat/",
            chats: [],
            creatingChat: false,
            users: [],
            selectedUsers: [],
            chatName: "",
            userSearch: "",
            currentMessage: "",
            currentChatSocket: undefined,
        }
    },
    methods: {
        uploadChats() {
            const accessToken = this.getAccessTokenOrRedirect();
            axios.get(this.chatsUrl, {
                headers: {
                    Authorization: `Token ${accessToken}`
                }
            })
                .then((response) => {
                    this.chats = response.data;
                    this.connectToChats();
                })
        },
        connectToChats() {
            for (const chat of this.chats) {
                this.connectToChatSocket(chat);
            }
        },
        connectToChatSocket(chat) {
            const accessToken = localStorage.getItem("accessToken");
            chat.chatSocket = new WebSocket(this.chatWsUrl + chat.id + "/" + `?${accessToken}`);
            chat.chatSocket.onmessage = this.getMessageFromSocket(chat, this.scrollMessagesToBottom);
        },
        getMessageFromSocket(chat, scrollFunc) {
            return (event) => {
                const func = () => {
                    const data = JSON.parse(event.data);
                    chat.last_message = data;
                    if (chat.messages) {
                        chat.messages.push(data);
                    }
                    return Promise.resolve("Succcess");
                }
                func().then(() => {
                    scrollFunc();
                })
            }
        },
        getAccessTokenOrRedirect() {
            const accessToken = localStorage.getItem("accessToken");
            if (!accessToken) {
                this.$router.push("/login");
            }
            return accessToken;
        },
        startCreatingChat() {
            this.creatingChat = true;
            this.uploadUsers();
        },
        async uploadUsers() {
            await axios.get(this.usersUrl)
                .then((response) => {
                    this.users = response.data;
                })
        },
        changeUserState(user) {
            if (this.selectedUsers.indexOf(user) >= 0) {
                this.selectedUsers = this.selectedUsers.filter((element) => {
                    return element != user;
                })
                return;
            }
            this.selectedUsers.push(user);
        },
        createChat() {
            const chatId = this.uuidv4();
            const accessToken = this.getAccessTokenOrRedirect();
            let usersId = [];
            this.selectedUsers.forEach((user) => {
                usersId.push(user.id);
            })

            const chatData = {
                id: chatId,
                name: this.chatName,
                participants: usersId
            }

            axios.post(this.chatsUrl, chatData, {
                headers: {
                    Authorization: `Token ${accessToken}`
                }
            })
                .then((response) => {
                    this.creatingChat = false;
                    this.chats.push(response.data);
                    const chat = this.chats[this.chats.length - 1]
                    this.connectToChatSocket(chat);
                })
        },
        uuidv4() {
            return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
                (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
            );
        },
        uploadMessages(chatId) {
            const accessToken = this.getAccessTokenOrRedirect();
            const url = this.chatsUrl + chatId + "/messages/";
            axios.get(url, {
                headers: {
                    Authorization: `Token ${accessToken}`
                }
            })
                .then((response) => {
                    for (const chat of this.chats) {
                        if (chat.id == chatId) {
                            chat.messages = response.data;
                            continue;
                        }
                        chat.messages = undefined;
                    }
                })
                .then(() => {
                    this.scrollMessagesToBottom();
                })
        },
        chatMessage() {
            const dataToSend = JSON.stringify({
                'message': this.currentMessage
            })
            this.currentChatSocket.send(dataToSend);
            this.currentMessage = "";
        },
        changeChat(chatId) {
            this.uploadMessages(chatId);
            this.currentChatSocket = this.chats.filter((chat) => {
                return chat.id == chatId;
            })[0].chatSocket
        },
        getFullImagePath(imagePath) {
            let result = imagePath;
            if (!result.startsWith("http")) {
                result = this.baseUrl + result;
            }
            return result;
        },
        scrollMessagesToBottom() {
            const messagesDiv = document.querySelector("#messages");
            let scrollHeight = messagesDiv.scrollHeight;
            messagesDiv.scrollTop = scrollHeight;
        }
    },
    mounted() {
        this.uploadChats();
    },
    computed: {
        filteredUsers() {
            return this.users.filter((user) => {
                return user.username.startsWith(this.userSearch);
            })
        },
        currentChatMessages() {
            for (const chat of this.chats) {
                if (chat.messages) {
                    return chat.messages;
                }
            }
            return [];
        }
    }
}
</script>

<template>
    <div class="d-flex flex-column align-items-center container-fluid mb-5">
        <div class="d-flex flex-row col-12 col-md-10 mb-3 justify-content-center">
            <button type="button" class="btn btn-outline-success" @click="startCreatingChat">Start new
                chat</button>
            <button v-if="creatingChat" class="btn btn-outline-danger mx-1"
                @click="creatingChat = false">Cancel</button>
        </div>
        <div class="d-flex flex-column col-12 col-md-10 mb-3 align-items-center" v-if="creatingChat">
            <div class="col-6 mb-3">
                <input class="form-control" type="text" placeholder="Enter chat name" v-model="chatName">
                <div class="col-6">
                </div>
                <div class="form-group d-flex flex-column align-items-center">
                    <label for="exampleFormControlSelect2">Choose users to add</label>
                    <div class="col-6">
                        <input class="form-control" type="text" placeholder="Enter username" v-model="userSearch">
                    </div>
                    <select multiple class="form-control" id="exampleFormControlSelect2">
                        <option v-for="user in filteredUsers" :key="user.id" @click="changeUserState(user)">
                            {{ user.username }}
                        </option>
                    </select>
                    <div class="d-flex flex-wrap p-1">
                        <p v-for="user in selectedUsers" :key="user.id" class="mx-1">
                            {{ user.username }}

                        </p>
                    </div>
                </div>
            </div>
            <button type="button" class="btn btn-success" @click="createChat">Create</button>
        </div>
        <div class="d-flex flex-row col-12 col-md-10 card">
            <div class="d-flex flex-column col-5 scrollingDiv fullSize p-4">
                <div v-for="chat in chats" :key="chat.id" class="clickable card m-1" @click="changeChat(chat.id)">
                    <div class="m-1">
                        <h5>{{ chat.name }}</h5>
                        <div v-if="chat.last_message">
                            <img :src="getFullImagePath(chat.last_message.owner.profile_image)" alt="mdo" width="30"
                                height="30" class="rounded-circle">
                            {{ chat.last_message.content }}
                        </div>
                        <div v-else>No messages yet</div>
                    </div>
                </div>
            </div>
            <div class="d-flex justify-content-end flex-column col-7 p-3 fullSize">
                <div class="d-flex flex-column scrollingDiv p-3" id="messages">
                    <div v-for="message in currentChatMessages" :key="message.id" class="m-right-3">
                        <div class="d-flex flex-row px-5 py-3 bg-light">
                            <img :src="getFullImagePath(message.owner.profile_image)" alt="mdo" width="30" height="30"
                                class="rounded-circle">
                            <div class="mx-3 mt-1 d-flex flex-column col-md-10">
                                <p>{{ message.owner.username }}</p>

                                <div>
                                    <p>{{ message.content }}</p>
                                </div>
                            </div>
                        </div>
                        <p> </p>
                    </div>
                </div>
                <form class="d-flex flex-row" @submit.prevent="chatMessage" v-if="currentChatSocket">
                    <input class="form-control" type="text" placeholder="Enter your message" v-model="currentMessage">
                    <button class="btn btn-outline-success">></button>
                </form>
            </div>
        </div>
    </div>
</template>

<style>
.showBorders {
    border: 1px solid black;
}

.clickable {
    cursor: pointer;
}

.scrollingDiv {
    overflow: scroll;
    overflow-x: hidden;
}

.fullSize {
    height: 75vh;
}
</style>
