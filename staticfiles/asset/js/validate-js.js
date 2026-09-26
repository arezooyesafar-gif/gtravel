function isNumberKey(evt) {
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode === 44) {
        return true;
    } else if (charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    }
}

function separateDigits() {
    let inputElement = document.getElementById('tour_price');
    let number = inputElement.value;
    let prePaidElement = document.getElementById('pre_paid')
    let preElement = document.getElementById('price_val');
    number = number.replace(/,/g, '');
    number = parseInt(number);
    prePaid = number / 2
    if (isNaN(number)) {
        inputElement.value = '0';
    } else {
        inputElement.value = number.toLocaleString("en-US");
        // prePaidElement.value = prePaid.toLocaleString("en-US");
        // preElement.innerHTML = prePaid.toLocaleString("en-US");
    }
}

function separateDigits2() {
    let inputElement = document.getElementById('pre_paid');
    let preElement = document.getElementById('price_val');
    let number = inputElement.value;
    number = number.replace(/,/g, '');
    number = parseInt(number);
    if (isNaN(number)) {
        inputElement.value = '0';
        preElement.innerHTML = '0';
    } else {
        inputElement.value = number.toLocaleString("en-US");
        preElement.innerHTML = number.toLocaleString("en-US");
    }
}

function installment_calculation() {
    let tourElement = document.getElementById('tour_price');
    let tour_price = tourElement.value.replace(/,/g, '');
    let paidElement = document.getElementById('pre_paid');
    let paidvalueElement = document.getElementById('pre_paid_value');
    let instPeriodElement = document.getElementById('inst_period');
    let pre_paid = paidElement.value.replace(/,/g, '');
    let instElement = document.getElementById('inst_num');
    let instValElement = document.getElementById('instal_val');
    let tourTotalElement = document.getElementById('tour_total_price');
    let debit = parseInt(tour_price) - parseInt(pre_paid)
    var commition_fee = (debit * 4) / 100
    var total_debit = (commition_fee * parseInt(instElement.value)) + debit
    var total_debit = Math.ceil((total_debit)/1000)*1000
    var inst_price = Math.ceil((total_debit / parseInt(instElement.value))/1000)*1000
    $('.resualt-box').slideDown(300)
    tourTotalElement.innerHTML = (total_debit + parseInt(pre_paid)).toLocaleString("en-US") + ' ' + 'تومان';
    paidvalueElement.innerHTML = (parseInt(pre_paid)).toLocaleString("en-US") + ' ' + 'تومان';
    instPeriodElement.innerHTML = instElement.value + ' ' + 'ماه'
    instValElement.innerHTML = inst_price.toLocaleString("en-US") + ' ' + 'تومان';


}

function checking_values() {
    let chequ_number = document.getElementById('chequ_num').value
    let inst_number = document.getElementById('inst_num')
    var checkboxes = document.querySelectorAll('.ckbx');
    if (chequ_number >= inst_number.value) {
        inst_number.value = chequ_number
        inst_number.setAttribute('min', chequ_number)
    }
    else if (chequ_number < inst_number.value) {
        inst_number.setAttribute('min', 3)
    }
    if (parseInt(chequ_number) > 1 && parseInt(inst_number.value) <= 6){
        for (i=0; i<parseInt(inst_number.value);i++) {
                checkboxes[i].removeAttribute('disabled')
                checkboxes[parseInt(inst_number.value)-1].checked = true
                checkboxes[parseInt(inst_number.value)-2].checked = false
        }
    }
    if (parseInt(chequ_number) === 1){
        for (i=0; i<parseInt(inst_number.value);i++) {
                checkboxes[i].setAttribute('disabled', 'true')
                checkboxes[i].checked = false
                checkboxes[parseInt(inst_number.value)-1].checked = true
        }
        checkboxes[parseInt(inst_number.value)-1].removeAttribute('disabled')

    }
}

function inst_chequ_month() {
    var checkboxes = document.querySelectorAll('.ckbx');
    let chequ_number = document.getElementById('chequ_num').value
    let inst_number = document.getElementById('inst_num')
    if (inst_number.value < chequ_number) {
         document.getElementById('chequ_num').value = inst_number.value
    }
    if (parseInt(chequ_number) === 1){
        for (i=0; i<checkboxes.length;i++) {
            checkboxes[i].checked = false
            checkboxes[i].setAttribute('disabled', 'true')
            checkboxes[parseInt(inst_number.value)-1].removeAttribute('disabled')
            checkboxes[parseInt(inst_number.value)-1].checked = true
        }
    }
    if (parseInt(chequ_number) > 1){
        for (i=0; i<checkboxes.length;i++) {
            checkboxes[i].checked = false
            // checkboxes[i].setAttribute('disabled', 'true')
            checkboxes[parseInt(inst_number.value)-1].removeAttribute('disabled')
            checkboxes[parseInt(inst_number.value)-1].checked = true
        }
    }
    if (parseInt(chequ_number) >1 && parseInt(inst_number.value) < 6){
        checkboxes[parseInt(inst_number.value)].setAttribute('disabled', 'true')
    }
}
function inst_month_check() {
    let chequ_num = document.getElementById('chequ_num').value
    let inst_number = document.getElementById('inst_num')
    var checkboxes = document.querySelectorAll('.ckbx');
    var checkedCheckboxes = [];
    checkboxes.forEach(function (checkbox) {
        if (checkbox.checked) {
            checkedCheckboxes.push(checkbox.id);
        }
    });
    if (checkedCheckboxes.length > chequ_num) {
        checkboxes.forEach(function (checkbox) {
            checkbox.checked = false;
        });
        checkboxes[parseInt(inst_number.value)-1].checked = true
    }
}