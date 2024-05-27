<template xmlns:div="http://www.w3.org/1999/html">
  <v-theme-provider :theme="themeIsDark ? 'dark' : 'light'">
  <v-app>
    <v-container>


      <div class="d-flex justify-space-between">
        <h1>Feature Request Form</h1>
        <div>
          <v-switch hide-details @click="toggleTheme" v-model="themeIsDark">
            <template #prepend>
              <v-icon>mdi-weather-sunny</v-icon>
            </template>
            <template #append>
              <v-icon>mdi-weather-night</v-icon>
            </template>
          </v-switch>
        </div>

      </div>
      <v-form validate-on="input" v-model="formValid" :readonly="submitting" theme="dark">
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
                  <v-tooltip text="Refresh user options">
                    <template v-slot:activator="{ props }">
                      <v-btn v-bind="props" color="green" class="h-100" @click="forceRefreshUsers" :disabled="usersRefreshing">
                        <v-icon v-if="!usersRefreshing">mdi-refresh</v-icon>
                        <v-progress-circular v-if="usersRefreshing" color="primary" indeterminate size="small"></v-progress-circular>
                      </v-btn>
                    </template>
                  </v-tooltip>
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
                  <v-tooltip text="Refresh tags/priorities options">
                    <template v-slot:activator="{ props }">
                      <v-btn v-bind="props" color="green" class="h-100" @click="forceRefreshOptions" :disabled="optionsRefreshing">
                        <v-icon v-if="!optionsRefreshing">mdi-refresh</v-icon>
                        <v-progress-circular v-if="optionsRefreshing" color="primary" indeterminate size="small"></v-progress-circular>
                      </v-btn>
                    </template>
                  </v-tooltip>

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
            >

              <template #append-inner>
                <v-tooltip text="Brief description of the feature">
                  <template v-slot:activator="{ props }">
                    <v-icon v-bind="props">mdi-information</v-icon>
                  </template>
                </v-tooltip>
              </template>
            </v-textarea>
          </v-col>
          <v-col cols="12">
            <v-textarea
              hide-details
              v-model="form.description"
              label="Feature Description"
              required
            >
              <template #append-inner>
                <v-tooltip text="Include more details, in  particular about specific functionalities and requirements">
                  <template v-slot:activator="{ props }">
                    <v-icon v-bind="props">mdi-information</v-icon>
                  </template>
                </v-tooltip>
              </template>
            </v-textarea>
          </v-col>
          <v-col cols="12">
            <v-textarea
              hide-details
              v-model="form.user_story"
              label="User Story"
              required
            >
              <template #append-inner>
                <v-tooltip text="Describe how the end-user will interact with this feature">
                  <template v-slot:activator="{ props }">
                    <v-icon v-bind="props">mdi-information</v-icon>
                  </template>
                </v-tooltip>
              </template>
            </v-textarea>
          </v-col>
          <v-col cols="12">
              <v-btn size="large" block color="green" @click="createPage" :disabled="submitting">
                <span class="me-2">Create Page</span>
                <v-progress-circular v-if="submitting" color="primary" indeterminate size="small"></v-progress-circular>
              </v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-container>
  </v-app>
  </v-theme-provider>

</template>

<script setup>
import { useTheme } from 'vuetify'

const theme = useTheme()

function toggleTheme () {
  console.log("theme", theme)
  theme.global.name = theme.global.current.dark ? 'light' : 'dark'
}
</script>

<script>
  import {useTheme} from "vuetify";

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
        themeIsDark: false,
        themes: ["light", "dark"],
        featureSummaryToolTip: false,
      }
    },
    setup() {
      const theme = useTheme();
      return {theme};
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
