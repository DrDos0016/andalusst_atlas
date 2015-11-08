function is_set(id)
{
    var field = $('#'+id);
    var label = $('#'+id).parent();
    if (field.val().trim() != "")
    {
        label.removeClass("error");
        return true;
    }
    label.addClass("error");
    return false;
}

function is_in(id, values)
{
    var field = $('#'+id);
    var label = $('#'+id).parent();
    if (values.indexOf(field.val()) != -1)
    {
        label.removeClass("error");
        return true;
    }
    label.addClass("error");
    return false;
}

function is_date(id)
{
    // No leap year support as it won't be relevant here until 2016
    var field = $('#'+id);
    var label = $('#'+id).parent();
    var regex = /[0-9]{4}-[0-9]{2}-[0-9]{2}/; // YYYY-MM-DD
    var valid = is_regex(id, regex);
    if (valid)
    {
        var today = new Date();
        var split = field.val().split("-");
        var year = split[0]; var month = split[1]; var day = split[2];
        if (year < 2013 || year > today.getFullYear())
            valid = false;
        if (month < 1 || month > 12)
            valid = false;
        if (day < 1)
            valid = false;
        if (month == 2 && day > 28)
            valid = false;
        if (day > 31 || (month == 4 || month == 6 || month == 9 || month == 11) && day > 30)
            valid = false;
        if (valid)
        {
            label.removeClass("error");
            return true;
        }
        label.addClass("error");
    }
    return false;
}

function is_regex(id, regex)
{
    var field = $('#'+id);
    var label = $('#'+id).parent();
    
    if (field.val().match(regex) != null)
    {
        label.removeClass("error");
        return true;
    }
    label.addClass("error");
    return false;
}

function is_fav_me(id)
{
    var field = $('#'+id);
    var label = $('#'+id).parent();
    if (field.val().substr(0,7) == "fav.me/")
        field.val("http://"+field.val());
    if (field.val().substr(0,14) == "http://fav.me/")
    {
        label.removeClass("error");
        return true;
    }
    label.addClass("error");
    return false;
}

function popup(title, text)
{
    return true;
}