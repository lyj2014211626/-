from flask import Flask
from flask import request,jsonify
import pandas as pd
import numpy as np 
import xlrd
import pickle
from flask_cors import *

app=Flask(__name__)

CORS(app, resources=r'/*')
@app.route('/classfy',methods=['GET','POST'])

def get_file():
	try:
		f = request.files.get('myfile')
		
		if f is None:
			resp = jsonify({'a':'b'})
			resp.status_code = 500
			return resp
		df = pd.read_excel(f)
		model = request.form.get("model", type = str)
		
		if model == "SVM":
			get_pre_res(model,df)
			re = "SVM"
		elif model == "DT":
			get_pre_res(model,df)
			re = "DT"
		elif model == "RF":
			get_pre_res(model,df)
			re = ""
		elif model == "xgboost":
			get_pre_res(model,df)
			re = " "
		elif model == "stacking":
			get_pre_res(model,df)
			re = " "
	except Exception as e:
		print(str(e))
		re = 'error'
	return jsonify({'result': re})

@app.route('/gene_csv',methods=['GET','POST'])
def gene_visual():
	try:
	
		path = request.form.get("path", type = str)
		sick = request.form.get("sick",type=str)
		print(path)
		re=sick;
	except Exception as e:
		print(str(e))
		re = 'error'
	return jsonify({'result': re})

@app.route('/gene_classfy',methods=['GET','POST'])
def gene_classify():
	try:
		f = request.files.get('myfile')
		print(f.filename)
		if f is None:
			resp = jsonify({'a':'b'})
			resp.status_code = 500
			return resp
		df = pd.read_excel(f)
		model = request.form.get("model", type = str)
		sick = request.form.get("sick",type=str)
		print(model)
		re=''
		if model == "HANE":
			filename=model+'_'+sick
			print(filename)
			df_pre=pd.read_excel(filename+'.xlsx')
			df_res=pd.merge(df,df_pre)
			df_res.to_csv('../frontend/data/'+filename+'.csv',sep='#')	
			re = "SVM"
		elif model == "HAN":
			filename=model+'_'+sick
			print(filename)
			df_pre=pd.read_excel(filename+'.xlsx')
			df_res=pd.merge(df,df_pre)
			df_res.to_csv('../frontend/data/'+filename+'.csv',sep='#')
			re = "DT"
		elif model == "GAT":
			filename=model+'_'+sick
			print(filename)
			df_pre=pd.read_excel(filename+'.xlsx')
			df_res=pd.merge(df,df_pre)
			df_res.to_csv('../frontend/data/'+filename+'.csv',sep='#')
			re = ""
		elif model == "GCN":
			filename=model+'_'+sick
			print(filename)
			df_pre=pd.read_excel(filename+'.xlsx')
			df_res=pd.merge(df,df_pre)
			df_res.to_csv('../frontend/data/'+filename+'.csv',sep='#')
			re = " "
		elif model == "Metapath2Vec":
			filename=model+'_'+sick
			print(filename)
			df_pre=pd.read_excel(filename+'.xlsx')
			df_res=pd.merge(df,df_pre)
			df_res.to_csv('../frontend/data/'+filename+'.csv',sep='#')
			re = " "
	except Exception as e:
		print(str(e))
		re = 'error'
	return jsonify({'result': re})	
##读取模型，预测结果并返回
def get_pre_res(model,df):
	with open(model+'/'+model+'.pickle', 'rb') as f:
		clf = pickle.load(f)
	with open(model+'/thresholds.pickle', 'rb') as f:
		thresholds = pickle.load(f)
	with open(model+'/feature.pickle', 'rb') as f:
		feature = pickle.load(f)
	x = df[feature.keys()].replace(2,0).values
	pre_proba = clf.predict_proba(x)[:,1]
	df_res = pd.concat([df[['ID']+list(feature.keys())],pd.DataFrame(pre_proba,columns = ['sick_pro'])],axis=1)[pre_proba>=thresholds]
	df_res.to_csv('../frontend/data/'+model+'.csv',index=False, sep='#')

if __name__=='__main__':
	app.debug=True
	app.run()
	app.run(debug =True)