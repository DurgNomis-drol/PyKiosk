$('#open_page').on('click',function(){
    var url_to_open = $('#url_to_open').val()
    $.ajax({
          url: "/rest/kiosk",
          type: 'POST',
          data: '{"url":"'+url_to_open+'"}',
          dataType: "json",
          contentType: 'application/json',
          headers: {
                "Authorization": "Bearer " + $('#token').val()
          },
    })});

$('#close_page').on('click',function(){
    $.ajax({
          url: "/rest/kiosk",
          type: 'DELETE',
          contentType: 'application/json',
          headers: {
                "Authorization": "Bearer " + $('#token').val()
          },
    })});

$('#reset').on('click',function(){
    $.ajax({
          url: "/rest/kiosk",
          type: 'POST',
          data: '{"url": "", "homepage": "true"}',
          dataType: "json",
          contentType: 'application/json',
          headers: {
                "Authorization": "Bearer " + $('#token').val()
          },
    })});

$('#go_to_homepage').on('click',function(){
    $.ajax({
          url: "/rest/kiosk",
          type: 'POST',
          data: '{"url": "", "homepage": "true"}',
          dataType: "json",
          contentType: 'application/json',
          headers: {
                "Authorization": "Bearer " + $('#token').val()
          },
    })});

$('#reboot').on('click',function(){
    $.ajax({
          url: "/rest/system/reboot",
          type: 'POST',
          contentType: 'application/json',
          headers: {
                "Authorization": "Bearer " + $('#token').val()
          },
    })});

$('#shutdown').on('click',function(){
    $.ajax({
          url: "/rest/system/shutdown",
          type: 'POST',
          contentType: 'application/json',
          headers: {
                "Authorization": "Bearer " + $('#token').val()
          },
    })});

$('#save_config').on('click',function(){
    var new_config = $('#config').val()
    $.ajax({
          url: "/rest/config",
          type: 'POST',
          data: '{"new_config":'+new_config+'}',
          dataType: "json",
          contentType: 'application/json',
          headers: {
                "Authorization": "Bearer " + $('#token').val()
          },
    })});