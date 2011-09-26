
var oldNadwaName = "";
var nadwaName = "";
var autoUpdate = false;

var n_hours = 0;
var n_minutes = 0;
var n_seconds = 0;
var running = false;
google.load("visualization", "1", {packages:["corechart"]});
var owner;
var tweets = [];
var topTweets = [];
var sizeLiveBoard = 100;
var showingTopTweets = true;
var slidDownDuration = 700;

$(function (){
	$('#Nadwa_Tabs').tabs();
	$('#Top_Tweets_Tabs').tabs();

	$('#quBut1').button();
	$('#quBut2').button();
	$('#quBut3').button();
	$('#quBut4').button();
	$('#quBut5').button();
	$('#autoUpdate').button();
	$('#showTopTen').button();
	$('#btnShowTopTWs').button();
	
	$('#alert').dialog({ autoOpen: false });
	$('#delUser').dialog({ autoOpen: false });
	$('#delTweet').dialog({ autoOpen: false });
	$('#errAddUser').dialog({ autoOpen: false });
	$('#errCreateNadwa').dialog({ autoOpen: false });
	$('#errShowTweets').dialog({ autoOpen: false });

	
	window.setInterval(updateTweets, 10000);
	window.setInterval(showNadwaTime, 1000);
	window.setInterval(updateLiveBoard, 10000);
	window.setInterval(_showTopTweets, 300000);
	window.setInterval(addLiveTW, 500);
	window.setInterval(syncTime, 30000);

	$.ajax({
		url : '/jsUsers?htmlTableGrid=tableUsers&htmlDivPager=tableUsersPager&handlerURL=handlerUsers/&editURL=editHandlerUsers/&gridCaption=Nadwa Users',
		success : function(js) {
			$('body').append(js);
		},
		cache : false
	});
	
	$.ajax({
		url : '/jsTweets?htmlTableGrid=tableTweets&htmlDivPager=tableTweetsPager&handlerURL=handlerTweets/&editURL=editHandlerTweets/&gridCaption=Tweets',
		success : function(js) {
			$('body').append(js);
		},
		cache : false
	});
	
	$(window).unload(function() {
		$.ajax({
			url : '/stopTracking?nadwaName='+nadwaName+'&owner='+owner,
			success : function(js) {
			},
			cache : false
		});
	});

})

function createNadwa(){
	nadwaName =  $("#hashTag").val();
	if(nadwaName == "" || nadwaName.length == 0){
		$('#errCreateNadwa').dialog('open');
	}else{
		$.ajax({
			url : '/createNadwa?nadwaName='+nadwaName,
			success : function(js) {
			js = eval(js)
				if(js == 1){
					$('#hashTag').val('');
					var confirmation_Label = '<label>#'+nadwaName+' Created Successfully...</label>';
					var br = '<br> <br>'
					var stream_button = '<button id = "streamButton" type="button" onclick="startTracking()"> Start Tracking </button>'
					owner = 1;
					$('#nadwaNameDiv').hide();
					$('#quBut3').show();
					$('#quBut4').show();
					$('#usersDiv').show();
					$('#tableUsersPager').show();
					$('#tableTweetsPager').show();
					
					$('#stream').html(confirmation_Label + br + stream_button);
					$('#streamButton').button();
					running = false;
					n_hours = 0;
					n_minutes = 0;
					n_seconds = 0;
					_showNadwaTime();
					removeLiveBoardTW();
					
				}else if(js == 0){
					owner = 0;
					var confirmation_Label = '<label> You are watching #'+nadwaName+' now.</label>';
					running = true;
					syncTime();
					$('#stream').html(confirmation_Label)
					$('#quBut3').hide();
					$('#quBut4').hide();
					$('#usersDiv').hide();
					$('#tableUsersPager').hide();
					$('#tableTweetsPager').hide();
					
					$('#Nadwa_Tabs').tabs( "select" , 2 );
					removeLiveBoardTW();
				}
			},
			cache : false
		});
	}
}

function syncTime(){
	if(!running)
		return;
	$.ajax({
		url : '/syncCreationTime?nadwaName='+nadwaName,
		success : function(res) {
			res = eval( '(' + res + ')' );
			var h = res[0];
			if(h == -1){
				var str = "#" + nadwaName + " is Stopped.";
				setNadwaState(str, "FF0000");
				running = false;
			}else{
				n_hours = res[0];
				n_minutes = res[1];
				n_seconds = res[2];
			}
		},
		cache : false
	});
}

function nadwaActionEnter(e){
	var keycode;
	if (window.event) 
		keycode = window.event.keyCode;
	else if (e) 
		keycode = e.which;
	else 
		return;
	
	if (keycode == 13)
	{
		createNadwa();
	}
}

function showNadwaTime(){
	if(!running)
		return;
	n_seconds = n_seconds + 1;
	if (n_seconds == 60){
		n_seconds = 0;
		n_minutes = n_minutes + 1;
		if(n_minutes == 60){
			n_minutes = 0;
			n_hours = n_hours + 1;
		}
	}
	 _showNadwaTime();
}

function _showNadwaTime(){
	var str = n_hours + 'h : ' + n_minutes + 'm : ' + n_seconds + 's'
	setNadwaState(str, "FFFFFF");
}

function startTracking(){
	$.ajax({
		url : '/startTracking?nadwaName='+nadwaName,
		success : function(js) {
		js = eval(js)
			if(js != 0){
				if(js == 1){
					var confirmation_Label = '<label> Tracking #' + nadwaName + ' Is In Progress Now...</label>';
					var br = '<br> <br>'
					var pause_button = '<button id = "pauseButton" type="button" onclick="pauseTracking()"> Pause Tracking </button>'
					var stop_button = '<button id = "stopButton" type="button" onclick="stopTracking()"> Stop Tracking </button>'
					$('#stream').html(confirmation_Label + br + pause_button + "  " + stop_button);
					$('#pauseButton').button();
					$('#stopButton').button();
					$("#tableUsers").trigger("reloadGrid");
					$("#tableTweets").trigger("reloadGrid");
					
					running = true;
					n_hours = 0;
					n_minutes = 0;
					n_seconds = 0;
					
					removeLiveBoardTW();
					
					$('#Nadwa_Tabs').tabs( "select" , 2 );
					
				}else if(js == 2){
					alert('Tracking #' + nadwaName + 'is already running...')
				}
			}else{
				$('#alert').dialog('open');
			}
		},
		cache : false
	});
}

function stopTracking(){
	$.ajax({
		url : '/stopTracking?nadwaName='+nadwaName,
		success : function(js) {
			js = eval(js)
			if (js == 1){
				var confirmation_Label = '<label> Tracking #' + nadwaName + ' Is Stopped</label>';
				var br = '<br> <br>'
				$('#stream').html(confirmation_Label + br);
				$('#nadwaNameDiv').show();
				running = false;
				var str = '#' + nadwaName + ' nadwa taken ' + n_hours + 'h : ' + n_minutes + 'm : ' + n_seconds + 's'
				setNadwaState(str, "FF0000");
				removeLiveBoardTW();
			}else if (js == 0){
				$('#alert').dialog('open');
			}
		},
		cache : false
	});
}

function setNadwaState(str, color){
	var html = '<font color="#'+ color + '">' + str + '</font>'
	$('#nadwaStartTime').html(html);
}

function pauseTracking(){
	$.ajax({
		url : '/pauseTracking?nadwaName='+nadwaName,
		success : function(js) {
			js = eval(js)
			if(js != 0){
				if (js == 1){
					var confirmation_Label = '<label> Tracking #'+ nadwaName +' is Paused. </label>';
					var br = '<br> <br>'
					var resume_button = '<button id = "resumeButton" type="button" onclick="resumeTracking()"> Resume Tracking </button>'
					var stop_button = '<button id = "stopButton" type="button" onclick="stopTracking()"> Stop Tracking </button>'
					$('#stream').html(confirmation_Label + br + resume_button + "  " + stop_button);
					$('#resumeButton').button();
					$('#stopButton').button();
				}else if (js == 2){
					alert('Tracking #' + nadwaName + 'didn' + "'" + 't start yet')
				}
			}else{
				$('#alert').dialog('open');
			}
		},
		cache : false
	});
}

function resumeTracking(){
	$.ajax({
		url : '/resumeTracking?nadwaName='+nadwaName,
		success : function(js) {
			js = eval(js)
			if(js != 0){
				if (js == 1){
					var confirmation_Label = '<label> Tracking #' + nadwaName + ' is resumed, and in progress now...</label>';
					var br = '<br> <br>'
					var pause_button = '<button id = "pauseButton" type="button" onclick="pauseTracking()"> Pause Tracking </button>'
					var stop_button = '<button id = "stopButton" type="button" onclick="stopTracking()"> Stop Tracking </button>'
					$('#stream').html(confirmation_Label + br + pause_button + "  " + stop_button);
					$('#pauseButton').button();
					$('#stopButton').button();
				}else if (js == 2){
					alert('Tracking #' + nadwaName + 'is already running...')
				}else if (js == 3){
					alert('Tracking #' + nadwaName + 'didn' + "'" + 't start yet')
				}
			}else{
				$('#alert').dialog('open');
			}
		},
		cache : false
	});
}

function removeLiveBoardTW(){
	var rows = $('#liveBoard >tbody >tr').length;
	while(rows >= 1){
		$('#liveBoard tbody tr:last').remove();
		rows = rows - 1;
	}
	
	removeTopLiveBoardTW();
	
	lastID = 0;
	tweets = [];
}

function removeTopLiveBoardTW(){
	var rows = $('#topliveBoard >tbody >tr').length;
	while(rows >= 1){
		$('#topliveBoard tbody tr:last').remove();
		rows = rows - 1;
	}
}

function activateAutoUpdate(){
	if(autoUpdate){
		autoUpdate = false;
		$('#autoUpdate').html('Acvtivate Auto Update');
	}else{
		autoUpdate = true;
		$('#autoUpdate').html('Deactivate Auto Update');
	}
}

function addUser(){
	if(nadwaName == ""){
		alert('Sorry, You Need To Create Your nadwa First');
		return;
	}
	userName =  $("#user").val();
	if(userName == "" || userName.length == 0){
		$('#errAddUser').dialog('open');
	}else{
		$.ajax({
			url : '/addUser?user='+userName+"&nadwaName="+nadwaName,
			success : function(js) {
				js = eval(js)
				if(js > 0){
					$('#user').val('');
					$("#tableUsers").trigger("reloadGrid");
				}else{
					$('#alert').dialog('open');
				}
			},
			cache : false
		});
	}
}

function userActionEnter(e){
	var keycode;
	if (window.event) 
		keycode = window.event.keyCode;
	else if (e) 
		keycode = e.which;
	else 
		return;
	
	if (keycode == 13)
	{
		addUser();
	}
}

function delUsers(){
	$.ajax({
		url : '/clearUsers?nadwaName='+nadwaName,
		success : function(js) {
		if(js == 'ok'){
			$('#user').val('');
			$('#delUser').dialog('open');
			$("#tableUsers").trigger("reloadGrid");
		}else{
			$('#alert').dialog('open');
		}
		},
		cache : false
	});
}

function delTweets(){
	$.ajax({
		url : '/clearStatus?nadwaName='+nadwaName,
		success : function(js) {
			if(js == 'ok'){
				$('#user').val('');
				$('#delTweet').dialog('open');
				$("#tableTweets").trigger("reloadGrid");
			}else{
				$('#alert').dialog('open');
			}
		},
		cache : false
	});
}

var lastID = 0;
function updateLiveBoard(){
	if(!running)
		return;
	$.ajax({
		url : '/liveBoard?nadwaName='+nadwaName+'&lastID='+lastID,
		success : function(res) {
			res = eval( '(' + res + ')' );
			for (i = 0; i < res.length-1; i++){
				tweets.push(res[i]);
			}
			if (res.length > 0){
				lastID = res[res.length-1][0];
			}
		},
		cache : false
	});
}

function addLiveTW(){
	if(!running)
		return;
	if(tweets.length > 0){
		var tweet = tweets[0];
		tweets.splice(0,1);
		var name = tweet[0],
			txt  = tweet[1],
			att	 = tweet[2],
			img  = tweet[3],
			id   = tweet[4];
		var org_tr = '<tr> <td>';
		var div = '<div id="'+ id +'" style="display: none;">';
		var table = '<table cellspacing="0" cellpadding="0">';
		var tr = '<tr class="bottomborder" >';
		var imgTD =  '<td class="username" align="center" valign = "center">';
			imgTD += '<a target="_blank" href="http://twitter.com/' + name + '">' + img + '</a>';
			imgTD += '</td>';
		var txtTD = '<td class="status-body" align="left" valign = "center">';
			txtTD += '<div class="msg"> <b> <font size="2" face="arial" color="#40AADD">' + name + '</font> </b> <br> <b> <font size="2" face="arial" color="#000000"> ' + txt + ' </font> </b> </div>';
			txtTD += '</td>';
		tr += imgTD;
		tr += txtTD;
		tr += '</tr>';
		table += tr;
		table += '</table>';
		div += table;
		div += '</div>';
		org_tr += div;
		org_tr += '</tr></td>';
		$('#liveBoard').prepend(org_tr);
		$('#' + id).slideDown(slidDownDuration);
		var rows = $('#liveBoard >tbody >tr').length;
		if(rows > sizeLiveBoard){
			$('#liveBoard tbody tr:last').remove();
		}
	}
}

var numTop = 0;
var topSidx = 0;
var topRows = 0;

function showTopTweets(){
	if(!running)
		return;
	if(showingTopTweets){
		showingTopTweets = false;
		$("#topTweetsBoard").hide();
		$('#btnShowTopTWs').html("show");
	}else{
		showingTopTweets = true;
		$("#topTweetsBoard").show();
		$('#btnShowTopTWs').html("Hide");
	}
}

function _showTopTweets(){
	if(!showingTopTweets || !running){
		return;
	}
	numTop =  $("#topTweets").val();
	var topSidx = 1;
	if(numTop == "" || numTop.length == 0 || eval(numTop) < 1){
		$("#topTweets").val('');
		return;
	}else{
		topSidx = $("#topTWOptions").val(); // 0 -> inside, 1 -> outside, 2 -> total
		numTop = eval(numTop);
	}
	
	removeTopLiveBoardTW();
	topRows = 0;
	
	$.ajax({
		url : '/topLiveBoard?nadwaName='+nadwaName+'&num='+numTop+'&sidx='+topSidx,
		success : function(res) {
			res = eval( '(' + res + ')' );
			for (i = (res.length-1); i >= 0 ; i--){
				var tweet = res[i];
				var name = tweet[0],
					txt  = tweet[1],
					att	 = tweet[2],
					img  = tweet[3],
					id   = tweet[4];
				var org_tr = '<tr> <td>';
				var div = '<div id="'+ id +'" style="display: none;">';
				var table = '<table cellspacing="0" cellpadding="0">';
				var tr = '<tr class="bottomborder" >';
				var imgTD =  '<td class="username tdTopTW" align="center" valign = "center">';
					imgTD += '<a target="_blank" href="http://twitter.com/' + name + '">' + img + '</a>';
					imgTD += '</td>';
				var txtTD = '<td class="status-body tdTopTW" align="left" valign = "center">';
					txtTD += '<div class="msg"> <b> <font size="2" face="arial" color="#40AADD">' + name + '</font> </b> <br> <b> <font size="2" face="arial" color="#000000"> ' + txt + ' </font> </b> </div>';
					txtTD += '</td>';
				tr += imgTD;
				tr += txtTD;
				tr += '</tr>';
				table += tr;
				table += '</table>';
				div += table;
				div += '</div>';
				org_tr += div;
				org_tr += '</tr></td>';
				$('#topliveBoard').prepend(org_tr);
				$('#' + id).slideDown(slidDownDuration);
				topRows++;
				if(topRows > numTop){
					$('#topliveBoard tr:last').remove();
					$('#topliveBoard tr:last').remove();
					topRows--;
				}
			}
			if(topRows > numTop){
				var rows = topRows;
				for(i = numTop+1; i <= rows; i++){
					$('#topliveBoard tr:last').remove();
					$('#topliveBoard tr:last').remove();
					topRows--;
				}
			}
			
		},
		cache : false
	});
}

function updateTweets() {
	if(!running)
		return;
	if(autoUpdate){
		$("#tableTweets").trigger("reloadGrid");
	}
}

function showTweetsEnter(e){
	var keycode;
	if (window.event) 
		keycode = window.event.keyCode;
	else if (e) 
		keycode = e.which;
	else 
		return;
	
	if (keycode == 13)
	{
		showTweets();
	}
}

function getDate(){
	var tmp =  $("#tweetsfromTime").val();
	if(tmp == "" || tmp.length == 0 || eval(tmp) < 1 || !isShowTweets){
		$("#tableTweets").trigger("reloadGrid");
		$('#showTime').html('');
	}else{
		tweetsfromTime = tmp;
		var today = new Date();
		var mins = eval(tweetsfromTime);
		var milli = today.getTime() - (1000 * 60 * mins);
		var d = new Date(milli);
		var year = d.getFullYear();
		var month = d.getMonth() + 1;
		var day = d.getDate();
		var hour = d.getHours();
		var min = d.getMinutes();
		var sec = d.getSeconds();
		var date = '' + year + '-' + month + '-' + day + ' ' + hour + ':' + min + ':' + sec + '';
		return date;
	}
	return 'No';
}

var data_inSide;
var data_outSide;
var data_total;
var data_interestTime;

function showTopTen(){
	if(nadwaName == ""){
		alert('Sorry, You Need To Create Your nadwa First');
		return;
	}
	$("#insideRT_div").html("");
	$("#outsideRT_div").html("");
	$("#totalRT_div").html("");
	$("#longestRTTime_div").html("");
	$.ajax({
		url : '/getTopTenInside?nadwaName='+nadwaName+'&date='+getDate(),
		success : function(res) {
			res = eval( '(' + res + ')' );
			if ( res.length > 0){
				data_inSide = new google.visualization.DataTable();
				data_inSide.addColumn('string', 'Users');
				data_inSide.addColumn('number', 'Retweets');
				data_inSide.addRows(res.length);
			}
			var html = '';
			var i;
			for (i = 0; i < res.length; i++){
				var tmp = res[i];
				html += '<div align="center" style="border:3px solid #40AAFF; padding:10px; margin:0px; -moz-border-radius: 20px 0px; border-bottom-right-radius: 20px 0px;">'
					html += '<div align="left" style="color:#40AAFF; font_size=20px">';
						html += tmp[4] + "   "
						html += tmp[0] + ' Inside Retweets for ' + tmp[1] + "'s tweet";
					html += '</div>';
					html += '<br>';
					html += '<div align="left">';
						html += tmp[2];
					html += '</div>';
					html += '<div align="right" style="color:#FF0000;" >';
						var attend = tmp[3];
						if(attend){
							html += 'Attendant';
						}
					html += '</div>';
				html += '</div>';
				html += '<br>';
				data_inSide.setCell(i, 0, tmp[1]);
				data_inSide.setCell(i, 1, tmp[0], '<span align="left">Regular Title<div id="gvTooltipData" align="left"> ' + tmp[4] + ' <b> <font size="2" face="arial" color="red"> ' + tmp[1] + ' </font> </b> have <b> <font size="2" face="arial" color="black"> ' + tmp[0] + ' </font> </b>  Retweets for:<br>' + tmp[2] + ' </div></span>');
			}
			if (res.length > 0){
				var chart = new google.visualization.ColumnChart(document.getElementById('insideRT_div'));
				chart.draw(data_inSide, {width: 600, height: 240, title: 'Inside Retweets',
							hAxis: {title: 'Users', titleTextStyle: {color: 'red'}},
							vAxis: {title: 'Retweets', titleTextStyle: {color: 'red'}}
							});
				var gvTooltipOptions = "{maxWidth: '400px', position: 'topRight', offsetBottom:-330}";
				gvTooltip("insideRT_div", "data_inSide", chart, gvTooltipOptions); 
			}
			//$('#TopTenInside').html(html);
		},
		cache : false
	});
	$.ajax({
		url : '/getTopTenOutside?nadwaName='+nadwaName+'&date='+getDate(),
		success : function(res) {
			res = eval( '(' + res + ')' );
			if ( res.length > 0){
				data_outSide = new google.visualization.DataTable();
				data_outSide.addColumn('string', 'Users');
				data_outSide.addColumn('number', 'Retweets');
				data_outSide.addRows(res.length);
			}
			var html = '';
			var i;
			for (i = 0; i < res.length; i++){
				var tmp = res[i];
				html += '<div align="center" style="border:3px solid #40AAFF; padding:10px; margin:0px; -moz-border-radius: 20px 0px; border-bottom-right-radius: 20px 0px;">'
					html += '<div align="left" style="color:#40AAFF; font_size=20px">';
						// var className = 'bar' + i;
						// html += '<span class="' + className + '"></span>'
						html += tmp[4] + "   "
						html += tmp[0] + ' Outside Retweets for ' + tmp[1] + "'s tweet";
					html += '</div>';
					html += '<br>';
					html += '<div align="left">';
						html += tmp[2];
					html += '</div>';
					html += '<div align="right" style="color:#FF0000;" >';
						var attend = tmp[3];
						if(attend){
							html += 'Attendant';
						}
					html += '</div>';
				html += '</div>';
				html += '<br>';
				data_outSide.setCell(i, 0, tmp[1]);
				data_outSide.setCell(i, 1, tmp[0], '<span align="left">Regular Title<div id="gvTooltipData" align="left"> ' + tmp[4] + ' <b> <font size="2" face="arial" color="red"> ' + tmp[1] + ' </font> </b> have <b> <font size="2" face="arial" color="black"> ' + tmp[0] + ' </font> </b> Retweets for:<br>' + tmp[2] + ' </div></span>');
			}
			if (res.length > 0){
				var chart = new google.visualization.ColumnChart(document.getElementById('outsideRT_div'));
				chart.draw(data_outSide, {width: 600, height: 240, title: 'Outside Retweets',
									hAxis: {title: 'Users', titleTextStyle: {color: 'red'}},
									vAxis: {title: 'Retweets', titleTextStyle: {color: 'red'}}
									});
				var gvTooltipOptions = "{maxWidth: '400px', position: 'topRight', offsetBottom:-330}";
				gvTooltip("outsideRT_div", "data_outSide", chart, gvTooltipOptions); 
			}
			//$('#TopTenOutside').html(html);
			// for (i = 0; i < res.length; i++){
				// var className = 'bar' + i;
				// var tmp = res[i];
				// $('.' + className).sparkline([tmp[0],0], {type: 'bar', barColor: 'green'} );
			// }
		},
		cache : false
	});
	$.ajax({
		url : '/getTopTenTotal?nadwaName='+nadwaName+'&date='+getDate(),
		success : function(res) {
			res = eval( '(' + res + ')' );
			if ( res.length > 0){
				data_total = new google.visualization.DataTable();
				data_total.addColumn('string', 'Users');
				data_total.addColumn('number', 'Retweets');
				data_total.addRows(res.length);
			}
			var html = '';
			var i;
			for (i = 0; i < res.length; i++){
				var tmp = res[i];
				html += '<div align="center" style="border:3px solid #40AAFF; padding:10px; margin:0px; -moz-border-radius: 20px 0px; border-bottom-right-radius: 20px 0px;">'
					html += '<div align="left" style="color:#40AAFF; font_size=20px">';
						html += tmp[4] + "   "
						html += tmp[0] + ' Total Retweets for ' + tmp[1] + "'s tweet";
					html += '</div>';
					html += '<br>';
					html += '<div align="left">';
						html += tmp[2];
					html += '</div>';
					html += '<div align="right" style="color:#FF0000;" >';
						var attend = tmp[3];
						if(attend){
							html += 'Attendant';
						}
					html += '</div>';
				html += '</div>';
				html += '<br>';
				data_total.setCell(i, 0, tmp[1]);
				data_total.setCell(i, 1, tmp[0], '<span align="left">Regular Title<div id="gvTooltipData" align="left"> ' + tmp[4] + ' <b> <font size="2" face="arial" color="red"> ' + tmp[1] + ' </font> </b> have <b> <font size="2" face="arial" color="black"> ' + tmp[0] + ' </font> </b> Retweets for:<br>' + tmp[2] + ' </div></span>');
			}
			if (res.length > 0){
				var chart = new google.visualization.ColumnChart(document.getElementById('totalRT_div'));
				chart.draw(data_total, {width: 600, height: 240, title: 'Total Retweets',
							hAxis: {title: 'Users', titleTextStyle: {color: 'red'}},
							vAxis: {title: 'Retweets', titleTextStyle: {color: 'red'}}
							});
				var gvTooltipOptions = "{maxWidth: '400px', position: 'topRight', offsetBottom:-330}";
				gvTooltip("totalRT_div", "data_total", chart, gvTooltipOptions); 
			}
			//$('#TopTenTotal').html(html);
		},
		cache : false
	});
	$.ajax({
		url : '/getTopTenLongestRTTime?nadwaName='+nadwaName+'&date='+getDate(),
		success : function(res) {
			res = eval( '(' + res + ')' );
			if ( res.length > 0){
				data_interestTime = new google.visualization.DataTable();
				data_interestTime.addColumn('string', 'Users');
				data_interestTime.addColumn('number', 'Interest Time');
				data_interestTime.addRows(res.length);
			}
			var html = '';
			var i;
			for (i = 0; i < res.length; i++){
				var tmp = res[i];
				html += '<div align="center" style="border:3px solid #40AAFF; padding:10px; margin:0px; -moz-border-radius: 20px 0px; border-bottom-right-radius: 20px 0px;">'
					html += '<div align="left" style="color:#40AAFF; font_size=20px">';
						html += tmp[4] + "   "
						html += tmp[0] + ' Minutes Interest Time for ' + tmp[1] + "'s tweet";
					html += '</div>';
					html += '<br>';
					html += '<div align="left">';
						html += tmp[2];
					html += '</div>';
					html += '<div align="right" style="color:#FF0000;" >';
						var attend = tmp[3];
						if(attend){
							html += 'Attendant';
						}
					html += '</div>';
				html += '</div>';
				html += '<br>';
				data_interestTime.setCell(i, 0, tmp[1]);
				data_interestTime.setCell(i, 1, tmp[0], '<span align="left">Regular Title<div id="gvTooltipData" align="left"> ' + tmp[4] + ' <b> <font size="2" face="arial" color="red"> ' + tmp[1] + ' </font> </b> have <b> <font size="2" face="arial" color="black"> ' + tmp[0] + ' </font> </b> minutes of interest time for: <br> </font> </b> have <font size="2" face="arial" color="black">' + tmp[2] + ' </font> </div></span>');
			}
			if (res.length > 0){
				var chart = new google.visualization.ColumnChart(document.getElementById('longestRTTime_div'));
				chart.draw(data_interestTime, {width: 600, height: 240, title: 'Longest Interest Time Of Tweets',
							hAxis: {title: 'Users', titleTextStyle: {color: 'red'}},
							vAxis: {title: 'Interest Time', titleTextStyle: {color: 'red'}}
							});
				var gvTooltipOptions = "{maxWidth: '400px', position: 'topRight', offsetBottom:-330}";
				gvTooltip("longestRTTime_div", "data_interestTime", chart, gvTooltipOptions); 
			}
			//$('#TopTenLongestRTTime').html(html);
		},
		cache : false
	});
}

var tweetsfromTime;
var isShowTweets = false;
function showTweets(){
	if(isShowTweets)
		return;
	isShowTweets = true;
	_showTweets();
	window.setInterval(_showTweets, 30000);
}

function _showTweets(){
	if(!running)
		return;
	var tmp =  $("#tweetsfromTime").val();
	if(tmp == "" || tmp.length == 0 || eval(tmp) < 1){
		$("#tableTweets").trigger("reloadGrid");
		$('#showTime').html('');
	}else{
		tweetsfromTime = tmp;
		var today = new Date();
		var mins = eval(tweetsfromTime);
		var milli = today.getTime() - (1000 * 60 * mins);
		var d = new Date(milli);
		var year = d.getFullYear();
		var month = d.getMonth() + 1;
		var day = d.getDate();
		var hour = d.getHours();
		var min = d.getMinutes();
		var sec = d.getSeconds();
		var date = '' + year + '-' + month + '-' + day + ' ' + hour + ':' + min + ':' + sec + '';
		var filter = 'filters={"groupOp":"AND","rules":[{"field":"nadwa_name","op":"eq","data":"' + nadwaName + '"},{"field":"created_at","op":"ge","data":"' + date + '"}]}';
		var sidx = 'inside_RT';
		if ($('#sidx').attr('checked')) {
			sidx = 'outside_RT';
		}

		var dist_url = '/handlerTweets/?_search=true&nd=1311161514713&rows=25&page=1&sidx=' + sidx + '&sord=desc&'+ filter +'&searchField=&searchString=&searchOper=&custom_search=&custom_filter=';
		$.ajax({
			url : dist_url,
			success : function(js) {
				autoUpdate = false;
				$('#autoUpdate').attr('value', 'Acvtivate Auto Update');
				$('#showTime').html('Show Tweets Since ' + date);
				js = eval( '(' + js + ')' );
				var mygrid = jQuery('#tableTweets')[0];
				mygrid.addJSONData(js);
			},
			cache : false
		});
		showTopTen();
	}
}
