window.onscroll = function() {myfunction()}
        
function myfunction() {
    if ( document.body.scrollTop > 130 || document.documentElement.scrollTop > 130 ){
        document.getElementById('navbar-id').style.background='rgba(0,0,50,0.3)';
        document.getElementById('navbar-id').style.position='sticky';
    
    }
    else{
        document.getElementById('navbar-id').style.background='initial';
        document.getElementById('navbar-id').style.position='initial';
    }
}
