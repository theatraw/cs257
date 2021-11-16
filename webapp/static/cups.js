/*
cups.js
Rodrick and Thea
10 November 2021
*/

window.onload = initialize;

function initialize() {

    loadWorldCupCheckBoxes();    

    loadTeamsSelector();

    loadWorldCupsSelector();

    loadPlayersSelector();

    //    loadWorldCupsSelector();
     
    loadPageTitle();

    let team_element = document.getElementById('team_selector');
    if (team_element) {
        team_element.onchange = onTeamsSelectionChanged;
    }

    let wc_element = document.getElementById('world_cup_selector');
    if (wc_element) {
        wc_element.onchange = onWorldCupsSelectionChanged;
    }


    


}

function getAPIBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/api';
    return baseURL;
}

function getBaseURL() {
let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/';
    return baseURL;
}    


function loadWorldCupCheckBoxes() {
    let url = getAPIBaseURL() + '/Allcups/';

    fetch(url, {method: 'get'})

	.then((response) => response.json())

	.then(function(worldcups) {
		let checkBoxesBody = '';
		for (let k = 0; k < worldcups.length; k++) {
		    let worldcup = worldcups[k];
		    world_cup_year = worldcup['wc_year']
		    world_cup_location = worldcup['wc_location']
		    checkBoxesBody += '<input type="checkbox" name="worldcup" id="'
			+world_cup_year + '" value="' + world_cup_year + '">\n'
			+'<label for ="' + world_cup_year + '">' + world_cup_location+' '+world_cup_year
			+ '</label><br>'

		}

		let boxes = document.getElementById('check_boxes_container');
		if (boxes) {
		    boxes.innerHTML = checkBoxesBody;
		}
	    })

        .catch(function(error) {
                console.log(error);
	    });
}

function loadTeamsSelector() {
    let url = getAPIBaseURL() + '/Allcups/teams/';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(teams) {
	    let selectorBody = '';
	    for (let k = 0; k < teams.length; k++) {
		let team = teams[k];
		//going to need to put 'id' as a return of the query, ok for now
		selectorBody += '<option value="' + team['id'] + '">'
                                + team['team_name'] + ' (' + team['team_abbreviation'] +')'
		                + '</option>/n';
	    }
	    let selector = document.getElementById('team_selector');
	    if (selector) {
		selector.innerHTML = selectorBody;
	    }

	})

	.catch(function(error) {
		console.log(error);
	    });
}

function onTeamsSelectionChanged() {
    let teamID = this.value;
    let url = getBaseURL() + 'AllCups/Team?team=' + teamID;
   
    window.location = url;
}

function getParam(param){
    return new URLSearchParams(window.location.search).get(param);
}


function loadPageTitle() {
    if (getParam('team') != '' && getParam('year') == '') {

    let url = getAPIBaseURL() + '/Allcups/teams/';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(teams) {
	    let titleBody = '';
	    for (let k = 0; k < teams.length; k++) {
		let team = teams[k];
		if (team['id'] == getParam('team')){
		titleBody += team['team_name'] + ' - All World Cups';
		}
	    }


	    let title = document.getElementById('page-title');
	    if (title) {
		title.innerHTML = titleBody;
	    }
	})
	
	.catch(function(error) {
		console.log(error);
	    });
}

   if (getParam('team') != '' && getParam('year') != '') {

       let url = getAPIBaseURL() + '/'+getParam('year')+'/teams/';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(teams) {
	    let titleBody = '';
	    for (let k = 0; k < teams.length; k++) {
		let team = teams[k];
		if (team['id'] == getParam('team') && team['id'] == getParam('year')){
		titleBody += team['team_name'] + ' in the '+team['id']+' World Cup';
		}
	    }


	    let title = document.getElementById('page-title');
	    if (title) {
		title.innerHTML = titleBody;
	    }
	})
	
	.catch(function(error) {
		console.log(error);
	    });
}





}



function loadWorldCupsSelector() {

    if (getParam('team') != '') {

	let url = getAPIBaseURL() + '/Allcups/'+getParam('team')+'/cups';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(worldcups) {
	    let selectorBody = '';
	    for (let k = 0; k < worldcups.length; k++) {
		let worldcup = worldcups[k];
		//going to need to put 'id' as a return of the query, ok for now
		selectorBody += '<option value="' + worldcup['id'] + '">'
                                + worldcup['wc_location'] + ' ' + worldcup['wc_year']
		                + '</option>/n';
	    }

	    let selector = document.getElementById('world_cup_selector');
	    if (selector) {
		selector.innerHTML = selectorBody;
	    }
	})

	.catch(function(error) {
		console.log(error);
	    });
}
}


function onWorldCupsSelectionChanged() {
    let worldcupID = this.value;
    let teamID = getParam('team');
    let url = getBaseURL() + 'SpecificCups/Team?year='+ worldcupID+'&team='+teamID;
   
    window.location = url;
}



function loadPlayersSelector() {

    if (getParam('team') != '' && getParam('wc') != '') {

	let url = getAPIBaseURL() + '/'+getParam('year')+'/'+getParam('team')+'/roster';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(players) {
	    let selectorBody = '';
	    for (let k = 0; k < players.length; k++) {
		let player = players[k];
		//going to need to put 'id' as a return of the query, ok for now
		selectorBody += '<option value="' + player['id'] + '">'
                                + player['surname'] + ', ' + player['given_name']
		                + '</option>/n';
	    }

	    let selector = document.getElementById('player_selector');
	    if (selector) {
		selector.innerHTML = selectorBody;
	    }
	})

	.catch(function(error) {
		console.log(error);
	    });
}
}







function dataSelect(evt) {

    let years = localStorage.getItem("year");
    if(evt.id === "Players"){
        alert("coming Soon")
    }
    if(evt.id === "Teams"){
        alert("coming Soon")
    }
    if(evt.id === "Stats"){
        alert("coming Soon")
    }
    if(evt.id === "p3"){
        
        if (evt.value === "All team queries") {
            
            teams = 'all'
            loadAllTeams()
            if (evt.value === "All player queries"){
                //loadAllPlayers(teams);
            }

        }
    }

    if(evt.id === "p2"){
        if (evt.value === "All team queries") {
            teams = 'all'
            //loadTeamYear(years)
            if (evt.value === "All player queries"){
                //loadAllPlayers(teams);
            }
        }
    }

}
function loadAllTeams() {
    
    
    let url = getAPIBaseURL() + '/Allcups/teams/';

    // Send the request to the teamss API /authors/ endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())
    
    // Once you have your list of author dictionaries, use it to build
    // an HTML table displaying the author names and lifespan.
    .then(function(teams) {
        // Add the <option> elements to the <select> element
        let tableBody = '';
        for (let k = 0; k < teams.length; k++) {
            let team = teams[k];
            
            tableBody += '<tr>'
                            + '<td>' + team['team_name'] + '</td>'
                            + '<td>' + team['team_abbreviation'] + '</td>'
                            + '</tr>\n';
        }

        let res = document.getElementById('results');
        if (res) {
            res.innerHTML = tableBody;
        }
    })
    
    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}

function loadTeamYear(years) {
    
    let url = getAPIBaseURL() + '/<years>/teams/';

    // Send the request to the teamss API /authors/ endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())
    
    // Once you have your list of author dictionaries, use it to build
    // an HTML table displaying the author names and lifespan.
    .then(function(teams) {
        // Add the <option> elements to the <select> element
        let tableBody = '';
        for (let k = 0; k < teams.length; k++) {
            let team = teams[k];
            tableBody += '<tr>'
                            + '<td>' + teams['team_name'] + '</td>'
                            + '<td>' + teams['team_abbreviation'] + '</td>'
                            + '</tr>\n';
        }

        let res = document.getElementById('results');
        if (res) {
            res.innerHTML = tableBody;
        }
    })
    
    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}

function loadAllPlayers(teams) {
    // if(teams == 'all'){
    //     teams = [1930,1934,1938,1950,1954,1958,1962,1966,
    //         1970,1974,1978,1982,1986,1990,1994,1998,2002,2006,2010,2014]
    // }
    window.location.href="/SpecificCups";
    let url = getAPIBaseURL() + '/<teams>/players/';

    // Send the request to the teamss API /authors/ endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

    // Once you have your list of author dictionaries, use it to build
    // an HTML table displaying the author names and lifespan.
    .then(function(teams) {
        // Add the <option> elements to the <select> element
        let tableBody = '';
        for (let k = 0; k < teams.length; k++) {
            let teams = teamss[k];
            tableBody += '<tr>'
                            + '<td>' + teams['coach'] + '</td>'
                            + '<td>' + teams['team_name'] + '</td>'
                            + '<td>' + teams['year'] + '</td>'
                            + '</tr>\n';
        }

        let res = document.getElementById('results');
        if (res) {
            res.innerHTML = tableBody;
        }
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}

function valGetter() {
    yrs = yearGetter()
    if(yrs.includes("all")){
        //Put links here
        window.location.href="/AllCups";
        loadAllTeams();
    }else{
        if(yrs.length != 0){
            window.location.href="/SpecificCups";

            loadTeamYear(yrs)
        }
        else{
            alert("You Must Print Something")
        }
    }
}

function yearGetter() {  

    let years = [];
    checkboxes = document.getElementsByName('worldcup');
    for (var i = 0, n = checkboxes.length; i < n; i++) {
        
        if(checkboxes[i].checked == true){
            val = checkboxes[i].value;
            years.push(val);
        }
           
    }
        // save data value
    localStorage.setItem("year", years);
    return years;
}

