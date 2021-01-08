var express = require('express');
var router = express.Router();
const get_data = require("./my_modules/get_data")
const toshow = require('./toshow')
/*
router.get('/', ensureAuthenticated, function(req, res){
	//这里面的data应该从配置文件里面读取的
	alg_data = [
								{url:'/knn',name:'k-近邻算法'},
								{url:'/svm',name:'支持向量机'},
								{url:'/c4_5',name:'C4.5算法'},
								{url:'/cart',name:'CART算法'},
								{url:'/adaboost',name:'AdaBoost'},
								{url:'/xgboost',name:'xgBoost'},
								{url:'/gbdt',name:'GBDT'},
								{url:'/rnd_forest',name:'随机森林'},
								{url:'/net',name:'人工神经网络'},
								{url:'/lg',name:'logistic回归'},
								{url:'/k_mean',name:'k-均值'},
								{url:'/line_reg',name:'线性回归'},
							]
	console.log(req.query);
	res.render('index',{layout:"layout-blank",data:alg_data});
});
*/

// Get Homepage
router.get('/', ensureAuthenticated, function(req, res){
		get_data.get_result_data(req.query.al,req.query.page,function(result_data){
		result_data.shift()
		head = ["源文件编号","性别","院系","年级","躯体化","强迫症状","人际敏感","抑郁","焦虑","敌对","恐怖","偏执","精神病性","其他","总均分","阳性项目均分","大于2.5因子个数","抑郁指数","幸福感总分","自尊总分","自杀意向新","预测自杀意向"]
		res.render('result_list',{
																head:head,
																flights_data:result_data,
																layout:"layout-blank",
																data:toshow.alg_data
															});
	})
});



function ensureAuthenticated(req, res, next){
	if(req.isAuthenticated()){
		return next();
	} else {
		req.flash('error_msg','You are not logged in');
		res.redirect('/users/login');
	}
}

module.exports = router;
