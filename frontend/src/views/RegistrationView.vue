<script>
import axios from "axios"

export default {
    name: "app-register-view",

    data() {
        return {
            inputs: {
                username: "",
                email: "",
                password: "",
                password2: "",
            },
            registerUrl: "http://sshishigin.space:8765/api/register/",
            validationError: false,
            image: undefined,
            errors: {
                email: "",
                username: "",
                password: "",
                password2: "",
            },
        }
    },

    methods: {
        async registerUser() {
            let formData = new FormData();
            formData.append("id", this.uuidv4())
            if (this.image) {
                formData.append("profile_image", this.image);
            }
            for (let key in this.inputs) {
                formData.append(key, this.inputs[key]);
            }
            await axios.post(this.registerUrl, formData, {
                headers: {
                    "content-type": "multipart/form-data"
                }
            })
                .then((response) => {
                    if (response.status == 200) {
                        this.validationError = false;
                        this.$router.push('login');
                    }
                })
                .catch((error) => {
                    console.log(error);
                    const errorData = error.response.data;

                    for (const [key, value] of Object.entries(errorData)) {
                        this.errors[key] = value;
                        this.inputs[key] = "";
                    }
                    this.inputs.password = "";
                    this.inputs.password2 = "";
                    this.validationError = true;
                })
        },
        changeImage(file) {
            this.image = file;
        },
        uuidv4() {
            return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
                (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
            );
        },
    },

}
</script>

<template>
    <div class="login d-flex justify-content-center " @submit.prevent="registerUser">
        <form class="col-md-5">
            <div class="alert alert-danger d-flex align-items-center" role="alert" v-if="validationError">
                <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:">
                    <use xlink:href="#exclamation-triangle-fill" />
                </svg>
                <div>
                    Some of your inputs are invalid. Please, try again.
                </div>
            </div>
            <div class="mb-3">
                <label class="form-label">Username</label>
                <input v-model="inputs.username" class="form-control errorOccured" :placeholder="errors.username">
            </div>
            <div class="mb-3">
                <label for="exampleInputEmail1" class="form-label">Email address</label>
                <input v-model="inputs.email" class="form-control errorOccured" aria-describedby="emailHelp"
                    id="exampleInputEmail1" :placeholder="errors.email">
                <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
            </div>
            <div class="mb-3">
                <label for="exampleInputPassword1" class="form-label">Password</label>
                <input v-model="inputs.password" type="password" class="form-control errorOccured"
                    :placeholder="errors.password">
            </div>
            <div class="mb-3">
                <label for="exampleInputPassword1" class="form-label">Please, repeate your password</label>
                <input v-model="inputs.password2" type="password" class="form-control errorOccured"
                    :placeholder="errors.password2">
            </div>
            <form class="mb-3">
                <div class="form-group">
                    <input type="file" class="form-control-file" @change="changeImage($event.target.files[0])">
                </div>
            </form>
            <button type=" submit" class="btn btn-warning">Submit</button>
        </form>
    </div>
</template>

<style>
/* .errorOccured {
    background-color: brown;
} */
</style>
