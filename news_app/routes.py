from flask import render_template, flash, redirect, request, url_for
from news_app import app, db, bcrypt
from news_app.models import News, Company, User
from news_app.forms import RegistrationForm, LoginForm, CompanyForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from news_app.scrapper import get_news


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    companies = Company.query.all()
    news = News.query.order_by(
        News.posted_at.desc()).paginate(per_page=20, page=page)
    return render_template('home.html', title='NEWS MATCHER', news=news, companies=companies)


@app.route('/match')
def match():
    companies = Company.query.all()
    latest_news = len(companies)
    page = request.args.get('page', 1, type=int)
    # News are stored by chunks of 10 news per company
    # news = News.query.all()[-10*latest_news:]
    news = News.query.order_by(News.posted_at.desc()).paginate(per_page=20, page=page)
    news_match_by_relevance = []

    # Every news has a relevance and this goes from 1 to 10, so get the
    # news from all companies that share the same relevance
    for i in range(1, 11):
        news_match_by_relevance.append(
            [new for new in news.items if new.relevance == i])
    return render_template('match.html', title='Match', data=news_match_by_relevance, news=news, companies=companies)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Encrypting pw
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if (user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Email or password incorrect', category='danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route('/add_company', methods=['GET', 'POST'])
@login_required
def add_company():
    form = CompanyForm()
    if form.validate_on_submit():
        new_company = Company(name=form.name.data, base_url=form.base_url.data,
                              html_element=form.html_element.data, element_class=form.element_class.data, html_label=form.html_label.data, label_class=form.label_class.data)
        db.session.add(new_company)
        db.session.commit()
        return redirect(url_for('companies'))
    return render_template('add_company.html', title='Add company', form=form)


@app.route('/companies')
def companies():
    companies = Company.query.all()
    return render_template('companies.html', title='Companies', companies=companies)


@app.route('/about', methods=['GET'])
def about():
    return 'About page'


@app.route('/reset_password', methods=['GET', 'POST'])
def request_reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    return render_template('request_reset_password.html', title='Request Reset', form=form)


@app.route('/get_all_news')
@login_required
def get_all_news():
    if current_user.is_authenticated:
        companies = Company.query.all()
        if companies:
            # companies_dict = {}
            for company in companies:
                get_news(company)
                # companies_dict[company.name] = get_news(company)
        return redirect(url_for('home'))
    return redirect(url_for('login'))