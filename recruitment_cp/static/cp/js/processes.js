function collectValues() {
    const language = document.querySelector("input[name='language']:checked").value;

    data = {
        'language': language,
        'hot': JSON.stringify(hot.getSourceData())
    };

    return data
};

function loadData() {
    $.ajax({
        url: loadUrl,
        data: collectValues(),
        dataType: 'json',
        type: 'POST',
        success: function (resp) {
            hot.loadData(JSON.parse(resp));

            try {
                loadSource(modelColumnMap);
            } catch (error) {
                console.info('This table has no dropdown columns!')
            }

            tableConsole.innerText = `${consoleText} : Data loaded...`;
        }
    });
};

function saveData() {
    $.ajax({
        url: saveUrl,
        data: collectValues(),
        dataType: 'json',
        type: 'POST',
        success: function (resp) {
            tableConsole.innerText = `${consoleText} : Data saved...`;
            loadData();
        }
    });
};

async function updateHotDroplist(model, map) {
    try {
        let resp = await $.ajax({
            url: '/cp/load-source',
            data: {...collectValues(), 'model': model},
            dataType: 'json',
            type: 'POST',
        });
        
        let newSource = JSON.parse(resp);
        let settings = hot.getSettings();
        map[model].forEach(id => {
            settings.columns[id].source = newSource;
        });
        hot.updateSettings(settings);
    } catch (error) {
        console.error("An error occurred:", error);
    };
};

async function loadSource(map) {
    for (let model of Object.keys(map)) {
        await updateHotDroplist(model, map);
    };
};

function swal(title, content) {
    Swal.fire({
        title: title,
        html: `
            <div class="content">${content}</div>`,
        showCloseButton: true,
        showConfirmButton: false,
        customClass: {
            container: 'swal',
            icon: 'hidden'
        }
    });
};