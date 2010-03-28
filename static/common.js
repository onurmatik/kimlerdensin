function flag(f, a, m, id)
{
	$.get('/flag/' + f + '/' + a + '/' + m + '/' + id + '/', function(data)
	{
		if (data == '0')
		{
			$('#flag_' + f) = '/flag_' + f + '_1.gif';
		}
		else
		{
			$('#flag_' + f) = '/flag_' + f + '_0.gif';
		}
	});
}

function update_messages_link()
{
	$.get('/mesajlar/ajax/new/', function(data)
	{
		if (data != '0')
		{
			$('#messages_link').empty().append('<span style="color:#ff0000">yeni mesaj!</span>');
		}
	});
}

function display_option(q_id, opt, disp)
{
	if (disp)
		$('#q_' + q_id + '_opt_' + opt).show();
	else
		$('#q_' + q_id + '_opt_' + opt).hide();
}

function ans(id, a)
{
	$.get('/ajax-ans/' + id + '/' + a + '/', function(data)
	{
		if (data == '0')
		{
			$('#question_' + id).removeClass('ans_1').removeClass('ans_2');
			$('#q_' + id + '_ans').empty();
			display_option(id, '0', 0);
			display_option(id, '1', 1);
			display_option(id, '2', 1);
		} 
		else if (data == '1')
		{
			$('#question_' + id).removeClass('ans_2').addClass('ans_1');
			$('#q_' + id + '_ans').empty().append('<span style="color:#66cc33">evet</span>');
			display_option(id, '0', 1);
			display_option(id, '1', 0);
			display_option(id, '2', 1);
		}
		else if (data == '2')
		{
			$('#question_' + id).removeClass('ans_1').addClass('ans_2');
			$('#q_' + id + '_ans').empty().append('<span style="color:#cc2222">hayır</span>');
			display_option(id, '0', 1);
			display_option(id, '1', 1);
			display_option(id, '2', 0);
		}
		else document.location = data;
	});
}

