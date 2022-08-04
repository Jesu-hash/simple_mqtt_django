

             
                    // $('#form_publish').on('submit', function(e) {
                    //     console.log(e)
                    //     e.preventDefault();
                    //     console.log("INGRESE A PUBLISH BUTTON")
                    //     var post_url = $("#form_publish").data("post-url");

                    //     const y = document.getElementsByTagName("input");
                    //     console.log("fffff",y)
                    //     // var val = $("#val").val();
                    //     // var comment = $("#comment").val();
                    //     // console.log("val ", val)
                    //     // console.log("comment ", comment)

                    //     var button_id = $(this).prop('id');
                    //     console.log("button_id",button_id)
                    //     var id = button_id.replace('submit_post_', '');
                    //     var textarea_id = '#id_text_publish_' + id;
                    //     var comment = $(textarea_id).val();
                    //     console.log("comment ", comment)

                    //     console.log("post_url ", post_url)
                    //     //var formData = new FormData(this);
                    //     console.log("clientID",client)

                    //     $.ajax({
                    //         url : '/publish/',
                    //         type: "POST",
                    //         headers: {'X-CSRFToken': csrftoken},
                    //         //headers: {'X-CSRFToken': '{{ csrf_token }}'},
                    //         //data : client,
                    //         data : {'client_id':client} ,
                    //         dataType: 'json',
                    //         //processData: false,
                    //         //contentType: false,
                    //         success:function(response){
                    //             var message = response.content.message
                    //             alert(message);
                    //         },
                    //         error: function(error){
                    //         console.log(error)
                    //         }
                    //     });
                
                    //     return false;
                    // });

 
 
                $('#btn_disconnect').on('click',function(){
                    console.log("ENTRE A btn_disconnect")
                    var post_url = $("#btn_disconnect").data("url");
                    console.log("post_url", post_url)
                    //const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                    $.ajax({
                             url: post_url,
                             type: "POST",
                             data: {'slug': 'Soy javascript disconnect', 'csrfmiddlewaretoken': csrftoken},                            
                             success:function(response) {
                                var chk= document.getElementById('btn_disconnect').disabled=false;
                                //chk.disabled = true;
                                 //chk.style.display="none";
                                 //document.getElementById("btn_disconnect").setAttribute("disabled","disabled");
                                 console.log(chk)
                              
           
                                  var message = response.content.message
                                  alert(message);
                                  
                              },
                              error:function(rs, e) {
                                     alert(rs.responseText);
                              }
                        }); 
                        return false;
                  });

              


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