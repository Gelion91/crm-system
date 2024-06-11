//$(document).ready(function(){
//
//
//    $(".btn").click(function(){
//        $.ajax({
//            url: '',
//            type: 'get',
//            data: {
//                    number: $(this).text()
//                  },
//            success: function(response) {
//                $(".filtered").text(response.seconds)
//                $("#seconds").append('<li>' + response.seconds + '</li>')
//            },
//        });
//    });
//
//    $(".btn").on('click', function() {
//    $.ajax({
//            url: '',
//            type: 'post',
//            data: {
//                    text: $(this).text()
//                  },
//            success: function(response) {
//                $(".btn").text(response.seconds)
//                $("#seconds").append('<li>' + response.seconds + '</li>')
//            },
//        });
//    });
//});

//const Delivery_form = document.getElementById('delivery-form')
//
//const volume = document.getElementById('id_volume')
//const weight = document.getElementById('id_weight')
//const density = document.getElementById('id_density')
//const csrf = document.getElementsByName('csrfmiddlewaretoken')
//
//window.onload = function () {
//    var e = document.getElementById("id_product_to");
//    console.log(e)
////    var a = JSON.parse(form.replace(/&quot;/g,'"'));
////    console.log(a)
//    console.log(data)
//    var data_pars = [
//    {% for item in data %}
//      parseFloat({{ item.summa }}),
//    {% endfor %}
//  ]
//    console.log(data_pars)
//
//
//
//    e.addEventListener('click', ()=>{
//                    var total = 0
////                    for (var prop in a) {
////                        if (a[prop].id == e.value)  {
////                            console.log('Есть совпадение')
////                            console.log(a[prop].id)
////                            console.log(e)
////                            console.log('----------------------------')
////                            console.log("obj." + prop + " = " + a[prop].full_price);
////                            var prop = {'id': e.value, 'full_price': a[prop].full_price}
////                            total.push(prop)
////                            }
////                    }
////                    console.log(total)
////                    for (var prop in e.options) {
////                        arr[e[prop].value] = e[prop].text
////                        var list = []
////                        list.push()
////                    }
//                    console.log(e.value)
//                    for (var index in e.options) {
//                        for (var prop in a) {
//                            if (a[prop].id == e.value)  {
//                                console.log('Есть совпадение')
//                                console.log(e.value)
//                                } {break}
//                        }
//                    }
//                    console.log(e.options)
//                    console.log(form)
//
//})
//
//};
//
//volume.addEventListener('input', ()=>{
//                    const volume_data = volume.value
//                    console.log(volume_data)
//                    density.value = parseFloat((weight.value / volume.value).toFixed(2))
//})


//
//console.log(Delivery_form)

//$(e).on('click', function() {
//    $.ajax({
//            url: '',
//            type: 'post',
//            data: {
//                    text: $(this).value,
//                    csrfmiddlewaretoken: csrf
//                  },
//            success: function(response) {
//                $(".id_product_to").text('Удалось')
//            },
//        });
//    });
