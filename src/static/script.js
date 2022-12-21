function deleteTask(task_id) {
    var data = {
        id: task_id,
        csrfmiddlewaretoken: csrftoken
    }
    $.ajax({
        url: 'remove-task/',
        type: 'POST',
        data: data,
    }).done(function(response) {
        if (response.status === 'success') {
            $('#'+task_id).remove();
        }
    })
}


function editButton(task_id) {
    var parent = $('#'+task_id)
    var title = parent.children('p')
    var text = title.text().trim();
    title.empty();
    title.addClass('flex-fill');
    title.html(`<input type="text" value="${text}" class="title form-control custom-input">`);
    parent.children('input').hide();
    parent.find('button.first').show();
    parent.find('button.second').hide();
    parent.removeClass('justify-content-between');
    parent.addClass('justify-content-start');
}


function saveTask(task_id) {
    var parent = $('#' + task_id)
    var input = parent.find('input.title')
    var data = {
        id: task_id,
        title: input.val(),
        csrfmiddlewaretoken: csrftoken
    }
    parent.children('p').empty()
    parent.children('p').text(input.val());
    parent.children('input').show();
    parent.find('button.first').hide();
    parent.find('button.second').show();
    parent.children('p').removeClass('flex-fill');
    parent.removeClass('justify-content-start');
    parent.addClass('justify-content-between');
    $.ajax({
        url: 'update-task/',
        type: 'POST',
        data: data
    }).done(function(response) {
        if (response.complete==true) {
            $('#' + task_id). children('p').html(`<s>${response.title}</s>`);
        }
    })
            
}


$('#add-form').submit(function(e) {
    e.preventDefault();
    var data = $(this).serialize();
    $.ajax({
        url: 'add-task/',
        type: 'POST',
        data:data
    }).done(function(response) {
        if (response.status === 'success') {
            var temp = `
                <li id="${response.id}" class="list-group-item d-flex align-items-center justify-content-between mb-3 rounded">
                <input type="checkbox" onclick="taskComp(${response.id})" class="form-check-input" {% if task.completed %}checked{% endif %}>
                <p onclick="taskComp(${response.id})" class="mt-3">${response.title}</p>
                <div>
                <button class="hide first btn btn-primary btn-lg" onclick="saveTask(${response.id})">Save</button>
                <button class="second custom-btn" onclick="editButton(${response.id})"><i class="fas fa-pencil-alt"></i></button>
                <button class="second custom-btn ms-3" onclick="deleteTask(${response.id})"><i class="fas fa-trash-alt"></i></button>
                    </div>
                    </li>
                    `
            $('#task-list').prepend(temp);
        }
    })
    $(this).trigger('reset');
})
        
/*
$('ul').on('click', 'li', function() {
    }).on('click', '#checkbox', function(event) {
            event.stopPropagation();
            if ($(this).checked == true) {
                $('#demo').text($('tt');
            }
    })
*/

        
function taskComp(task_id) {
    var parent = $('#' + task_id)
    var p_tag = parent.children('p');
    var title = p_tag.text()
    var len = p_tag.children().length
    if (p_tag.children('input').length) {
        return;
    }
    if (!len) {
        p_tag.empty();
        p_tag.append(`<s>${title}</s>`);
        parent.children('input').prop('checked', true);
    } else {
        p_tag.remove($('s'));
        p_tag.text(title);
        parent.children('input').prop('checked', false);
    }
    var data = {
        id: task_id,
        complete: len,
        csrfmiddlewaretoken: csrftoken
    }
    $.ajax({
        url: 'complete-task/',
        type: 'POST',
        data: data
    }).done(function(response) {
    })
}

