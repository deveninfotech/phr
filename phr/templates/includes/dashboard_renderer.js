frappe.provide("templates/includes");
{% include "templates/includes/utils.js" %}

function render_dashboard(profile_id){
	function render_providers(profile_id){
		
	}
	function render_linked_phr(profile_id){
		frappe.call({
			method:'phr.templates.pages.profile.get_linked_phrs',
			args:{'profile_id':profile_id},
			callback: function(r) {
				console.log(r)
				render_lphr(r.message)
				/*if(r.message) {
					$("input").val("");
					var dialog = frappe.msgprint(r.message);
				}*/
			}
		})
	
	}
	function render_emer_details(profile_id){
		console.log("emer")
	}
	function render_to_do(profile_id){
		console.log("to_do")
	}
	function bind_ids(profile_id){
		console.log("ids")
	}
	function render_middle_section(profile_id){
		console.log("middle")
	}
	function render_advertisements(profile_id){
		console.log("adv")	
	}	
	return {
        render_providers: render_providers,
        render_linked_phr: render_linked_phr,
        render_emer_details: render_emer_details,
        render_to_do: render_to_do,
        bind_ids: bind_ids,
        render_middle_section: render_middle_section,
        render_advertisements:render_advertisements
    }
    function render_lphr(data){
    	var me=this
		$('#linkedphr').find('p.nophr').remove()
		$wrap=$('#linkedphr')
		console.log(data.actualdata)		
		meta=JSON.parse(data.actualdata)
		meta_dic={}
		$.each(meta,function(i,data){
			$(repl_str('<div class="list-group-item-side %(entityid)s">\
			<a noherf data-name=%(entityid)s>%(person_firstname)s </a>\
			</div>', data.profile)).appendTo($wrap)
		})
    }
}

