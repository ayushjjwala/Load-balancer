var http = require("http");

var exports = module.exports = {};
hubUrl = "http://localhost:8085/"

exports.Request = function (adbId) {
	this._request = http.request(hubUrl+adbId,function(res){
		res.on('end',function(){
		})
	}).on('error',function(e){
		console.log('Error occured');
	});
	_request.end();
	return ;
}
