$( document ).ready(function() {

    var deleteBtn = $('.delete-btn');
    var searchBtn = $('#search-btn');
    var searchForm = $('#search-form');
    var logoutForm = $('#logout-form');
    var logoutButton = $('#logout-button');
    var filter = $('#filter');
    
    $(deleteBtn).on('click', function(e) {

        e.preventDefault();

        var delLink = $(this).attr('href');
        var result = confirm('Quer deletar esta tarefa?');

        if(result) {
            window.location.href = delLink;
        }

    });

    $(searchBtn).on('click', function() {
        searchForm.submit();
    });

    $(logoutButton).on('click', function(e) {
        e.preventDefault();
        logoutForm.submit();
    });

    $(filter).change(function(){
        var value = $(this).val();
        window.location.href = `http://localhost:8000/?filter=${value}`;
    })

});