let icons = ['fas fa-globe-americas','fas fa-globe-europe', 'fas fa-globe-africa', 'fas fa-globe-asia' ]
let count = 0;
export function animateInternetIcon(){
    setTimeout(()=>{
        document.getElementById("InternetIcon").className = icons[count]
        count++;
        count = count%4;
        animateInternetIcon();
    }, 1000)
}