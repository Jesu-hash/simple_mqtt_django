
                  function publish(id) {
                    console.log("ID", id)

                    console.log("INGRESE A PUBLISH BUTTON")
                        var post_url = $("#form_publish").data("post-url");

                        const msg = document.getElementById("text_publish_"+id).value;
                        console.log("id_text_publish",msg)
                       

                        console.log("post_url ", post_url)
                        //var formData = new FormData(this);
     

                        $.ajax({
                            url : '/publish/',
                            type: "POST",
                            headers: {'X-CSRFToken': csrftoken},
                            //headers: {'X-CSRFToken': '{{ csrf_token }}'},
                            //data : client,
                            data : {'client_id':id, 'msg': msg},
                            dataType: 'json',
                            //processData: false,
                            //contentType: false,
                            success:function(response){
                                var message = response.content.message
                                alert(message);
                            },
                            error: function(error){
                            console.log(error)
                            }
                        });
                
                        return false;
                }