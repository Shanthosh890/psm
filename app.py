from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
import pandas as pd
import mysql.connector
import hashlib
from io import BytesIO
from datetime import datetime, timedelta
# print(pd.__version__)

app = Flask(__name__)
app.secret_key = 'admin@455'  

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="developers",
    password="Develop2022#",
    database="psm"
)

def generate_hashed_password(password):
    salt = b'sha979190' 
    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()
    return hashed_password


def parse_date(date_str):
    date_formats = [
        '%Y-%m-%d', '%d-%m-%Y', '%Y-%d-%m', '%m-%d-%Y',
        '%Y/%m/%d', '%d/%m/%Y', '%Y/%d/%m', '%m/%d/%Y'
    ]
    for date_format in date_formats:
        try:
            return datetime.strptime(date_str, date_format).date()
        except ValueError:
            continue
    return None



def process_excel_data(file_data):
    try:
        df = pd.read_excel(BytesIO(file_data), engine='openpyxl')
        cursor = db.cursor()

        for index, row in df.iterrows():
            try:
                no=row['No.']
                confirmdate = parse_date(str(row['Confirm Date'])) if pd.notnull(row['Confirm Date']) else None
                invoicedate = parse_date(str(row['Invoice Date'])) if pd.notnull(row['Invoice Date']) else None
                deliverydate = parse_date(str(row['Delivery Date'])) if pd.notnull(row['Delivery Date']) else None
                status = row['Status'] if pd.notnull(row['Status']) else None
                invoiceno = row['Invoice No'] if pd.notnull(row['Invoice No']) else None
                registrationname = row['Registration Name'] if pd.notnull(row['Registration Name']) else None
                contactnum1 = str(row['Contact Num1']) if pd.notnull(row['Contact Num1']) else None 
                contactnum2 = str(row['Contact Num2']) if pd.notnull(row['Contact Num2']) else None
                contactnum3 = str(row['Contact Num3']) if pd.notnull(row['Contact Num3']) else None
                model = row['Model'] if pd.notnull(row['Model']) else None
                variant = row['Variant'] if pd.notnull(row['Variant']) else None
                color = row['Color'] if pd.notnull(row['Color']) else None
                hmiinvoiceno = row['HMI Invoice No'] if pd.notnull(row['HMI Invoice No']) else None
                vinnumber = row['Vin Number'] if pd.notnull(row['Vin Number']) else None
                purchasedate = parse_date(str(row['PURCHASE DATE'])) if pd.notnull(row['PURCHASE DATE']) else None
                deliverydate1 = parse_date(str(row['DELIVERY DATE'])) if pd.notnull(row['DELIVERY DATE']) else None
                modeofpay = row['Mode of Purchase'] if pd.notnull(row['Mode of Purchase']) else None
                dsafin = row['DSA/Financier'] if pd.notnull(row['DSA/Financier']) else None
                basicamount = str(row['Basic Amount']).replace(',', '') if pd.notnull(row['Basic Amount']) else None
                invoiceprice = str(row['Invoice Price']).replace(',', '') if pd.notnull(row['Invoice Price']) else None
                otherchargeamount = str(row['Other Charge Amount']).replace(',', '') if pd.notnull(row['Other Charge Amount']) else None
                delaercashdis = str(row['Dealer Cash Discount']).replace(',', '') if pd.notnull(row['Dealer Cash Discount']) else None
                otherdiscount = str(row['Other Discount']).replace(',', '') if pd.notnull(row['Other Discount']) else None
                cgstamount = str(row['CGST Amount']).replace(',', '') if pd.notnull(row['CGST Amount']) else None
                sgstamount = str(row['SGST Amount']).replace(',', '') if pd.notnull(row['SGST Amount']) else None
                igstamount = str(row['IGST Amount']).replace(',', '') if pd.notnull(row['IGST Amount']) else None
                compcessamount = str(row['Comp Cess Amount']).replace(',', '') if pd.notnull(row['Comp Cess Amount']) else None

                # Convert the cleaned string values to integers or floats as needed
                basicamount = int(basicamount) if basicamount is not None else None
                invoiceprice = int(invoiceprice) if invoiceprice is not None else None
                otherchargeamount = int(otherchargeamount) if otherchargeamount is not None else None
                delaercashdis = int(delaercashdis) if delaercashdis is not None else None
                otherdiscount = int(otherdiscount) if otherdiscount is not None else None
                cgstamount = int(cgstamount) if cgstamount is not None else None
                sgstamount = int(sgstamount) if sgstamount is not None else None
                igstamount = int(igstamount) if igstamount is not None else None
                compcessamount = int(compcessamount) if compcessamount is not None else None
                
              
                insuranceinhouse = row['Insurance In house (Y/N)'] if pd.notnull(row['Insurance In house (Y/N)']) else None
                gmname = row['GM NAME'] if pd.notnull(row['GM NAME']) else None
                consultantname = row['Consultant Name'] if pd.notnull(row['Consultant Name']) else None
                address = row['Address'] if pd.notnull(row['Address']) else None
                city = row['City'] if pd.notnull(row['City']) else None
                state = row['State'] if pd.notnull(row['State']) else None
                pinno = row['Pin No.'] if pd.notnull(row['Pin No.']) else None
                age = row['Age'] if pd.notnull(row['Age']) else None
                panno = row['PAN No'] if pd.notnull(row['PAN No']) else None
                customerid = row['CustomerID'] if pd.notnull(row['CustomerID']) else None
                bookingdate = parse_date(str(row['Booking Date'])) if pd.notnull(row['Booking Date']) else None
                cgstp = row['CGST %'] if pd.notnull(row['CGST %']) else None
                sgstp = row['SGST %'] if pd.notnull(row['SGST %']) else None
                igstp = row['IGST %'] if pd.notnull(row['IGST %']) else None
                compcess = row['Comp Cess %'] if pd.notnull(row['Comp Cess %']) else None
                # cgstamount = row['CGST Amount'] if pd.notnull(row['CGST Amount']) else None
                # sgstamount = row['SGST Amount'] if pd.notnull(row['SGST Amount']) else None
                # igstamount = row['IGST Amount'] if pd.notnull(row['IGST Amount']) else None
                # compcessamount = row['Comp Cess Amount'] if pd.notnull(row['Comp Cess Amount']) else None
                customergstno = row['Customer GST No'] if pd.notnull(row['Customer GST No']) else None
                source = row['Source'] if pd.notnull(row['Source']) else None
                subsource = row['Sub-source'] if pd.notnull(row['Sub-source']) else None
                activity = row['Activity'] if pd.notnull(row['Activity']) else None
                location = row['Location'] if pd.notnull(row['Location']) else None
                deliverydateupdatingmethod = row['delivery date updating method'] if pd.notnull(row['delivery date updating method']) else None
                deliveryindays = row['delivery in days'] if pd.notnull(row['delivery in days']) else None
                sheetcreatedby = row['Created By'] if pd.notnull(row['Created By']) else None
                purchaseincgst = row['PURCHASE INCLUDING GST'] if pd.notnull(row['PURCHASE INCLUDING GST']) else None
                purchasecost = row['purchase cost'] if pd.notnull(row['purchase cost']) else None
                margin = row['Margin'] if pd.notnull(row['Margin']) else None
                insurance = row['Insurance'] if pd.notnull(row['Insurance']) else None
                insmargin = row['INS MARGIN'] if pd.notnull(row['INS MARGIN']) else None
                finance = row['Finance'] if pd.notnull(row['Finance']) else None
                finmargin = row['FIN MARGIN'] if pd.notnull(row['FIN MARGIN']) else None
                accs = row['ACCS'] if pd.notnull(row['ACCS']) else None
                accmargin = row['ACC MARGIN'] if pd.notnull(row['ACC MARGIN']) else None
                ewsot = row['EW / SOT'] if pd.notnull(row['EW / SOT']) else None
                incentive = row['INCENTIVE'] if pd.notnull(row['INCENTIVE']) else None
                income = row['INCOME'] if pd.notnull(row['INCOME']) else None
                hyundaioffershare = row['Hyundai offer SHARE'] if pd.notnull(row['Hyundai offer SHARE']) else None
                offerpsmshare = row['OFFER PSM SHARE'] if pd.notnull(row['OFFER PSM SHARE']) else None
                hyundaiofferinsurance = row['Hyundai offer Insurance'] if pd.notnull(row['Hyundai offer Insurance']) else None
                insurancepsmshare = row['INSURANCE PSM SHARE'] if pd.notnull(row['INSURANCE PSM SHARE']) else None
                hyundaiofferexchange = row['Hyundai offer Exchange'] if pd.notnull(row['Hyundai offer Exchange']) else None
                exchangepsmshare = row['EXCHANGE PSM SHARE'] if pd.notnull(row['EXCHANGE PSM SHARE']) else None
                hyundaiofferextwarranty = row['Hyundai Offer Ext Warranty'] if pd.notnull(row['Hyundai Offer Ext Warranty']) else None
                ewpsmshare = row['EW PSM SHARE'] if pd.notnull(row['EW PSM SHARE']) else None
                hyundaiofferrsa = row['Hyundai Offer RSA'] if pd.notnull(row['Hyundai Offer RSA']) else None
                rsapsmshare = row['RSA PSM SHARE'] if pd.notnull(row['RSA PSM SHARE']) else None
                hyundaiofferother = row['Hyundai Offer others'] if pd.notnull(row['Hyundai Offer others']) else None
                otherspsmshare = row['OTHERS PSM SHARE'] if pd.notnull(row['OTHERS PSM SHARE']) else None
                psmextwarrenty = row['Peeyesyem Ext warrenty'] if pd.notnull(row['Peeyesyem Ext warrenty']) else None
                psmoffer = row['PSM OFFER'] if pd.notnull(row['PSM OFFER']) else None
                psmacc = row['PSM ACC'] if pd.notnull(row['PSM ACC']) else None
                deliveryexp = row['DELIVERY EXP'] if pd.notnull(row['DELIVERY EXP']) else None
                incentive1 = row['INCENTIVE 1'] if pd.notnull(row['INCENTIVE 1']) else None
                financecost = row['FINANCE COST'] if pd.notnull(row['FINANCE COST']) else None
                hyundaiofferpoi = row['Hyundai Offer POI'] if pd.notnull(row['Hyundai Offer POI']) else None
                poipsmshare = row['POI PSM SHARE'] if pd.notnull(row['POI PSM SHARE']) else None
                totalexp = row['TOTAL EXP'] if pd.notnull(row['TOTAL EXP']) else None
                netmargin = row['NET MARGIN'] if pd.notnull(row['NET MARGIN']) else None

                crdate = datetime.now().strftime("%Y-%m-%d")
                username = session['username']

                query = "SELECT * FROM psmupload WHERE vinnumber = %s"
                cursor.execute(query, (vinnumber,))
                existing_data = cursor.fetchone()

                if existing_data:
                    update_query = "UPDATE psmupload SET no=%s,confirmdate = %s, invoicedate = %s, deliverydate = %s,status=%s,invoiceno=%s,registrationname=%s,contactnum1=%s,contactnum2=%s,contactnum3=%s,model=%s,variant=%s,color=%s,hmiinvoiceno=%s,purchasedate=%s,deliverydate1=%s,modeofpay=%s,dsafin=%s,basicamount=%s,invoiceprice=%s,otherchargeamount=%s,delaercashdis=%s,otherdiscount=%s,insuranceinhouse=%s,gmname=%s,consultantname=%s,address=%s,city=%s,state=%s,pinno=%s,age=%s,panno=%s,customerid=%s,bookingdate=%s,cgstp=%s,sgstp=%s,igstp=%s,compcess=%s,cgstamount=%s,sgstamount=%s,igstamount=%s,compcessamount=%s,customergstno=%s,source=%s,subsource=%s,activity=%s,location=%s,deliverydateupdatingmethod=%s,deliveryindays=%s,sheetcreatedby=%s,purchaseincgst=%s,purchasecost=%s,margin=%s,insurance=%s,insmargin=%s,finance=%s,finmargin=%s,accs=%s,accmargin=%s,ewsot=%s,incentive=%s,income=%s,hyundaioffershare=%s,offerpsmshare=%s,hyundaiofferinsurance=%s,insurancepsmshare=%s,hyundaiofferexchange=%s,exchangepsmshare=%s,hyundaiofferextwarranty=%s,ewpsmshare=%s,hyundaiofferrsa=%s,rsapsmshare=%s,hyundaiofferother=%s,otherspsmshare=%s,psmextwarrenty=%s,psmoffer=%s,psmacc=%s,deliveryexp=%s,incentive1=%s,financecost=%s,hyundaiofferpoi=%s,poipsmshare=%s,totalexp=%s,netmargin=%s,updatedby=%s,updateddate=%s  WHERE vinnumber = %s"
                    cursor.execute(update_query, (no,confirmdate, invoicedate, deliverydate,status,invoiceno,registrationname,contactnum1,contactnum2,contactnum3,model,variant,color,hmiinvoiceno,purchasedate,deliverydate1,modeofpay,dsafin,basicamount,invoiceprice,otherchargeamount,delaercashdis,otherdiscount,insuranceinhouse,gmname,consultantname,address,city,state,pinno,age,panno,customerid,bookingdate,cgstp,sgstp,igstp,compcess,cgstamount,sgstamount,igstamount,compcessamount,customergstno,source,subsource,activity,location,deliverydateupdatingmethod,deliveryindays,sheetcreatedby,purchaseincgst,purchasecost,margin,insurance,insmargin,finance,finmargin,accs,accmargin,ewsot,incentive,income,hyundaioffershare,offerpsmshare,hyundaiofferinsurance,insurancepsmshare,hyundaiofferexchange,exchangepsmshare,hyundaiofferextwarranty,ewpsmshare,hyundaiofferrsa,rsapsmshare,hyundaiofferother,otherspsmshare,psmextwarrenty,psmoffer,psmacc,deliveryexp,incentive1,financecost,hyundaiofferpoi,poipsmshare,totalexp,netmargin,username,crdate,vinnumber))
                else:
                    insert_query = "INSERT INTO psmupload ( no,confirmdate,invoicedate, deliverydate,status,invoiceno, registrationname,contactnum1, vinnumber,contactnum2,contactnum3,model,variant,color,hmiinvoiceno,purchasedate,deliverydate1,modeofpay,dsafin,basicamount,invoiceprice,otherchargeamount,delaercashdis,otherdiscount,insuranceinhouse,gmname,consultantname,address,city,state,pinno,age,panno,customerid,bookingdate,cgstp,sgstp,igstp,compcess,cgstamount,sgstamount,igstamount,compcessamount,customergstno,source,subsource,activity,location,deliverydateupdatingmethod,deliveryindays,sheetcreatedby,purchaseincgst,purchasecost,margin,insurance,insmargin,finance,finmargin,accs,accmargin,ewsot,incentive,income,hyundaioffershare,offerpsmshare,hyundaiofferinsurance,insurancepsmshare,hyundaiofferexchange,exchangepsmshare,hyundaiofferextwarranty,ewpsmshare,hyundaiofferrsa,rsapsmshare,hyundaiofferother,otherspsmshare,psmextwarrenty,psmoffer,psmacc,deliveryexp,incentive1,financecost,hyundaiofferpoi,poipsmshare,totalexp,netmargin,createdby,createddate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(insert_query, (no,confirmdate, invoicedate, deliverydate,status,invoiceno,registrationname,contactnum1, vinnumber,contactnum2,contactnum3,model,variant,color,hmiinvoiceno,purchasedate,deliverydate1,modeofpay,dsafin,basicamount,invoiceprice,otherchargeamount,delaercashdis,otherdiscount,insuranceinhouse,gmname,consultantname,address,city,state,pinno,age,panno,customerid,bookingdate,cgstp,sgstp,igstp,compcess,cgstamount,sgstamount,igstamount,compcessamount,customergstno,source,subsource,activity,location,deliverydateupdatingmethod,deliveryindays,sheetcreatedby,purchaseincgst,purchasecost,margin,insurance,insmargin,finance,finmargin,accs,accmargin,ewsot,incentive,income,hyundaioffershare,offerpsmshare,hyundaiofferinsurance,insurancepsmshare,hyundaiofferexchange,exchangepsmshare,hyundaiofferextwarranty,ewpsmshare,hyundaiofferrsa,rsapsmshare,hyundaiofferother,otherspsmshare,psmextwarrenty,psmoffer,psmacc,deliveryexp,incentive1,financecost,hyundaiofferpoi,poipsmshare,totalexp,netmargin,username,crdate))
            except Exception as row_error:
                print(f"Error processing row {index}: {row_error}")
                return False

        db.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Error processing Excel data: {e}")
        return False


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['upass']

        cursor = db.cursor(dictionary=True)
        query = "SELECT username, password, uid FROM systemuser WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            hashed_password = generate_hashed_password(password)

            if hashed_password == user['password']:
                session['username'] = user['username']
                session['uid'] = user['uid']
                return redirect(url_for('dashboard'))

        error = 'Invalid credentials. Please try again.'
        return render_template('index.html', error=error)

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username)
    else:
        return redirect(url_for('home'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            
            file = request.files['file']
            
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if file:
                try:
                    file_data = file.read()
                    if process_excel_data(file_data):
                        flash('File data uploaded successfully', 'success')
                    else:
                        flash('Failed to process file data', 'error')
                except Exception as e:
                    print(f"Error reading file: {e}")
                    flash('Failed to read file', 'error')

                return redirect(url_for('upload'))

        return render_template('upload.html', username=username)
    else:
        return redirect(url_for('home'))
    

@app.route('/report')
def report():
    if 'username' in session:
        username = session['username']
       
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT vinnumber FROM psmupload")
        vinnumber_options = cursor.fetchall()
        cursor.close()
        
        cursor1 = db.cursor()
        cursor1.execute("SELECT DISTINCT registrationname FROM psmupload")
        regname_options = cursor1.fetchall()
        cursor1.close()

        cursor2 = db.cursor()
        cursor2.execute("SELECT DISTINCT model FROM psmupload")
        modeloptions = cursor2.fetchall()
        cursor2.close()

        cursor3 = db.cursor()
        cursor3.execute("SELECT DISTINCT gmname FROM psmupload")
        gmnameoptions = cursor3.fetchall()
        cursor3.close()
        
        return render_template('report.html', username=username,vinnumber_options=vinnumber_options,regname_options=regname_options,modeloptions=modeloptions,gmnameoptions=gmnameoptions)
    else:
        return redirect(url_for('home'))

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
   
    vinnumber = request.form.get('vinnumber')
    from_date = request.form.get('from')
    to_date = request.form.get('to')
    registrationname = request.form.get('registrationname')
    model = request.form.get('model')
    gmname = request.form.get('gmname')

   
    sql = "SELECT * FROM psmupload WHERE 1=1 "

    if vinnumber:
        sql += f"AND vinnumber = '{vinnumber}' "
 
    if from_date and to_date:
        sql += f"AND invoicedate BETWEEN '{from_date}' AND '{to_date}' "

    if registrationname:
        sql += f"AND registrationname = '{registrationname}' "

    if model:
        sql += f"AND model = '{model}' "

    if gmname:
        sql += f"AND gmname = '{gmname}' "

    cursor = db.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()

   
    if result:
        return jsonify(result)
    else:
        return jsonify([])  
    

@app.route('/branchwise')
def branchwise():
    if 'username' in session:
        username = session['username']
        return render_template('branchwisereport.html', username=username)
    else:
        return redirect(url_for('home'))


@app.route('/branchwisefetch_data', methods=['POST'])
def branchwisefetch_data():
    from_date = request.form.get('from')
    to_date = request.form.get('to')

    sql = """
        SELECT gmname, COUNT(*) as gmname_count, SUM(purchasecost) as total_purchasecost,SUM(invoiceprice) as total_invoiceprice,SUM(margin) as total_margin,SUM(insmargin) as total_insmargin,SUM(finmargin) as total_finmargin,SUM(accmargin) as total_accmargin,SUM(incentive) as total_incentive,SUM(income) as total_income,SUM(offerpsmshare) as total_offerpsmshare,SUM(psmoffer) as total_psmoffer,SUM(deliveryexp) as total_deliveryexp,SUM(incentive1) as total_incentive1,SUM(totalexp) as total_totalexp,SUM(netmargin) as total_netmargin,SUM(financecost) as total_financecost
        FROM psmupload
        WHERE 1=1
    """

    if from_date and to_date:
        sql += f" AND invoicedate BETWEEN '{from_date}' AND '{to_date}' "

    sql += " GROUP BY gmname"

    cursor = db.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()

    if result:
        return jsonify(result)
    else:
        return jsonify([])


@app.route('/carwise')
def carwise():
    if 'username' in session:
        username = session['username']
        return render_template('carwisereport.html', username=username)
    else:
        return redirect(url_for('home'))


@app.route('/carwisefetch_data', methods=['POST'])
def carwisefetch_data():
    from_date = request.form.get('from')
    to_date = request.form.get('to')

    sql = """
        SELECT model, COUNT(*) as gmname_count, SUM(purchasecost) as total_purchasecost,SUM(invoiceprice) as total_invoiceprice,SUM(margin) as total_margin,SUM(insmargin) as total_insmargin,SUM(finmargin) as total_finmargin,SUM(accmargin) as total_accmargin,SUM(incentive) as total_incentive,SUM(income) as total_income,SUM(offerpsmshare) as total_offerpsmshare,SUM(psmoffer) as total_psmoffer,SUM(deliveryexp) as total_deliveryexp,SUM(incentive1) as total_incentive1,SUM(totalexp) as total_totalexp,SUM(netmargin) as total_netmargin,SUM(financecost) as total_financecost
        FROM psmupload
        WHERE 1=1
    """

    if from_date and to_date:
        sql += f" AND invoicedate BETWEEN '{from_date}' AND '{to_date}' "

    sql += " GROUP BY model"

    cursor = db.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()

    if result:
        return jsonify(result)
    else:
        return jsonify([])
    

@app.route('/carsalesmodel')
def carsalesmodel():
    if 'username' in session:
        username = session['username']
        return render_template('carsalesmodelreport.html', username=username)
    else:
        return redirect(url_for('home'))


@app.route('/carsalesmodelfetch_data', methods=['POST'])
def carsalesmodelfetch_data():
    from_date = request.form.get('from')
    to_date = request.form.get('to')

    sql = """
        SELECT model, gmname, COUNT(*) as gm_count
        FROM psmupload 
        WHERE 1=1 
    """

    if from_date and to_date:
        sql += f" AND invoicedate BETWEEN '{from_date}' AND '{to_date}' "

    sql += " GROUP BY model, gmname"

    cursor = db.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()

    if result:
        return jsonify(result)
    else:
        return jsonify([])


@app.route('/carsalesamount')
def carsalesamount():
    if 'username' in session:
        username = session['username']
        return render_template('carsalesamountreport.html', username=username)
    else:
        return redirect(url_for('home'))


@app.route('/carsalesamountfetch_data', methods=['POST'])
def carsalesamountfetch_data():
    from_date = request.form.get('from')
    to_date = request.form.get('to')

    sql = """
        SELECT model, gmname, SUM(invoiceprice) as total_invoiceprice
        FROM psmupload
        WHERE 1=1
    """

    if from_date and to_date:
        sql += f" AND invoicedate BETWEEN '{from_date}' AND '{to_date}' "

    sql += " GROUP BY model, gmname"

    cursor = db.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()

    if result:
        return jsonify(result)
    else:
        return jsonify([])
    

@app.route('/fetch-monthly-data', methods=['GET'])
def fetch_monthly_data():
    try:
        # Database connection
        connection = mysql.connector.connect(
            host="localhost",
            user="developers",
            password="Develop2022#",
            database="psm"
        )
        cursor = connection.cursor(dictionary=True)

        # Get current year and month
        now = datetime.now()
        start_date = now.replace(day=1).strftime('%Y-%m-%d')
        end_date = (now.replace(day=1, month=now.month + 1) - timedelta(days=1)).strftime('%Y-%m-%d')

        # Query to get distinct gmname values and invoice prices for the current month
        query = """
        SELECT DISTINCT gmname
        FROM psmupload
        """
        cursor.execute(query)
        distinct_gmnames = [row['gmname'] for row in cursor.fetchall()]

        # Query to get data for the current month
        query = """
        SELECT gmname, COALESCE(SUM(invoiceprice), 0) as total_invoiceprice
        FROM psmupload
        WHERE invoicedate BETWEEN %s AND %s
        GROUP BY gmname
        """
        cursor.execute(query, (start_date, end_date))
        result = cursor.fetchall()

        # Format data for chart
        labels = [gmname for gmname in distinct_gmnames]
        data = [next((row['total_invoiceprice'] for row in result if row['gmname'] == gmname), 0) for gmname in distinct_gmnames]

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return jsonify({'labels': labels, 'data': data})

    except mysql.connector.Error as err:
        print("Database error:", err)
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        print("General error:", e)
        return jsonify({'error': 'An error occurred'}), 500


@app.route('/fetch-yearly-data', methods=['GET'])
def fetch_yearly_data():
    try:
        # Database connection
        connection = mysql.connector.connect(
            host="localhost",
            user="developers",
            password="Develop2022#",
            database="psm"
        )
        cursor = connection.cursor(dictionary=True)

        # Get current year
        now = datetime.now()
        year = now.year

        # Query to get data for the current year, grouped by month
        query = """
        SELECT MONTH(invoicedate) as month, SUM(invoiceprice) as total_invoiceprice
        FROM psmupload
        WHERE YEAR(invoicedate) = %s
        GROUP BY MONTH(invoicedate)
        ORDER BY MONTH(invoicedate)
        """
        cursor.execute(query, (year,))
        result = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Debugging: Print the result to check data format
        print("Yearly Query Result:", result)

        # Format data for chart
        labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        data = [0] * 12  # Initialize data array with 12 zeros

        for row in result:
            month = row['month']
            data[month - 1] = row['total_invoiceprice']

        return jsonify({'labels': labels, 'data': data})

    except mysql.connector.Error as err:
        print("Database error:", err)
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        print("General error:", e)
        return jsonify({'error': 'An error occurred'}), 500
    


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
