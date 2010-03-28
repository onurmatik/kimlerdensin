var el_arr = new Array();	// array to hold all of our important 'elements': ['id', 'content_type_repr', 'object_id_repr']

function generic_init() {
	select_el_arr = document.getElementsByTagName('select');
	content_type_el_arr = new Array();
	for (var i = 0; i < select_el_arr.length; i++){
		if (select_el_arr[i].id.indexOf('content_type') > -1) {	// grab all 'select' elements which are 'content_type's
			content_type_args = select_el_arr[i].id.split('.');	// could be id_modelname.x.content_type or id_modelname.content_type
			
			if (content_type_args.length == 3) {
				content_type_id = content_type_args[1];
				content_type_repr = select_el_arr[i].id;
				object_id_repr = content_type_args[0] + '.' + content_type_args[1] + '.object_id';	
			} else {
				content_type_id = '';
				content_type_repr = select_el_arr[i].id;
				object_id_repr = 'id_object_id';
			}

			temp_arr = new Array(content_type_id, content_type_repr, object_id_repr);

			el_arr.push(temp_arr);
		}
	}
	
	for (var i = 0; i < el_arr.length; i++) {
		// let's do some magic			
		arr_index = i;
		content_type_el = document.getElementById(el_arr[arr_index][1]);
		content_type_el.setAttribute('onchange', 'javascript:generic_change(' + arr_index + ');');
		//content_type_el.addEventListener('onchange', generic_change(arr_index), false);
		a = generic_init_links(arr_index);
	}
};

function generic_init_links(arr_index) {
	content_type_el = document.getElementById(el_arr[arr_index][1]);
	object_id_el = document.getElementById(el_arr[arr_index][2]);
    parent_el = object_id_el.parentNode;
    if (content_type_el.value != '') {
    	for (var i = 0; i < model_url_arr.length; i++)
    		if (model_url_arr[i][0] == content_type_el.value)
    			related_lookup_url = '../../../' + model_url_arr[i][1];
    	parent_el.innerHTML += '<a href="' + related_lookup_url + '" class="related-lookup" id="lookup_' + object_id_el.id + '" onclick="return showRelatedObjectLookupPopup(this);"><img src="/admin_media/img/admin/selector-search.gif" width="16" height="16" alt="Lookup"></a>';
    }
};

function generic_link(arr_index) {
	content_type_el = document.getElementById(el_arr[arr_index][1]);
	object_id_el = document.getElementById(el_arr[arr_index][2]);
	
    link = document.getElementById('lookup_' + object_id_el.id);	// Check for the existence of a related-lookup link already
    if (!link){
        parent_el = object_id_el.parentNode;
        for (var i = 0; i < model_url_arr.length; i++) {
        	//alert('checking model_url_arr['+i+'] = ' + model_url_arr[i][0] +' against el_arr['+arr_index+'][1].value = ' + el_arr[arr_index][1].value);
        	if (model_url_arr[i][0] == content_type_el.value)
        		related_lookup_url = '../../../' + model_url_arr[i][1];
        }
        parent_el.innerHTML += '<a href="' + related_lookup_url + '" class="related-lookup" id="lookup_' + object_id_el.id + '" onclick="return showRelatedObjectLookupPopup(this);"><img src="/admin_media/img/admin/selector-search.gif" width="16" height="16" alt="Lookup"></a>';
    } else {
        // Link already exists, change it's href
        match = false;
        for (var i = 0; i < model_url_arr.length; i++) {
        	if (model_url_arr[i][0] == content_type_el.value) {
        		related_lookup_url = '../../../' + model_url_arr[i][1];
        		link.href = related_lookup_url;
        		match = true;
        	}
        }
        
        if (!match)
        	link.parentNode.removeChild(link);
    }
    
    return true;
};
    
function generic_change(arr_index) {
	//alert('you passed generic_change an arr_index of ' + arr_index);
    el1 = document.getElementById(el_arr[arr_index][1]);
    el2 = document.getElementById(el_arr[arr_index][2]);
    generic_link(arr_index, el1, el2);
    
    return true;
};

window.addEventListener('load', generic_init, false);