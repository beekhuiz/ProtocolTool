function isEven(n) {
   return n % 2 == 0;
}

function writeLabelLine(tablebody, index=1, label, text){
    /*
    write a line of text with a label to a table. The index is deprecated and was used to create
    a potential striped table
    */
    var trclass = ""
    if(isEven(index)){
        //trclass = "trdark";
        trclass = "";
    }

    $(tablebody).append(
          '<tr class="' + trclass + '">' +
          '<td class="col-md-2 infotext"><strong>' + label + '</strong></td>' +
          '<td class="col-md-10 infotext">' + text + '</td></tr>')
}

function writeLabelTwoLines(tablebody, label, text){
    $(tablebody).append(
          '<tr><td class="infotext"><strong>' + label + '</strong><br>' + text + '</td></tr>')
}


function checkValidField(item){
   if(item.val() === null || item.val() === "" ){
       item.addClass('error');
       return false;
   }
   else {
        item.removeClass('error');
        return true;
   }
}

function warningPopup(messageText){
//   BootstrapDialog.show({
//      type: BootstrapDialog.TYPE_WARNING,
//      message: messageText,
//      buttons: [{
//            label: 'Close',
//            action: function(dialogItself){
//                dialogItself.close();
//            }
//        }]
//   });

     bootbox.alert(messageText, function() {
         console.log("Alert Callback");
     });
}


// Validate form (client side) TODO: Make validation checks for all fields -->
function checkform() {

    validShortname = checkValidField($('#id_basic_shortname'));
    validTitle = checkValidField($('#id_basic_title'));

    //var okName = /[^a-zA-Z0-9]/.test(expTitle);

    if (validShortname && validTitle){
       document.getElementById('dataset_form').submit();
    }
    else{
        warningPopup('Please fill in a full experiment name and a short name')
    }
}


function back() {

    validShortname = checkValidField($('#id_basic_shortname'));
    validTitle = checkValidField($('#id_basic_title'));

    if (validShortname && validTitle){
        bootbox.confirm('Data in the form fields on the left that are not added or saved will be lost. Are you sure you wish to go back to the participate tool?', function(result){
            if(result){
                $('#dataset_form').submit();
            }
        });
    }
    else{
        bootbox.confirm('No valid full experiment name or short name, the new protocol will not be stored. Are you sure you wish to go back to the participate tool?', function(result){
            if(result){
                $('#dataset_form').submit();
            }
        });
    }
}


function setMessage(messagetype, messagefa, messagetext){
	try {
		$('#messagetype').removeClass().addClass(messagetype);
		$('#messagefa').removeClass().addClass(messagefa);
		$('#messagetext').text(messagetext);
	}
		catch(err) {
			console.log(err.message);
	}
}


function refreshAll(){
    refreshExperimentInfo();
    refreshPartners();
    refreshReqs();
    refreshExpSteps();
    refreshReporting();
}


function refreshExperimentInfo(){

//    writeLabelLine("#experimentTable > tbody", 2, "Full name:", "{{ existingExperimentInfo.title|linebreaks }}");
//    writeLabelLine("#experimentTable > tbody", 2, "Short name:", "{{ existingExperimentInfo.shortname|linebreaks }}");
//    writeLabelLine("#experimentTable > tbody", 1, "Idea:", "{{ existingExperimentInfo.experimentIdea|linebreaks }}");
//    writeLabelLine("#experimentTable > tbody", 2, "Hypothesis:", "{{ existingExperimentInfo.hypothesis|linebreaks }}");
//    writeLabelLine("#experimentTable > tbody", 1, "Objective:", "{{ existingExperimentInfo.researchObjective|linebreaks }}");
//    writeLabelLine("#experimentTable > tbody", 2, "Last update:", "{{ existingExperimentInfo.dateLastUpdate|linebreaks }}");

    $("#experimentTable tbody tr").remove();

    writeLabelTwoLines("#experimentTable > tbody", "Full name:", existingExperimentInfo.title);
    writeLabelTwoLines("#experimentTable > tbody", "Short name:", existingExperimentInfo.shortname);
    writeLabelTwoLines("#experimentTable > tbody", "Idea:", existingExperimentInfo.experimentIdea);
    writeLabelTwoLines("#experimentTable > tbody", "Hypothesis:", existingExperimentInfo.hypothesis);
    writeLabelTwoLines("#experimentTable > tbody", "Objective:", existingExperimentInfo.researchObjective);
}


function refreshPartners(){

    // Reset all Partner stuff
    $('#id_partner_name').val("");
    $('#id_partner_email').val("");
    $('#id_partner_organisation').val("");
    $('#id_partner_lead').prop('checked', false);

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


function refreshReqs(existingList=existingReqs){

    existingReqs = existingList

    $('#id_req_done').prop('checked', false)
    $('#id_req_task').val("")
    $('#id_req_properties').val("")
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
    $('#incrTaskNrReportingID').removeClass( "active" ).addClass( "disabled" );
    $('#incrTaskNrReportingID').prop( "disabled", true);
    $('#decrTaskNrReportingID').removeClass( "active" ).addClass( "disabled" );
    $('#decrTaskNrReportingID').prop( "disabled", true);


    var arrayLength = existingReqs.length;
    $("#reqTableID tbody tr").remove();

    if(arrayLength == 0){
        $("#reqTableID > tbody").append(
            '<tr><td class="col-md-8">...</td>' +
            '<td class="col-md-4"></td></tr>')
    }

    for (i = 0; i < arrayLength; i++) {

        var taskDone = 'No'
        if (existingReqs[i].done == 'True'){
            taskDone = 'Yes'
        }

        $("#reqTableID > tbody").append(
            '<tr id = ' +  existingReqs[i].id + '>' +
            '<td class="col-md-1">' + existingReqs[i].taskNr + '</td>' +
            '<td class="col-md-7">' + existingReqs[i].task + '</td>' +
            '<td class="col-md-2">' + existingReqs[i].deadline + '</td>' +
            '<td class="col-md-2">' + taskDone + '</td></tr>')
    }
}

function refreshExpSteps(existingList=existingExpSteps){

    // use the existingreportings by default; however, if a new list is given to the refresh function
    // by updating, deleting, etc. in this way the new list can be passed to the refresh function
    existingExpSteps = existingList

    $('#id_exp_task').val("")
    $('#id_exp_properties').val("")

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
    $('#incrTaskNrReportingID').removeClass( "active" ).addClass( "disabled" );
    $('#incrTaskNrReportingID').prop( "disabled", true);
    $('#decrTaskNrReportingID').removeClass( "active" ).addClass( "disabled" );
    $('#decrTaskNrReportingID').prop( "disabled", true);


    var arrayLength = existingExpSteps.length;
    $("#expStepTableID tbody tr").remove();

    if(arrayLength == 0){
        $("#expStepTableID > tbody").append(
            '<tr><td class="col-md-8">...</td>' +
            '<td class="col-md-4"></td></tr>')
    }

    for (i = 0; i < arrayLength; i++) {

        var taskDone = 'No'
        if (existingExpSteps[i].done == 'True'){
            taskDone = 'Yes'
        }

        $("#expStepTableID > tbody").append(
            '<tr id = ' +  existingExpSteps[i].id + '>' +
            '<td class="col-md-1">' + existingExpSteps[i].taskNr + '</td>' +
            '<td class="col-md-7">' + existingExpSteps[i].task + '</td>' +
            '<td class="col-md-2">' + existingExpSteps[i].deadline + '</td>' +
            '<td class="col-md-2">' + taskDone + '</td></tr>')
    }
}

function refreshReporting(existingList=existingReportings){

    // use the existingreportings by default; however, if a new list is given to the refresh function
    // by updating, deleting, etc. in this way the new list can be passed to the refresh function
    existingReportings = existingList

    $('#id_reporting_task').val("")
    $('#id_reporting_properties').val("")

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
    $('#incrTaskNrReportingID').removeClass( "active" ).addClass( "disabled" );
    $('#incrTaskNrReportingID').prop( "disabled", true);
    $('#decrTaskNrReportingID').removeClass( "active" ).addClass( "disabled" );
    $('#decrTaskNrReportingID').prop( "disabled", true);

    var arrayLength = existingReportings.length;
    $("#reportingTableID tbody tr").remove();

    if(arrayLength == 0){
        $("#reportingTableID > tbody").append(
            '<tr><td class="col-md-8">...</td>' +
            '<td class="col-md-4"></td></tr>')
    }

    for (i = 0; i < arrayLength; i++) {

        var taskDone = 'No'
        if (existingReportings[i].done == 'True'){
            taskDone = 'Yes'
        }

        $("#reportingTableID > tbody").append(
            '<tr id = ' +  existingReportings[i].id + '>' +
            '<td class="col-md-1">' + existingReportings[i].taskNr + '</td>' +
            '<td class="col-md-7">' + existingReportings[i].task + '</td>' +
            '<td class="col-md-2">' + existingReportings[i].deadline + '</td>' +
            '<td class="col-md-2">' + taskDone + '</td></tr>')
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
    if($('#id_partner_lead').is(':checked')){

        var existingLead = 'False';

        // check if there is already a lead partner
        var nrPartners = existingPartners.length;
        for (j = 0; j < nrPartners; j++) {
            if(existingPartners[j].lead == 'True'){
                existingLead = 'True';
            }
        }

        if(existingLead == 'True'){
            warningPopup('There is already a partner in the lead; ' +
                         'please uncheck the lead box or change the existing partner in the lead')
            return;
        }

        lead = 'True';
    }

    dataToSend = {datasetID: datasetID,
       name: $('#id_partner_name').val(),
       email: $('#id_partner_email').val(),
       organisation: $('#id_partner_organisation').val(),
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
    if($('#id_req_done').is(':checked')){
        done = 'True';
    }

    dataToSend = {
        datasetID: datasetID,
        task: $('#id_req_task').val(),    // use the class set in the widget in 'forms.py' to identify the field
        properties: $('#id_req_properties').val(),
        partnerID: $("#partnerDataReq").val(),
        deadline: $('#id_req_deadline').val(),
        done: done,
        csrfmiddlewaretoken: csrfmiddlewaretoken}

    if (update == true){
        url = "/project/updatereq/"
        dataToSend['stepID'] = $('#selectedReqID').val();
    }

    sendInfoToServer(dataToSend, url, existingReqs, refreshReqs)

} // end sendReqInfoToServer


function sendExpStepInfoToServer(update){

    url = "/project/addstep/"

     // get all filled in data
     var done = 'False';
     if($('#id_exp_done').is(':checked')){
        done = 'True';
     }

    dataToSend = {
        datasetID: datasetID,
        task: $('#id_exp_task').val(),    // use the class set in the widget in 'forms.py' to identify the field
        properties: $('#id_exp_properties').val(),
        partnerID: $("#partnerExpStep").val(),
        deadline: $("#id_exp_deadline").val(),
        done: done,
        csrfmiddlewaretoken: csrfmiddlewaretoken}

    if (update == true){
        url = "/project/updatestep/"
        dataToSend['stepID'] = $('#selectedExpStepID').val();
    }


    sendInfoToServer(dataToSend, url, existingExpSteps, refreshExpSteps)

} // end sendExpStepsInfoToServer


function sendReportingInfoToServer(update){

    url = "/project/addreporting/"

     // get all filled in data
     var done = 'False';
     if($('#id_reporting_done').is(':checked')){
        done = 'True';
     }

    dataToSend = {
        datasetID: datasetID,
        task: $('#id_reporting_task').val(),    // use the class set in the widget in 'forms.py' to identify the field
        properties: $('#id_reporting_properties').val(),
        partnerID: $("#partnerReporting").val(),
        deadline: $('#id_reporting_deadline').val(),
        done: done,
        csrfmiddlewaretoken: csrfmiddlewaretoken}

    if (update == true){
        url = "/project/updatereporting/"
        dataToSend['stepID'] = $('#selectedReportingID').val();
    }

    sendInfoToServer(dataToSend, url, existingReportings, refreshReporting)

} // end sendreportingInfoToServer


function sendInfoToServer(dataToSend, urlToSend, existingList, refreshFunction){

    $.ajax({
        url: urlToSend,
        type: "POST",
        data: dataToSend,

        // handle a successful response
        success : function(json) {
            existingList = JSON.parse(json['existingListJSON']);
            refreshFunction(existingList);
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}