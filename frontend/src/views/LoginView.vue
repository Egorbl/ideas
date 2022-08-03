<script>
import axios from "axios"

export default {
  name: "app-login-view",

  data() {
    return {
      email: "",
      password: "",
      loginUrl: "http://localhost:8000/api/login/",
      validationError: false,
    }
  },

  methods: {
    async authenticateUser() {

      await axios.post(this.loginUrl, {
        username: this.email,
        password: this.password
      }).then((response) => {
        const accessToken = response.data.token;
        const username = response.data.username;
        const accountId = response.data.id;
        const imagePath = response.data.image;
        localStorage.setItem("accessToken", accessToken);
        localStorage.setItem("username", username);
        localStorage.setItem("accountId", accountId);
        localStorage.setItem("imagePath", imagePath);
        location.reload();
      }).catch(() => {
        this.validationError = true;
        this.password = "";
      })
    },

    validateEmail() {

    }
  },

  created() {
    const accessToken = localStorage.getItem("accessToken");
    if (accessToken) {
      this.$router.push("/");
    }
  }
}
</script>

<template>
  <div class="login d-flex justify-content-center " @submit.prevent="authenticateUser">
    <form class="col-md-5">
      <div v-if="validationError" class="alert alert-danger mb-3" role="alert">
        Email or password is incorrect
      </div>
      <div class="mb-3">
        <label for="exampleInputEmail1" class="form-label">Email address</label>
        <input v-model="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
        <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
      </div>
      <div class="mb-3">
        <label for="exampleInputPassword1" class="form-label">Password</label>
        <input v-model="password" type="password" class="form-control" id="exampleInputPassword1">
      </div>
      <button type="submit" class="btn btn-warning">Submit</button>
    </form>
  </div>
</template>

<style>
</style>