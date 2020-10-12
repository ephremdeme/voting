var dept = {
    PRE: null,
    SoEEC: ["CSE", "ECE", "EPCE"],
    SoMMC: ["TAE", "CE", "MDME", "MSE", "MSVE"],
    SoCEA: ["A", "B", "C"]
}

var school = {
    1: "PRE",
    2: ["SoEEC", "SoMMC", "SoANS", "SoCEA"],
    3: ["SoEEC", "SoMMC", "SoANS", "SoCEA"],
    4: ["SoEEC", "SoMMC", "SoANS", "SoCEA"],
    5: ["SoEEC", "SoMMC", "SoANS", "SoCEA"]
}



$.fn.replaceOptions = function (options) {
    var self, option;

    self = this;
    $.each(options, function (index, option) {
        $option = $("<option> </option>").attr("value", option).text(option)
        self.append($option)
    })

    $("h3").hide()
}

$("#schoolselect").replaceOptions(school[2])
$("#deptselect").replaceOptions(dept['SoEEC'])

$('#search').on('click', (e) => {
    e.preventDefault()
    if ($('#key').val() != '') {
        fetch('/' + $('#searchBy').val() + '/' + $('#key').val())
            .then(res => res.json())
            .then(data => {
                if($('#searchBy').val()==='block'){
                    
                    prepareBlockVote(data['block'].transactions)
                    prepareBlock(data['block'])
                }else if($('#searchBy').val()==='vote'){
                    prepareBlockVote(data['cand'])
                }else{
                    prepareVote(data['vote'])
                    prepareBlock(data['block'])
                }
                
            })
            $("h3").show()
    }
    console.log($('#searchBy').val())

})


function prepareBlock(block){
    let table = '<tbody>'
    table +=  '<tr> ' + ' <td class="bold">Block Hash</td> <td> '  +block.hash + '</td> </tr>'
    table +=  '<tr> ' + ' <td class="bold">Block Index</td> <td> '  +block.index + '</td> </tr>'
    table +=  '<tr> ' + ' <td class="bold">Block Nonce</td> <td> '  +block.nonce + '</td> </tr>'
    table +=  '<tr> ' + ' <td class="bold">Block Timestamp</td> <td> '  +block.timestamp + '</td> </tr>'
    table +=  '<tr> ' + ' <td class="bold">Block Previous Block Hash</td> <td> '  +block.previousBlockHash + '</td> </tr>'
    table += '</tbody>'

    $("#blockTable").html(table)
}

function prepareBlockVote(voteArray){
let head = '<thead class="thead-dark"><tr><th scope="col">#</th> <th scope="col">ID</th> <th scope="col">VOTER</th> <th scope="col">CANDIDATE</th> </tr></thead>'
    let table = head+ '<tbody>'
    let i =1;
    voteArray.forEach(element => {
        table +=  '<tr> <th scope="row">' + i +  '</th>  <td> '  +element.id + '</td> <td> '  +element.from_address + '</td>  <td> '  +element.to_address + '</td> </tr>'
        i +=1
    });
    table += '</tbody>'
    $("#voteTable").html(table)
}

function prepareVote(vote){
    let table = '<tbody>'
    
        table +=  '<tr> ' + ' <td class="bold">Vote ID</td> <td> '  +vote.id + '</td> </tr>'
        table +=  '<tr> ' + ' <td class="bold">Voter Address</td> <td> '  +vote.from_address + '</td> </tr>'
        table +=  '<tr> ' + ' <td class="bold">Candidate</td> <td> '  +vote.to_address + '</td> </tr>'

    table += '</tbody>'
    $("#voteTable").html(table)
}

function prepareResult(vote){
    let table = '<tbody>'

        table +=  '<tr> ' + ' <td class="bold">Vote ID</td> <td> '  +vote.id + '</td> </tr>'
        table +=  '<tr> ' + ' <td class="bold">Voter Address</td> <td> '  +vote.from_address + '</td> </tr>'
        table +=  '<tr> ' + ' <td class="bold">Candidate</td> <td> '  +vote.to_address + '</td> </tr>'

    table += '</tbody>'
    $("#voteTable").html(table)
}


console.log("hello")
