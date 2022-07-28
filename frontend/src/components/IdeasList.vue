<script>
import axios from "axios"
import Observer from "./Observer.vue"

export default {
    name: "app-ideas-list",

    components: {
        Observer,
    },

    data() {
        return {
            ideas: [],
            currentPage: 1,
            lastPage: undefined,
            ideasUrl: "http://localhost:8000/api/ideas/",
            likesUrl: "http://localhost:8000/api/likes/",
            pageSize: 2,
        }
    },

    methods: {
        async uploadIdeas() {
            if (this.lastPage != null && this.currentPage > this.lastPage) { return }

            let accessToken = localStorage.getItem("accessToken")
            let headers = {

            };

            if (accessToken) {
                headers["Authorization"] = `Token ${accessToken}`;
            }

            const fetchData = await axios.get(this.ideasUrl + `?page=${this.currentPage++}` + `&page_size=${this.pageSize}`, {
                headers: headers
            })
            const ideasData = fetchData.data;

            console.log(this.lastPage);
            this.lastPage = Math.ceil(ideasData.count / this.pageSize);

            const ideas = ideasData.results;
            this.ideas.push(...ideas);
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
        async postLike(idea) {
            const accessToken = localStorage.getItem("accessToken");
            const ideaId = idea.id;
            if (!accessToken) {
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
                    idea.is_liked = !idea.is_liked;
                });
        }
    },

    mounted() {
        this.uploadIdeas()
    }
}
</script>

<template>
    <p>______________________________________</p>
    <div v-for="idea in ideas" :key="idea.id">
        <p>{{ idea.owner.username }}</p>
        <p>{{ idea.title }}</p>
        <p>{{ idea.content }}</p>
        <p>{{ idea.tags }}</p>
        <p>{{ idea.category }}</p>
        <p>Date added: {{ idea.date_added }}</p>
        <button v-if="idea.is_owner" @click="updateIdea(idea)" type="button" class="btn btn-warning">Update
            idea</button>
        <button v-if="idea.is_owner" @click="deleteIdea(idea.id)" type="button" class="btn btn-danger">Delete</button>
        <span @click="postLike(idea)">
            <fa v-if="idea.is_liked" class="clickableFa fa-2x" icon="fa-solid fa-heart"></fa>
            <fa v-else class="clickableFa fa-2x" icon="fa-regular fa-heart"></fa>
        </span>
        <p>_____________________________________________</p>
    </div>
    <Observer @intersect="uploadIdeas" />
    <p>Footer</p>
</template>

<style>
.clickableFa {
    cursor: pointer
}
</style>