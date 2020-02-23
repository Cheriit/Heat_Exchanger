<template>
  <v-card raised loading="isRunning && isLive">
    <v-card-title>
      Specification
    </v-card-title>
    <v-card-text>
      <h1>Main params:</h1>
      <v-form ref="form" v-model="isValid" lazy-validation>
        <v-select
          v-model="selectedFluid"
          :items="fluids"
          item-text="name"
          :rules="[v => !!v || 'You have to choose fluid']"
          label="Fluid"
          :disabled="isRunning"
          required
        ></v-select>
        <v-row>
          <v-col class="col-12">
            <v-text-field
              v-model="power"
              :rules="[v => (!isNaN(v) && v>0) || 'You must enter a valid number!  ']"
              label="Power"
              hide-details="auto"
              :disabled="isRunning"
              required
              dense
            >
              <template slot="append">[W] </template>
            </v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="col-lg-6 col-12">
            <v-text-field
              v-model="timestamp"
              :rules="[v => (!isNaN(v) && v>0) || 'You must enter a valid number!  ']"
              label="Timestamp"
              hide-details="auto"
              :disabled="isRunning"
              required
              dense
            >
              <template slot="append">[s]</template>
            </v-text-field>
          </v-col>
          <v-col class="col-lg-6 col-12">
            <v-text-field
              v-model="targetTemp"
              :rules="[v => (!isNaN(v) && v>0) || 'You must enter a valid number!  ']"
              label="Target temperature"
              hide-details="auto"
              :disabled="isRunning"
              required
              dense
            >
              <template slot="append">[<span class="sup">o</span>C] </template>
            </v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="col-lg-6 col-12">
            <v-text-field
              v-model="startVolume"
              :rules="[v => (!isNaN(v) && v>0) || 'You must enter a valid number!  ']"
              label="Fluid vol. at the start"
              hide-details="auto"
              :disabled="isRunning"
              required
              dense
            >
              <template slot="append">[l]</template>
            </v-text-field>
          </v-col>
          <v-col class="col-lg-6 col-12">
            <v-text-field
              v-model="startTemp"
              :rules="[v => (!isNaN(v) && v>0) || 'You must enter a valid number!  ']"
              label="Fluid temp. at the start"
              hide-details="auto"
              :disabled="isRunning"
              required
              dense
            >
              <template slot="append">[<span class="sup">o</span>C] </template>
            </v-text-field>
          </v-col>
        </v-row>
        <v-checkbox
          v-model="isLive"
          label="Live simulation"
          dense
          @change="changeIsLive"
        ></v-checkbox>
        <v-expand-transition>
          <div v-if="isLive">
            <h1>Live simulation params</h1>
            <v-col cols="12">
              <v-subheader class="pl-0"
                >Temp. of pouring in water [<span class="sup">o</span>C]
              </v-subheader>
              <v-slider
                class="mt-3"
                v-model="tempIn"
                :thumb-size="24"
                thumb-label="always"
                @change="updateLiveData"
                hide-details
                dense
              ></v-slider>
            </v-col>
            <v-col cols="12">
              <v-subheader class="pl-0"
                >Vol. of pouring in water per hour [l/h]
              </v-subheader>
              <v-slider
                class="mt-3"
                v-model="volIn"
                :thumb-size="24"
                thumb-label="always"
                max="999"
                @change="updateLiveData"
                hide-details
                dense
              ></v-slider>
            </v-col>
            <v-col cols="12">
              <v-subheader class="pl-0"
                >Vol. of pouring out water per hour [l/h]
              </v-subheader>
              <v-slider
                class="mt-3"
                v-model="volOut"
                :thumb-size="24"
                thumb-label="always"
                max="999"
                @change="updateLiveData"
                hide-details
                dense
              ></v-slider>
            </v-col>
          </div>
        </v-expand-transition>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn
        color="success"
        icon
        :disabled="!isValid || (!isLive && isRunning) || (isLive && !isPaused)"
        @click="runSimulation"
      >
        <v-icon dark right>mdi-play</v-icon>
      </v-btn>
      <v-fade-transition>
        <v-btn
          color="primary"
          icon
          v-if="isLive"
          :disabled="!isRunning || isPaused"
          @click="pauseSimulation"
        >
          <v-icon dark right>mdi-pause</v-icon>
        </v-btn>
      </v-fade-transition>
      <v-btn color="error" icon :disabled="!isRunning" @click="stopSimulation">
        <v-icon dark right>mdi-stop</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>
<script>
import axios from "axios";

export default {
  name: "data-form",
  data: () => ({
    isLive: false,
    isValid: false,
    isRunning: false,
    isPaused: true,
    selectedFluid: null,
    fluids: [],
    power: 0,
    timestamp: 0,
    targetTemp: 0,
    startVolume: 0,
    startTemp: 0,
    tempIn: 0,
    volIn: 0,
    volOut: 0
  }),
  methods: {
    runSimulation() {
      if (this.selectedFluid != null && this.startVolume > 0 && this.power > 0 && this.timestamp > 0) {
        this.isRunning = true;
        this.isPaused = false;
        const {
          power,
          timestamp,
          targetTemp,
          startVolume,
          startTemp,
          tempIn,
          volIn,
          volOut,
          selectedFluid
        } = this;
        const selectedFluidFiltered = this.fluids.filter( x => x.name == selectedFluid)[0];
        const density = selectedFluidFiltered.density;
        const heatSpecific = selectedFluidFiltered.heatSpecific;
        this.$emit("startSimulation", {
          power,
          timestamp,
          targetTemp,
          startVolume,
          startTemp,
          tempIn,
          volIn,
          volOut,
          density,
          heatSpecific
        });
      }
    },
    pauseSimulation() {
      this.isPaused = true;
      this.$emit("pauseSimulation");
    },
    stopSimulation() {
      this.isRunning = false;
      this.isPaused = true;
      this.$emit("stopSimulation");
    },
    changeIsLive() {
      this.stopSimulation();
      this.$emit("changedIsLive", this.isLive);
    },
    updateLiveData() {
      const { tempIn, volIn, volOut } = this;
      this.$emit("updateLiveData", {
        tempIn,
        volIn,
        volOut
      });
    }
  },
  mounted() {
    axios
      .get("http://127.0.0.1:5000/get_liquids", {
        headers: {
          'Access-Control-Allow-Origin': '*',
        }
      })
      .then(({data}) => {
        this.fluids = data;
        this.selectedFluid = data[0].name;
      })
      .catch(error => {
        console.log(error);
      });
  }
};
</script>
<style type="scss">
.sup {
  vertical-align: super;
  font-size: 10px;
}
</style>
