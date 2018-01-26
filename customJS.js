function bleh(Show){
if(Show == "" || Show == null){
    Show = "Alert is Empty";
}
alert(Show);
}

function lookupTweet(SearchInput, ParentInput, ChildInput){

    $(SearchInput).on( "click", function() {
      Console.log("click");
    });

    $(SearchInput).on('keyup', function(){
        var searchTerm = $(this).val().toLowerCase();
        $(ParentInput).find(ChildInput).each(function(){
        if ($(this).text().toLowerCase().indexOf(searchTerm) > -1 || searchTerm.length < 1) {
            if($(this).text().toLowerCase().indexOf(searchTerm) == 0 || searchTerm == "" || searchTerm == " "){
                $(this).collapse('hide');
            } else {
                $(this).collapse('show');
            }
        }else {
            $(this).collapse('hide');
        }
        });
    });
}

