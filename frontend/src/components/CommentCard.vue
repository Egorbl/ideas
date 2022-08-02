<script>
import axios from "axios";

export default {
    name: "app-comment-card",
    props: {
        comment: Object,
    },
    emits: [
        'commentDelete',
        'commentUpdate'
    ],
    data() {
        return {
            commentsUrl: "http://localhost:8000/api/comments/",
            likesUrl: "http://localhost:8000/api/likes/",
            updating: false,
            commentText: "",
        }
    },
    methods: {
        async deleteComment(comment) {
            const accessToken = localStorage.getItem("accessToken");
            const commentId = comment.id;
            let headers = {};
            if (accessToken) {
                headers["Authorization"] = `Token ${accessToken}`;
            }

            await axios.delete(this.commentsUrl + commentId + "/", {
                headers: headers
            }).then(() => {
                this.$emit('commentDelete', comment);
            })
        },
        cancelUpdate() {
            this.commentText = "";
            this.updating = false;
        },
        startUpdate() {
            this.commentText = this.comment.content;
            this.updating = true;
        },
        async updateComment(comment) {
            const commentId = comment.id;
            const accessToken = localStorage.getItem("accessToken");
            let headers = {};

            if (accessToken) {
                headers["Authorization"] = `Token ${accessToken}`;
            }

            await axios.patch(this.commentsUrl + commentId + '/', {
                content: this.commentText
            }, { headers: headers })
                .then((response) => {
                    this.cancelUpdate();
                    this.$emit('commentUpdate', response.data);
                })
        },
        async postLike(comment) {
            const accessToken = localStorage.getItem("accessToken");
            const commentId = comment.id;
            if (!accessToken) {
                this.$router.push("/login");
                return;
            }
            await axios.post(this.likesUrl + commentId + "/", {
                id: this.uuidv4()
            }, {
                headers: {
                    Authorization: `Token ${accessToken}`
                }
            })
                .then(() => {
                    if (comment.is_liked) {
                        comment.likes = comment.likes - 1;
                    } else {
                        comment.likes = comment.likes + 1;
                    }
                    comment.is_liked = !comment.is_liked;
                });
        },
        uuidv4() {
            return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
                (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
            );
        },
    },
}
</script>

<template>
    <div class="d-flex flex-row px-5 py-3 bg-light">
        <img src="https://github.com/mdo.png" alt="mdo" width="30" height="30" class="rounded-circle">
        <div class="mx-3 mt-1 d-flex flex-column col-md-10">
            <p>{{ comment.owner.username }}</p>

            <form v-if="updating" class="d-flex flex-column w-100" @submit.prevent="updateComment(comment)">
                <textarea v-model="commentText"></textarea>
                <div class="d-flex flex-row mt-1">
                    <button type="button" class="btn btn-danger" @click="cancelUpdate">Cancel</button>
                    <button type="submit" class="btn btn-primary mx-1">Save</button>
                </div>
            </form>
            <div v-else>
                <p>{{ comment.content }}</p>
            </div>
        </div>
        <div class="d-flex justify-content-between flex-column">
            <div class="d-flex flex-row mt-1" v-if="comment.is_owner">
                <fa icon="fa-solid fa-pen" class="fa-clickable m-1" @click="startUpdate"></fa>
                <fa icon="fa-solid fa-trash" class="faClickable m-1" @click="deleteComment(comment)"></fa>
            </div>
            <div class="ms-auto d-flex flex-row">
                <span @click="postLike(comment)">
                    <fa v-if="comment.is_liked" icon="fa-solid fa-heart" class="fa-clickable mt-2"></fa>
                    <fa v-else icon="fa-regular fa-heart" class="fa-clickable mt-2"></fa>
                </span>
                <p class="mx-1 display-7 mt-1">{{ comment.likes }}</p>
            </div>
        </div>
    </div>
</template>

<style>
.faClickable {
    cursor: pointer;
}

.show-borders {
    border: 1px solid black;
}

.break-words {
    word-wrap: break-word;
}
</style>