const express = require('express');
let axios = require('axios');
let cors = require('cors');
const app = express();

app.use(cors());
app.use(express.urlencoded({extended : false}));
app.use(express.json());

let SEC_TOKEN = '';
let PORT = 5000;

app.use('/',(req,res)=>{
	axios.get('http://localhost:5001/chat',{
		params : {
			question : req.body.question,
			sec_token : SEC_TOKEN
		}
	}).then(function(response) {
		if(response.data.includes("CLS")) return res.status(200).send("Sorry I did not understand.");
		return res.status(200).send(response.data);
	}).catch(function(err) {
		console.log(err);
		return res.status(500).json({message : "Internal Server Error"});
	});
});

app.listen(PORT,()=>{
	SEC_TOKEN = process.argv[2];
	console.log("BERT-API-NODE-SCRIPT Initialized");
	console.log("App Listening @ https://localhost:" + PORT);
});
