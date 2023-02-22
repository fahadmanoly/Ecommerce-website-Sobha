$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})


$('.plus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];
    console.log('entered')
    // console.log(eml)
    // console.log('Hello');
    // console.log(id); 

    $.ajax(
        {
            type: "GET",
            url: "/pluscart",
            data: {
                prod_id: id
            },
            success:  (data) => {
                // console.log(document.querySelector('.amount'));
                console.log(data);
                eml.innerText = data.quantity;
                console.log(this.parentNode.nextElementSibling.querySelector('.amount').innerHTML)
                const amount = this.parentNode.nextElementSibling.querySelector('.amount').innerHTML
                
                this.parentNode.nextElementSibling.querySelector('.total-amount').innerHTML = amount * data.quantity;
                // document.getElementById("amount").innerText = data.amount.toFixed(2);
                document.getElementById("totalAmount").innerText = data.amount.toFixed(2);
                document.getElementById("totalamount").innerText = data.totalamount.toFixed(2);
                this.parentNode.nextElementSibling.nextElementSibling.innerText = data.message;
                // document.querySelector('.quantity').innerText = data.message;
            }
        })
});

$('.minus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];
    console.log('Hello');

    $.ajax(
        {
            type: "GET",
            url: "/minuscart",
            data: {
                prod_id: id
            },
            success:  (data) => {
                // console.log(document.querySelector('.amount'));
                // console.log('Hello');
                console.log(data)
                eml.innerText = data.quantity;
                const amount = this.parentNode.nextElementSibling.querySelector('.amount').innerHTML
                
                this.parentNode.nextElementSibling.querySelector('.total-amount').innerHTML = amount * data.quantity;
                // document.getElementById("amount").innerText = data.amount.toFixed(2);
                document.getElementById("totalAmount").innerText = data.amount.toFixed(2);
                document.getElementById("totalamount").innerText = data.totalamount.toFixed(2);
                this.parentNode.nextElementSibling.nextElementSibling.innerText = data.message;
            }
        })
});

$('.remove-cart').click(function () {
    var id = $(this).attr("pid").toString();
    console.log(this);
    var elm = this;
    // console.log(elm.parentNode.parentNode.parentNode.parentNode) ;
    $.ajax(
        {
            type: "GET",
            url: "/removecart",
            data: {
                prod_id: id
            },
            success: (data) => {
                console.log(data)
                // document.getElementById("amount").innerText = data.amount;
                // document.getElementById("totalamount").innerText = data.totalamount;
                // this.parentNode.nextElementSibling.querySelector('.total-amount').innerHTML = amount * data.quantity;
                // document.getElementById("amount").innerText = data.amount.toFixed(2);
                document.getElementById("totalAmount").innerText = data.amount.toFixed(2);
                document.getElementById("totalamount").innerText = data.totalamount.toFixed(2);
                elm.parentNode.parentNode.parentNode.parentNode.remove();
                window.location.reload();
            }
        })
});

