<script>
import axios from "axios";

export default {
    name: "app-idea-card",
    props: {
        idea: Object
    },
    data() {
        return {
            ideasUrl: "http://sshishigin.space:8765/api/ideas/",
            likesUrl: "http://sshishigin.space:8765/api/likes/",
            baseUrl: "http://sshishigin.space:8765/media/",
            imagePath: "http://sshishigin.space:8765/media/images/dummy_image.png"
        }
    },
    methods: {
        getStandardDate(date) {
            return date;
        },
        getImagePath() {
            return this.imagePath;
        },
        async postLike(idea) {
            const accessToken = localStorage.getItem("accessToken");
            const ideaId = idea.id;
            if (!accessToken) {
                this.$router.push("/login");
                return;
            }
            await axios.post(this.likesUrl + ideaId + "/", {
                id: this.uuidv4()
            }, {
                headers: {
                    Authorization: `Token ${accessToken}`
                }
            })
                .then(() => {
                    if (idea.is_liked) {
                        idea.likes = idea.likes - 1;
                    } else {
                        idea.likes = idea.likes + 1;
                    }
                    idea.is_liked = !idea.is_liked;
                });
        },
        async deleteIdea(idea_id) {
            const accessToken = localStorage.getItem("accessToken");
            if (!accessToken) {
                return;
            }

            await axios.delete(this.ideasUrl + idea_id + "/", {
                headers: {
                    Authorization: `Token ${accessToken}`
                }
            })
            location.reload()
        },

        updateIdea(idea) {
            idea.category = idea.category.id;
            let tags = [];

            idea.tags.forEach((tag) => {
                tags.push(tag.id)
            })
            idea.tags = tags;

            this.$router.push(`ideaForm/${idea.id}/`)
        },
        uuidv4() {
            return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
                (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
            );
        },
        async uploadImagePath() {
            this.imagePath = this.idea.owner.profile_image;
        },
        getProfileLink() {
            return `/profile/${this.idea.owner.username}`;
        }
    },
    mounted() {
        this.uploadImagePath();
    }
}
</script>

<template>
    <div class="mb-4 p-5 pt-4 col-md-8 col-sm-10 bg-light card">
        <div class="">
            <div class="d-flex flex-row mb-3">
                <router-link :to="getProfileLink()" class="d-flex flex-row text-dark">
                    <div>
                        <img :src="getImagePath()" alt="mdo" width="50" height="50" class="rounded-circle">
                    </div>
                    <h5 class="mt-3 px-3 fs-6">{{ idea.owner.username }}</h5>
                </router-link>
                <h5 class="mt-3 px-3 fs-6 ms-auto text-secondary">Added: {{ getStandardDate(idea.date_added) }}</h5>
                <div class="ms-auto d-flex flex-row" v-if="idea.is_owner">
                    <div class="m-2">
                        <fa icon="fa-solid fa-pen" class="fa-lg fa-clickable" @click="updateIdea(idea)"></fa>
                    </div>
                    <div class=" m-2">
                        <fa icon="fa-solid fa-trash" class="fa-lg fa-clickable" @click="deleteIdea(idea.id)"></fa>
                    </div>
                </div>
            </div>
            <h5 class="fw-bold">{{ idea.title }}</h5>
            <p class="col-md-10 fs-6 mt-3">{{ idea.content }}</p>
            <div class="d-flex flex-row mt-3">
                <button class="btn btn-primary btn" type="button"
                    @click="this.$router.push({ name: 'idea', params: { ideaId: idea.id } })">Read full</button>
                <span @click="postLike(idea)" class="ms-auto">
                    <fa v-if="idea.is_liked" class="clickableFa fa-2x" icon="fa-solid fa-heart"></fa>
                    <fa v-else class="clickableFa fa-2x" icon="fa-regular fa-heart"></fa>
                </span>
                <h5 class="px-2 py-1">{{ idea.likes }}</h5>
            </div>
        </div>
    </div>
</template>

<style>
.fa-clickable {
    cursor: pointer;
}
</style>
