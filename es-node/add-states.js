var elasticsearch = require('elasticsearch');
var elasticSearchClient = new elasticsearch.Client({
    host: 'https://newsai:XkJRNRx2EGCd6@search.newsai.org',
    // log: 'trace',
    rejectUnauthorized: false
});

var states = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AS": "American Samoa",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District Of Columbia",
    "FM": "Federated States Of Micronesia",
    "FL": "Florida",
    "GA": "Georgia",
    "GU": "Guam",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MH": "Marshall Islands",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "MP": "Northern Mariana Islands",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PW": "Palau",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VI": "Virgin Islands",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}

var esActions = [];

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

function isNumber(text) {
    var reg = /^\d+$/;
    if (text) {
        return reg.test(text);
    }
    return false;
}

function removeSpecial(text) {
    if (text) {
        var lower = text.toLowerCase();
        var upper = text.toUpperCase();
        var result = '';
        for (var i = 0; i < lower.length; ++i) {
            if (isNumber(text[i]) || (lower[i] != upper[i]) || (lower[i].trim() === '')) {
                result += text[i];
            }
        }
        return result;
    }
    return '';
}

var esActions = [];

for (state in states) {
    var stateId = removeSpecial(states[state]);
    stateId = stateId.trim();
    stateId = stateId.replaceAll(' ', '-');
    stateId = stateId.toLowerCase();

    var indexRecord = {
        index: {
            _index: 'locations',
            _type: 'state',
            _id: stateId
        }
    };
    var dataRecord = {
        'fixedCountryName': 'United States',
        'stateName': states[state]
    };
    esActions.push(indexRecord);
    esActions.push({
        data: dataRecord
    });
}

console.log(esActions);

elasticSearchClient.bulk({
    body: esActions
}, function(error, response) {
    if (error || response && response.errors) {
        if (!error) {
            error = 'Could not send data to ES';
        }
        console.error(error)
    } else {
        console.log(response);
    }
});