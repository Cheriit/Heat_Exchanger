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
              :chart-labels="chartLabels"
              chart-color="#d32f2f7a"
              title="Temperature over time chart"
              :height="352"
              class="mb-3"
              y-axis-label="Temperature [oC]"
            />
            <v-fade-transition>
              <chart
                v-if="isLive"
                :chart-data="volumeData"
                :chart-labels="chartLabels"
                chart-color="#1e88e57a"
                title="Water volume over time chart"
                :height="264"
                y-axis-label="Volume [l]"
              />
            </v-fade-transition>
          </v-col>
          <v-col class="col-lg-4 col-12">
            <data-form
              @changedIsLive="updateIsLive"
              @stopSimulation="stopSimulation"
              @startSimulation="startSimulation"
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
    temperatureData: [],
    volumeData: [],
    chartLabels: [],
    isLive: false,
    isPaused: false,
    formData: {},
    intervalId: 0
  }),
  methods: {
    fillData() {
      this.temperatureData = [this.getRandomInt(), this.getRandomInt()];
      this.chartLabels = [this.getRandomInt(), this.getRandomInt()];
    },
    appendData() {
      this.temperatureData = [...this.temperatureData, this.getRandomInt()];
      this.volumeData = [...this.volumeData, this.getRandomInt()];
      this.chartLabels = [...this.chartLabels, this.getRandomInt()];
    },
    getRandomInt() {
      return Math.floor(Math.random() * (50 - 5 + 1)) + 5;
    },
    updateIsLive(isLive) {
      this.isLive = isLive;
    },
    stopSimulation() {
      clearInterval(this.intervalId);
      this.isPaused = false;
      this.temperatureData = [];
      this.volumeData = [];
      this.chartLabels = [];
    },
    startSimulation(data) {
      this.formData = data;
      this.isPaused = false;
      // RUN REQUEST IN LOOP IF isLive
      if (this.isLive) {
        this.intervalId = setInterval(() => this.appendData(), 1000);
      } else {
        this.fillData();
      }
    },
    pauseSimulation() {
      this.isPaused = true;
      // Stop runSimulation
      clearInterval(this.intervalId);
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
