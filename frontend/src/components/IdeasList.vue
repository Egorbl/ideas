<script>
import axios from "axios"
import Observer from "./Observer.vue"

export default {
    name: "app-ideas-list",

    components: {
        Observer,
    },
    props: {
        categoryId: undefined
    },

    watch: {
        categoryId() {
            this.lastPage = undefined;
            this.currentPage = 1;
            this.ideas = [];
            this.uploadIdeas();
        }
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
            if (this.lastPage == null && this.currentPage == 2) { return }
            if (this.lastPage != null && this.currentPage > this.lastPage) { return }

            let accessToken = localStorage.getItem("accessToken")
            let headers = {

            };

            if (accessToken) {
                headers["Authorization"] = `Token ${accessToken}`;
            }

            let url = this.ideasUrl + `?page=${this.currentPage++}` + `&page_size=${this.pageSize}`;
            if (this.categoryId) {
                url += `&category=${this.categoryId}`;
            }

            await axios.get(url, {
                headers: headers
            })
                .then((response) => {
                    const ideasData = response.data;

                    this.lastPage = Math.ceil(ideasData.count / this.pageSize);

                    const ideas = ideasData.results;
                    this.ideas.push(...ideas);
                })
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
        getStandardDate(date) {
            return date;
        }
    },

    mounted() {
        console.log(this.categoryId);
        this.uploadIdeas()
    }
}
</script>

<template>
    <div class="d-flex flex-column align-items-center mt-3">
        <div v-for="idea in ideas" :key="idea.id" class="mb-4 p-5 bg-light col-md-8 col-sm-10">
            <div class="container-fluid">
                <div class="d-flex flex-row mb-3">
                    <div>
                        <img src="https://github.com/mdo.png" alt="mdo" width="50" height="50" class="rounded-circle">
                    </div>
                    <h5 class="mt-3 px-3 fs-6">{{ idea.owner.username }}</h5>
                    <h5 class="mt-3 px-3 fs-6 ms-auto text-secondary">Added: {{ getStandardDate(idea.date_added) }}</h5>
                </div>
                <h5 class="fw-bold">{{ idea.title }}</h5>
                <p class="col-md-10 fs-6 mt-3">{{ idea.content }}</p>
                <div class="d-flex flex-row mt-3">
                    <button class="btn btn-primary btn" type="button">Read full</button>
                    <button v-if="idea.is_owner" class="btn btn-warning mx-1" @click="updateIdea(idea)">Update</button>
                    <button v-if="idea.is_owner" class="btn btn-danger mx-1"
                        @click="deleteIdea(idea.id)">Delete</button>
                    <span @click="postLike(idea)" class="ms-auto">
                        <fa v-if="idea.is_liked" class="clickableFa fa-2x" icon="fa-solid fa-heart"></fa>
                        <fa v-else class="clickableFa fa-2x" icon="fa-regular fa-heart"></fa>
                    </span>
                    <h5 class="px-2 py-1">{{ idea.likes }}</h5>
                </div>
            </div>
        </div>
    </div>
    <Observer @intersect="uploadIdeas" />
    <p invisible>Footer</p>
</template>

<style>
.clickableFa {
    cursor: pointer
}
</style>