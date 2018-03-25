var addCommentToPage = function(id) {
    comments = document.getElementById('comment'+id);
    text = document.getElementById('text'+id);
    comments.innerHTML+= "<b>You: </b>"+ text.value + "<br>";
    text.value="";
}

var app = new Vue({
    el: '#app',
    data: {
        classObject: {
        },
        posts: [
            {
                id: 0,
                cl: "post-wrapper",
                name: "Shaina",
                likes: 0,
                idea: "thing",
                commentlist: [
                    {user: 'comm', message:'idk'},
                    {user: 'comm2', message:'idk as well'}
                ],
                dummy: ''
            },
            {
                id: 1,
                name: "Shakil",
                likes: 0,
                idea: "thing2",
                commentlist: [
                    {user: 'comm3', message:'idk and'},
                    {user: 'comm4', message:'idk or'}
                ],
                dummy: ''
            }
        ],
    },
    methods: {
        addlike: function(user) {
            user.likes+=1;
        },
        addPost: function(content) {
            posts.push({
                name: 'You',
                idea: content,
                likes: 0,
                commentlist: []
            });
        },
        addComment: function(post) {
            post.commentlist.push({user: 'You', message: post.dummy});
            post.dummy = '';
        }
    }
})

