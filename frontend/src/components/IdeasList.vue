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
            pageSize: 2
        }
    },

    methods: {
        async uploadIdeas() {
            if (this.lastPage != null && this.currentPage > this.lastPage) { return }

            const fetchData = await axios.get(this.ideasUrl + `?page=${this.currentPage++}` + `&page_size=${this.pageSize}`)
            const ideasData = fetchData.data;

            this.lastPage = Math.ceil(ideasData.count / this.pageSize);

            const ideas = ideasData.results;
            this.ideas.push(...ideas);
            console.log("pushing")
        }
    },

    created() {
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
        <p>_____________________________________________</p>
    </div>
    <Observer @intersect="uploadIdeas" />
</template>