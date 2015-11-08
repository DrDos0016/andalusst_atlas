function getCookie(name)
{
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
 
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {        
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

function get_app(url, img_loc, txt_loc)
{
    if (url == "" || url == "#")
        return false;
    else if (url.indexOf("fav.me") == -1)
        return false;
    
    var oembed_url = 'http://backend.deviantart.com/oembed?url='+encodeURIComponent(url)+'&format=jsonp&callback=?';
    dat = $.getJSON(oembed_url, function(data) {
        if (data.type == "photo" || data.type == "link")
        {
            if (data.type == "photo")
                img_src = data.url;
            else if (data.type == "link")
                img_src = data.fullsize_url;
            
            $('#'+txt_loc).hide();
            $('#'+img_loc).attr('src', img_src);
            $('#'+img_loc).show();
            var type = "artist";
        }
        else
        {
            $('#'+txt_loc).html("<iframe id='iframe' src='"+url+"'></iframe>");
            $('#iframe').css("height", ($("#team_info").height() - 200));
            $('#'+img_loc).hide();
            $('#'+txt_loc).show();
            var type = "writer";
        }
        
        var author = data.author_url.replace(".deviantart.com", "");
        author = author.replace("http://", "");
        
        have_app({"type":type, "author":author, "url":url});
    });
}

function x(data)
{
    alert("TEST");
}

function get_customization(url)
{
    if (url == "" || url == "#")
    {
        $("#txt_customization").hide();
        $("#img_customization").attr('src', "/assets/images/blank_customization.png");
        $("#img_customization").show();
        return false;
    }
    else if (url.indexOf("fav.me") == -1)
    {
        $("#txt_customization").hide();
        $("#img_customization").attr('src', "/assets/images/blank_customization.png");
        $("#img_customization").show();
        return false;
    }
    
    var oembed_url = 'http://backend.deviantart.com/oembed?url='+encodeURIComponent(url)+'&format=jsonp&callback=?';
    dat = $.getJSON(oembed_url, function(data) {
        if (data.type == "photo")
        {
            img_src = data.url;
            $("#txt_customization").hide();
            $("#img_customization").attr('src', img_src);
            $("#img_customization").show();
        }
        else
        {
            $("#txt_customization").html("<iframe id='iframe' src='"+url+"'></iframe>");
            $("#iframe").css("height", 750);
            $("#img_customization").hide();
            $("#txt_customization").show();
        }
    });
}

function get_item(inventory_id)
{
    data = $.ajax({
        url: "/ajax/get_item",
        data: {"inventory_id":inventory_id},
        type: "POST",
        async: false,
        success: function(data) {
            return data;
        }
    });
    
    return data.responseText;
}

function move_ref(teammate)
{
    species = $("#species"+teammate+" option:selected" ).text();
    $("#move_ref"+teammate).attr("href", "http://veekun.com/dex/pokemon/"+species+"#moves");
    $("#ability_ref"+teammate).attr("href", "http://veekun.com/dex/pokemon/"+species+"#essentials");
}

function remove_params(text)
{
    var output = text.split("?", 2)[0];
    return output;
}