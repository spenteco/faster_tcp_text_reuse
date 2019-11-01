
function toggle_all_matches_report() {
    
    if ($('#all_matches_report_toggle').html() == 'Show summary report') {

        $('#clicked_match_details').html('');

        $('#all_matches_report_toggle').html('Hide summary report');
        $('#all_matches_table').css('display', 'block');
    }
    else {

        $('#clicked_match_details').html('');

        $('#all_matches_report_toggle').html('Show summary report');
        $('#all_matches_table').css('display', 'none');
    }

}

function set_normal_text_links() {

    $('.links').each(function() {
        var links = $(this).attr('link_data').split(';');
        if (links.length > 1) {
            var new_font_size = 16;
            $(this).css('font-size', new_font_size + 'px');
        }
        $(this).css('background-color', '#FFFF99');
    });

    $('.links').mouseover(function() {
        $(this).css({'text-decoration': 'underline',
                    'color': 'blue',
                    'font-weight': 'bold',
                    'cursor': 'pointer'});
        
    });

    $('.links').mouseout(function() {
        $(this).css({'text-decoration': 'none',
                    'color': 'black',
                    'font-weight': 'normal',
                    'cursor': 'default'});
    });

    $('.links').click(function(e) {

        var links = $(this).attr('link_data').split(';');

        var ids_and_dates = [];
        for (var a = 0; a < links.length; a++) {
            var tcp_id = links[a].split(',')[1];
            var m = metadata_lookup_table[tcp_id];
            ids_and_dates.push([m[2], tcp_id]);
        }

        ids_and_dates.sort();
        var unique_ids_and_dates = [ids_and_dates[0],];

        for (var a = 0; a < ids_and_dates.length; a++) {
            var b = unique_ids_and_dates.length - 1;
            if (ids_and_dates[a][1] == unique_ids_and_dates[b][1]) {
            }
            else {
                unique_ids_and_dates.push(ids_and_dates[a]);
            }
        }
        
        out_html = '';
        for (var a = 0; a < unique_ids_and_dates.length; a++) {
            var tcp_id = unique_ids_and_dates[a][1];
            var m = metadata_lookup_table[tcp_id];
            out_html = out_html + '<div class="metadata_display_line">' + 
                                        //'<span class="mdl_tcp_id">' + tcp_id + '</span>' + 
                                        '<span class="mdl_year">' + m[2] + '</span>' + 
                                        '<span class="mdl_author">' + m[0].substring(0, 30) + '</span>' + 
                                        '<spa class="mdl_title">' + m[1].substring(0, 50) + '</span>' + 
                                    '</div>';
        }        
        out_html = '<div id="metadata_display_block">' + out_html + '</div>'

        $('#clicked_match_details').html(out_html);
        $('#metadata_display_block').css({'position': 'absolute', 'top': e.pageY + 'px'});
        

    });
}

function handle_table_link(tcp_id, e) {

    $('#clicked_match_details').html('');

    var matching_tokens = [];

    $('.links').each(function() {
        var links = $(this).attr('link_data').split(';');
        for (var a = 0; a < links.length; a++) {
            var link_parts = links[a].split(',');
            if (link_parts[1] == tcp_id) {
                matching_tokens.push([link_parts[0], $(this).html()]);
                break;
            }
        }
    });

    var m = metadata_lookup_table[tcp_id];

    var all_matching_text = '<div class="matching_text_metadata">' + 
                                    '<span class="mtm_year">' + m[2] + '</span>' + 
                                    '<span class="mtm_author">' + m[0].substring(0, 30) + '</span>' + 
                                    '<spa class="mtm_title">' + m[1].substring(0, 50) + '</span>' + 
                                '</div>';

    if (matching_tokens.length == 0) {
        all_matching_text = all_matching_text + '<div class="matching_text"><i>Matching sequences not available for this text.</i></div>';
    }
    else {

        var last_link_n = '';
        var link_text = ''

        for (var a = 0; a < matching_tokens.length; a++) {
            if (matching_tokens[a][0] != last_link_n && last_link_n > '') {
                all_matching_text = all_matching_text + '<div class="matching_text">' + link_text + '</div>';
                link_text = '';
            }
            last_link_n = matching_tokens[a][0];
            if (link_text > '') {
                link_text = link_text + ' ';
            }
            link_text = link_text + matching_tokens[a][1];
        }
                
        all_matching_text = all_matching_text + '<div class="matching_text">' + link_text + '</div>';
    }

    $('#clicked_match_details').html('<div id="all_matching_text">' + all_matching_text + '</div>');
    $('#all_matching_text').css({'position': 'absolute', 'top': e.pageY + 'px'});
}

function noop() {
}

$( document ).ready(function() {

    $('#all_matches_table').append('<thead><tr><th>year</th><th>author</th><th>title</th><th>tokens matches</th></tr></thead><tbody id="all_matches_tbody"></tbody>');
    
    for (var a = 0; a < text_counts_table.length; a++) {
        $('#all_matches_tbody').append('<tr><<td>' + text_counts_table[a][3] + 
                                        '</td><td>' + text_counts_table[a][1].substring(0, 30) +
                                        '</td><td><a href="javascript:noop();" onclick="javascript:handle_table_link(\'' + 
                                            text_counts_table[a][0] + 
                                            '\', event);">' + 
                                            text_counts_table[a][2].substring(0, 50) + "</a>" + 
                                        '</td><td class="numeric_field">' + text_counts_table[a][5] + 
                                        '</td></tr>');
    };

    $('#all_matches_table').tablesorter(); 

    set_normal_text_links();
});
