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

const Delivery_form = document.getElementById('delivery-form')

const volume = document.getElementById('id_volume')
const weight = document.getElementById('id_weight')
const density = document.getElementById('id_density')
const product = document.getElementsByName('product')[0]
const csrf = document.getElementsByName('csrfmiddlewaretoken')

volume.addEventListener('input', ()=>{
                    const volume_data = volume.value
                    console.log(volume_data)
                    density.value = parseFloat((weight.value / volume.value).toFixed(2))
})

console.log(Delivery_form)
console.log(product)


