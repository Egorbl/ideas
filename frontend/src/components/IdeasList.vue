<script>
import axios from "axios"
import Observer from "./Observer.vue"
import IdeaCard from "./IdeaCard.vue";

export default {
    name: "app-ideas-list",

    components: {
        Observer,
        IdeaCard,
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
            pageSize: 4,
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
    },

    mounted() {
        this.uploadIdeas()
    }
}
</script>

<template>
    <div class="d-flex flex-column align-items-center mt-3">
        <IdeaCard v-for="idea in ideas" :key="idea.id" :idea="idea"></IdeaCard>
    </div>
    <Observer @intersect="uploadIdeas" />
    <!-- <p>Footer</p> -->
</template>

<style>
.clickableFa {
    cursor: pointer
}
</style>