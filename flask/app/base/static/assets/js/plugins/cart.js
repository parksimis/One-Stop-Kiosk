/* temp.js */

$('.minus').click(function (){
    var tmp_num = parseInt($(this).next('input').val());

    if (tmp_num-1 == -1){
        alert('최소 주문 수량입니다.')
        $(this).next('input').val(0);
    } else {
        $(this).next('input').val(tmp_num-1);
    }
})

$('.plus').click(function (){
    var tmp_plus = parseInt($(this).prev('input').val());

    if (tmp_plus == 10){
        alert('최대 주문 수량입니다.');
        $(this).prev('input').val(0);
    } else {
        $(this).prev('input').val(tmp_plus+1);
    }

})
