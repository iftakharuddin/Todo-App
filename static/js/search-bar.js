
$(document).ready(function(){
    $('#search-bar').on('input', function(){
        var query = $(this).val();
        $.get('/search', {query: query}, function(data) {
            $('#todo-list').empty();
            var htmlData = "";
            data.forEach(function(todo) {
                let html = `
                    <div class="ui segment">
                        <p class="ui big header">${todo.id} | ${todo.title}</p>
                        ${todo.complete === false 
                            ? '<span class="ui gray label">Not Complete</span>' 
                            : '<span class="ui green label">Completed</span>'}
                        <a class="ui blue button" href="/todo/update/${todo.id}">Mark as Complete</a>
                        <a class="ui red button delete-btn" data-id="${ todo.id }">Delete</a>
                        <a class="ui blue button" href="/todo/edit/${todo.id}">Edit</a>
                        <span class="ui green label">Created: ${todo.created_datetime}</span>
                        <span class="ui red label">${todo.priority_level}</span>
                    </div>
                `;
                htmlData += html;
            });
            //$('#todo-list').html(htmlData);
            document.getElementById("todo-list").innerHTML = htmlData;
            console.log(document.querySelectorAll(".delete-btn"));
        });
        
    });
});