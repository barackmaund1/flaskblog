@app.route('/signup', methods=['POST','GET'])
def signup():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,username=form.username.data, email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering, you able to login now','success')
        return redirect(url_for('login'))
    return render_template('admin/signup.html', form=form)



@app.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        next = request.args.get('next')
        return redirect(next or url_for('admin'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash('This user not exists','warning')
            return redirect(url_for('login'))
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully.','success')
            next = request.args.get('next')
            return redirect(next or url_for('admin'))
        flash('Invalid password','danger')
    return render_template('admin/login.html', form=form)