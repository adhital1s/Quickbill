$(document).ready(function () {
    console.log(parseInt($('.length')[0].textContent)+1)
    var counter = parseInt($('.length')[0].textContent)+1
    var addItem = function () {
        var parent = document.querySelector('tbody')
        var template = ''
        template += '<tr data-id="' + counter + '">'
        template += '<td class="no" data-id="' + counter + '">' + counter + '</td>'
        template += '<td ><input type="text" data-id="' + counter +
            '" class="form-control form-control-plaintext item"></td>'
        template += '<td ><input type="text" data-id="' + counter +
            '" class="form-control form-control-plaintext description"></td>'
        template += '<td ><input type="text" data-id="' + counter +
        '" class="form-control form-control-plaintext alt_quantity" disabled></td>'
        template += '<td ><input type="text" data-id="' + counter +
            '" class="form-control form-control-plaintext quantity" disabled></td>'
        template += '<td ><input type="text" data-id="' + counter +
            '" class="form-control form-control-plaintext rate"></td>'
        template +=
            '<td ><select class="form-control form-control-plaintext per" name="" data-id="' +
            counter + '"><option >mtr</option><option>pcs</option></select></td>'
            template += '<td ><input type="text" data-id="' + counter +
            '" class="form-control form-control-plaintext amount" disabled></td>'
        template += '<td><button class = "delete" data-id="' + counter +
            '" style="border: 0ch;background: transparent;"><i class="fas fa-trash" style="color: red;"></i></button></td>'
        template += '</tr>'
        counter += 1
        parent.insertAdjacentHTML('beforeEnd', template)
    }

    function updateQty(data_id) {
        desc = $(".description[data-id = " + data_id + "]")
        qty = $(".quantity[data-id = " + data_id + "]")
        alt_amt = $(".alt_quantity[data-id = " + data_id + "]")
        item = []
        total_qty=[]
        alt_total = 0
        item = (desc[0].value)
        item = item.split(',')
        for (i = 0; i < item.length; i++) {
            item[i] = item[i].split('*')
        }

        for (i = 0; i < item.length; i++) {
            for (j = 0; j < item[i].length; j++)
                item[i][j] = parseFloat(item[i][j])
        }
        for (i = 0; i < item.length; i++) {
            if (isNaN(item[i][1])) {
                item[i][1] = 1
            }
            if (isNaN(item[i][0])) {
                item[i][0] = 0
            }
            alt_total += item[i][1]
           
            total_qty[i] = item[i][0] * item[i][1]
            
        }
        total = total_qty.reduce(function (a, b) {
            return a + b
        })
        qty[0].value = Math.round(total*100) /100
        alt_amt[0].value = alt_total
        console.log($('.per[data-id = 1]').val())
        updateRate(data_id)
    }

    function updateRate(data_id) {
        this_rate = $(".rate[data-id = " + data_id + "]")
        this_amt = $(".amount[data-id = " + data_id + "]")
        this_qty = $(".quantity[data-id = " + data_id + "]")
        this_amt[0].value = Math.round(parseFloat(this_qty[0].value) * parseFloat(this_rate[0].value))
        if (isNaN(this_amt[0].value)) {
            this_amt[0].value = 0
        } else {
            this_amt[0].value = parseFloat(this_qty[0].value) * parseFloat(this_rate[0].value)
        }
        updateTotal()
    }


    $('#add_item').click(function () {
        addItem()
        description = $('.description');
        del = $('.delete')
        rate = $('.rate')
        description.keyup(function () {
            data_id = this.getAttribute('data-id')
            updateQty(data_id)
        })
        rate.keyup(function () {
            data_id = this.getAttribute('data-id')
            updateRate(data_id)
        })
        deleteThis()
    })

    var description = $('.description')
    description.keyup(function () {
        data_id = this.getAttribute('data-id')
        updateQty(data_id)
    })

    var rate = $('.rate')
    rate.keyup(function () {
        data_id = this.getAttribute('data-id')
        updateRate(data_id)
    })

    per_list = []
    function updateTotal() {
        amt = $('.amount')
        per = $('.per')
        total_amt = $('#total')
        paid_amt = $('#payment')
        discount = $('#discount')
        remain_amt = $('#remaning')
        total = 0
        for (i = 0; i < amt.length; i++) {
            if (isNaN(parseInt(amt[i].value))) {
                amt[i].value = 0
            }
            total += parseInt(amt[i].value)
            per_list[i] = (per[i].value)
            
        }
        console.log(per_list)
        total_amt[0].value = total
        remain_amt[0].value = total_amt[0].value - paid_amt[0].value - discount[0].value

    }


    var del = $('.delete')
    function deleteThis() {
        del.click(function () {
            amt = $('.amount')
            data_id = this.getAttribute('data-id')
            per_list.splice(data_id-1,1)
            $("tr[data-id = " + data_id + "]").remove()
            updateTotal()
        })
    }

    $('#payment').keyup(function(){
        updateTotal()
    })
    $('#discount').keyup(function(){
        updateTotal()
    })
    deleteThis();

    $('.submit').click(function(){
        items = $('.item')
        description = $('.description');
        alt_quantity = $('.alt_quantity');
        quantity = $('.quantity');
        rate = $('.rate');
        per = $('.per');
        amount = $('.amount');
        all_items = '';
        all_description = '';
        all_alt_quantity = '';
        all_quantity = '';
        all_rate = '';
        all_per = '';
        all_amount = '';

        for(i=0;i<description.length;i++){
            all_items += items[i].value + '/n'
            all_description += description[i].value + '/n'
            all_alt_quantity += alt_quantity[i].value +'/n'
            all_quantity += quantity[i].value + '/n'
            all_rate += rate[i].value + '/n'
            all_per += per[i].value + '/n'
            all_amount += amount[i].value + '/n'
        }
        console.log()
        if($('#costumer_name')[0].value != '/add_client'){
            $('#b_name')[0].value = $('#costumer_name')[0].value
        }else{
            $('.name_error').fadeIn().delay(5000).fadeOut(1000)
            
        }
        console.log()
        if($('#costumer_name')[0].value != 'Select Client'){
            $('#b_name')[0].value = $('#costumer_name')[0].value
        }else{
            $('.name_error').fadeIn().delay(5000).fadeOut(1000)
            
        }
        $('#b_item')[0].value = all_items
        $('#b_description')[0].value = all_description
        $('#b_alternate_quantity')[0].value = all_alt_quantity
        $('#b_quantity')[0].value = all_quantity
        $('#b_rate')[0].value = all_rate
        $('#b_per')[0].value = all_per
        $('#b_amount')[0].value = all_amount
        $('#b_total_amount')[0].value = $('#total')[0].value
        $('#b_discount')[0].value = $('#discount')[0].value
        $('#b_paid_amount')[0].value = $('#payment')[0].value
        $('#b_remaning_amount')[0].value = $('#remaning')[0].value
    })


})
