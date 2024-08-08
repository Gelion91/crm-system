
const order_form = document.getElementById('order_form')


//const old_margin = id_margin.value

const product = document.getElementsByName('product')[0]
const csrf = document.getElementsByName('csrfmiddlewaretoken')


$(document).ready(function(){
        function hideInputs() {
            $('label[for=id_takemoney]').hide();
            $('select[name=takemoney]').hide();
        }
    var val = $('select[name=paid_method]').val();
    console.log(val)
       if (val == 'Наличные') {
                $('label[for=id_takemoney]').show();
                $('select[name=takemoney]').show();
            }
             else {
                $('label[for=id_takemoney]').hide();
                $('select[name=takemoney]').hide();
            }
        $('select[name=paid_method]').on('change', function(){
            var val = $('select[name=paid_method]').val();
            if (val == 'Наличные') {
                $('label[for=id_takemoney]').show();
                $('select[name=takemoney]').show();
            }
             else {
                hideInputs();
            }
        });

});

