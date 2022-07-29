<script>
import axios from "axios"

export default {
    name: "app-idea-form-view",

    data() {
        return {
            categories: [],
            tags: [],
            tagsUrl: "http://localhost:8000/api/tags/",
            categoriesUrl: "http://localhost:8000/api/categories/",
            ideasUrl: "http://localhost:8000/api/ideas/",
            errors: {
                "title": "",
                "content": "",
            },
            validationError: false,
            idea: {
                title: "",
                content: "",
                tags: [],
                category: null,
            },
        }
    },

    mounted() {
        this.uploadTags();
        this.uploadCategories();

        let ideaId = this.$route.params.ideaId
        if (ideaId) {
            this.uploadIdea(ideaId);
        }
    },

    methods: {
        async uploadIdea(ideaId) {
            await axios.get(this.ideasUrl + ideaId + "/")
                .then((response) => {
                    let ideaData = response.data;
                    this.idea.title = ideaData.title;
                    this.idea.content = ideaData.content;
                    this.idea.category = ideaData.category.id;

                    let tagsId = [];
                    ideaData.tags.forEach((tag) => {
                        tagsId.push(tag.id);
                    })

                    this.tags.forEach((tag) => {
                        let tagId = tag.id;
                        if (tagsId.includes(tagId)) {
                            tag.checked = true;
                        }
                    })
                })
        },
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

        async uploadCategories() {
            await axios.get(this.categoriesUrl)
                .then((response) => {
                    const categories = response.data
                    this.categories = categories;
                    if (!this.idea.category) {
                        this.idea.category = categories[0].id;
                    }
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
        },

        uuidv4() {
            return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
                (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
            );
        },
        pushIdea() {
            this.validateIdeaData();

            if (this.validationError) {
                return;
            }

            let ideaId = this.$route.params.ideaId;

            if (ideaId) {
                this.updateIdea(ideaId);
            } else {
                this.postIdea();
            }
        },
        validateIdeaData() {
            this.validationError = false;
            this.errors.title = "";
            this.errors.content = "";

            if (!this.idea.title) {
                this.errors.title = "This field may not be blank";
                this.validationError = true;
            }

            if (!this.idea.content) {
                this.errors.content = "This field may not be blank";
                this.validationError = true;
            }
        },
        async updateIdea(ideaId) {
            let idea = this.idea;
            idea.tags = this.getCheckedTags();
            let accessToken = localStorage.getItem("accessToken");

            if (!accessToken) {
                return;
            }

            await axios.patch(this.ideasUrl + ideaId + "/", idea, {
                headers: {
                    Authorization: `Token ${accessToken}`
                }
            })
                .then(() => {
                    this.$router.push("/");
                })
        },

        async postIdea() {
            let idea = this.idea;
            idea.id = this.uuidv4();
            idea.tags = this.getCheckedTags();
            let accessToken = localStorage.getItem("accessToken");

            if (!accessToken) {
                return;
            }

            await axios.post(this.ideasUrl, idea, {
                headers: {
                    Authorization: `Token ${accessToken}`
                }
            })
                .then(() => {
                    this.$router.push("/");
                })
        }
    },
}
</script>

<template>

    <div class="login d-flex justify-content-center " @submit.prevent="pushIdea">
        <form class="col-md-6">
            <div class="dropdown">
                <div v-if="validationError" class="alert alert-danger mb-3" role="alert">
                    Please, fill the form correctly.
                </div>
                <p>You can choose some tags that match your idea to make it easier for other users to find it.</p>
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
            <div class="btn-group mb-3" role="group" aria-label="Basic radio toggle button group">
                <div v-for="category in categories" :key="category.id">
                    <input type="radio" class="btn-check" name="btnradio" :id="category.id" :value="category.id"
                        v-model="idea.category">
                    <label class="btn btn-outline-primary" :for="category.id">{{ category.name }}</label>
                </div>
            </div>
            <div class="mb-3">
                <label class="form-label">Title</label>
                <input class="form-control" :placeholder="errors.title" v-model="idea.title">
            </div>
            <div class="mb-3">
                <label class="form-label">Content</label>
                <textarea class="form-control" rows="10" :placeholder="errors.content"
                    v-model="idea.content"></textarea>
            </div>
            <button type="submit" class="btn btn-primary mb-3">Submit</button>
        </form>
    </div>
</template>
