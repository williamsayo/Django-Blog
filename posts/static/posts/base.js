// document.getElementById("search-menu").addEventListener("click", SearchDisplay)

function SearchDisplay(){

    if (document.getElementById("search-menu").style.display != 'block'){
        document.getElementById("search-menu").style.display = "block";
    }
    else {
        document.getElementById("search-menu").style.display = "none";
    }
}

function OpenSlideMenu(){
    document.getElementById('menu').style.width='250px';
    document.getElementById('sidebar').style.marginRight='250px';
}

function CloseSlideMenu(){
    document.getElementById('menu').style.width='0';
    document.getElementById('sidebar').style.marginRight='0';
}
