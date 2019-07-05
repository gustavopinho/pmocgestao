var appAnexo = new Vue({
  el: '#app-anexo',
  delimiters: ["[[","]]"],
  data: {
    empresa: '',
    cliente: '',
    equipamento: '',
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
        var url = '/empresa/' + this.empresa +'/cliente/'+ this.cliente + '/equipamento-anexo/' + this.equipamento + '/create';
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
      var url = '/empresa/' + this.empresa +'/cliente/'+ this.cliente + '/equipamento-anexo/' + this.equipamento + '/list';
      this.$http.get(url).then(response => {
        this.files = response.body.results;
      }, response => { console.log(response.body); });
    },
    deleteAnexo: function (id) {
      if(confirm("Deseja excluír esse anexo?"))
      {
        var url = '/empresa/' + this.empresa +'/cliente/'+ this.cliente + '/equipamento-anexo/' + this.equipamento + '/delete/' + id;
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