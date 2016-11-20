var options = {
	events_url: '/lecture/list',
	view: 'month',
	tmpl_path: '/static/tpl/calendar/',
	tmpl_cache: false,
	holidays: { }, // http://files.apple.com/calendars/South32Korean32Holidays.ics ,
	first_day: 0,
	onAfterEventsLoad: function(events) {
		if(!events) {
			return;
		}
		var list = $('#eventlist > tbody');
		list.html('');

		$.each(events, function(key, val) {
			// $(document.createElement('li')).html('<div class="event_desc">' + moment(val.start).format('YYYY/MM/DD') + ' - ' + val.room_name + '</div><a href="#" data-event-id="' + val.id + '" data-start="' + val.start + '" data-end-"' + val.end + '">' + val.title + '</a>').appendTo(list);
		    var hrs = moment(val.end).diff(val.start, 'hours')
		    if(hrs == '0hrs') hrs = '30mins'
		    val.room_name = val.room_name.replace(/연수센터 [0-9]층 \:\s?/, '')
		    $(document.createElement('tr')).html([
                '<td>'+ moment(val.start).format('MM/DD HH:mm') + '</td>',
                '<td>' + hrs + 'hrs</td>',
                '<td>' + val.room_name + '</td>',
                '<td>' + val.admin + '</td>'
		    ].join('')).appendTo(list);
		});

		/*$('a[data-event-id]').click(function() {
            var win = window.open('/lecture/view/' + $(this).data('event-id'), '_blank', 'width=350, height=420, toolbar=no, location=no, status=no, menubar=no, scrollbars=yes, resizable=no');
            win.focus();

            return false;
		});*/
	},
	onAfterViewLoad: function(view) {
		$('.page-header h3').text(this.getTitle());
		// $('.btn-group button').removeClass('active');
		// $('button[data-calendar-view="' + view + '"]').addClass('active');
		$('[data-toggle="tooltip"]').tooltip();

		$('a[data-event-id]').click(function() {
            var win = window.open('/lecture/view/' + $(this).data('event-id'), '_blank', 'width=350, height=420, toolbar=no, location=no, status=no, menubar=no, scrollbars=yes, resizable=no');
            win.focus();

            return false;
		});

		/*$('[data-calendar-view="day"], [data-cal-view="day"]').click(function() {
		    return false;
		});*/
	},
	classes: {
		months: {
			general: 'label'
		}
	}
};

var	calendar = $('#calendar').calendar(options);
calendar.setLanguage('ko-KR');
calendar.view();

$('button[data-calendar-nav]').each(function() {
	var $this = $(this);
	$this.click(function() {
		calendar.navigate($this.data('calendar-nav'));
	});
});
$('button[data-calendar-view]').each(function() {
	var $this = $(this);
	$this.click(function() {
		calendar.view($this.data('calendar-view'));
	});
});

setInterval(function() {
    calendar.view();
}, 30000);