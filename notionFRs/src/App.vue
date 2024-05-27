<template xmlns:div="http://www.w3.org/1999/html">
  <v-theme-provider :theme="themeIsDark ? 'dark' : 'light'">
  <v-app>
    <v-container>
      <div class="d-flex justify-space-between">
        <div class="d-flex">
          <h1>Feature Request Form</h1>
        </div>

        <v-chip class="py-6">
          <v-switch hide-details inset @click="toggleTheme" v-model="themeIsDark">
            <template #prepend>
              <v-icon>mdi-weather-sunny</v-icon>
            </template>
            <template #append>
              <v-icon>mdi-weather-night</v-icon>
            </template>
          </v-switch>
        </v-chip>

      </div>
      <v-form validate-on="input" v-model="formValid" :readonly="submitting" theme="dark">
        <v-row>
          <v-col class="pb-0 pt-6" cols="12">
            <v-alert class="mb-0" :style="{opacity: alertData ? 100 : 0}" :type="alertData?.type || 'success'"> {{ alertData?.text || "1" }}</v-alert>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-text-field
              density="comfortable"
              variant="outlined"
              hide-details
              v-model="form.title"
              label="Feature Request Title"
              required
            >
              <template #append-inner>
                <v-tooltip text="Displayed Title of this Feature Request">
                  <template v-slot:activator="{ props }">
                    <v-icon v-bind="props">mdi-format-title</v-icon>
                  </template>
                </v-tooltip>
              </template>
            </v-text-field>
          </v-col>
          <v-col cols="6">
            <v-autocomplete
              hide-details
              variant="outlined"
              density="comfortable"
              v-model="form.requested_by"
              :items="users"
              label="Request By"
              required
            >
              <template #append-inner>
                <v-tooltip text="Refresh user options">
                  <template v-slot:activator="{ props }">
                    <v-btn :loading="usersRefreshing" density="compact" v-bind="props" flat icon="mdi-refresh" @click="forceRefreshUsers" :disabled="usersRefreshing" />
                  </template>
                </v-tooltip>
              </template>
            </v-autocomplete>
          </v-col>
          <v-col cols="6">
            <v-select
              variant="outlined"
              density="comfortable"
              hide-details
              v-model="form.priority"
              :items="priorities"
              label="Priority"
              required
            >
              <template #append-inner>
                <v-tooltip text="Refresh tags/priorities options">
                  <template v-slot:activator="{ props }">
                    <v-btn density="compact" flat :loading="optionsRefreshing" v-bind="props" icon="mdi-refresh" @click="forceRefreshOptions" :disabled="optionsRefreshing">

                    </v-btn>
                  </template>
                </v-tooltip>
              </template>
            </v-select>

          </v-col>
          <v-col cols="12">
            <v-card variant="outlined" style="border-color: #BDBDBD">
              <v-card-text style="position: relative;">
                <div class="d-flex">
                  <h2 class="text-h6 mb-2 text-grey-darken-2">Choose Relevant Tags </h2>
                </div>

                <v-chip-group multiple filter column>
                  <v-chip variant="outlined" v-for="tag in tags">
                    {{ tag.title }}
                  </v-chip>
                </v-chip-group>
              </v-card-text>
            </v-card>

          </v-col>


          <v-col cols="12">

            <v-textarea
              variant="outlined"
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
              variant="outlined"
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
          <v-col cols="12" class="pb-0">
            <v-textarea
              variant="outlined"
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

          <v-col cols="12" class="py-0">
              <v-checkbox v-model="form.send_notification" hide-details label="Notify on #eng-main (WIP)"></v-checkbox>
              <v-btn size="large" block color="green" @click="createPage" :disabled="submitting">
                <span class="me-2"><v-icon>mdi-content-save</v-icon> Create Feature Request</span>
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
          send_notification: true,
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
      propertyTicks() {
        if (!this.options?.Priority) {
          return {};
        }

        let ticks = {};
        let i = 0;
        for (let priority of this.options.Priority) {
          ticks[i++] = priority.name;
        }
        console.log(ticks)
        return ticks;
      },
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
          send_notification: true,
        }

      }
    }
  }
</script>
<style>
.v-chip--selected {
  background-color: #4CAF50 !important;
  color: white !important;
}
</style>
