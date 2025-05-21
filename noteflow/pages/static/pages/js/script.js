// Утилита для отправки запросов
async function makeRequest(url, method, data = {}) {
    try {
        const response = await fetch(url, {
            method,
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error('Ошибка при запросе');
        }

        return await response.json();
    } catch (error) {
        showErrorNotification(error.message);
        throw error; // Бросаем ошибку, чтобы ее можно было обработать в вызывающем коде
    }
}


// Централизованная обработка ошибок
function showErrorNotification(message) {
    alert(message);
}


// Сохранение заметки
async function saveNote() {

    const text = noteInput.value.trim();

    if (!text) {

        showErrorNotification('Введите текст заметки');

        return;
    }

    const data = await makeRequest(urls.create, 'POST', { text });

    if (data.status === 'success') {

        notesList.prepend(createNoteElement(data.note));
        noteInput.value = ''; // Очищаем поле ввода
        showNotification('success', 'Заметка успешно создана');

    }
}


// Редактирование заметки
async function editNote(noteId, newText) {
    const data = await makeRequest(urls.edit(noteId), 'POST', { text: newText });

    if (data.status === 'success') {a

        const noteItem = notesList.querySelector(`[data-id='${noteId}']`);
        noteItem.querySelector('.note-text').textContent = newText;
        showNotification('success', 'Заметка обновлена');

    } else {
        showErrorNotification(data.message || 'Ошибка при обновлении заметки');
    }
}

// Удаление заметки
async function deleteNote(noteId) {

    const data = await makeRequest(urls.delete(noteId), 'POST');

    if (data.status === 'success') {

        const noteItem = notesList.querySelector(`[data-id='${noteId}']`);
        noteItem.remove();
        showNotification('success', 'Заметка удалена');

    } else {
        showErrorNotification(data.message || 'Ошибка при удалении заметки');
    }
}

// Слушатели событий
saveBtn.addEventListener('click', saveNote);

notesList.addEventListener('click', async (event) => {

    const target = event.target;
    const noteItem = target.closest('.note-item');

    if (!noteItem) return;

    const noteId = noteItem.dataset.id;
    const noteTextElement = noteItem.querySelector('.note-text');

    // Редактирование
    if (target.classList.contains('edit-btn')) {

        const newText = prompt('Редактировать заметку:', noteTextElement.textContent);

        if (newText) {
            await editNote(noteId, newText);
        }
    }

    // Удаление
    if (target.classList.contains('delete-btn')) {

        if (confirm('Вы уверены, что хотите удалить эту заметку?')) {
            await deleteNote(noteId);
        }
    }
});