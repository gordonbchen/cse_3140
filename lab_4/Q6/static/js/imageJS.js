function setImages() {
    document.body.style.backgroundImage = "url('static/images/Background/deddog.jpg')"
    document.getElementById("mainHandler").style.backgroundImage = "url('static/images/Blob/msc.jpg')";

    var link = document.createElement('link');
    link.type = 'image/x-icon';
    link.rel = 'shortcut icon';
    link.href = "static/images/Icon/derp.ico";
    document.getElementsByTagName('head')[0].appendChild(link);
} 
setImages();