<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <h1>Boiler simulator</h1>
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
import Chart from "./components/Chart";
import DataForm from "./components/DataForm";
import axios from "axios";

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
    intervalId: 0,
    prevTemp: null,
    prevVolume: null
  }),
  methods: {
    appendData() {
      this.formData = {
        ...this.formData,
        startTemp: this.prevTemp,
        startVolume: this.prevVolume
      };
      console.log(this.formData);
      axios
        .get("http://127.0.0.1:5000/get_live_simulation", {
          params: this.formData,
          headers: {
            "Access-Control-Allow-Origin": "*"
          }
        })
        .then(({ data }) => {
          console.log(data);
          this.temperatureData = [...this.temperatureData, data.temperature];
          this.volumeData = [...this.volumeData, data.volume];
          this.chartLabels = [
            ...this.chartLabels,
            (this.formData.timestamp * this.chartLabels.length / 60).toFixed(2)
          ];
          this.prevVolume = data.volume;
          this.prevTemp = data.temperature;
        })
        .catch(error => {
          console.log(error);
        });
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
      this.prevTemp = null;
      this.prevVolume = null;
    },
    startSimulation(data) {
      this.formData = data;
      this.isPaused = false;
      if (this.isLive) {
        if (this.prevTemp === null) {
          this.prevTemp = data.startTemp;
          this.prevVolume = data.startVolume;
          this.temperatureData = [data.startTemp];
          this.volumeData = [data.startVolume];
          this.chartLabels = [];
        }
        this.intervalId = setInterval(() => this.appendData(), 1000);
      } else {
        axios
          .get("http://127.0.0.1:5000/get_water_temperature", {
            params: this.formData,
            headers: {
              "Access-Control-Allow-Origin": "*"
            }
          })
          .then(({ data }) => {
            this.temperatureData = data.temperatures;
            this.chartLabels = data.times;
          })
          .catch(error => {
            console.log(error);
          });
      }
    },
    pauseSimulation() {
      this.isPaused = true;
      clearInterval(this.intervalId);
    },
    updateLiveData(data) {
      this.formData = { ...this.formData, ...data };
    }
  }
};
</script>

<style type="scss"></style>
