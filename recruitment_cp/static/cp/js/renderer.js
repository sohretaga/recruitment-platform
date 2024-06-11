function scrollableTextRenderer(instance, td, row, column, prop, value, cellProperties) {
    if (value !== null){
        td.innerHTML = "<div class='largest-content'>" + value + '</div>';
    }
};

function fitTextRenderer(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.renderers.TextRenderer.apply(this, arguments);
  var escaped = Handsontable.helper.stringify(value);
  td.innerHTML = `<div class="fit-text">${escaped}</div>`;
}

function infoIconRenderer(instance, td, row, col, prop, value, cellProperties) {
  let id = instance.getDataAtRowProp(row, 'id');

  td.style.alignItems = 'center';
  td.style.justifyContent = 'space-between';

  if (!td.classList.contains('htMiddle')) {
    td.classList.add('htMiddle');
  }

  td.innerHTML = `<div style="display: flex;"><span>${value || ''}</span> <i class="fas fa-info-circle info-icon"></i></div>`;

  const icon = td.querySelector('.fa-info-circle');
  if (icon && id) {

    td.title = `Click for info`;

    icon.addEventListener('click', function() {
      $.ajax({
          url: '/cp/bmt/load-relevant-data/',
          data: {...collectValues(), 'prop': prop, 'code': value},
          dataType: 'json',
          type: 'POST',
          success: function(resp) {
            swal('', resp.description);
          }
      });
    });
  }else {
    td.title = `Save for info`;
  };

}

function logoRenderer (instance, td, row, col, prop, value, cellProperties) {
  td.innerHTML = `<div style="display: flex; justify-content: space-around;">
              <a href='#'><i class="fa fa-upload fa-lg" style="color: rgb(177, 160, 199); margin: 0;" title="Upload Logo"></i></a>
              <a ${value ? `href='/media/${value}'`: ''} target="_blank"><i class="fa fa-image fa-lg" style="color: rgb(177, 160, 199); margin: 0;" title="View Logo"></i></a>
          </div>`
  return td;
};