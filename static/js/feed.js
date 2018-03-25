var addCommentToPage = function(id) {
    comments = document.getElementById('comment'+id);
    text = document.getElementById('text'+id);
    comments.innerHTML+= "<b>You: </b>"+ text.value + "<br>";
    text.value="";
}
