// Validate form (client side) TODO: Make validation checks for all fields -->
function checkform() {

    var expTitle = $('#id_basic_title').val();
    console.log(expTitle);
    //var okName = /[^a-zA-Z0-9]/.test(expTitle);

    if (expTitle == ""){
        alert("Please give a valid experiment title");
    }
    else{
        document.getElementById('dataset_form').submit();
    }
}


function refreshAll(){
    refreshPartners();
    refreshReqs();
    refreshExpSteps();
    refreshReporting();
}


function refreshPartners(){

    // Reset all Partner stuff
    $('#id_name').val("");
    $('#id_email').val("");
    $('#id_organisation').val("");
    $('#id_lead').prop('checked', false);

    // update buttons
    $('#updatePartnerID').removeClass( "active" ).addClass( "disabled" );
    $('#updatePartnerID').prop( "disabled", true);
    $('#deletePartnerID').removeClass( "active" ).addClass( "disabled" );
    $('#deletePartnerID').prop( "disabled", true);

    // reset selected partner ID
    $('#selectedPartnerID').val('-99')

    // reset partner table
    var arrayLength = existingPartners.length;
    $("#partnerTable tbody tr").remove();

    for (i = 0; i < arrayLength; i++) {
        var leadText = "";
        if (existingPartners[i].lead == 'True'){
            leadText = "<strong>lead</strong>"
        }

        $("#partnerTable > tbody").append('<tr class="partnerRow"><td class="col-md-5 partnername">' + existingPartners[i].name +
        '<td class="col-md-5">' + existingPartners[i].organisation + '</td><td class="col-md-2">' + leadText + '</td></tr>');
    }

    // also refresh the partners in the reqs table
    selectedPartnerID = $("#partnerDataReq").val()  // temporary store selected partner
    $("#partnerDataReq").empty();
    for (i = 0; i < arrayLength; i++) {
        $("#partnerDataReq").append('<option value = ' + existingPartners[i].id + '>' + existingPartners[i].name + '</option>');
    }
    $("#partnerDataReq").val(selectedPartnerID)


    // also refresh the partners in the exp steps table
    selectedPartnerID = $("#partnerExpStep").val()  // temporary store selected partner
    $("#partnerExpStep").empty();
    for (i = 0; i < arrayLength; i++) {
        $("#partnerExpStep").append('<option value = ' + existingPartners[i].id + '>' + existingPartners[i].name + '</option>');
    }
    $("#partnerExpStep").val(selectedPartnerID)

    // also refresh the partners in the reporting table
    selectedPartnerID = $("#partnerReporting").val()  // temporary store selected partner
    $("#partnerReporting").empty();
    for (i = 0; i < arrayLength; i++) {
        $("#partnerReporting").append('<option value = ' + existingPartners[i].id + '>' + existingPartners[i].name + '</option>');
    }
    $("#partnerReporting").val(selectedPartnerID)
}


function refreshReqs(){

    $('#id_done').prop('checked', false)
    $('.reqdesc').val("")
    $('.reqprop').val("")
    //$('.reqdeadline').val("1970-01-01")

    $("#partnerDataReq").empty();
    var arrayLength = existingPartners.length;
    for (i = 0; i < arrayLength; i++) {
        $("#partnerDataReq").append('<option value = ' + existingPartners[i].id + '>' + existingPartners[i].name + '</option>');
    }
    $("#partnerDataReq").val(null)

    // update buttons
    $('#updateReqID').removeClass( "active" ).addClass( "disabled" );
    $('#updateReqID').prop( "disabled", true);
    $('#deleteReqID').removeClass( "active" ).addClass( "disabled" );
    $('#deleteReqID').prop( "disabled", true);

    var arrayLength = existingReqs.length;
    $("#reqTableID tbody tr").remove();

    for (i = 0; i < arrayLength; i++) {

        var reqDone = 'No'
        if (existingReqs[i].done == 'True'){
            reqDone = 'Yes'
        }

        $("#reqTableID > tbody").append(
            '<tr class="reqRow" id = ' +  existingReqs[i].id + '>' +
            '<td class="col-md-7">' + existingReqs[i].description + '</td>' +
            '<td class="col-md-3">' + existingReqs[i].deadline + '</td>' +
            '<td class="col-md-2">' + reqDone + '</td></tr>')
    }
}

function refreshExpSteps(){

    $('.expstepdesc').val("")
    $('.expstepproperties').val("")
    //$('.expstepdeadline').val("1970-01-01")

    $("#partnerExpStep").empty();
    var arrayLength = existingPartners.length;
    for (i = 0; i < arrayLength; i++) {
        $("#partnerExpStep").append('<option value = ' + existingPartners[i].id + '>' + existingPartners[i].name + '</option>');
    }
    $("#partnerExpStep").val(null)

    // update buttons
    $('#updateExpStepID').removeClass( "active" ).addClass( "disabled" );
    $('#updateExpStepID').prop( "disabled", true);
    $('#deleteExpStepID').removeClass( "active" ).addClass( "disabled" );
    $('#deleteExpStepID').prop( "disabled", true);


    var arrayLength = existingExpSteps.length;
    $("#expStepTableID tbody tr").remove();

    for (i = 0; i < arrayLength; i++) {

        $("#expStepTableID > tbody").append(
            '<tr class="expStepRow" id = ' +  existingExpSteps[i].id + '>' +
            '<td class="col-md-8">' + existingExpSteps[i].description + '</td>' +
            '<td class="col-md-4">' + existingExpSteps[i].deadline + '</td></tr>')
    }
}

function refreshReporting(){

    $('.reportingdesc').val("")
    $('.reportingproperties').val("")
    //$('.reportingdeadline').val("1970-01-01")

    $("#partnerReporting").empty();
    var arrayLength = existingPartners.length;
    for (i = 0; i < arrayLength; i++) {
        $("#partnerReporting").append('<option value = ' + existingPartners[i].id + '>' + existingPartners[i].name + '</option>');
    }
    $("#partnerReporting").val(null)

    // update buttons
    $('#updateReportingID').removeClass( "active" ).addClass( "disabled" );
    $('#updateReportingID').prop( "disabled", true);
    $('#deleteReportingID').removeClass( "active" ).addClass( "disabled" );
    $('#deleteReportingID').prop( "disabled", true);

    var arrayLength = existingReportings.length;
    $("#reportingTableID tbody tr").remove();

    for (i = 0; i < arrayLength; i++) {
        $("#reportingTableID > tbody").append(
            '<tr class="reportingRow" id = ' +  existingReportings[i].id + '>' +
            '<td class="col-md-8">' + existingReportings[i].description + '</td>' +
            '<td class="col-md-4">' + existingReportings[i].deadline + '</td></tr>')
    }
}

function getPartnerByID(partnerID){

    var nrPartners = existingPartners.length;

    for (j = 0; j < nrPartners; j++) {
        if(existingPartners[j].id == partnerID){
            return existingPartners[j];
        }
    }

    return null;
}


function sendPartnerInfoToServer(update){

    url = "/project/addpartner/"

    var lead = 'False';
    if($('#id_lead').is(':checked')){
        lead = 'True';
    }

    dataToSend = {datasetID: datasetID,
       name: $('#id_name').val(),
       email: $('#id_email').val(),
       organisation: $('#id_organisation').val(),
       lead: lead,
       csrfmiddlewaretoken: csrfmiddlewaretoken
    }

    if (update == true){
        url = "/project/updatepartner/"
        partnerID = $('#selectedPartnerID').val();
        dataToSend['partnerID'] = partnerID;
    }

    $.ajax({
        url: url,
        type: "POST",
        data: dataToSend,

        // handle a successful response
        success : function(json) {
            existingPartners = JSON.parse(json['existingPartnersJSON']);
            refreshPartners();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

} // end sendPartnerInfoToServer


function sendReqInfoToServer(update){

    url = "/project/addreq/"

     // get all filled in data
    var done = 'False';
    if($('#id_done').is(':checked')){
        done = 'True';
    }

    dataToSend = {
        datasetID: datasetID,
        description: $('.reqdesc').val(),    // use the class set in the widget in 'forms.py' to identify the field
        properties: $('.reqprop').val(),
        partnerID: $("#partnerDataReq").val(),
        deadline: $('.reqdeadline').val(),
        done: done,
        csrfmiddlewaretoken: csrfmiddlewaretoken}

    if (update == true){
        url = "/project/updatereq/"
        dataToSend['reqID'] = $('#selectedReqID').val();
    }

    $.ajax({
        url: url,
        type: "POST",
        data: dataToSend,

        // handle a successful response
        success : function(json) {
            existingReqs = JSON.parse(json['existingReqsJSON']);
            refreshReqs();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

} // end sendReqInfoToServer


function sendExpStepInfoToServer(update){

    url = "/project/addstep/"

     // get all filled in data
    dataToSend = {
        datasetID: datasetID,
        description: $('.expstepdesc').val(),    // use the class set in the widget in 'forms.py' to identify the field
        properties: $('.expstepproperties').val(),
        partnerID: $("#partnerExpStep").val(),
        deadline: $('.expstepdeadline').val(),
        csrfmiddlewaretoken: csrfmiddlewaretoken}

    if (update == true){
        url = "/project/updatestep/"
        dataToSend['expStepID'] = $('#selectedExpStepID').val();
    }

    $.ajax({
        url: url,
        type: "POST",
        data: dataToSend,

        // handle a successful response
        success : function(json) {
            existingExpSteps = JSON.parse(json['existingExpStepsJSON']);
            refreshExpSteps();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

} // end sendExpStepsInfoToServer


function sendReportingInfoToServer(update){

    url = "/project/addreporting/"

     // get all filled in data
    dataToSend = {
        datasetID: datasetID,
        description: $('.reportingdesc').val(),    // use the class set in the widget in 'forms.py' to identify the field
        properties: $('.reportingproperties').val(),
        partnerID: $("#partnerReporting").val(),
        deadline: $('.reportingdeadline').val(),
        csrfmiddlewaretoken: csrfmiddlewaretoken}

    if (update == true){
        url = "/project/updatereporting/"
        dataToSend['reportingID'] = $('#selectedReportingID').val();
    }

    $.ajax({
        url: url,
        type: "POST",
        data: dataToSend,

        // handle a successful response
        success : function(json) {
            existingReportings = JSON.parse(json['existingReportingsJSON']);
            refreshReporting();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

} // end sendreportingInfoToServer