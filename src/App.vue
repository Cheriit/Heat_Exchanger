<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <h1>Heat exchanger</h1>
      </div>
    </v-app-bar>
    <v-content>
      <v-container>
        <v-row>
          <v-col class="col-lg-8 col-12">
            <chart
              :chart-data="temperatureData"
              title="Temperature over time chart"
              :height="352"
              class="mb-3"
            />
            <v-fade-transition>
              <chart
                v-if="isLive"
                :chart-data="volumeData"
                title="Water volume over time chart"
                :height="264"
              />
            </v-fade-transition>
          </v-col>
          <v-col class="col-lg-4 col-12">
            <data-form
              @changedIsLive="updateIsLive"
              @stopSimulation="stopSimulation"
              @runSimulation="runSimulation"
              @pauseSimulation="pauseSimulation"
              @updateLiveData="updateLiveData"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import Chart from "./Chart";
import DataForm from "./DataForm";

export default {
  name: "App",
  components: {
    DataForm,
    Chart
  },
  data: () => ({
    temperatureData: {},
    volumeData: {},
    isLive: false,
    isPaused: false,
    formData: {}
  }),
  methods: {
    fillData() {
      this.temperatureData = {
        labels: [this.getRandomInt(), this.getRandomInt()],
        datasets: [
          {
            label: "Data One",
            backgroundColor: "#f87979",
            data: [this.getRandomInt(), this.getRandomInt()]
          },
          {
            label: "Data One",
            backgroundColor: "#f87979",
            data: [this.getRandomInt(), this.getRandomInt()]
          }
        ]
      };
    },
    getRandomInt() {
      return Math.floor(Math.random() * (50 - 5 + 1)) + 5;
    },
    updateIsLive(isLive) {
      this.isLive = isLive;
    },
    stopSimulation() {
      this.isPaused = false;
      this.temperatureData = { labels: [], datasets: [] };
      this.volumeData = { labels: [], datasets: [] };
    },
    runSimulation(data) {
      this.formData = data;
      this.isPaused = false;
      // RUN REQUEST IN LOOP IF isLive
    },
    pauseSimulation() {
      this.isPaused = true;
      // Stop runSimulation
    },
    updateLiveData(data) {
      this.formData = { ...this.formData, data };
    }
  },
  mounted: function() {
    this.fillData();
  }
};
</script>

<style type="scss"></style>
