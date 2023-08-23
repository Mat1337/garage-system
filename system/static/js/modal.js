// get the modal
var modal = document.getElementById("user_add_modal");

// when the user add button is clicked open the modal
document.getElementById("user_add_btn").onclick = () => {
    modal.style.display = 'flex';
}

// when the user clicks anywhere outside the modal, close it
window.onclick = function(event) {
  if (event.target === modal) {
    modal.style.display = "none";
  }
}