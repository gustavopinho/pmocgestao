$(document).ready(function() {
    $('.select2').select2();
    
    //Date picker
    $('.datepicker').datepicker({
        autoclose: true,
        language: 'pt-BR',
        format: 'dd/mm/yyyy',
    });

    /* Mask */
    $(".date").inputmask("99/99/9999");
    $(".cep").inputmask("99999-999");
    $(".phone").inputmask('(99) 99999999[9]');
    $(".cnpj").inputmask("99.999.999/9999-99");

    $(".delete").click(function (event) {
        event.preventDefault();
        var url = $(this).attr('href');
        bootbox.dialog({
            message: "Deseja Excluír esse item?",
            title: "Atenção!",
            buttons: {
                success: {
                    label: "Confirmar",
                    className: "btn-success",
                    callback: function() {
                        window.location=url;
                    }
                },
                danger: {
                    label: "Cancelar",
                    className: "btn-danger",
                    callback: function() {
                        bootbox.hideAll();
                    }
                },
            }
        });
    });

    /** add active class and stay opened when selected */
    var url = window.location;

    // for sidebar menu entirely but not cover treeview
    $('ul.sidebar-menu a').filter(function() {
         return this.href == url;
    }).parent().addClass('active');

    // for treeview
    $('ul.treeview-menu a').filter(function() {
         return this.href == url;
    }).parentsUntil(".sidebar-menu > .treeview-menu").addClass('active');

    /* Busca CEP https://viacep.com.br/exemplo/jquery/*/
    $(".cep").blur(function() {
        //Nova variável "cep" somente com dígitos.
        var cep = $(this).val().replace(/\D/g, '');

        //Verifica se campo cep possui valor informado.
        if (cep != "") {

            //Expressão regular para validar o CEP.
            var validacep = /^[0-9]{8}$/;

            //Valida o formato do CEP.
            if(validacep.test(cep)) {

                //Preenche os campos com "..." enquanto consulta webservice.
                $("[name='logradouro']").val("...");
                $("[name='complemento']").val("...");
                $("[name='bairro']").val("...");
                $("[name='cidade']").val("...");
                $("[name='uf']").val("...");

                //Consulta o webservice viacep.com.br/
                $.getJSON("https://viacep.com.br/ws/"+ cep +"/json/?callback=?", function(dados) {

                    if (!("erro" in dados)) {
                        //Atualiza os campos com os valores da consulta.
                        $("[name='logradouro']").val(dados.logradouro);
                        $("[name='complemento']").val(dados.complemento);
                        $("[name='bairro']").val(dados.bairro);
                        $("[name='cidade']").val(dados.localidade);
                        $("[name='uf']").val(dados.uf);
                        $("[name='numero']").focus();

                    } //end if.
                    else {
                        //CEP pesquisado não foi encontrado.
                        limpa_formulário_cep();
                        alert("CEP não encontrado.");
                    }
                });
            } //end if.
            else {
                //cep é inválido.
                limpa_formulário_cep();
                alert("Formato de CEP inválido.");
            }
        } //end if.
        else {
            //cep sem valor, limpa formulário.
            limpa_formulário_cep();
        }   
    });
});
