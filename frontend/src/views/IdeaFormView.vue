<script>
import axios from "axios"

export default {
    name: "app-idea-form-view",

    data() {
        return {
            tags: [],
            tagsUrl: "http://localhost:8000/api/tags/",
        }
    },

    created() {
        this.uploadTags()
    },

    methods: {
        async uploadTags() {
            await axios.get(this.tagsUrl)
                .then((response) => {
                    const tags = response.data
                    tags.forEach((tag) => {
                        tag['checked'] = false;
                    })
                    this.tags = tags;
                })
        },

        getCheckedTags() {
            var tagsId = [];

            this.tags.forEach((tag) => {
                if (tag.checked) {
                    tagsId.push(tag.id);
                }
            })
            return tagsId;
        }
    },
}
</script>

<template>
    <p>______________________________________</p>
    <p>Please, tell about your idea</p>
    <p>______________________________________</p>

    <div class="login d-flex justify-content-center " @submit.prevent="authenticateUser">
        <form class="col-md-6">
            <div class="dropdown">
                <p>Нou can choose some tags that match your idea to make it easier for other users to find it.</p>
                <button class="btn btn-secondary dropdown-toggle mb-3" type="button" id="dropdownMenuButton1"
                    data-bs-toggle="dropdown" aria-expanded="false">
                    Choose tags
                </button>
                <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                    <li v-for="tag in tags" :key="tag.id">
                        <a class="dropdown-item" href="#">
                            <input v-model="tag.checked" class="form-check-input" type="checkbox" value=""
                                id="flexCheckDefault" />
                            {{ tag.name }}
                        </a>
                    </li>
                </ul>
            </div>
            <div class="mb-3">
                <label class="form-label">Title</label>
                <input class="form-control">
            </div>
            <div class="mb-3">
                <label class="form-label">Content</label>
                <textarea class="form-control" rows="10"></textarea>
            </div>
        </form>
    </div>
</template>
