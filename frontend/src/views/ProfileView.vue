<script>
import axios from 'axios';

export default {
    name: "app-profile-view",
    data() {
        return {
            username: undefined,
            userUrl: "http://localhost:8000/api/users/",
            baseUrl: "http://localhost:8000",
            userData: undefined,
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
    <p>{{ userData }}</p>

    <div>

    </div>

</template>