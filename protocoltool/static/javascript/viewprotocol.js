function writeLabelLine(tablebody, label, text){

      $(tablebody).append(
            '<tr>' +
            '<td class="col-md-2"><strong>' + label + '</strong></td>' +
            '<td class="col-md-10">' + text + '</td></tr>')
}

function writePartnerLine(name, email, organisation, lead){

     var leadText = ""
     if(lead == 'True'){
        leadText = " (lead)"
     }

      $("#partnerTable > tbody").append(
            '<tr>' +
            '<td class="col-md-2">' + name + leadText + '</td>' +
            '<td class="col-md-2">' + email + '</td>' +
            '<td class="col-md-2">' + organisation + '</td></tr>')
}