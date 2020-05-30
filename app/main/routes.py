from app import db #, app
from app.main import bp
from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime, timedelta
from werkzeug.urls import url_parse
from app.main.forms import PaperSubmissionForm, ManualSubmissionForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Paper
from app.main.scraper import Scraper

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    users = User.query.all()
    return render_template('main/index.html', users=users)

@bp.route('/vote')
@login_required
def vote():
    papers = Paper.query.filter_by(voted=False).all()
    return render_template('main/vote.html', title='Vote', papers=papers)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('main/user.html', user=user,
                           subs=user.subs, showsub=False)

last_month = datetime.today() - timedelta(days = 30)

@bp.route('/submit_m', methods=['GET', 'POST'])
@login_required
def submit_m():
    form = ManualSubmissionForm()
    if form.validate_on_submit():
        p = Paper(link=form.link.data, subber=current_user,
                  authors=form.authors.data, abstract=form.abstract.data,
                  title=form.title.data, comment=form.comments.data)
        db.session.add(p)
        db.session.commit()
        if form.volunteering.data:
            Paper.query.filter_by(
                link=form.link.data).first().volunteer = current_user
            db.session.commit()
        flash('Paper submitted.')
        return redirect(url_for('main.submit'))
    papers = Paper.query.filter(Paper.timestamp >= last_month).all()
    return render_template('main/submit_m.html', papers=papers,
                           form=form, title='Submit Paper', showsub=True)

@bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    form = PaperSubmissionForm()
    if form.validate_on_submit():
        scraper = Scraper()
        scraper.get(form.link.data)
        if scraper.failed:
            flash('Scraping failed, submit manually.')
            return redirect(url_for('submit_m'))
        if scraper.error:
            flash('Scraping error, check link or submit manually.')
            return redirect(url_for('submit'))
        authors = ", ".join(scraper.authors)
        abstract = scraper.abstract
        title = scraper.title
        p = Paper(link=form.link.data, subber=current_user,
                  authors=authors, abstract=scraper.abstract,
                  title=scraper.title, comment=form.comments.data)
        db.session.add(p)
        db.session.commit()
        if form.volunteering.data:
            Paper.query.filter_by(
                link=form.link.data).first().volunteer = current_user
            db.session.commit()
        flash('Paper submitted.')
        return redirect(url_for('main.submit'))
    papers = Paper.query.filter(Paper.timestamp >= last_month).all()
    return render_template('main/submit.html', papers=papers,
                           title='Submit Paper', form=form, showsub=True)
