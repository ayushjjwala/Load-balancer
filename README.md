After installing appium:
1) Open the folder '/opt/node/lib/node_modules/appium/lib'
2) Copy and paste the 'hub_client.js' in the above folder.
3) Open the file 'appium.js' present the same folder
4) Add the following at line number 16 :- 

	, hub_client = require('./hub_client.js').Request; //imports the Request module from hub_client.js 


5) Look for the class "timeoutWaitingForCommand" and add the following lines at the start:-
	
	var a = hub_client(this.device.adb.curDeviceId);"
	console.log(a);
