<script>
import axios from "axios";

export default {
    name: "app-header",

    data() {
        return {
            username: "",
            categoriesUrl: "http://localhost:8000/api/categories/",
            mediaUrl: "http://localhost:8000",
            categories: [],
        }
    },

    methods: {
        getUserName() {
            return localStorage.getItem("username");
        },
        getImagePath() {
            return this.mediaUrl + localStorage.getItem("image");
        },
        isUserAuthenticated() {
            const accessToken = localStorage.getItem("accessToken");
            if (accessToken == null) {
                return false;
            }
            return true;
        },

        async uploadCategories() {
            await axios.get(this.categoriesUrl)
                .then((response) => {
                    const categories = response.data
                    this.categories = categories;
                })

        },

        signOut() {
            localStorage.removeItem("accessToken");
            location.reload();
        },
        addIdea() {
            if (this.isUserAuthenticated()) {
                this.$router.push("/ideaForm");
                return
            }
            this.$router.push("login");
        },
        getIdeasOnCategory(categoryId) {
            this.$router.push({
                name: "category",
                params: {
                    category: categoryId
                }
            })
        },
        goToProfile() {
            const username = localStorage.getItem("username");
            this.$router.push(`/profile/${username}`);
        },
        goLogin() {
            this.$router.push('/login');
        }
    },

    mounted() {
        this.uploadCategories();
    }
}
</script>

<template>
    <header class="p-3 border-bottom mb-3">
        <div class="container">
            <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
                <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
                    <li>
                        <router-link to="/" class="nav-link px-2 link-secondary">Home
                        </router-link>
                    </li>
                    <li v-for="category in categories" :key="category.id">
                        <a href="#" @click="getIdeasOnCategory(category.id)" class="nav-link px-2 link-dark">{{
                                category.name
                        }}
                        </a>
                    </li>
                    <li>
                        <a href="#" class="nav-link px-2 link-success" @click="addIdea">Suggest idea</a>
                    </li>
                    <button type="button" class="btn btn-outline-primary mx-1"
                        @click="this.$router.push('/chat')">Chat</button>
                </ul>

                <!-- <form class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3">
                    <input type="search" class="form-control" placeholder="Search..." aria-label="Search">
                </form> -->

                <div v-if="isUserAuthenticated()" class="dropdown text-end">
                    <a href="#" class="d-block link-dark text-decoration-none dropdown-toggle" id="dropdownUser1"
                        data-bs-toggle="dropdown" aria-expanded="false">
                        <img :src="getImagePath()" alt="mdo" width="32" height="32" class="rounded-circle">
                    </a>
                    <ul class="dropdown-menu text-small" aria-labelledby="dropdownUser1">
                        <li><a class="dropdown-item" href="#" @click.prevent="goToProfile">Profile</a>
                        </li>
                        <li><a class="dropdown-item" href="#">Settings</a></li>
                        <li>
                            <hr class="dropdown-divider">
                        </li>
                        <li>
                            <a href="#" class="dropdown-item" @click="signOut">Sign out</a>
                        </li>
                    </ul>
                </div>
                <div v-else class="text-end">
                    <button type="button" class="btn btn-light me-2" @click="goLogin">Login</button>
                    <button type="button" class="btn btn-warning"
                        @click="this.$router.push('/register')">Sign-up</button>
                </div>
            </div>
        </div>
    </header>
</template>
