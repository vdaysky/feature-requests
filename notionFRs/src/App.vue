<template xmlns:div="http://www.w3.org/1999/html">
  <v-app>
  <!--  create a form meant to be embedded in iframe
   fields:
   "requested_by": "68a19168-98df-4006-a28a-7e5de618bfba",
  "priority": "09abb3c0-04e5-4f00-a349-a1e11d1522f2",
  "tags": [
    "9fd8e7dd-13f3-4de4-826c-00bd96d926d6"
  ],
  "due_date": "2024-05-26",
  "title": "api created feature reqyest",
  "summary": "short summaryg",
  "description": "dscription goes here ",
  "user_story": "user story"
   -->
    <v-container>

      <h1>Feature Request Form</h1>
      <v-form validate-on="input" v-model="formValid" :readonly="submitting">
        <v-row>
          <v-col>
            <v-alert v-if="alertData" :type="alertData.type"> {{ alertData.text }}</v-alert>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <div class="d-flex">
              <v-text-field
                class="me-4"
                hide-details
                v-model="form.title"
                label="Feature Request Title"
                required
              ></v-text-field>
              <v-select
                hide-details
                v-model="form.requested_by"
                :items="users"
                label="Feature Requested By"
                required
              >
                <template #append>
                  <v-btn color="green" class="h-100" @click="forceRefreshUsers" :disabled="usersRefreshing">
                    <v-icon v-if="!usersRefreshing">mdi-refresh</v-icon>
                    <v-progress-circular v-if="usersRefreshing" color="primary" indeterminate size="small"></v-progress-circular>
                  </v-btn>
                </template>
              </v-select>
            </div>
          </v-col>
          <v-col cols="12">
            <div class="d-flex">
              <v-select
                class="me-4"
                hide-details
                v-model="form.tags"
                :items="tags"
                label="Tags"
                chips
                multiple
                required
              ></v-select>
              <v-select
                hide-details
                v-model="form.priority"
                :items="priorities"
                label="Priority"
                required
              >
                <template #append>
                  <v-btn color="green" class="h-100" @click="forceRefreshOptions" :disabled="optionsRefreshing">
                    <v-icon v-if="!optionsRefreshing">mdi-refresh</v-icon>
                    <v-progress-circular v-if="optionsRefreshing" color="primary" indeterminate size="small"></v-progress-circular>
                  </v-btn>
                </template>
              </v-select>
            </div>
          </v-col>
          <v-col cols="12">
            <v-textarea
              hide-details
              v-model="form.summary"
              label="Feature Summary"
              required
            ></v-textarea>
          </v-col>
          <v-col cols="12">
            <v-textarea
              hide-details
              v-model="form.description"
              label="Feature Description"
              required
            ></v-textarea>
          </v-col>
          <v-col cols="12">
            <v-textarea
              hide-details
              v-model="form.user_story"
              label="User Story"
              required
            ></v-textarea>
          </v-col>
          <v-col cols="12">
              <v-btn block color="green" @click="createPage" :disabled="submitting">
                <span class="me-2">Create Page</span>
                <v-progress-circular v-if="submitting" color="primary" indeterminate size="small"></v-progress-circular>
              </v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-container>
  </v-app>
</template>

<script>
  import {ca} from "vuetify/locale";

  const API = "https://feature-requests.odays.ky/api";
  export default {
    data() {
      return {
        form: {
          user_story: "",
          description: "",
          summary: "",
          due_date: null,
          tags: [],
          priority: "",
          requested_by: null,
          title: "",
        },
        alertData: null,
        options: {},
        usersRaw: {},
        submitting: false,
        optionsRefreshing: false,
        usersRefreshing: false,
      }
    },
    computed: {
      tags() {
        if (!this.options.Tags) return [];
        return this.options.Tags.map(tag => (
          {title: tag.name, value: tag.id}
        )) || [];
      },
      priorities() {
        if (!this.options.Priority) return [];
        return this.options.Priority.map(pri => ({
          title: pri.name,
          value: pri.id

        })) || [];
      },
      users() {
        if (!this.usersRaw.results) return [];
        return this.usersRaw.results.filter(user => user.type === "person").map(user => ({
          title: user.name,
          value: user.id
        })) || [];
      }
    },
    async created() {
      // get /users
      this.usersRaw = await fetch(`${API}/users`).then(res => res.json());
      this.options = await fetch(`${API}/options`).then(res => res.json());
    },
    methods: {

      async forceRefreshUsers(){
        this.usersRefreshing = true;
        this.usersRaw = await fetch(`${API}/users?force_refresh=True`).then(res => res.json());
        this.usersRefreshing = false;
      },
      async forceRefreshOptions(){
        this.optionsRefreshing = true;
        this.options = await fetch(`${API}/options?force_refresh=True`).then(res => res.json());
        this.optionsRefreshing = false;
      },
      showAlert(type, text, timeout) {
        const id = Math.random();
        this.alertData = {type, text, id};
        setTimeout(() => {
          if (this.alertData.id === id) {
            this.alertData = null;
          }
        }, timeout);
      },
      async createPage() {
        if (!this.formValid) {
          this.showAlert("error", "Form is invalid", 5000);
          return;
        }

        this.submitting = true;
        let res;
        try {
          res = await fetch(`${API}/create`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify(this.form)
          });
          console.log(res);
        } catch (e) {
          this.showAlert("error", "Failed to create page", 5000);
          this.submitting = false;
          return;
        }
        this.submitting = false;
        if (!res.ok) {
          this.showAlert("error", "Failed to create page", 5000);
          return;
        }
        this.showAlert("success", "Page created successfully!", 5000);
        this.form = {
          user_story: "",
          description: "",
          summary: "",
          due_date: null,
          tags: [],
          priority: "",
          requested_by: "",
          title: "",
        }

      }
    }
  }
</script>
