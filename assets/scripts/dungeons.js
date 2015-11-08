var x = 1;
var y = 1;
var old_x = 1;
var old_y = 1;
var map = null;
var highlight = null;

var information = [
    {"name":"Wall", "desc":"A wall."},
    {"name":"Room", "desc":"The floor."},
    {"name":"Dungeon Entrance", "desc":"The entrance to the dungeon. Your team will begin their expedition from this point."},
    {"name":"Dungeon Exit", "desc":"The exit to the dungeon! Your team's ultimate goal. Where will it lead?"},
    {"name":"Stairs Up", "desc":"A staircase to the previous level of the dungeon."},
    {"name":"Stairs Down", "desc":"A staircase to the next level of the dungeon."}
];

function rnd(min, max)
{
    return Math.floor(Math.random()*max)+min;
}

//$(document).ready(function(){
$(window).bind("load", function() {
    map = document.getElementById("map").getContext("2d");
    $("#loading").hide();
    $("#map").show();
    draw_map();
    draw_entities();
    
    $("#map").mousemove(function(e){
        x = parseInt((e.pageX - this.offsetLeft) / 24);
        y = parseInt((e.pageY - this.offsetTop) / 24);
        tile_type = tiles[y][x];
        $('#debugCoords').html(x +  " / " + y);
    });
    
    $("#map").click(function(e){
        draw_tile(old_x,old_y);
        if (entity_at(old_x,old_y))
            redraw_entity(old_x,old_y);
        old_x = x;
        old_y = y;
        x = parseInt((e.pageX - this.offsetLeft) / 24);
        y = parseInt((e.pageY - this.offsetTop) / 24);
        tile_type = tiles[y][x]
        //console.log("X / Y / Tile :: " + x + " / " + y + " / " + tile_type);
        // Debug
        get_blocked(x,y);
        
        var has_entity = entity_at(x,y)
        if (has_entity)
        {
            // Use entity message
            $("#info-name").html(entity_info[has_entity]["name"]);
            $("#info-desc").html(entity_info[has_entity]["desc"]);
            $("#info-img").attr("src", "/assets/images/dungeons/details/"+entity_info[has_entity]["image"]+".png");
        }
        else
        {
            $("#info-img").attr("src", "");
            if (tile_type == -1) // Void
            {
                $("#info-name").html(information[0].name);
                $("#info-desc").html(information[0].desc);
            }
            else if (tile_type == 1) // Rooms
            {
                $("#info-name").html(information[tile_type].name);
                //write = "No desc found for ("+x+","+y+")";
                write = "A doorway. The next room is dead ahead.";
                for (var idx = 0; idx < descriptions.length; idx++)
                {
                    if (x >= descriptions[idx]["tl_x"] && x <= descriptions[idx]["br_x"] && y >= descriptions[idx]["tl_y"] && y <= descriptions[idx]["br_y"])
                        write = descriptions[idx]["description"];
                }
                $("#info-img").attr("src", "/assets/images/dungeons/details/floor.png");
                $("#info-desc").html(write);
            }
            else
            {
                // Otherwise default tile message
                $("#info-name").html(information[tile_type].name);
                $("#info-desc").html(information[tile_type].desc);
                
                if (tile_type == 2)
                    $("#info-img").attr("src", "/assets/images/dungeons/details/entrance.png");
                else if (tile_type == 3)
                    $("#info-img").attr("src", "/assets/images/dungeons/details/exit.png");
            }
        }
        
        //console.log("OLD " + old_x + "/" + old_y);
        //draw_tile(old_x,old_y);
        tile = document.getElementById("highlight");
        map.drawImage(tile, x*24,y*24);
    });
});

function draw_map()
{
    offset = 0;
    for (var y = 0; y < 24; y++)
    {
        for (var x = 0; x < 24; x++)
        {
            draw_tile(x,y);
        }
    }
    
    // Draw entities
    for (var idx = 0; idx < entities.length; idx++)
    {
        //console.log(idx + " / " + entities[idx] + " / " + entities[idx]["id"]);
        tile = document.getElementById(entity_info[""+entities[idx]["id"]]["tile"]);
        map.drawImage(tile, entities[idx]["coords"][0]*24, entities[idx]["coords"][1]*24);
    }
    //console.log("Map drawn");
}

function draw_tile(x,y)
{
    //index = (y + x) % 3 + 1;
    if (x % 3 == 0 )
        offset += 1;
    if (y % 3 == 0)
        offset += 2;
    
    index = (offset) % 3 + 1;
    
    switch (tiles[y][x])
    {
        case -1:
            //offset = (x+y) % 4
            //tile = document.getElementById("void"+offset);
            tile = document.getElementById("void");
            break;
        case 0:
            key = get_blocked(x,y);
            tile = document.getElementById(key);
            break;
        case 1:
            tile = document.getElementById("floor");
            break;
        case 2:
            tile = document.getElementById("entrance");
            break;
        case 3:
            tile = document.getElementById("exit");
            break;
        case 4:
            tile = document.getElementById("stairs_up");
            break
        case 5:
            tile = document.getElementById("stairs_down");
            break;
    }
    if (! tile)
        tile = document.getElementById("undefined");
        //tile = document.getElementById("checker");
    
    map.drawImage(tile, x*24,y*24);
}

function get_blocked(x,y)
{
    // NSEW void/wall/floor
    key = "";
    // North
    if (y-1 >= 0)
    {
        if (tiles[y-1][x] == 0 || tiles[y-1][x] > 1)
            key += "w";
        if (tiles[y-1][x] == 1)
            key += "f";
        if (tiles[y-1][x] == -1)
            key += "v";
    }
    else
        key += "v";
        
    // South
    if (y+1 < 24)
    {
        if (tiles[y+1][x] == 0 || tiles[y+1][x] > 1)
            key += "w";
        if (tiles[y+1][x] == 1)
            key += "f";
        if (tiles[y+1][x] == -1)
            key += "v";
    }
    else
        key += "v";
    
    // East
    if (x+1 < 24)
    {
        if (tiles[y][x+1] == 0 || tiles[y][x+1] > 1)
            key += "w";
        if (tiles[y][x+1] == 1)
            key += "f";
        if (tiles[y][x+1] == -1)
            key += "v";
    }
    else
        key += "v";
    
    
    // West
    if (x-1 >= 0)
    {
        if (tiles[y][x-1] == 0 || tiles[y][x-1] > 1)
            key += "w";
        if (tiles[y][x-1] == 1)
            key += "f";
        if (tiles[y][x-1] == -1)
            key += "v";
    }
    else
        key += "v";
        
    var count = (key.match(/w/g) || []).length; // That empty array is neat, in a bizarre way
    if (count >= 3)
    {
        old_key = key;
        key += "-";
        
        // Northeast
        if (y-1 >= 0 && x+1 < 24)
        {
            if (tiles[y-1][x+1] == 0 || tiles[y-1][x+1] > 1)
                key += "x";
            if (tiles[y-1][x+1] == 1)
                key += "f";
            if (tiles[y-1][x+1] == -1)
                key += "x";
        }
        else
            key += "x";
            
        // Southeast
        if (y+1 < 24 && x+1 < 24)
        {
            if (tiles[y+1][x+1] == 0 || tiles[y+1][x+1] > 1)
                key += "x";
            if (tiles[y+1][x+1] == 1)
                key += "f";
            if (tiles[y+1][x+1] == -1)
                key += "x";
        }
        else
            key += "x";
            
        // Southwest
        if (y+1 < 24 && x-1 >= 0)
        {
            if (tiles[y+1][x-1] == 0 || tiles[y+1][x-1] > 1)
                key += "x";
            if (tiles[y+1][x-1] == 1)
                key += "f";
            if (tiles[y+1][x-1] == -1)
                key += "x";
        }
        else
            key += "x";
            
        // Northwest
        if (y-1 >= 0 && x-1 >= 0)
        {
            if (tiles[y-1][x-1] == 0 || tiles[y-1][x-1] > 1)
                key += "x";
            if (tiles[y-1][x-1] == 1)
                key += "f";
            if (tiles[y-1][x-1] == -1)
                key += "x";
        }
        else
            key += "x";
            
        if (! document.getElementById(key))
        {
            //console.log("Falling back from " + key + " to " + old_key);
            //key = old_key;
            console.log("Missing: " + key);
        }
    }
    console.log(x + "/" + y + ":" + key + " -- Tile: " + tiles[y][x]);
    return key;
}

function draw_entities()
{   
    //map.drawImage(tile, x*24,y*24);
}

function entity_at(x,y)
{
    for (var idx = 0; idx < entities.length; idx++)
    {
        if (entities[idx]["coords"][0] == x && entities[idx]["coords"][1] == y)
            return (""+entities[idx]["id"])
    }
    return false
}

function redraw_entity(x,y)
{
    for (var idx = 0; idx < entities.length; idx++)
    {
        if ((entities[idx]["coords"][0] == x) && (entities[idx]["coords"][1] == y))
        {
            tile = document.getElementById(entity_info[""+entities[idx]["id"]]["tile"]);
            map.drawImage(tile, entities[idx]["coords"][0]*24, entities[idx]["coords"][1]*24);
        }
    }
}