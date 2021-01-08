var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var exphbs = require('express-handlebars');
var expressValidator = require('express-validator');
var flash = require('connect-flash');
var session = require('express-session');
var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;
var mongo = require('mongodb');
var mongoose = require('mongoose');

mongoose.connect('mongodb://10.2.3.195/loginapp');
var db = mongoose.connection;

var routes = require('./routes/index');
var users = require('./routes/users');
var classfy = require('./routes/classfy');
var gene_classfy = require('./routes/gene_classfy');
var knn = require('./routes/knn')
var GCN = require('./routes/GCN')
var asd = require('./routes/asd')
var gene_clf = require('./routes/gene_clf')
var gene_csv = require('./routes/gene_csv')
var net = require('./routes/net')
var svm = require('./routes/svm')
var svm_clf = require('./routes/svm_clf')
var DT_clf = require('./routes/DT_clf')
var DT = require('./routes/DT')
var RF = require('./routes/RF')
var RF_clf = require('./routes/RF_clf')
var xgboost_clf = require('./routes/xgboost_clf')
var stacking_clf = require('./routes/stacking_clf')
var c4_5 = require('./routes/c4_5')
var cart = require('./routes/cart')
var adaboost = require('./routes/adaboost')
var xgboost = require('./routes/xgboost')
var stacking = require('./routes/stacking')
var gbdt = require('./routes/gbdt')
var rnd_forest = require('./routes/rnd_forest')
var lg = require('./routes/lg')
var k_mean = require('./routes/k_mean')
var get_run_output_api = require('./routes/api/get_run_output_api')
var get_complete_rate_api = require('./routes/api/get_complete_rate_api')
var control_api = require('./routes/api/control_api')
var setting = require('./routes/setting')
var compare = require('./routes/compare')
var get_result = require('./routes/get_result')

// Init App
var app = express();

// View Engine
app.set('views', path.join(__dirname, 'views'));
app.engine('handlebars', exphbs({}));
app.set('view engine', 'handlebars');

// BodyParser Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());

// Set Static Folder
app.use(express.static(path.join(__dirname, 'public')));

// Express Session
app.use(session({
    secret: 'jintianxingqiji',
    saveUninitialized: true,
    resave: true
}));

// Passport init
app.use(passport.initialize());
app.use(passport.session());

// Express Validator
app.use(expressValidator({
  errorFormatter: function(param, msg, value) {
      var namespace = param.split('.')
      , root    = namespace.shift()
      , formParam = root;

    while(namespace.length) {
      formParam += '[' + namespace.shift() + ']';
    }
    return {
      param : formParam,
      msg   : msg,
      value : value
    };
  }
}));

// Connect Flash
app.use(flash());

// Global Vars
app.use(function (req, res, next) {
  res.locals.success_msg = req.flash('success_msg');
  res.locals.error_msg = req.flash('error_msg');
  res.locals.error = req.flash('error');
  res.locals.user = req.user || null;
  next();
});



app.use('/', routes);
app.use('/users', users);
app.use('/knn', knn)
app.use('/classfy', classfy)
app.use('/gene_classfy',gene_classfy)
app.use('/GCN', GCN)
app.use('/gene_csv', gene_csv)
app.use('/asd', asd)
app.use('/gene_clf', gene_clf)
app.use('/svm', svm)
app.use('/svm_clf', svm_clf)
app.use('/DT_clf', DT_clf)
app.use('/RF_clf', RF_clf)
app.use('/xgboost_clf', xgboost_clf)
app.use('/stacking_clf', stacking_clf)
app.use('/DT', DT)
app.use('/RF', RF)
app.use('/c4_5', c4_5)
app.use('/cart', cart)
app.use('/adaboost', adaboost)
app.use('/xgboost', xgboost)
app.use('/stacking', stacking)
app.use('/gbdt', gbdt)
app.use('/rnd_forest', rnd_forest)
app.use('/lg', lg)
app.use('/net', net)
app.use('/k_mean', k_mean)

app.use('/get_run_output_api',get_run_output_api)
app.use('/get_complete_rate_api',get_complete_rate_api)
app.use('/control_api',control_api)
app.use('/setting',setting)
app.use('/compare',compare)
app.use('/get_result',get_result)
app.get('/404', function(req, res, next){
  // trigger a 404 since no other middleware
  // will match /404 after this one, and we're not
  // responding here
  next();
});

app.use(function(req, res, next){
  res.status(404);

  if (req.accepts('html')) {
    res.render('404', { url: req.url });
    return;
  }

  if (req.accepts('json')) {
    res.send({ error: 'Not found' });
    return;
  }

  res.type('txt').send('Not found');
});

// Set Port
app.set('port', (process.env.PORT || 3001));

app.listen(app.get('port'), function(){
	console.log('Server started on port '+app.get('port'));
});
