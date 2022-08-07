<script>
import axios from 'axios';

export default {
    name: "app-profile-view",
    data() {
        return {
            username: undefined,
            userUrl: "http://localhost:8000/api/users/",
            baseUrl: "http://localhost:8000",
            userData: {},
            userImage: "/media/images/dummy_image.png"
        }
    },
    methods: {
        async uploadProfile() {
            const accessToken = localStorage.getItem("accessToken");
            const headers = {};

            if (accessToken) {
                headers["Authorization"] = `Token ${accessToken}`;
            }

            await axios.get(this.userUrl + this.username + "/", {
                headers: headers
            })
                .then((response) => {
                    this.userData = response.data;
                    this.userImage = this.userData.profile_image;
                })
        },
        getStandardDate(date) {
            return date;
        }
    },
    async mounted() {
        this.username = this.$route.params.username;
        await this.uploadProfile();
    },
    computed: {
        fullImageUrl() {
            return this.baseUrl + this.userImage;
        }
    }
}
</script>

<template>
    <!-- <p>{{ userData }}</p> -->

    <div class="d-flex flex-column align-items-center">
        <img :src="fullImageUrl" alt="mdo" width="300" height="300" class="rounded-circle mb-3">
        <p class="mb-3">Username: {{ userData.username }}</p>
        <span>
            <p v-if="userData.hide_email && !userData.is_owner">Email: ****</p>
            <p v-else>Email: {{ userData.email }}</p>
        </span>
        <p>Date joined: {{ getStandardDate(userData.date_joined) }}</p>
        <p>Last login: {{ getStandardDate(userData.last_login) }}</p>
        <div v-if="userData.is_owner" class="d-flex flex-row">
            <button type="button" class="btn btn-success mx-1" @click="this.$router.push('/updateProfile')">Change
                profile data</button>
            <button type="button" class="btn btn-warning" @click="this.$router.push('/changePassword')">Change
                password</button>
        </div>
    </div>

</template>