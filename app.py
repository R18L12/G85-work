from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///letters.db'
db = SQLAlchemy(app)

# Database Model
class Letter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    recipient = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

# Home page (View all letters)
@app.route('/')
def index():
    query = request.args.get('q')
    if query:
        letters = Letter.query.filter(
            (Letter.sender.like(f"%{query}%")) |
            (Letter.recipient.like(f"%{query}%"))
        ).all()
    else:
        letters = Letter.query.all()
    return render_template('index.html', letters=letters)


# Add new letter
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_letter = Letter(
            sender=request.form['sender'],
            recipient=request.form['recipient'],
            subject=request.form['subject'],
            content=request.form['content']
        )
        db.session.add(new_letter)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

# Edit letter
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    letter = Letter.query.get_or_404(id)
    if request.method == 'POST':
        letter.sender = request.form['sender']
        letter.recipient = request.form['recipient']
        letter.subject = request.form['subject']
        letter.content = request.form['content']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', letter=letter)

# Delete letter
@app.route('/delete/<int:id>')
def delete(id):
    letter = Letter.query.get_or_404(id)
    db.session.delete(letter)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

