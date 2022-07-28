<script>
export default {
    name: "app-header",

    data() {
        return {
            username: "",
        }
    },

    methods: {
        getUserName() {
            return localStorage.getItem("username");
        },

        isUserAuthenticated() {
            const accessToken = localStorage.getItem("accessToken");
            console.log("checking authentication");
            if (accessToken == null) {
                console.log("not authenticated");
                return true;
            }
            console.log("authenticated");
            return false;
        }
    }
}
</script>

<template>
    <nav>
        <router-link to="/">Home</router-link> |
        <span v-if="isUserAuthenticated()">
            <router-link to="/login">Login</router-link> |
            <router-link to="register">Register</router-link>
        </span>
        <span v-else>
            <router-link to="logout">Logout</router-link> |
            <span>Hello, {{ getUserName() }}</span>
        </span>
    </nav>
</template>