<script>
import axios from "axios";

export default {
    name: "app-change-password-view",
    emits: ["changeHeader"],
    data() {
        return {
            changePasswordUrl: "http://5.9.178.136:8765/api/change_password/",
            validationError: false,
            inputs: {
                oldPassword: "",
                newPassword: "",
                newPassword2: ""
            },
            errors: {
                oldPassword: "",
                newPassword: "",
                newPassword2: "",
            },
        }
    },
    methods: {
        changePassword() {
            const accessToken = localStorage.getItem("accessToken");
            if (!accessToken) {
                return;
            }
            const accountId = localStorage.getItem("accountId");
            const url = this.changePasswordUrl + accountId + "/";
            axios.patch(url, this.inputs)
                .then(() => {
                    localStorage.removeItem("username");
                    localStorage.removeItem("accessId");
                    localStorage.removeItem("accountId");
                    localStorage.removeItem("email");
                    localStorage.removeItem("image");
                    localStorage.removeItem("accessToken");
                    this.$emit("changeHeader");
                    this.$router.push("/login");
                })
                .catch((errors) => {
                    this.errors = errors.response.data;
                    console.log(this.errors);
                    this.validationError = true;
                    this.inputs = {};
                })
        }
    }
}

</script>

<template>
    <div class="login d-flex justify-content-center " @submit.prevent="changePassword">
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
                <label for="exampleInputPassword1" class="form-label">Old password</label>
                <input v-model="inputs.oldPassword" type="password" class="form-control errorOccured"
                    :placeholder="errors.oldPassword">
            </div>
            <div class="mb-3">
                <label for="exampleInputPassword1" class="form-label">New password</label>
                <input v-model="inputs.newPassword" type="password" class="form-control errorOccured"
                    :placeholder="errors.newPassword">
            </div>
            <div class="mb-3">
                <label for="exampleInputPassword1" class="form-label">Please, repeate your password</label>
                <input v-model="inputs.newPassword2" type="password" class="form-control errorOccured"
                    :placeholder="errors.newPassword2">
            </div>
            <button type=" submit" class="btn btn-warning">Save password</button>
        </form>
    </div>
</template>
