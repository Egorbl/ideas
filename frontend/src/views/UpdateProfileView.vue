<script>
import axios from "axios";

export default {
    name: "app-update-profile",
    emits: ["changeHeader"],
    data() {
        return {
            updateUrl: "http://sshishigin.space:8765/api/update_user/",
            profileData: {
                password: "",
            },
            errors: {
                username: "",
                email: "",
                password: "",
            },
            validationError: false,
            image: undefined
        }
    },
    mounted() {
        this.profileData.username = localStorage.getItem("username");
        this.profileData.email = localStorage.getItem("email");
    },
    methods: {
        changeImage(file) {
            this.image = file;
        },
        updateUser() {
            const accountId = localStorage.getItem("accountId");
            const url = this.updateUrl + accountId + "/";
            let formData = new FormData();

            formData.append("id", accountId);

            if (this.image) {
                formData.append("profile_image", this.image);
            }
            for (let key of Object.keys(this.profileData)) {
                formData.append(key, this.profileData[key]);
            }
            const headers = {
                "content-type": "multipart/form-data"
            }

            axios.patch(url, formData, {
                headers: headers
            })
                .then((response) => {
                    for (const [key, value] of Object.entries(response.data)) {
                        localStorage.setItem(key, value);
                    }
                    this.$emit("changeHeader");
                    this.$router.push(`/profile/${localStorage.getItem("username")}`);
                })
                .catch((errors) => {
                    for (const key of Object.keys(this.errors)) {
                        this.errors[key] = "";
                    }
                    const errorData = errors.response.data;
                    this.validationError = true;
                    this.profileData.password = "";
                    for (const [key, value] of Object.entries(errorData)) {
                        this.errors[key] = value;
                        this.profileData[key] = localStorage.getItem(key);
                    }
                })
        },
    },
    computed: {
        niceError() {
            let error = "";
            for (const [key, value] of Object.entries(this.errors)) {
                if (value) {
                    error = `${key}: ${value}`
                    return error;
                }
            }
            return error;
        }

    },
}
</script>

<template>
    <div class="login d-flex flex-column align-items-center " @submit.prevent="updateUser">
        <form class="col-md-5">
            <h5 class="">Please, update your profile data, if you want.</h5>
            <div class="alert alert-danger d-flex justify-content-center" role="alert" v-if="validationError">
                <p>{{ niceError }}</p>
            </div>
            <div class="mb-3">
                <label class="form-label">Username</label>
                <input v-model="profileData.username" class="form-control errorOccured" :placeholder="errors.username">
            </div>
            <div class="mb-3">
                <label for="exampleInputEmail1" class="form-label">Email address</label>
                <input v-model="profileData.email" class="form-control errorOccured" aria-describedby="emailHelp"
                    id="exampleInputEmail1" :placeholder="errors.email">
                <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
            </div>
            <div class="mb-3">
                <label for="exampleInputPassword1" class="form-label">Password</label>
                <input v-model="profileData.password" type="password" class="form-control errorOccured"
                    :placeholder="errors.password">
            </div>
            <form class="mb-3">
                <div class="form-group">
                    <input type="file" class="form-control-file" @change="changeImage($event.target.files[0])">
                </div>
            </form>
            <button type=" submit" class="btn btn-warning">Save changes</button>
        </form>
    </div>
</template>
