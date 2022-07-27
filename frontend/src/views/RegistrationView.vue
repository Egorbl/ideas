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
            registerUrl: "http://localhost:8000/api/register/",
            validationError: false,
            errors: {
                email: "",
                username: "",
                password: "",
                password2: "",
            },
            success: false,
        }
    },

    methods: {
        async registerUser() {
            console.log("registrating");
            await axios.post(this.registerUrl, this.inputs)
                .then((response) => {
                    if (response.status == 200) {
                        this.validationError = false;
                        this.success = true;
                    }
                })
                .catch((error) => {
                    const errorData = error.response.data;

                    for (const [key, value] of Object.entries(errorData)) {
                        this.errors[key] = value;
                        this.inputs[key] = "";
                    }
                    this.inputs.password = "";
                    this.inputs.password2 = "";
                    this.validationError = true;
                })
        }
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
            <div v-if="success" class="alert alert-success d-flex align-items-center" role="alert">
                <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:">
                    <use xlink:href="#check-circle-fill" />
                </svg>
                <div>
                    You have successfully registered
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
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
</template>

<style>
/* .errorOccured {
    background-color: brown;
} */
</style>