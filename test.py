import os
print(os.getcwdb())
import matplotlib.pyplot as plt
import numpy as np
'''
#don't think i need this anymore but ill keep it just in case
@app.route('/test', methods=['GET','POST'])
def test():
    if request.method == 'POST':
        if 'file' not in request.files:
            error='no file selected'
            return redirect('index')
        file = request.files['file']
        if file.filename =='':
            error = 'no selected file'
            return redirect('index')
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    return render_template('test.html')
 '''      




x = np.array(['A', 'B', 'V','D'])
y = np.array([3,8,1,10])
plt.barh(x,y)
plt.show()



@app.route('/update_review/<int:review_id>', methods=['GET','POST'])
@login_required
def update_review(review_id):
    db = get_db()
    review = db.execute(''' SELECT * FROM reviews WHERE review_id=?; ''',(review_id,)).fetchone()['review']
    edit_review = review
    form = EditReview()
    if form.validate_on_submit():
        review = form.edit
        return redirect('/')
    return render_template('edit_review.html', form=form, review=review)


@app.route('/delete_review/<int:review_id>')
@login_required
def delete_review(review_id):
    db = get_db()
    db.execute('''DELETE FROM reviews WHERE review_id=? ''',(review_id,))
    db.commit
    return redirect(url_for('user'))