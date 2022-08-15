
 
                // $('#btn_disconnect').on('click',function(){
                //     console.log("ENTRE A btn_disconnect")
                //     var post_url = $("#btn_disconnect").data("url");
                //     console.log("post_url", post_url)
                //     //const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                //     $.ajax({
                //              url: post_url,
                //              type: "POST",
                //              data: {'slug': 'Soy javascript disconnect', 'csrfmiddlewaretoken': csrftoken},                            
                //              success:function(response) {
                //                 var chk= document.getElementById('btn_disconnect').disabled=false;
                //                 //chk.disabled = true;
                //                  //chk.style.display="none";
                //                  //document.getElementById("btn_disconnect").setAttribute("disabled","disabled");
                //                  console.log(chk)
                              
           
                //                   var message = response.content.message
                //                   alert(message);
                                  
                //               },
                //               error:function(rs, e) {
                //                      alert(rs.responseText);
                //               }
                //         }); 
                //         return false;
                //   });


                //   $('#btn_connect').on('click',function(){
                //     console.log("ENTRE A btn_connect");

                //     // document.getElementById("header").innerHTML = "Bonjour";
                //     // console.log("targetDiv ",document.getElementById("header"));

                //     var post_url = $("#btn_connect").data("url");
                //     console.log("post_url", post_url)
                //     //const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                //     $.ajax({
                //              url: post_url,
                //              type: "POST",
                //              headers: {'X-CSRFToken': csrftoken},
                //              data: {'slug': 'Soy javascript connect'}, 
                //              dataType: "json",
                //             //  data: {'slug': 'Soy javascript connect', 'csrfmiddlewaretoken': csrftoken},                            
                //              success:function(response) {
                //                 console.log("entre success")
                //                 var message = response.content.message
                //                 //location.reload();
                //                 alert(message);
                                  
                //               },
                //               error:function(rs, e) {
                //                 console.log("entre ERROR")
                //                     alert(rs.responseText);
                //               }
                //         }); 
                //         return false;
                //   });

              


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