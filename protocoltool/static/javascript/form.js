$(document).ready(function(){

    // fill in all the partner information
    refreshAll();

    $('#partnerTable').on('click', 'tr', function(){

        selectedPartner = $(this).find(".partnername").text();
        var arrayLength = existingPartners.length;

        for (i = 0; i < arrayLength; i++) {

            if(existingPartners[i].name == selectedPartner){

                // set fields to valid
                $('#id_partner_name').removeClass('error');
                $('#id_partner_email').removeClass('error');
                $('#id_partner_organisation').removeClass('error');

                $('#id_partner_lead').prop('checked', false);

                $('#id_partner_name').val(existingPartners[i].name);
                $('#id_partner_email').val(existingPartners[i].email);
                $('#id_partner_organisation').val(existingPartners[i].organisation);

                if(existingPartners[i].lead == 'True'){
                    console.log("Check the cb!");
                    $('#id_partner_lead').prop('checked', true);
                }
                else{
                    $('#id_partner_lead').prop('checked', false);
                }

                $('#selectedPartnerID').val(existingPartners[i].id);

                // update buttons
                $('#updatePartnerID').removeClass( "disabled" ).addClass( "active" );
                $('#updatePartnerID').prop( "disabled", false);
                $('#deletePartnerID').removeClass( "disabled" ).addClass( "active" );
                $('#deletePartnerID').prop( "disabled", false);
            }
        }
    });


    $('#saveInfoID').on('click', function(){
        /*
        Save the generic experiment info in the database
        */

        // check if all values are valid
        validShortname = checkValidField($('#id_basic_shortname'));
        validTitle = checkValidField($('#id_basic_title'));

        if(validShortname === true && validTitle === true){

            var dataToSend = {
                    shortname: $('#id_basic_shortname').val(),
                    title: $('#id_basic_title').val(),
                    experimentIdea: $('#id_basic_experimentIdea').val(),
                    hypothesis: $('#id_basic_hypothesis').val(),
                    researchObjective: $('#id_basic_researchObjective').val(),
                    datasetID: datasetID,
                    csrfmiddlewaretoken: csrfmiddlewaretoken}

            $.ajax({
                url: "/project/saveexperimentinfo/",
                type: "POST",
                data: dataToSend,

                // handle a successful response
                success : function(json) {
                    existingExperimentInfo = JSON.parse(json['existingExperimentInfoJSON']);
                    console.log(existingExperimentInfo)

                    refreshExperimentInfo();
                },
                // handle a non-successful response
                error : function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            });

        }
        else{
            warningPopup("One or more required fields are filled in incorrectly");
        }
    });


    $('#addPartnerID').on('click', function(){

        // check if all values are valid
        validName = checkValidField($('#id_partner_name'));
        validEmail = checkValidField($('#id_partner_email'));
        validOrganisation = checkValidField($('#id_partner_organisation'));

        if(validName === true && validEmail === true && validOrganisation === true){
            sendPartnerInfoToServer(false);
        }
        else{
            warningPopup("One or more fields are filled in incorrectly");
        }
    });

    $('#updatePartnerID').on('click', function(){
        // check if all values are valid
        validName = checkValidField($('#id_partner_name'));
        validEmail = checkValidField($('#id_partner_email'));
        validOrganisation = checkValidField($('#id_partner_organisation'));

        if(validName === true && validEmail === true && validOrganisation === true){
            sendPartnerInfoToServer(true);
        }
        else{
            warningPopup("One or more fields are filled in incorrectly");
        }
    });

    $('#deletePartnerID').on('click', function(){

        var partnerID = $('#selectedPartnerID').val();

        // check if all the partner is not used in the reqs
        partnerUsed = false
        var nrReqs = existingReqs.length;
        for (i = 0; i < nrReqs; i++) {
            if (existingReqs[i].partnerID == partnerID){
                partnerUsed = true;
                warningPopup("This partner is a contributing partner in the data&method preparation, removal is therefore not allowed.");
            }
        }

        // check if all the partner is not used in the exp steps
        var nrExpSteps = existingExpSteps.length;
        for (i = 0; i < nrExpSteps; i++) {
            if (existingExpSteps[i].partnerID == partnerID){
                partnerUsed = true;
                warningPopup("This partner is a contributing partner in the experiment steps, removal is therefore not allowed.")
            }
        }

        if(partnerUsed == false){
            $.ajax({
                url: "/project/deletepartner/",
                type: "POST",
                data: {partnerID: partnerID,
                       datasetID: datasetID,
                       csrfmiddlewaretoken: csrfmiddlewaretoken},

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
        }
    });


    //
    // FUNCTIONS FOR THE DATA REQS
    //

    $('#reqTableID').on('click', 'tbody tr', function(){

        selectedReqID = $(this).closest("tr").attr('id');
        $(this).closest("tr").addClass("highlight").siblings().removeClass("highlight");

        var nrReqs = existingReqs.length;

        for (i = 0; i < nrReqs; i++) {

            if (existingReqs[i].id == selectedReqID){

                // remove all error classes
                $('#id_req_task').removeClass('error');
                $('#id_req_properties').removeClass('error');
                $('#partnerDataReq').removeClass('error');

                $('#id_req_task').val(existingReqs[i].task);
                $('#id_req_properties').val(existingReqs[i].properties);
                $('#id_req_deadline').val(existingReqs[i].deadline);
                 if(existingReqs[i].done == 'True'){
                    $('#id_done').prop('checked', true);
                }
                else{
                    $('#id_done').prop('checked', false);
                }

                contrPartner = getPartnerByID(existingReqs[i].partnerID);

                $('#partnerDataReq').val(contrPartner.id);
                $('#selectedReqID').val(selectedReqID);

                // update buttons
                $('#updateReqID').removeClass( "disabled" ).addClass( "active" );
                $('#updateReqID').prop( "disabled", false);
                $('#deleteReqID').removeClass( "disabled" ).addClass( "active" );
                $('#deleteReqID').prop( "disabled", false);
                $('#incrTaskNrReqID').removeClass( "disabled" ).addClass( "active" );
                $('#incrTaskNrReqID').prop( "disabled", false);
                $('#decrTaskNrReqID').removeClass( "disabled" ).addClass( "active" );
                $('#decrTaskNrReqID').prop( "disabled", false);

            }
        } // end for

    }); // end on reqTable clicked

    $('#addReqID').on('click', function(){

        // check if all values are valid
        validTask = checkValidField($('#id_req_task'));
        validProp = checkValidField($('#id_req_properties'));
        validPartner = checkValidField($('#partnerDataReq'));

        if(validTask === true && validProp === true && validPartner === true){
            sendReqInfoToServer(false);
        }
        else{
            warningPopup("One or more fields are filled in incorrectly");
        }
    });

    $('#updateReqID').on('click', function(){
        // check if all values are valid
        validTask = checkValidField($('#id_req_task'));
        validProp = checkValidField($('#id_req_properties'));
        validPartner = checkValidField($('#partnerDataReq'));

        if(validTask === true && validProp === true && validPartner === true){
            sendReqInfoToServer(true);
        }
        else{
            warningPopup("One or more fields are filled in incorrectly");
        }
    });

    $('#deleteReqID').on('click', function(){

         var dataToSend = {stepID: $('#selectedReqID').val(),
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken}

         sendInfoToServer(dataToSend, "/project/deletereq/", existingReqs, refreshReqs)
    });

    $('#incrTaskNrReqID').on('click', function(){
        var dataToSend = {reqID: $('#selectedReqID').val(),
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken}

        sendInfoToServer(dataToSend, "/project/increasereq/", existingReqs, refreshReqs)
    });

    $('#decrTaskNrReqID').on('click', function(){
        var dataToSend = {reqID: $('#selectedReqID').val(),
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken}

        sendInfoToServer(dataToSend, "/project/decreasereq/", existingReqs, refreshReqs)
    });

    //
    // FUNCTIONS FOR THE STEPS
    //

    $('#expStepTableID').on('click', 'tbody tr', function(){

        selectedExpStepID = $(this).closest("tr").attr('id');
        $(this).closest("tr").addClass("highlight").siblings().removeClass("highlight");

        var nrExpSteps = existingExpSteps.length;

        for (i = 0; i < nrExpSteps; i++) {

            if (existingExpSteps[i].id == selectedExpStepID){

                // remove all error classes
                $('#id_exp_task').removeClass('error');
                $('#id_exp_properties').removeClass('error');
                $('#partnerExpStep').removeClass('error');

                $('#id_exp_task').val(existingExpSteps[i].task);
                $('#id_exp_properties').val(existingExpSteps[i].properties);
                $('#id_exp_deadline').val(existingExpSteps[i].deadline);

                contrPartner = getPartnerByID(existingExpSteps[i].partnerID);

                $('#partnerExpStep').val(contrPartner.id);
                $('#selectedExpStepID').val(selectedExpStepID);

                // update buttons
                $('#updateExpStepID').removeClass( "disabled" ).addClass( "active" );
                $('#updateExpStepID').prop( "disabled", false);
                $('#deleteExpStepID').removeClass( "disabled" ).addClass( "active" );
                $('#deleteExpStepID').prop( "disabled", false);
                $('#incrTaskNrExpStepID').removeClass( "disabled" ).addClass( "active" );
                $('#incrTaskNrExpStepID').prop( "disabled", false);
                $('#decrTaskNrExpStepID').removeClass( "disabled" ).addClass( "active" );
                $('#decrTaskNrExpStepID').prop( "disabled", false);
            }
        } // end for

    }); // end on expStepTable clicked

    $('#addExpStepID').on('click', function(){

        // check if all values are valid
        validTask = checkValidField($('#id_exp_task'));
        validProp = checkValidField($('#id_exp_properties'));
        validPartner = checkValidField($('#partnerExpStep'));

        if(validTask === true && validProp === true && validPartner === true){
            sendExpStepInfoToServer(false);
        }
        else{
            warningPopup("One or more fields are filled in incorrectly");
        }
    });

    $('#updateExpStepID').on('click', function(){
        // check if all values are valid
        validTask = checkValidField($('#id_exp_task'));
        validProp = checkValidField($('#exp_properties'));
        validPartner = checkValidField($('#partnerExpStep'));

        if(validTask === true && validProp === true && validPartner === true){
            sendExpStepInfoToServer(true);
        }
        else{
            warningPopup("One or more fields are filled in incorrectly");
        }
    });

    $('#deleteExpStepID').on('click', function(){

         var dataToSend = {stepID: $('#selectedExpStepID').val(),
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken}

         sendInfoToServer(dataToSend, "/project/deletestep/", existingExpSteps, refreshExpSteps)
    });
    
    $('#incrTaskNrExpStepID').on('click', function(){
        var dataToSend = {expStepID: $('#selectedExpStepID').val(),
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken}

        sendInfoToServer(dataToSend, "/project/increaseexpstep/", existingExpSteps, refreshExpSteps)
    });

    $('#decrTaskNrExpStepID').on('click', function(){
        var dataToSend = {expStepID: $('#selectedExpStepID').val(),
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken}

        sendInfoToServer(dataToSend, "/project/decreaseexpstep/", existingExpSteps, refreshExpSteps)
    });

    
    //
    // FUNCTIONS FOR THE REPORTING
    //

    $('#reportingTableID').on('click', 'tbody tr', function(){

        selectedReportingID = $(this).closest("tr").attr('id');
        $(this).closest("tr").addClass("highlight").siblings().removeClass("highlight");

        var nrReportings = existingReportings.length;

        for (i = 0; i < nrReportings; i++) {

            if (existingReportings[i].id == selectedReportingID){

                // remove all error classes
                $('#id_reporting_task').removeClass('error');
                $('#id_reporting_properties').removeClass('error');
                $('#partnerReporting').removeClass('error');

                $('#id_reporting_task').val(existingReportings[i].task);
                $('#id_reporting_properties').val(existingReportings[i].properties);
                $('#id_reporting_deadline').val(existingReportings[i].deadline);

                contrPartner = getPartnerByID(existingReportings[i].partnerID);

                $('#partnerReporting').val(contrPartner.id);
                $('#selectedReportingID').val(selectedReportingID);

                // update buttons
                $('#updateReportingID').removeClass( "disabled" ).addClass( "active" );
                $('#updateReportingID').prop( "disabled", false);
                $('#deleteReportingID').removeClass( "disabled" ).addClass( "active" );
                $('#deleteReportingID').prop( "disabled", false);
                $('#incrTaskNrReportingID').removeClass( "disabled" ).addClass( "active" );
                $('#incrTaskNrReportingID').prop( "disabled", false);
                $('#decrTaskNrReportingID').removeClass( "disabled" ).addClass( "active" );
                $('#decrTaskNrReportingID').prop( "disabled", false);
            }
        } // end for

    }); // end on reportingTable clicked

    $('#addReportingID').on('click', function(){

        // check if all values are valid
        validTask = checkValidField($('#id_reporting_task'));
        validProp = checkValidField($('#id_reporting_properties'));
        validPartner = checkValidField($('#partnerReporting'));

        if(validTask === true && validProp === true && validPartner === true){
            sendReportingInfoToServer(false);
        }
        else{
            warningPopup("One or more fields are filled in incorrectly");
        }
    });

    $('#updateReportingID').on('click', function(){
        // check if all values are valid
        validTask = checkValidField($('#id_reporting_task'));
        validProp = checkValidField($('#id_reporting_properties'));
        validPartner = checkValidField($('#partnerReporting'));

        if(validTask === true && validProp === true && validPartner === true){
            sendReportingInfoToServer(true);
        }
        else{
            warningPopup("One or more fields are filled in incorrectly");
        }
    });

    $('#deleteReportingID').on('click', function(){

        var dataToSend = {stepID: $('#selectedReportingID').val(),
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken}

        sendInfoToServer(dataToSend, "/project/deletereporting/", existingReportings, refreshReporting)

    });

    $('#incrTaskNrReportingID').on('click', function(){
        var dataToSend = {reportingID: $('#selectedReportingID').val(),
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken}

        sendInfoToServer(dataToSend, "/project/increasereporting/", existingReportings, refreshReporting)
    });

    $('#decrTaskNrReportingID').on('click', function(){
        var dataToSend = {reportingID: $('#selectedReportingID').val(),
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken}

        sendInfoToServer(dataToSend, "/project/decreasereporting/", existingReportings, refreshReporting)
    });

});
