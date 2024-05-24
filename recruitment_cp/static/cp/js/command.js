const csrf_token = document.getElementById('csrf-token').value;

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        xhr.setRequestHeader('X-CSRFToken', csrf_token);
        $('body').css('cursor', 'wait');
    },
    complete: function () {
        $('body').css('cursor', 'default');
    },
    error: function () {
        tableConsole.innerText = 'Failure when operation performed...';
    }
});

$$ = function(id) {
    return document.getElementById(id);
};

const tableConsole = $$('bmt-console')
const load = $$('load')
const save = $$('save')
const clear = $$('clear')
const add = $$('add')
const import_data = $$('import_data')
const file = $$('file')
const clearConditions = $$('clear-conditions')

Handsontable.dom.addEvent(load, 'click', function(event) {
    event.preventDefault();
    loadData();
});

Handsontable.dom.addEvent(save, 'click', function(event) {
    event.preventDefault();
    saveData();
});

Handsontable.dom.addEvent(add_row, 'click', function (event) {
    event.preventDefault();
    hot.alter('insert_row', '', 1);
    tableConsole.innerText = `${consoleText} : New row added...`;
});

Handsontable.dom.addEvent(del_row, 'click', function (event) {
    event.preventDefault();
    let lastRow = hot.countRows() - 1;
    let idColumnIndex = 1;
    hot.setDataAtCell(lastRow, idColumnIndex, '');
    saveData();
    tableConsole.innerText = `${consoleText} : Last row deleted...`;
});

Handsontable.dom.addEvent(clearConditions, 'click', function (event) {
    event.preventDefault();
    const filter = hot.getPlugin('Filters');
    for (let i = 0; i < hot.countCols(); i++) {
        filter.removeConditions(i);
    };
    filter.filter();
    tableConsole.innerText = 'EES Calculate ::  All filters have been cleaned!';
});

document.getElementById('data-filter').addEventListener('change', function(event) {
    if (event.target.tagName === 'INPUT') {
        const name = event.target.name;
        const inputs = document.querySelectorAll(`#data-filter input[name='${name}']`);
        inputs.forEach(input => {
            if (input !== event.target) {
                input.checked = false;
            }
        });

        loadData();
    };
});