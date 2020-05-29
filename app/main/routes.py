from app import db #, app
from app.main import bp
from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime, timedelta
from werkzeug.urls import url_parse
from app.main.forms import PaperSubmissionForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Paper
from app.main.scraper import Scraper

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    papers = Paper.query.all()
    return render_template('main/index.html', title='website', papers=papers)

@bp.route('/vote')
@login_required
def vote():
    papers = Paper.query.filter_by(voted=False).all()
    return render_template('main/vote.html', title='Vote', papers=papers)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    points = {'hotpoints': 23, 'sumpoints': 235}
    return render_template('main/user.html', user=user, points=points,
                           subs=user.subs)
        
@bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    form = PaperSubmissionForm()
    if form.validate_on_submit():
        scraper = Scraper()
        scraper.get(form.link.data)
        authors = ", ".join(scraper.authors)
        p = Paper(link=form.link.data, subber=current_user,
                  authors=authors, abstract=scraper.abstract,
                  title=scraper.title)
        db.session.add(p)
        db.session.commit()
        if form.volunteering.data:
            Paper.query.filter_by(
                link=form.link.data).first().volunteer = current_user
            db.session.commit()
        flash('Paper submitted.')
        return redirect(url_for('main.submit'))
    last_month = datetime.today() - timedelta(days = 30)
    papers = Paper.query.filter(Paper.timestamp >= last_month).all()
    return render_template('main/submit.html', papers=papers,
                           title='Submit Paper', form=form)

@bp.route('/submit_m', methods=['GET', 'POST'])
@login_required
def submit_m():
    pass
