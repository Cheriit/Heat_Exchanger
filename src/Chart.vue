<template>
  <v-card raised>
    <v-card-title>
      {{ title }}
    </v-card-title>
    <v-card-text class="chart">
      <line-chart :chart-data="chartData" :height="height" />
    </v-card-text>
    <v-card-actions>
      <v-spacer />
    </v-card-actions>
  </v-card>
</template>
<script>
import LineChart from "./components/LineChart";

export default {
  name: "chart",
  components: { LineChart },
  props: {
    chartData: {},
    title: {},
    height: {}
  }
};
</script>
