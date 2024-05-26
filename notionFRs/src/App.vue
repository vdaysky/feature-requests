<template>
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
      <v-form validate-on="input" v-model="formValid">
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="form.title"
              label="Title"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-select
              v-model="form.priority"
              :items="priorities"
              label="Priority"
              required
            ></v-select>
          </v-col>
          <v-col cols="12" md="6">
            <v-select
              v-model="form.requested_by"
              :items="users"
              label="Requested By"
              required
            ></v-select>
          </v-col>
          <v-col cols="12" md="6">
            <v-select
              v-model="form.tags"
              :items="tags"
              label="Tags"
              multiple
              required
            ></v-select>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              type="date"
              v-model="form.due_date"
              label="Due Date"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="form.summary"
              label="Summary"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-textarea
              v-model="form.description"
              label="Description"
              required
            ></v-textarea>
          </v-col>
          <v-col cols="12" md="6">
            <v-textarea
              v-model="form.user_story"
              label="User Story"
              required
            ></v-textarea>
          </v-col>
          <v-col cols="12">
            <v-btn @click="createPage" :disabled="!formValid">Submit</v-btn>
          </v-col>
        </v-row>
      </v-form>
      <v-alert v-if="!formValid" type="error">Please fill out all required fields</v-alert>
      <v-alert v-if="requestFail" type="error">Request failed</v-alert>
    </v-container>
  </v-app>
</template>

<script>
const API = "http://127.0.0.1:8000";
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
        options: {},
        usersRaw: {},
        formValid: false,
        requestFail: false,
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
      async createPage() {
        if (!this.formValid) {
          return;
        }
        this.requestFail = false;

        const res = await fetch(`${API}/create`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(this.form)
        });
        if (!res.ok) {
          this.requestFail = true;
        }
        console.log(res);
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
