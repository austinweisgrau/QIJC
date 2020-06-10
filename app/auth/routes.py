from app import db #, app
from app.auth import bp
from flask import (Flask, render_template, request, flash,
                   redirect, url_for)
from datetime import datetime, timedelta
from werkzeug.urls import url_parse
from app.auth.forms import (LoginForm, RegistrationForm, InviteUserForm,
                            ManageUserForm)
from flask_login import (current_user, login_user, logout_user,
                         login_required)
from app.models import User, Paper

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user.password_hash == 'waiting':
            flash('Admin has not yet approved account.')
            return redirect(url_for('auth.login'))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            flash('Recover account? <Not yet functional>')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign in', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    firstname=form.firstname.data,
                    lastname=form.lastname.data)
        user.set_password(form.password.data, 1)
        db.session.add(user)
        db.session.commit()
        flash('Successfully registered. Sent to admins for approval.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register',
                           form=form)

@bp.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    manageforms = []
    if not current_user.admin:
        flash('Admin privilege required to manage.')
        return redirect(url_for('main.index'))
    inviteform = InviteUserForm()
    if inviteform.submit.data and inviteform.validate_on_submit():
        user = User(email=inviteform.email.data)
        db.session.add(user)
        db.session.commit()
        flash('Invitation sent.')
        return redirect(url_for('auth.manage'))
    users = (User.query.order_by(User.password_hold.desc())
             .order_by(User.admin.desc()).order_by('firstname').all())
    for user in users:
        user.manage_form = ManageUserForm(user_=user.id)
        manageforms.append(user.manage_form)
    for form in manageforms:
        if form.submit_.data and form.validate_on_submit():
            if (form.action_.data == 'del') or (
                    form.action2_.data == 'del'):
                # Add a confirmation warning.
                # This cannot be undone.
                user = User.query.get(form.user_.data)
                flash('Deleted {}.'.format(user))
                db.session.delete(user)
                db.session.commit()
            elif form.action_.data == 'adm':
                User.query.get(form.user_.data).admin = True
                db.session.commit()
            elif form.action2_.data == 'rma':
                User.query.get(form.user_.data).admin = False
                db.session.commit()
            elif form.approve.data:
                u = User.query.get(form.user_.data)
                u.password_hash = u.password_hold
                u.password_hold = None
                db.session.commit()
                 
            return redirect(url_for('auth.manage'))
    return render_template('auth/manage.html', title='Manage',
                           inviteform=inviteform,
                           manageforms=manageforms, users=users)
