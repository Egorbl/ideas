<script>
import axios from "axios";
import IdeaCard from "../components/IdeaCard.vue"
import CommentCard from "../components/CommentCard.vue"
import Observer from "@/components/Observer.vue";

export default {
    name: "app-idea",
    components: {
        IdeaCard,
        CommentCard,
        Observer
    },
    data() {
        return {
            ideaUrl: "http://5.9.178.136:8765/api/ideas/",
            comments: [],
            idea: undefined,
            page_size: 2,
            page: 1,
            lastPage: undefined,
            commentText: ""
        }
    },
    methods: {
        async uploadIdea() {
            const ideaId = this.$route.params.ideaId;
            const accessToken = localStorage.getItem("accessToken");
            let headers = {};

            if (accessToken) {
                headers["Authorization"] = `Token ${accessToken}`;
            }
            await axios.get(this.ideaUrl + ideaId + "/", {
                headers: headers
            })
                .then((response) => {
                    this.idea = response.data;
                })
        },
        async uploadComments() {
            if (this.lastPage == null && this.page == 2) { return }
            if (this.lastPage != null && this.page > this.lastPage) { return }
            const ideaId = this.$route.params.ideaId;
            const accessToken = localStorage.getItem("accessToken");
            let headers = {};

            if (accessToken) {
                headers["Authorization"] = `Token ${accessToken}`;
            }

            let url = this.ideaUrl + ideaId + '/comments/'
            url += `?page=${this.page++}`
            url += `&page_size=${this.page_size}`
            await axios.get(url, {
                headers: headers
            })
                .then((response) => {
                    this.lastPage = Math.ceil(response.data.count / this.page_size);
                    this.comments.push(...response.data.results);
                })
        },
        async postComment() {
            const accessToken = localStorage.getItem("accessToken");
            const ideaId = this.$route.params.ideaId;
            await axios.post(this.ideaUrl + ideaId + "/comments/", {
                id: this.uuidv4(),
                idea_id: ideaId,
                content: this.commentText,
            }, {
                headers: {
                    Authorization: `Token ${accessToken}`
                }
            })
                .then((response) => {
                    this.commentText = "";
                    this.comments.splice(0, 0, response.data);
                })
                .catch(() => {
                    return;
                })

        },
        uuidv4() {
            return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
                (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
            );
        },
        deleteComment(commentForDelete) {
            this.comments = this.comments.filter((comment) => {
                return comment != commentForDelete;
            })
        },
        commentUpdate(comment) {
            const commentId = comment.id;
            for (const ind in this.comments) {
                if (this.comments[ind].id == commentId) {
                    this.comments.splice(ind, 1, comment);
                    return;
                }
            }
        }
    }
    ,
    mounted() {
        this.uploadIdea();
        this.uploadComments();
    }
}
</script>

<template>
    <div v-if="idea" class="d-flex flex-column align-items-center mt-3">
        <IdeaCard :idea="idea"></IdeaCard>
        <div class="mb-3 col-md-8 col-sm-10">
            <form @submit.prevent="postComment" class="w-100 d-flex flex-row">
                <input type="text" class="form-control" placeholder="Write your comment here"
                    aria-describedby="button-addon2" v-model="commentText">
                <button class="btn btn-outline-secondary" type="submit" id="button-addon2">></button>
            </form>
        </div>
        <div v-if="comments.length != 0" class="col-md-8 col-sm-10 mb-3">
            <div class="d-flex flex-column mb-3" v-for="comment in comments" :key="comment.id">
                <CommentCard @commentUpdate="(updatedComment) => commentUpdate(updatedComment)"
                    @commentDelete="deleteComment(comment)" :comment="comment" />
            </div>
        </div>
        <div v-else class='col-md-8 col-sm-10 mb-3 d-flex flex-row justify-content-center'>
            <h5 class="align-self-center mt-1">No comments yet</h5>
        </div>
        <Observer @intersect="uploadComments"></Observer>
    </div>
</template>
