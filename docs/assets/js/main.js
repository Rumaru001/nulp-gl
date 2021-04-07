let lorem = `Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.`
 // style="height: ' + height + 'px"
function makeNote(number) {
  // var height = parseInt(100 + Math.random() * 500, 10);
  let size = Math.floor(Math.random() * parseInt(lorem.length));
  let text = lorem.slice(size, lorem.length);
  console.log(text);
  let note = '' +
  '<div class="note">' +
    '<div class="inner">' +
        '<div class="title">Title '+ number +'</div>' +
        '<div class="text">'+ text +'</div>' +
        '<div class="footer">' +
            '<button><a href="#popup-share"><img src="images/share.svg"></a></button>' +
            '<button><a href="#popup-edit"><img src="images/edit.svg"></a></button>' +
            '<button><a href="#popup-add-tag"><img src="images/tag.svg"></a></button>' +
            '<button><a href="#popup-delete"><img src="images/delete.svg"></a></button>' +
        '</div>' +
    '</div>' + 
  '</div>';
  return note;
};

function generateNotes() {
  let notes = document.querySelector(".notes");
  for(var i = 0; i < 10; ++i){
    let note = makeNote(i);
    notes.insertAdjacentHTML('beforeend', note);
  }
  let iso = new Isotope( notes, {
      itemSelector: '.note',
      layoutMode: 'masonry'
  });
}

generateNotes();
