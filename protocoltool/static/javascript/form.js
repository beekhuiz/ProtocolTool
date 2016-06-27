$(document).ready(function(){

    // fill in all the partner information
    refreshAll();

    $('#partnerTable').on('click', 'tr', function(){

        selectedPartner = $(this).find(".partnername").text();
        var arrayLength = existingPartners.length;

        for (i = 0; i < arrayLength; i++) {

            if(existingPartners[i].name == selectedPartner){
                $('#id_name').val(existingPartners[i].name);
                $('#id_email').val(existingPartners[i].email);
                $('#id_organisation').val(existingPartners[i].organisation);

                if(existingPartners[i].lead == 'True'){
                    console.log("Check the cb!");
                    $('#id_lead').prop('checked', true);
                }
                else{
                    $('#id_lead').prop('checked', false);
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

    $('#addPartnerID').on('click', function(){
        sendPartnerInfoToServer(false);
    });

    $('#updatePartnerID').on('click', function(){
        sendPartnerInfoToServer(true);
    });

    $('#deletePartnerID').on('click', function(){

        var partnerID = $('#selectedPartnerID').val();

        // check if all the partner is not used in the reqs
        partnerUsed = false
        var nrReqs = existingReqs.length;
        for (i = 0; i < nrReqs; i++) {
            if (existingReqs[i].partnerID == partnerID){
                partnerUsed = true;
                alert("This partner is a contributing partner in the data&method preparation, removal is therefore not allowed.")
            }
        }

        // check if all the partner is not used in the exp steps
        var nrExpSteps = existingExpSteps.length;
        for (i = 0; i < nrExpSteps; i++) {
            if (existingExpSteps[i].partnerID == partnerID){
                partnerUsed = true;
                alert("This partner is a contributing partner in the experiment steps, removal is therefore not allowed.")
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

    $('#reqTableID').on('click', 'tr', function(){

        selectedReqID = $(this).closest("tr").attr('id');

        var nrReqs = existingReqs.length;

        for (i = 0; i < nrReqs; i++) {

            if (existingReqs[i].id == selectedReqID){

                $('.reqdesc').val(existingReqs[i].description);
                $('.reqprop').val(existingReqs[i].properties);
                $('.reqdeadline').val(existingReqs[i].deadline);
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
            }
        } // end for

    }); // end on reqTable clicked

    $('#addReqID').on('click', function(){

        // check if a partner is selected
        if($("#partnerDataReq").val()){
            sendReqInfoToServer(false);
        }
        else{
            alert("Please add a partner");
        }
    });

    $('#updateReqID').on('click', function(){
        sendReqInfoToServer(true);
    });

    $('#deleteReqID').on('click', function(){

        var reqID = $('#selectedReqID').val();

        $.ajax({
            url: "/project/deletereq/",
            type: "POST",
            data: {reqID: reqID,
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken},

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
    });


    //
    // FUNCTIONS FOR THE STEPS
    //

    $('#expStepTableID').on('click', 'tr', function(){

        selectedExpStepID = $(this).closest("tr").attr('id');
        var nrExpSteps = existingExpSteps.length;

        for (i = 0; i < nrExpSteps; i++) {

            if (existingExpSteps[i].id == selectedExpStepID){

                $('.expstepdesc').val(existingExpSteps[i].description);
                $('.expstepprop').val(existingExpSteps[i].properties);
                $('.expstepdeadline').val(existingExpSteps[i].deadline);

                contrPartner = getPartnerByID(existingExpSteps[i].partnerID);

                $('#partnerExpStep').val(contrPartner.id);
                $('#selectedExpStepID').val(selectedExpStepID);

                // update buttons
                $('#updateExpStepID').removeClass( "disabled" ).addClass( "active" );
                $('#updateExpStepID').prop( "disabled", false);
                $('#deleteExpStepID').removeClass( "disabled" ).addClass( "active" );
                $('#deleteExpStepID').prop( "disabled", false);
            }
        } // end for

    }); // end on expStepTable clicked

    $('#addExpStepID').on('click', function(){

        console.log($("#partnerExpStep").val())

        // check if a partner is selected
        if($("#partnerExpStep").val()){
            sendExpStepInfoToServer(false);
        }
        else{
            alert("Please add a partner");
        }
    });

    $('#updateExpStepID').on('click', function(){
        sendExpStepInfoToServer(true);
    });

    $('#deleteExpStepID').on('click', function(){

        var expStepID = $('#selectedExpStepID').val();
        console.log(expStepID)

        $.ajax({
            url: "/project/deletestep/",
            type: "POST",
            data: {expStepID: expStepID,
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken},

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
    });
    
    
    //
    // FUNCTIONS FOR THE REPORTING
    //

    $('#reportingTableID').on('click', 'tr', function(){

        selectedReportingID = $(this).closest("tr").attr('id');
        var nrReportings = existingReportings.length;

        for (i = 0; i < nrReportings; i++) {

            if (existingReportings[i].id == selectedReportingID){

                $('.reportingdesc').val(existingReportings[i].description);
                $('.reportingprop').val(existingReportings[i].properties);
                $('.reportingdeadline').val(existingReportings[i].deadline);

                contrPartner = getPartnerByID(existingReportings[i].partnerID);

                $('#partnerReporting').val(contrPartner.id);
                $('#selectedReportingID').val(selectedReportingID);

                // update buttons
                $('#updateReportingID').removeClass( "disabled" ).addClass( "active" );
                $('#updateReportingID').prop( "disabled", false);
                $('#deleteReportingID').removeClass( "disabled" ).addClass( "active" );
                $('#deleteReportingID').prop( "disabled", false);
            }
        } // end for

    }); // end on reportingTable clicked

    $('#addReportingID').on('click', function(){

        // check if a partner is selected
        if($("#partnerReporting").val()){
            sendReportingInfoToServer(false);
        }
        else{
            alert("Please add a partner");
        }
    });

    $('#updateReportingID').on('click', function(){
        sendReportingInfoToServer(true);
    });

    $('#deleteReportingID').on('click', function(){

        var reportingID = $('#selectedReportingID').val();
        console.log(reportingID)

        $.ajax({
            url: "/project/deletereporting/",
            type: "POST",
            data: {reportingID: reportingID,
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken},

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
    });    

});
