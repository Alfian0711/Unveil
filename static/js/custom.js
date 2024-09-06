// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();


// isotope js
$(window).on('load', function () {
    $('.filters_menu li').click(function () {
        $('.filters_menu li').removeClass('active');
        $(this).addClass('active');

        var data = $(this).attr('data-filter');
        $grid.isotope({
            filter: data
        })
    });

    var $grid = $(".grid").isotope({
        itemSelector: ".all",
        percentPosition: false,
        masonry: {
            columnWidth: ".all"
        }
    })
});

// nice select
$(document).ready(function() {
    $('select').niceSelect();
  });

/** google_map js **/
function myMap() {
    var mapProp = {
        center: new google.maps.LatLng(40.712775, -74.005973),
        zoom: 18,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}

// client section owl carousel
$(".client_owl-carousel").owlCarousel({
    loop: true,
    margin: 0,
    dots: false,
    nav: true,
    navText: [],
    autoplay: true,
    autoplayHoverPause: true,
    navText: [
        '<i class="fa fa-angle-left" aria-hidden="true"></i>',
        '<i class="fa fa-angle-right" aria-hidden="true"></i>'
    ],
    responsive: {
        0: {
            items: 1
        },
        768: {
            items: 2
        },
        1000: {
            items: 2
        }
    }
});


//  drag n drpp
const dropZone = document.querySelector('.drop-zone');
const fileInput = document.querySelector('#fileInput');
const previewImg = document.querySelector('#previewImg');
const objectToHide = document.querySelector('#objectToHide');

dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
  dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.classList.remove('dragover');
  const files = e.dataTransfer.files;
  fileInput.files = files;

  // Create a URL for the uploaded file
  const file = files[0];
  const reader = new FileReader();
  reader.onload = () => {
    const url = reader.result;
    previewImg.src = url;
  };
  reader.readAsDataURL(file);
});



fileInput.addEventListener('change', () => {
  const files = fileInput.files;
  const file = files[0];
  const reader = new FileReader();
  reader.onload = () => {
    const url = reader.result;
    previewImg.src = url;
    objectToHide.style.display = 'none'; // hide the object
  };
  reader.readAsDataURL(file);
  
});
// Menyembunyikan elemen preview
document.querySelectorAll('div').forEach(function(element) {
    if (element.innerText.includes('Preview')) {
        element.style.display = 'none';
    }
});

