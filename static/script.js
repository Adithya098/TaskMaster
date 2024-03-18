
function addTask(e) {
    e.preventDefault();

    const name = document.getElementById('name').value;
    const description = document.getElementById('description').value;
    const priority = document.getElementById('priority').value;
    const deadline = document.getElementById('deadline').value;

    fetch('/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, description, priority, deadline, progress: "To Do" }),
    })
    .then(handleResponse)
    .then(displayTasks)
    .catch(handleError);

    // Clear the form fields
    document.getElementById('name').value = '';
    document.getElementById('description').value = '';
    document.getElementById('priority').value = '';
    document.getElementById('deadline').value = '';
}

function handleResponse(response) {
    if (!response.ok && response.status === 409) {
        return response.json().then(json => Promise.reject(json));
    }
    return response.json();
}

function handleError(error) {
    console.error('Error:', error);
    alert(error.message || 'Failed to add task. Please try again.');
}


window.updateTask = (id) => {
    const taskRow = document.querySelector(`#task-row-${id}`);
    if (!taskRow) {
        console.error('Task row not found');
        return;
    }

    // Assume that the original values are stored in the data attributes of the row
    const originalName = taskRow.getAttribute('data-name');
    const originalDescription = taskRow.getAttribute('data-description');
    const originalDeadline = taskRow.getAttribute('data-deadline');
    const originalProgress = taskRow.getAttribute('data-progress');
    const originalPriority=taskRow.getAttribute('data-priority')
    // Create a select element for the progress
    const progressSelect = document.createElement('select');
    ["To Do", "In-Progress", "Completed"].forEach(state => {
        const option = document.createElement('option');
        option.value = state;
        option.text = state;
        option.selected = originalProgress === state;
        progressSelect.appendChild(option);
    });
    progressSelect.innerHTML = getUpdatedSelectInnerHTML(progressSelect);

    // Create a select element for the progress
    const prioritySelect = document.createElement('select');
    ["low", "medium", "high"].forEach(state => {
        const option = document.createElement('option');
        option.value = state;
        option.text = state;
        option.selected = originalPriority === state;
        prioritySelect.appendChild(option);
    });
    prioritySelect.innerHTML = getUpdatedSelectInnerHTML(prioritySelect);

    // Update the innerHTML of the row to include input fields for editing
    taskRow.innerHTML = `
        <td><p>${id}</p> </td>
        <td><input type="text" value="${originalName}" data-original-value="${originalName}"></td>
        <td><textarea data-original-value="${originalDescription}">${originalDescription}</textarea></td>
        <td>${prioritySelect.outerHTML}</td>
        <td><input type="date" value="${originalDeadline}" data-original-value="${originalDeadline}"></td>
        <td>${progressSelect.outerHTML}</td>
        <td>
            <button type="button" class="btn rounded-2 updateButton" onclick="saveUpdatedTask(${id})">Save</button>
            <button type="button" class="btn rounded-2" onclick="cancelUpdateTask(${id},
                '${originalName}',
                '${originalDescription}',
                '${originalPriority}',
                '${originalDeadline}',
                '${originalProgress}')">Cancel</button>
        </td>
    `;
};

function getUpdatedSelectInnerHTML(selectElement) {
    let innerHTML = `<select>`;
    
    for (let option of selectElement.options) {
        const selectedAttr = option.selected ? ' selected' : '';
        innerHTML += `<option value="${option.value}"${selectedAttr}>${option.text}</option>`;
    }
    
    innerHTML += '</select>';
    return innerHTML;
}


window.saveUpdatedTask = (id) => {
    const taskRow = document.querySelector(`#task-row-${id}`);
    if (!taskRow) {
        console.error('Task row not found');
        return;
    }

    const inputs = taskRow.querySelectorAll('input');
    const textarea = taskRow.querySelector('textarea');
    const selects = taskRow.querySelectorAll('select');

    const updatedName = inputs[0].value;
    const updatedPriority = selects[0].value;
    const updatedDeadline = inputs[1].value;
    const updatedDescription = textarea.value;
    const updatedProgress = selects[1].value;

    fetch(`/tasks/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: updatedName,
            description: updatedDescription,
            priority: updatedPriority,
            deadline: updatedDeadline,
            progress: updatedProgress
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Update Success:', data);
        displayTasks(); // Refresh the task list
    })
    .catch((error) => {
        console.error('Update Error:', error);
    });
};


window.cancelUpdateTask = (id, originalName, originalDescription, originalPriority, originalDeadline, originalProgress) => {
    const taskRow = document.querySelector(`#task-row-${id}`);
    if (!taskRow) {
        console.error('Task row not found');
        return;
    }
    
    // Restore the original HTML using the original values
    taskRow.innerHTML = `
        <td>${id}</td>
        <td>${originalName}</td>
        <td>${originalDescription}</td>
        <td>${originalPriority}</td>
        <td>${originalDeadline}</td>
        <td>${originalProgress}</td>
        <td>
            <button type="button" class="btn btn-primary rounded-2" onclick="updateTask(${id})">Update</button>
            <button type="button" class="btn btn-danger rounded-2" onclick="deleteTask(${id})">Delete</button>
        </td>
    `;
};



window.deleteTask = (id) => {
    if (!confirm("Are you sure you want to delete this task?")) return;

    fetch(`/tasks/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        console.log('Delete Success:', data);
        displayTasks(); // Refresh the task list
    })
    .catch((error) => {
        console.error('Delete Error:', error);
    });
};

function displayTasks() {
    fetch('/tasks')
    .then(response => response.json())
    .then(tasks => {
        var tableEle = document.getElementsByClassName('taskTable')[0];
        var noTaskEle = document.getElementsByClassName('noTaskMsg')[0];
        if (tasks.length > 0) {
            tableEle.setAttribute('style', 'display: block;margin-top: 6em !important;');
            noTaskEle.setAttribute('style', 'display: none;');
        } else {
            tableEle.setAttribute('style', 'display: none;');
            noTaskEle.setAttribute('style', 'display: block;');
        }
        const taskTableBody = document.getElementById('taskTableBody');
        taskTableBody.innerHTML = ''; // Clear the task list
        tasks.forEach(task => {
            const row = taskTableBody.insertRow(); // Assumes taskTableBody is already defined
            row.setAttribute("id", "task-row-" + task.id);

            row.setAttribute('data-name', task.name);
            row.setAttribute('data-description', task.description);
            row.setAttribute('data-priority', task.priority);
            row.setAttribute('data-deadline', task.deadline);
            row.setAttribute('data-progress', task.progress);
            // Insert cells for each piece of task information
            const idCell = row.insertCell();
            const nameCell = row.insertCell();
            const descriptionCell = row.insertCell();
            const priorityCell = row.insertCell();
            const deadlineCell = row.insertCell();
            const progressCell = row.insertCell();
            const actionsCell = row.insertCell(); // Cell for buttons
        
            // Assign text content for each cell
            idCell.textContent = task.id;
            nameCell.textContent = task.name;
            descriptionCell.textContent = task.description;
            priorityCell.textContent = task.priority;
            deadlineCell.textContent = task.deadline;
            progressCell.textContent = task.progress;
        
            // Create and append the Update and Delete buttons to the actionsCell
            const updateButton = document.createElement('button');
            updateButton.textContent = 'Update';
            updateButton.setAttribute('onclick', `updateTask(${task.id})`);
            updateButton.setAttribute('type', `button`);
            updateButton.setAttribute('class', `btn btn-primary rounded-2 updateButton`);
            updateButton.setAttribute('onclick', `updateTask(${task.id})`);
        
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.setAttribute('onclick', `deleteTask(${task.id})`);
            deleteButton.setAttribute('type', `button`);
            deleteButton.setAttribute('class', `btn btn-danger rounded-2`);
            deleteButton.setAttribute('onclick', `deleteTask(${task.id})`);
        
            actionsCell.appendChild(updateButton);
            actionsCell.appendChild(deleteButton);
        });        
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('update-button')) {
            const id = e.target.closest('tr').dataset.id; // Assuming there is a data-id attribute on the row
            updateTask(id);
        } else if (e.target.classList.contains('delete-button')) {
            const id = e.target.closest('tr').dataset.id;
            deleteTask(id);
        } else if (e.target.classList.contains('save-button')) {
            const id = e.target.closest('tr').dataset.id;
            saveUpdatedTask(id);
        } else if (e.target.classList.contains('cancel-button')) {
            const id = e.target.closest('tr').dataset.id;
            cancelUpdateTask(id);
        }
    });

    // Attach the submit event to the form
    document.getElementById('taskForm').addEventListener('submit', addTask);

    // Display tasks when the page is fully loaded
    displayTasks();
});