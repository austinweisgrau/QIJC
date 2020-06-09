from app import db #, app
from app.main import bp
from flask import (Flask, render_template, request,
                   flash, redirect, url_for)
from datetime import datetime, timedelta
from werkzeug.urls import url_parse
from app.main.forms import (PaperSubmissionForm, ManualSubmissionForm,
                            FullVoteForm)
from flask_login import (current_user, login_user, logout_user,
                         login_required)
from app.models import User, Paper
from app.main.scraper import Scraper

last_month = datetime.today() - timedelta(days = 30)

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    users = User.query.all()
    return render_template('main/index.html', users=users)

@bp.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
    papers_v = (Paper.query.filter(Paper.voted == False)
              .filter(Paper.volunteer_id != None)
              .order_by(Paper.timestamp.desc()).all())
    papers_ = (Paper.query.filter(Paper.voted == False)
               .order_by(Paper.timestamp.desc()).all())
    papers = papers_v + papers_
    list_p = []
    for paper in papers:
        d = {str(paper.id): paper}
        list_p.append(d)
    voteform = FullVoteForm(votes=list_p)
    voteforms = list(zip(papers, voteform.votes))
    print(voteform.votes)
    for i in range(len(voteform.data['votes'])):
        paper = voteforms[i][0]
        data = voteform.data['votes'][i]
        if voteform.data['votes'][i]['vote_num']:
            paper.score_n = data['vote_num']
            paper.score_d = data['vote_den']
            paper.voted = True
            db.session.commit()
            flash('Votes counted.')
    return render_template('main/vote.html', title='Vote', showsub=True,
                           voteform=voteform, voteforms=voteforms)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    subs = (Paper.query.filter_by(subber=user)
            .order_by(Paper.timestamp.desc()))[:10]
    return render_template('main/user.html', user=user,
                           subs=subs, showsub=False)

@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    return render_template('main/search.html')

@bp.route('/history')
@login_required
def history():
    week = request.args.get('week', None)
    if week:
        print(week)
        papers = Paper.query.filter_by(voted = week).all()
        print(len(papers))
        return render_template('main/history.html', papers=papers,
                               showvote=True, showsub=True)
    weeks = [paper.voted for paper
             in Paper.query.group_by(Paper.voted).all()]
    return render_template('main/history.html', weeks=weeks)

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
        link_str = form.link.data.split('?')[0].split('.pdf')[0]
        scraper = Scraper()
        scraper.get(link_str)
        if scraper.failed:
            flash('Scraping failed, submit manually.')
            return redirect(url_for('main.submit_m'))
        if scraper.error:
            flash('Scraping error, check link or submit manually.')
            return redirect(url_for('main.submit'))
        authors = ", ".join(scraper.authors)
        abstract = scraper.abstract
        title = scraper.title
        comment_ = (str(current_user.firstname) + ': '
                    + form.comments.data)
        p = Paper(link=link_str, subber=current_user,
                  authors=authors, abstract=scraper.abstract,
                  title=scraper.title, comment=comment_)
        db.session.add(p)
        db.session.commit()
        if form.volunteering.data:
            Paper.query.filter_by(
                link=link_str).first().volunteer = current_user
            db.session.commit()
        flash('Paper submitted.')
        return redirect(url_for('main.submit'))
    papers = (Paper.query.filter(Paper.timestamp >= last_month)
              .order_by(Paper.timestamp.desc()).all())[:10]
    return render_template('main/submit.html', papers=papers,
                           title='Submit Paper', form=form, showsub=True)

