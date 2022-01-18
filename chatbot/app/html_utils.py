def build_html_chat(is_me, text, time):
  me_avatar = "static/avatar_user.png";
  bot_avatar = "static/avatar_bot.png";
  
  if is_me:
      html_message = (
        '<li style="width:100%">' +
            '<div class="msj macro">' +
                '<div class="avatar">'
                  '<img class="img-circle" style="width:100%;" src="'+ me_avatar +'" />' + 
                '</div>' +
                '<div class="text text-l">' +
                    '<p>'+ text +'</p>' +
                    '<p><small>'+ time +'</small></p>' +
                '</div>' +
            '</div>' +
        '</li>'
      )
    
  else:
      html_message = (
        '<li style="width:100%;">' +
            '<div class="msj-rta macro">' +
                '<div class="text text-r">' +
                    '<p>'+ text +'</p>' +
                    '<p><small>'+ time +'</small></p>' +
                '</div>' +
                '<div class="avatar" style="padding:0px 0px 0px 10px !important">' +
                  '<img class="img-circle" style="width:100%;" src="'+ bot_avatar +'" />' +
                '</div>' +   
            '</div>' +
        '</li>'
      )
  
  return html_message