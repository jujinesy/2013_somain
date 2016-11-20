$(document).ready(function(){
    $("#validation-form").validate({
        rules:{
            username: {
                required: true,
                minlength: 4
            },
            email:{
                required:true,
                email: true
            },
            password:{
                required:true,
                minlength: 4,
            },
            password_confirm:{
                required:true,
                equalTo: "#id_password"
            },
            age: {
                required: true,
                digits: true,
                min: 15,
                max: 99,
            },
            gender:"required",
            birthday: {
                required: true,
                date: true,
            },
            rr_number_0: {
                required: true,
                minlength: 6,
                digits: true,
            },
            rr_number_1: {
                required: true,
                minlength: 7,
                digits: true,
            },
            home_number_0: {
                required: true,
                minlength: 2,
                digits: true,
            },
            home_number_1: {
                required: true,
                minlength: 3,
                digits: true,
            },
            home_number_2: {
                required: true,
                minlength: 3,
                digits: true,
            },
            phone_number_0: {
                required: true,
                minlength: 3,
                digits: true,
            },
            phone_number_1: {
                required: true,
                minlength: 3,
                digits: true,
            },
            phone_number_2: {
                required: true,
                minlength: 3,
                digits: true,
            },
            school: {
                required: true,
            }
        },
        messages:{
            username: {
                required: "아이디를 입력해주세요",
                minlength: "아이디는 최소 4글자 이상이어야 합니다"
            },
            email:{
                required: "이메일을 입력해주세요",
                email: "이메일 형식이 올바르지 않습니다",
                remote: "{% url 'check_id' %}"
            },
            password: {
                required: "비밀번호를 입력해주세요",
                minlength: "비밀번호는 최소 4글자 이상이어야 합니다"
            },
            password_confirm: {
                required: "비밀번호 확인란을 입력해주세요",
                equalTo: "비밀번호와 확인란의 비밀번호가 같지 않습니다"
            },
            gender: "성별을 선택해주세요",
            birthday: {
                required: "생일을 입력해주세요",
                date: "날짜 형식에 맞게 입력해주세요. ex)1988-03-24"
            },
            rr_number_0: {
                required: "주민등록번호 앞자리를 입력해주세요",
                minlength: "",
                digits: "숫자만 입력해주세요"
            },
            rr_number_1: {
                required: "주민등록번호 뒷자리를 입력해주세요",
                minlength: "",
                digits: "숫자만 입력해주세요"
            },
            school: {
                required: "학교명을 입력해주세요"
            }
        },
        errorElement: "span",
        errorClass: "help-inline",
        validClass: "help-inline",
        highlight: function(element, errorClass, validClass) {
            $(element).removeClass('valid');
            $(element).parents('.control-group').removeClass('success');
            $(element).parents('.control-group').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).addClass('valid');
            $(element).parents('.control-group').removeClass('error');
            $(element).parents('.control-group').addClass('success');
        }
    });
});

$(function() {
  $( "#id_birthday" ).datepicker({
    yearRange: '-40:-15',
    changeMonth: true,
    changeYear: true,

    dateFormat: 'yy-mm-dd',
    prevText: '이전 달',
    nextText: '다음 달',
    monthNames: ['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'],
    monthNamesShort: ['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'],
    dayNames: ['일','월','화','수','목','금','토'],
    dayNamesShort: ['일','월','화','수','목','금','토'],
    dayNamesMin: ['일','월','화','수','목','금','토'],
    showMonthAfterYear: true,
    yearSuffix: '년'
    });
});

var find_zipcode = function(keyword) {
    if(!keyword) {
        $('#zip_search').show();
        $('#zip_list').html('');
    } else {
        $.ajax({
            url: '/korzip/search',
            data: { keyword: keyword },
            success: function(data) {
                if(!data.status) {
                    alert('검색 오류');
                    return;
                }

                if(data.count == 0) {
                    alert('결과값이 없습니다.');
                    return;
                } else {
                    $('#zip_list').html('');
                    for(var d in data.data) {
                        $('#zip_list').append(
                            '<li onclick=\'select_zipcode("' + data.data[d].zipcode + '", "' + data.data[d].address + '")\'><strong>' + data.data[d].zipcode + '</strong> ' + data.data[d].address + '</li>'
                        );
                    }
                }
            }
        });
    }
};
var select_zipcode = function(zipcode, address) {
    $('#zip_list').html('');
    zipcode = zipcode.split("-");
    $('#id_zipcode_0').val(zipcode[0]);
    $('#id_zipcode_1').val(zipcode[1]);
    $('#{{ form.address1.id_for_label }}').val(address);
    $('#{{ form.address2.id_for_label }}').removeAttr('readonly');

    $('#zip_search').hide();
};
