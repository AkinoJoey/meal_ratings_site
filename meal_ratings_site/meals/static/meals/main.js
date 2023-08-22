document.addEventListener('DOMContentLoaded', function () {
    const sortSelect = document.getElementById('sort-select');
    
    sortSelect.addEventListener('change', function () {
        const selectedValue = sortSelect.value;
        window.location.href = `?order=${selectedValue}`;
    });


});


