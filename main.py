from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():

    users= [
        {
            'name': "Shaina",
            'likes': 0,
            'id':0,
            'idea': "Ad ea velit deserunt irure esse minim proident ut adipisicing irure ex adipisicing consectetur et ipsum labore deserunt. Est anim enim amet cupidatat ad consequat irure ad do consectetur quis dolor nostrud est qui. Tempor amet sint culpa et culpa duis sint esse laborum duis eiusmod. Esse enim proident enim eu aliquip do ea anim culpa tempor. Qui exercitation quis fugiat enim amet mollit officia ullamco. Est sit cillum tempor sit excepteur irure anim ad occaecat.",
            'commentlist': [
                {'user': 'comm', 'message':'idk'},
                {'user': 'comm2', 'message':'idk as well'}
            ]
        },
        {
            'name': "Shakil",
            'likes': 0,
            'id':1,
            'idea': "thing2",
            'commentlist': [
                {'user': 'comm3', 'message':'idk and'},
                {'user': 'comm4', 'message':'idk or'}
            ]
        }
    ]
    print users
    return render_template('feed.html', users=users)

@app.route('/network')
def network():
    return render_template('network.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
