from flask import render_template, flash, redirect, url_for, session, request
from app import app, db
from app.forms import SubmitForm
from analytic_ig import IGTracker
from app.models import IgAccount, IgData

import json
from datetime import datetime


@app.route('/', methods=['GET', 'POST'])
def submit_user():

    form = SubmitForm()
    if form.validate_on_submit():
        verify_user = IgAccount.query.filter_by(username=form.username.data).first()
        if not verify_user:
            new_user = IgAccount(username=form.username.data)
            db.session.add(new_user)
            db.session.commit()
            flash(f'New account added to the database : {form.username.data}')
        return redirect(url_for('results', username=form.username.data))

    return render_template('submit.html', title='Submit Username', form=form)

@app.route('/results/<username>', methods=['GET', 'POST'])
def results(username):

    now_date = datetime.now().date()

    fresh_data = json.loads(IGTracker(username).get_ig_data())
    user_exist = IgData.query.filter_by(ig_account_username=username, update_date=now_date).first()
    if not user_exist:
        new_data = IgData(followers=fresh_data.get('followers'), followings=fresh_data.get('followings'), avg_likes=fresh_data.get('avg_likes'),
                          avg_comments=fresh_data.get('avg_comments'), ig_account_username=username)
        db.session.add(new_data)
        db.session.commit()

    all_data = IgData.query.filter_by(ig_account_username=username).all()
    dates = [d.update_date.strftime('%d/%m/%Y') for d in all_data]

    followers = [(f.followers) for f in all_data]
    avg_likes = [(f.avg_likes) for f in all_data]

    def return_avg_diff(some_list):
        average_diff_list = []
        inverted_list = some_list[::-1]

        for i in range(len(some_list)-1):
            average_diff_list.append(inverted_list[i] - inverted_list[i+1])

        average_diff = sum(average_diff_list) / len(average_diff_list)
        return f'{average_diff:+.2f}'


    if len(followers) >= 2:
        oneday_engagement = (avg_likes[-1]/followers[-1]*100) - (avg_likes[-2]/followers[-2]*100)


        stats = {
            'oneday_followers_diff': f'{followers[-1] - followers[-2]:+}',
            'alltime_followers_diff' : return_avg_diff(followers),
            'oneday_avglikes_diff': f'{avg_likes[-1] - avg_likes[-2]:+}',
            'alltime_avglikes_diff': return_avg_diff(avg_likes),
            'oneday_engagement' : f'{oneday_engagement:+.2f} %'
        }
    else:
        stats = {
            'oneday_followers': 0,
            'oneday_avglikes': 0,
            'oneday_engagement': f'0 %'
        }

    return render_template('ig_results.html', title='Your results', fresh_data=fresh_data, dates=dates, followers=followers, avg_likes=avg_likes, username=username, stats=stats)