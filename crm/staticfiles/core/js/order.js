
const order_form = document.getElementById('order_form')

const exchange_for_client = document.getElementById('id_exchange_for_client')
const exchange_for_company = document.getElementById('id_exchange_for_company')
const total_price_rub = document.getElementById('id_total_price_rub')
const id_total_price = document.getElementById('id_total_price')
const id_margin = document.getElementById('id_margin')
const price = id_total_price.value
const old_margin = id_margin.value

const product = document.getElementsByName('product')[0]
const csrf = document.getElementsByName('csrfmiddlewaretoken')

exchange_for_client.addEventListener('input', ()=>{
                    exchange_for_company.value = parseFloat(exchange_for_client.value - parseFloat(0.3)).toFixed(2)
                    id_total_price_rub.value =  parseFloat(exchange_for_client.value*id_total_price.value).toFixed(2)
})

id_margin.addEventListener('change', ()=>{
                    console.log(price)
                    exchange_for_company.value = parseFloat(exchange_for_client.value - parseFloat(0.3)).toFixed(2)
                    if (id_margin.value < old_margin) {
                      id_total_price.value = parseFloat(parseFloat(price) - parseFloat(Math.abs(old_margin - id_margin.value))).toFixed(2)
                    } else {
                      id_total_price.value = parseFloat(parseFloat(price) + parseFloat(Math.abs(old_margin - id_margin.value))).toFixed(2)
                    }
                    id_total_price_rub.value =  parseFloat(exchange_for_client.value*id_total_price.value).toFixed(2)
})


console.log(exchange_for_company)
console.log(product)
