
document.addEventListener('DOMContentLoaded', function () {
    const onClickList = document.querySelectorAll('.onclick-list2');

    onClickList.forEach(function (list) {
        list.addEventListener('click', function (event) {
            const hideList = this.nextElementSibling;

            if (window.getComputedStyle(hideList).display === 'none') {
                hideList.style.display = 'block';
            } else {
                hideList.style.display = 'none';
            }

            event.stopPropagation();
        });
    });

    // Close hide-list when clicking outside of it
    document.addEventListener('click', function (event) {
        onClickList.forEach(function (list) {
            const hideList = list.nextElementSibling;
            hideList.style.display = 'none';
        });
    });
});
