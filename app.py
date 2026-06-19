# app.py
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

# Mock data for demonstration
LOAN_PRODUCTS = {
    'small': {'min': 1000, 'max': 10000, 'interest': 5, 'months': 1},
    'medium': {'min': 10001, 'max': 30000, 'interest': 8, 'months': 3},
    'large': {'min': 30001, 'max': 50000, 'interest': 12, 'months': 6}
}

@app.route('/')
def index():
    """Homepage - Landing page with loan application form"""
    return render_template('index.html')

@app.route('/how-to-borrow')
def how_to_borrow():
    """How to borrow page"""
    return render_template('how_to_borrow.html')

@app.route('/reviews')
def reviews():
    """Customer reviews page"""
    return render_template('reviews.html')

@app.route('/privacy')
def privacy():
    """Privacy policy page"""
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    """Terms and conditions page"""
    return render_template('terms.html')

@app.route('/apply-loan', methods=['POST'])
def apply_loan():
    """Handle loan application submission"""
    try:
        # Get form data
        full_name = request.form.get('full_name')
        phone_number = request.form.get('phone_number')
        id_number = request.form.get('id_number')
        loan_amount = float(request.form.get('loan_amount', 0))
        employment_status = request.form.get('employment_status')
        monthly_income = float(request.form.get('monthly_income', 0))
        
        # Validation
        if not all([full_name, phone_number, id_number, loan_amount]):
            return jsonify({'success': False, 'message': 'Please fill all required fields'})
        
        if loan_amount < 1000 or loan_amount > 50000:
            return jsonify({'success': False, 'message': 'Loan amount must be between KES 1,000 and KES 50,000'})
        
        # Determine loan product
        if loan_amount <= 10000:
            product = LOAN_PRODUCTS['small']
            interest_amount = loan_amount * (product['interest'] / 100)
        elif loan_amount <= 30000:
            product = LOAN_PRODUCTS['medium']
            interest_amount = loan_amount * (product['interest'] / 100)
        else:
            product = LOAN_PRODUCTS['large']
            interest_amount = loan_amount * (product['interest'] / 100)
        
        total_repayment = loan_amount + interest_amount
        
        # Store application in session for demo
        session['current_application'] = {
            'full_name': full_name,
            'phone_number': phone_number,
            'loan_amount': loan_amount,
            'interest_amount': interest_amount,
            'total_repayment': total_repayment,
            'term_months': product['months'],
            'application_id': datetime.now().strftime('%Y%m%d%H%M%S')
        }
        
        return jsonify({
            'success': True,
            'message': 'Application submitted successfully! Decision will be made in 15 minutes.',
            'application_id': session['current_application']['application_id']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/check-status')
def check_status():
    """Check loan application status (mock)"""
    if 'current_application' in session:
        return jsonify({
            'status': 'approved',
            'message': 'Your loan has been approved! Money will be sent to your M-Pesa within 1 minute.',
            'application': session['current_application']
        })
    return jsonify({'status': 'no_application', 'message': 'No active application found'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Simple login for returning customers"""
    if request.method == 'POST':
        phone = request.form.get('phone')
        # In a real app, you'd verify OTP or password
        session['logged_in'] = True
        session['user_phone'] = phone
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Customer dashboard"""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)