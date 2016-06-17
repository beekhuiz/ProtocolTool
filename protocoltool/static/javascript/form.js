
// Validate form (client side) TODO: Make validation checks for all fields -->
function checkform() {
    document.getElementById('dataset_form').submit();
}


function refreshPartners(){
    // Reset all stuff
    $('#id_name').val("");
    $('#id_email').val("");
    $('#id_lead').prop('checked', false);

    // update buttons
    $('#updatePartnerID').removeClass( "active" ).addClass( "disabled" );
    $('#deletePartnerID').removeClass( "active" ).addClass( "disabled" );

    // reset selected partner ID
    $('#selectedPartnerID').val('-99')

    var arrayLength = existingPartners.length;
    $("#partnerTable tbody tr").remove();

    for (i = 0; i < arrayLength; i++) {
        $("#partnerTable > tbody").append('<tr class="partnerRow"><td class="col-md-8 partnername">' + existingPartners[i].name + '</td>' +
                                '<td class="col-md-4">' + existingPartners[i].lead + '</td></tr>');
    }
}


$(document).ready(function(){

    $('#partnerTable').on('click', 'tr', function(){

        console.log("partnerList clicked");
        //console.log($(this).find(".partnername").text());

        selectedPartner = $(this).find(".partnername").text();

        var arrayLength = existingPartners.length;

        for (i = 0; i < arrayLength; i++) {

            if(existingPartners[i].name == selectedPartner){
                $('#id_name').val(existingPartners[i].name);
                $('#id_email').val(existingPartners[i].email);

                if(existingPartners[i].lead == 'True'){
                    console.log("Check the cb!");
                    $('#id_lead').prop('checked', true);
                    //cb.val(cb.prop('checked'));
                }
                else{
                    $('#id_lead').prop('checked', false);
                }

                $('#selectedPartnerID').val(existingPartners[i].id);

                // update buttons
                $('#updatePartnerID').removeClass( "disabled" ).addClass( "active" );
                $('#deletePartnerID').removeClass( "disabled" ).addClass( "active" );
            }
        }
    });


    $('#addPartnerID').on('click', function(){

//        var arrayLength = existingPartners.length;
//
//        // get a new partnerID (max ID + 1)
//        var maxPartnerID = 0;
//        for (i = 0; i < arrayLength; i++) {
//            if(existingPartners[i].id > maxPartnerID){
//                maxPartnerID = existingPartners[i].id;
//            }
//        }
//
//        var lead = 'False';
//        if($('#checkbox').is(':checked')){
//            lead = 'True';
//        }
//        newID = maxPartnerID + 1
//
//        var newPartner = {"id": String(newID), "name": $('#id_name').val(), "email": $('#id_email').val(), "lead": lead};
//        existingPartners.push(newPartner);
//        console.log(newPartner);
//        console.log("Existing: ");
//        console.log(existingPartners);
//
//        // Reset all stuff
//        $('#id_name').val("");
//        $('#id_email').val("");
//        $('#id_lead').prop('checked', false);
//
//        // update buttons
//        $('#updatePartnerID').removeClass( "active" ).addClass( "disabled" );
//        $('#deletePartnerID').removeClass( "active" ).addClass( "disabled" );
//
//        // reset selected partner ID
//        $('#selectedPartnerID').val('-99')
//
//        // update list
//        $('#partnerList').empty();
//
//        var arrayLength = existingPartners.length;
//        for (i = 0; i < arrayLength; i++) {
//            $('#partnerList').append("<li>" + existingPartners[i].name + "</li>");
//        }
        // get all filled in data
        var lead = 'False';
        if($('#id_lead').is(':checked')){
            lead = 'True';
        }

        console.log("lead: ")
        console.log(lead)


        $.ajax({
            url: "/project/addpartner/",
            type: "POST",
            data: {datasetID: datasetID,
                   name: $('#id_name').val(),
                   email: $('#id_email').val(),
                   lead: lead,
                   csrfmiddlewaretoken: csrfmiddlewaretoken},

            // handle a successful response
            success : function(json) {
                console.log("success"); // another sanity check
                console.log(json['existingPartnersJSON']); // another sanity check
                existingPartners = JSON.parse(json['existingPartnersJSON']);
                refreshPartners();
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });

    });


    $('#updatePartnerID').on('click', function(){

        var partnerID = $('#selectedPartnerID').val();

        var lead = 'False';
        if($('#id_lead').is(':checked')){
            lead = 'True';
        }

        $.ajax({
            url: "/project/updatepartner/",
            type: "POST",
            data: {partnerID: partnerID,
                   datasetID: datasetID,
                   name: $('#id_name').val(),
                   email: $('#id_email').val(),
                   lead: lead,
                   csrfmiddlewaretoken: csrfmiddlewaretoken},

            // handle a successful response
            success : function(json) {
                console.log("success"); // another sanity check
                console.log(json['existingPartnersJSON']); // another sanity check
                existingPartners = JSON.parse(json['existingPartnersJSON']);
                refreshPartners();
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
//        var partnerID = $('#selectedPartnerID').val();
//        var arrayLength = existingPartners.length;
//
//        for (i = 0; i < arrayLength; i++) {
//            if(existingPartners[i].id == partnerID){
//
//                console.log("Name: " + $('#id_name').val());
//
//                existingPartners[i].name = $('#id_name').val();
//                existingPartners[i].email = $('#id_email').val();
//
//                if($('#checkbox').is(':checked')){
//                    existingPartners[i].lead = 'True';
//                }
//                else{
//                    existingPartners[i].lead = 'False';
//                }
//            }
//        }
//
//        // Reset all stuff
//        $('#id_name').val("");
//        $('#id_email').val("");
//        $('#id_lead').prop('checked', false);
//
//        // update buttons
//        $('#updatePartnerID').removeClass( "active" ).addClass( "disabled" );
//        $('#deletePartnerID').removeClass( "active" ).addClass( "disabled" );
//
//        // reset selected partner ID
//        $('#selectedPartnerID').val('-99')
//
//        // update list
//        $('#partnerList').empty();
//        for (i = 0; i < arrayLength; i++) {
//            $('#partnerList').append("<li>" + existingPartners[i].name + "</li>");
//        }
    });


    $('#deletePartnerID').on('click', function(){

        var partnerID = $('#selectedPartnerID').val();

        $.ajax({
            url: "/project/deletepartner/",
            type: "POST",
            data: {partnerID: partnerID,
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken},

            // handle a successful response
            success : function(json) {
                console.log("success"); // another sanity check
                console.log(json['existingPartnersJSON']); // another sanity check
                existingPartners = JSON.parse(json['existingPartnersJSON']);
                refreshPartners();
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
//        console.log("Partner ID: " + partnerID);
//
//        var arrayLength = existingPartners.length;
//        console.log("existingPartners before splice: ")
//        console.log(existingPartners);
//        console.log("Array length before splice: " + arrayLength);
//
//        for (i = 0; i < arrayLength; i++) {
//            if(existingPartners[i].id == partnerID){
//                console.log("Remove partner id");
//                var indexPartnerToRemove = i;
//            }
//        }
//
//        existingPartners.splice(indexPartnerToRemove, 1);
//
//        $('#partnerList').empty();
//
//        // update the array length after the splice
//        var arrayLength = existingPartners.length;
//
//        console.log("existingPartners after splice: ")
//        console.log(existingPartners);
//        console.log("Array length after splice: " + arrayLength);
//
//        for (i = 0; i < arrayLength; i++) {
//            $('#partnerList').append("<li>" + existingPartners[i].name + "</li>");
//        }
//
//        $('#id_name').val("");
//        $('#id_email').val("");
//        $('#id_lead').prop('checked', false);
//
//        // update buttons
//        $('#updatePartnerID').removeClass( "active" ).addClass( "disabled" );
//        $('#deletePartnerID').removeClass( "active" ).addClass( "disabled" );
//
//        // reset selected partner ID
//        $('#selectedPartnerID').val('-99')
    });

});
