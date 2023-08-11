const formatter = Intl.NumberFormat('en', {
  notation: 'compact'
});

export default {
  responsive: true,
  maintainAspectRatio: false,
  spanGaps: false,
  interaction: {
    intersect: false,
    mode: 'index',
  },
  plugins: {
    legend: {
      display: false,
    },
  },
  scales: {
    x: {
      display: true,
      title: {
        display: true,
        text: 'Day (UTC)',
        color: '#999'
      }
    },
    y: {
      display: true,
      ticks: {
        callback: function (value, index, ticks) {
          return formatter.format(value);
        }
      },
      title: {
        display: true,
        text: 'Amount',
        color: '#999'
      }
    }
  }
};
