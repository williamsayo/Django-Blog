// document.getElementById("user-menu").addEventListener("click", OpenUserMenu())

function OpenUserMenu(){

    if (document.getElementById("user-menu").style.display != 'block'){
        document.getElementById("user-menu").style.display = "block";
        document.getElementById("user-icon").style.color = 'red';
    }

    else {
        document.getElementById("user-menu").style.display = "none";
        document.getElementById("user-icon").style.color = 'white';       
    }
}


