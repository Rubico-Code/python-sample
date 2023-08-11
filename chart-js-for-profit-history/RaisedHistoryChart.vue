<template>
  <div class="card shadow-sm mb-3">
    <div class="card-header bg-white">
      <div class="row no-gutters">
        <div class="col-8 my-auto h5">
          Raised in month <i class="fas fa-xs fa-spin fa-sync text-muted" v-show="loading"/>
        </div>
        <div class="col-4 my-auto">
          <div class="form-group m-0">
            <div class="input-group">
              <flat-pickr
                id="input-month"
                v-model="params.month"
                :config="dateConfig"
                class="form-control"
                placeholder="Select month"
                name="month"
                :disabled="loading"
              />
              <div class="input-group-append">
                <button
                  v-show="!params.month"
                  class="btn btn-outline-secondary"
                  type="button"
                  title="Toggle"
                  :disabled="loading"
                  data-toggle
                >
                  <i class="fa fa-sm fa-calendar-alt"/>
                </button>
                <button
                  v-show="params.month"
                  class="btn btn-outline-danger"
                  type="button"
                  title="Clear"
                  :disabled="loading"
                  data-clear
                >
                  <i class="fa fa-sm fa-times"/>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <canvas
        ref="canvas"
        width="100%"
        style="height: 300px"
      />
    </div>
  </div>
</template>

<script>
import {
  Chart,
  CategoryScale,
  LineElement,
  PointElement,
  LineController,
  LinearScale,
  Decimation,
  Filler,
  Tooltip,
} from 'chart.js';

Chart.register(
  LineElement,
  CategoryScale,
  PointElement,
  LineController,
  LinearScale,
  Decimation,
  Filler,
  Tooltip
);

import LineChartOptions from '@/js/admin/Components/Dashboard/lineChartOptions';
import {formatDatetime} from '@/js/shared/Util/datetime';
import flatPickr from 'vue-flatpickr-component';
import MonthSelectPlugin from 'flatpickr/dist/plugins/monthSelect/index.js'
import dayjs from 'dayjs';

const defaultDataset = {
  data: [],
  fill: true,
  borderWidth: 1,
  pointRadius: 4,
  pointBackgroundColor: '#ff9800',
  backgroundColor: 'rgba(197,179,88,0.5)',
  borderColor: '#ff9800',
};

export default {
  name: 'TotalRaisedChart',
  chart: null, // non-reactive
  data() {
    return {
      charges: [],
      loading: true,
      params: {
        month: dayjs().format('MM') + '/' + dayjs().format('YYYY'),
      },
      dateConfig: {
        dateFormat: 'm/Y',
        wrap: true,
        altInput: true,
        disableMobile: true,
        maxDate: new Date(),
        plugins: [
          new MonthSelectPlugin({
            shorthand: true,
            dateFormat: 'm/Y',
            altFormat: 'M, Y',
          })
        ]
      }
    }
  },
  components: {
    flatPickr
  },
  mounted() {
    this.initChart();
    this.fetch();
  },
  methods: {
    createGradient() {
      const ctx = this.$refs.canvas.getContext('2d');
      const gradient = ctx.createLinearGradient(0, 0, 0, 400);
      gradient.addColorStop(0, 'rgba(250,174,50,1)');
      gradient.addColorStop(1, 'rgba(250,174,50,0)');
      return gradient;
    },
    initChart() {
      this.chart = new Chart(this.$refs.canvas.getContext('2d'), {
        type: 'line',
        data: {
          labels: [],
          datasets: [],
        },
        options: LineChartOptions
      });
    },
    fetch() {
      this.loading = true;

      this.$http.get('/charts/total-raised', {params: this.params})
        .then(response => {
          this.charges = response.data.data;

          this.$nextTick(() => {
            this.chart.data.datasets = this.datasets;
            this.chart.update();
          })
        })
        .catch(() => {
          this.$toast.error('Failed to load raised history chart.')
        })
        .finally(() => {
          this.loading = false
        })
    },
  },
  watch: {
    params: {
      deep: true,
      handler: function (newVal) {
        this.fetch()
      }
    }
  },
  computed: {
    datasets() {
      let datasets = [];

      const axes = this.charges.map(charge => {
        return {
          x: formatDatetime(charge.date_created, 'MM/DD/YY'),
          y: charge.raised_total
        }
      });

      datasets.push(Object.assign({}, defaultDataset, {
        label: 'Amount',
        backgroundColor: this.createGradient(),
        data: axes,
      }));

      return datasets;
    }
  },
  beforeDestroy() {
    this.chart && this.chart.destroy();
  },
}
</script>
