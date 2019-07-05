var appOperacao = new Vue({
  el: '#app-operacao',
  delimiters: ["[[","]]"],
  data: {
    baseUrl: '',
    empresa: '',
    cliente: '',
    grupo: 0,
    grupo_operacao: [],
    operacoes: [],
    checkedOperacoes: [],
    manutencaoOperacoes: [],
  },
  methods: {
    grupoOperacao: function () {
      var url = '/empresa/' + this.empresa +'/cliente/'+ this.cliente + '/operacoes/' + this.manutencao + '/grupo-operacao';
      this.$http.get(url).then(response => {
          this.grupo_operacao = response.body.results;
      }, response => { console.log(response.body); });
    },
    getOperacoes: function () {
      var url = '/empresa/' + this.empresa +'/cliente/'+ this.cliente + '/operacoes/' + this.manutencao + '/grupo/' + this.grupo;
      this.checkedOperacoes = [];
      this.$http.get(url).then(response => {
          this.operacoes = response.body.results;
      }, response => { console.log(response.body); });
    },
    allOperacoes: function () {
      var url = '/empresa/' + this.empresa +'/cliente/'+ this.cliente + '/operacoes/' + this.manutencao + '/all';
      this.$http.get(url).then(response => {
          this.manutencaoOperacoes = response.body.results;
      }, response => { console.log(response.body); });
    },
    saveOperacoes: function () {
      var data = new FormData();
      data.set('operacoes', this.checkedOperacoes);

      if(this.checkedOperacoes.length > 0) {
        var url = '/empresa/' + this.empresa +'/cliente/'+ this.cliente + '/operacoes/' + this.manutencao + '/save'; 
        this.$http.post(url, data).then(response => {
          alert(response.body.message);
          this.getOperacoes();
          this.allOperacoes();
        }, function (response) { console.log(response.body); });
      } 
    },
    deleteOperacoes: function (pk) {
      var url = '/empresa/' + this.empresa +'/cliente/'+ this.cliente + '/operacoes/' + this.manutencao + '/delete/' + pk;
      if(confirm("Deseja excluír essa operação?"))
      {
        this.$http.get(url).then(response => {
          alert(response.body.message);
          this.allOperacoes();
        }, function (response) { console.log(response.body); });
      }
    }
  }
});


var appMedicao = new Vue({
  el: '#app-medicao',
  delimiters: ["[[","]]"],
  data: {
    baseUrl: '',
    empresa: '',
    cliente: '',
    manutencao: '',
    item: {
      id: 0,
      pressao_baixa: 0,
      pressao_alta: 0,
      temperatura_insuflamento: 0,
      temperatura_retorno: 0,
      tensao: 0,
      corrente: 0,
      observacao: '',
    },
    items: [],
  },
  methods: {
    saveMedicao: function() {
        var url = '/empresa/' + this.empresa +'/cliente/'+ this.cliente +'/medicoes/'+ this.manutencao + '/save';
        if(this.item.pk) {
          url = url + '/' + this.item.pk;
        }

        var data = new FormData();
        data.set('pressao_baixa', this.item.pressao_baixa);
        data.set('pressao_alta', this.item.pressao_alta);
        data.set('temperatura_insuflamento', this.item.temperatura_insuflamento);
        data.set('temperatura_retorno', this.item.temperatura_retorno);
        data.set('tensao', this.item.tensao);
        data.set('corrente', this.item.corrente);
        data.set('observacao', this.item.observacao);

        this.$http.post(url, data).then(response => {
          alert(response.body.message);
          this.refreshMedicao();
          this.allMedicoes();
        }, function (response) {

        });
    },
    allMedicoes: function() {
        var url = '/empresa/'+ this.empresa +'/cliente/'+ this.cliente +'/medicoes/'+ this.manutencao +'/all';
        this.$http.get(url).then(response => {
          this.items = response.body.results;
        }, response => {

        });
    },
    getMedicoes: function(id) {
      var url = '/empresa/'+ this.empresa +'/cliente/'+ this.cliente +'/medicoes/'+ this.manutencao +'/save/' + id;
      this.$http.get(url).then(response => {
          this.item = response.body.result;
      }, response => {

      });
    },
    refreshMedicao: function () {
      this.item = {
        id: 0,
        pressao_baixa: 0,
        pressao_alta: 0,
        temperatura_insuflamento: 0,
        temperatura_retorno: 0,
        tensao: 0,
        corrente: 0,
        observacao: '',
      };
    },
    deleteMedicoes: function(id) {
      var url = '/empresa/'+ this.empresa +'/cliente/'+ this.cliente +'/medicoes/'+ this.manutencao +'/delete/' + id;
      if(confirm("Deseja excluír essa medição?"))
      {
        this.$http.get(url).then(response => {
          alert(response.body.message);
          this.allMedicoes();
        }, response => {

        });
      }
    }
  }
});


var appAnexo = new Vue({
  el: '#app-anexo',
  delimiters: ["[[","]]"],
  data: {
    empresa: '',
    cliente: '',
    manutencao: '',
    nome: '',
    files: [],
    progress: 0,
  },
  methods: {
    uploadAnexo: function() {
      if(this.file) {
        var data = new FormData();
        data.set('anexo', this.file);
        data.set('nome', this.nome);
        var url = '/empresa/' + this.empresa +'/cliente/'+ this.cliente + '/registro-manutencao-anexo/' + this.manutencao + '/create';
        this.progress = 0;
        this.$http.post(url, data, {
          progress: e => {
            if (e.lengthComputable) {
              this.progress = parseInt( Math.round( ( e.loaded * 100 ) / e.total ) );
            }
          }
        }).then(response => {
          alert(response.body.message);
          this.reset();
          this.listAnexo();
        },response => {
          this.reset();
          alert('Falha ao adicionar anexo!');
          console.log(response.body.message);
        });
      } else {
        alert('É necessário escolher um arquivo!');
      }
    },
    processAnexo: function (event) {
      this.file = event.target.files[0];
    },
    listAnexo: function () {
      var url = '/empresa/' + this.empresa +'/cliente/'+ this.cliente + '/registro-manutencao-anexo/' + this.manutencao + '/list';
      this.$http.get(url).then(response => {
        this.files = response.body.results;
      }, response => { console.log(response.body); });
    },
    deleteAnexo: function (id) {
      if(confirm("Deseja excluír esse anexo?"))
      {
        var url = '/empresa/' + this.empresa +'/cliente/'+ this.cliente + '/registro-manutencao-anexo/' + this.manutencao + '/delete/' + id;
        this.$http.get(url).then(response => {
          alert(response.body.message);
          this.reset();
          this.listAnexo();
        }, response => { console.log(response.body); });
      }
    },
    reset() {
      const input = this.$refs.fileInput;
      input.type = 'text';
      input.type = 'file';
      this.file = null;
      this.nome = '';
      this.progress = 0;
    }
  }
});