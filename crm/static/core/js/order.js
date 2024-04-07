
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


//id_margin.addEventListener('change', ()=>{
//                    console.log(price)
//                    exchange_for_company.value = parseFloat(exchange_for_client.value - parseFloat(0.3)).toFixed(2)
//                    console.log(Boolean(Number(id_margin.value) < Number(old_margin)));
//                    console.log(id_margin.value)
//                    console.log(old_margin)
//                    console.log(Math.abs(old_margin - id_margin.value))
//
//                    if (Number(id_margin.value) < Number(old_margin)) {
//                      id_total_price.value = parseFloat(parseFloat(price) - parseFloat(Math.abs(old_margin - id_margin.value))).toFixed(2)
//                      console.log('Новая наценка ниже старой')
//                      console.log(old_margin)
//                      console.log(id_margin.value)
//
//                    } else {
//                      id_total_price.value = parseFloat(parseFloat(price) + parseFloat(Math.abs(old_margin - id_margin.value))).toFixed(2)
//                      console.log('Новая наценка выше старой')
//                      console.log(old_margin)
//                      console.log(id_margin.value)
//                      console.log(id_total_price.value)
//                    }
//                    id_total_price_rub.value =  parseFloat(exchange_for_client.value*id_total_price.value).toFixed(2)
//})


console.log(exchange_for_company)
console.log(product)
