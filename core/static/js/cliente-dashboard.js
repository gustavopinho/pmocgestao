Vue.component('line-chart', {
  extends: VueChartJs.Line,
  mounted () {
    this.renderChart({
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
      datasets: [
        {
          label: 'Data One',
          backgroundColor: '#f87979',
          data: [40, 39, 10, 40, 39, 80, 40]
        }
      ]
    }, {responsive: true, maintainAspectRatio: false});
  }
});

Vue.component('pie-chart', {
  extends: VueChartJs.Pie,
  mixins: [VueChartJs.mixins.reactiveProp],
  mounted () {
    this.renderChart(this.chartData, {responsive: true, maintainAspectRatio: false});
  }
});

Vue.component('bar-chart', {
  extends: VueChartJs.Bar,
  mixins: [VueChartJs.mixins.reactiveProp],
  data: function () {
    return {
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            },
            gridLines: {
              display: true
            }
          }],
          xAxes: [{
            ticks: {
              beginAtZero: true
            },
            gridLines: {
              display: false
            }
          }]
        },
        legend: {
          display: true
        },
        tooltips: {
          enabled: true,
          mode: 'single',
          callbacks: {
            label: function(tooltipItems, data) {
              return tooltipItems.yLabel;
            }
          }
        },
        responsive: true,
        maintainAspectRatio: false,
        height: 200
      }
    };
  },
  mounted () {
    this.renderChart(this.chartData, this.options);
  }
});


var appManutencoes = new Vue({
  el: '#app-manutencoes',
  delimiters: ["[[","]]"],
  data: {
    empresa: 0,
    cliente: 0,
    ano: (new Date()).getFullYear(),
    chartDataMes: null,
    chartDataAno: null,
  },
  methods: {
    getManutencaoMes: function () {
      var url = '/empresa/' + this.empresa +'/cliente/'+ this.cliente + '/dashboard/relatorios?rel=R1&ano='+this.ano;
      this.$http.get(url).then(response => {
        this.chartDataMes = response.body.results;
      }, response => { console.log(response.body); });
    },
    getManutencaoAno: function () {
      var url = '/empresa/' + this.empresa +'/cliente/'+ this.cliente + '/dashboard/relatorios?rel=R2&ano='+this.ano;
      this.$http.get(url).then(response => {
        this.chartDataAno = response.body.results;
      }, response => { console.log(response.body); });
    },
    refresh: function () {
      this.getManutencaoMes();
      this.getManutencaoAno();
    },
  },
});
