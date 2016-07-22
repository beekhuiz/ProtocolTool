function isEven(n) {
   return n % 2 == 0;
}

function writeLabelLine(tablebody, index, label, text){

    var trclass = ""
    if(isEven(index)){
        //trclass = "trdark";
        trclass = "";
    }

    $(tablebody).append(
          '<tr class="' + trclass + '">' +
          '<td class="col-md-2"><strong>' + label + '</strong></td>' +
          '<td class="col-md-10">' + text + '</td></tr>')
}

//function writePartnerLine(tablebody, name, email, organisation, lead){
//
//    console.log("Added partner")
//
//     var leadText = ""
//     if(lead == 'True'){
//        leadText = " (lead)"
//     }
//
//     $(tablebody).append(
//            '<tr>' +
//            '<td class="col-md-2">' + name + leadText + '</td>' +
//            '<td class="col-md-2">' + email + '</td>' +
//            '<td class="col-md-2">' + organisation + '</td></tr>')
//}