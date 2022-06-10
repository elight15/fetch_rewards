from flask import Blueprint,request,render_template, flash
from datetime import datetime
import re

pages = Blueprint('pages', __name__)

values, entire_data = [], [],
keys = ["payer", "points", "timestamp"]
spending = 0

'''@pages.route('/', methods=['GET', 'POST'])
def home():
    return render_template("main.html")'''

@pages.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST': 
        payer = request.form.get('payer')
        points = request.form.get('points', type=int, default=0)
        clocked = datetime.now()
        timelock = clocked.strftime("%Y-%m-%dT%H:%M:%SZ")

        if payer == '' and payer != str:
            flash('Payer can not be empty', 'error')
        else:
            values.insert(0, payer)
            values.insert(1, int(points))
            values.insert(2, timelock)
            zip_record = zip(keys, values)
            point_record = dict(zip_record)
            entire_data.append(point_record)
            flash('Record added, every empty "points" entry will result with a 0.', 'success')
    return render_template("main.html")


@pages.route('/added_transactions', methods=['GET', 'POST'])
def add_transaction():
    return render_template("added_transactions.html", data=entire_data)

new_data = entire_data

@pages.route('/spend', methods=['GET', 'POST'])
def spend_points():
    hold, new_data = [], []
    if request.method == 'POST': 
        spending = request.form.get('points', type=int, default=0)
        if spending == '':
            flash('Points can not be empty', 'error')
        else:
            hold.append(subpoints(new_data, spending))
    return render_template("spend.html", data=hold)


@pages.route('/balance', methods=['GET', 'POST'])
def points_balance():
    hold = []
    hold.append(balance(entire_data))
    return render_template("balance.html", bal=hold)

#########################################################################
#Helper Functions
def sumoflist(record):
    total = 0
    for i in range(len(record)):
        total += record[i].get("points")
    return total

def balance(listed):
    ky, nodupli, = [], []
    cur_points = {}
    for i in range(len(listed)):
        ky.append(listed[i].get("payer"))
    [nodupli.append(x) for x in ky if x not in nodupli]
    
    for j in range(len(nodupli)):
        v = 0
        for x in listed:
            if nodupli[j] == x.get("payer"):
                v += x.get("points")
            else:
                v += 0
        cur_points[nodupli[j]] = v
    return cur_points

def subpoints(listing, point):
    spend = point
    less, w = 0, 0
    t, final = [], []
    recordsort = sorted(listing, key=lambda d: d["timestamp"]) 
    availpoints = sumoflist(recordsort)
    if availpoints < spend:
        t = balance(recordsort)
        flash('Note that system will process a zero if input greater than available points.', 'success')
         
    elif spend < 0:
        flash('Note that system will process a zero if input less than 0.', 'success')
    
    else:
        for z in range(len(recordsort)):
            f = recordsort[z]
            w = f.get("points")
            if w > spend:
                less = spend * -1
                w = w - spend
                f["points"] = less
                t.append(f)    
            else:
                less = w * -1
                spend = spend - w
                f["points"] = less
                t.append(f)
                
        final = balance(t)
    return  final