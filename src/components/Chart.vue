<template>
  <v-card raised>
    <v-card-title>
      {{ title }}
    </v-card-title>
    <v-card-text class="chart">
      <line-chart
        :chart-data="formattedChartData"
        :height="height"
        :options="options"
      />
    </v-card-text>
    <v-card-actions>
      <v-spacer />
    </v-card-actions>
  </v-card>
</template>
<script>
import LineChart from "./LineChart";

export default {
  name: "chart",
  components: { LineChart },
  props: {
    chartData: {
      type: Array,
      default: function() {
        return [];
      }
    },
    chartLabels: {
      type: Array,
      default: function() {
        return [];
      }
    },
    chartColor: {},
    title: {},
    height: {},
    yAxisLabel: {}
  },
  data: () => ({
    formattedChartData: {
      labels: [],
      datasets: [
        {
          borderColor: "",
          backgroundColor: "",
          borderWidth: 1,
          pointBorderColor: "",
          data: []
        }
      ]
    }
  }),
  computed: {
    options() {
      return {
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true
              },
              gridLines: {
                display: true
              },
              scaleLabel: {
                display: true,
                labelString: this.yAxisLabel
              }
            }
          ],
          xAxes: [
            {
              gridLines: {
                display: false
              },
              scaleLabel: {
                display: true,
                labelString: "Time [min]"
              }
            }
          ]
        },
        legend: {
          display: false
        },
        tooltips: {
          enabled: true,
          callbacks: {
            title: tooltopitems => {
              return `Time: ${tooltopitems[0].xLabel} min`;
            },
            label: tooltipItem => {
              return `${tooltipItem.yLabel.toFixed(2)} oC`;
            }
          }
        },
        responsive: true,
        maintainAspectRatio: false
      };
    }
  },
  watch: {
    chartData: function() {
      this.formattedChartData.datasets[0] = {
        ...this.formattedChartData.datasets[0],
        data: this.chartData
      };
      this.formattedChartData = {
        ...this.formattedChartData,
        labels: this.chartLabels
      };
    }
  },
  created() {
    this.formattedChartData.datasets[0] = {
      ...this.formattedChartData.datasets[0],
      backgroundColor: this.chartColor
    };
  }
};
</script>
