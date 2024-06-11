
const order_form = document.getElementById('order_form')

const exchange_for_client = document.getElementById('id_exchange_for_client')
const exchange_for_company = document.getElementById('id_exchange_for_company')
const total_price_rub = document.getElementById('id_total_price_rub')
const total_price_rub_company = document.getElementById('id_total_price_rub_company')
const total_price = document.getElementById('id_total_price')
const total_price_company = document.getElementById('id_total_price_company')
const profit = document.getElementById('id_profit')
//const id_margin = document.getElementById('id_margin')
const price = total_price.value
//const old_margin = id_margin.value

const product = document.getElementsByName('product')[0]
const csrf = document.getElementsByName('csrfmiddlewaretoken')


exchange_for_company.addEventListener('input', ()=>{
                    total_price_rub.value =  parseFloat(exchange_for_client.value*total_price.value).toFixed(2)
                    total_price_rub_company.value = parseFloat(exchange_for_company.value*total_price_company.value).toFixed(2)
                    profit.value = parseFloat(total_price_rub.value - total_price_rub_company.value).toFixed(2)

})
exchange_for_client.addEventListener('input', ()=>{
                    exchange_for_company.value = parseFloat(exchange_for_client.value - parseFloat(0.3)).toFixed(2)
                    total_price_rub.value =  parseFloat(exchange_for_client.value*total_price.value).toFixed(2)
                    total_price_rub_company.value = parseFloat(exchange_for_company.value*total_price_company.value).toFixed(2)
                    profit.value = parseFloat(total_price_rub.value - total_price_rub_company.value).toFixed(2)
})

$("input").focus(function(){
  $(this).select();
});

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



console.log(exchange_for_company)
console.log(product)
