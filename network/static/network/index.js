document.addEventListener('DOMContentLoaded', function(){
    like_check();

    document.addEventListener('click', event=>{
        //event.preventDefault()
        const element = event.target;
        if(element.className==='like'){
            event.preventDefault()
            
            fetch(`like/${element.parentElement.className}`)
            .then(response => response.json())
            .then(data => {

                if (data.status==="success"){
                    like_check();
                    element.parentElement.children[1].textContent = data.num_likes
                    console.log(element.parentElement.children[1]);
                }
            })
        }
    })

    
    document.addEventListener('click', event =>{
        const element = event.target;
        if(element.className === 'edit-post'){
            const parents =  element.parentElement;
            console.log(parents.children);
            /*parents.children[5].style.display = 'none';
            parents.children[4].style.display = 'block';
            parents.children[0].style.display = 'none';
            parents.children[1].style.display = 'block';*/

            //hide post content
            parents.children[3].style.display = 'none';
            //display textarea
            parents.children[2].style.display = 'block';
            //hide edit button
            parents.children[5].style.display = 'none';
            //show save btn
            parents.children[6].style.display = 'display';





            document.addEventListener('click', event =>{
                const save = event.target;
                if(save.className === 'save'){
                    const parent = save.parentElement;
                    const new_post = parent.children[4].value;
                    fetch(`editpost/${save.parentElement.id}?newpost=${new_post}`)
                    .then(response => response.json())
                    .then(result => {
                        if(result.status=== 'success'){
                            parent.children[5].textContent = new_post;
                            parent.children[5].style.display ='block';
                            parent.children[4].style.display = 'none';
                            parent.children[0].style.display = 'block';
                            parent.children[1].style.display = 'none';
                            

                        }
                        else{
                            console.log(result.status)
                        }

                    })
                }
                
            })
            
            

            

        }

    } )
})
function like_check(){
    document.querySelectorAll('.like').forEach(e =>{
        fetch(`/check_like?id=${e.parentElement.className}`)
        .then(res=>res.json())
        .then(data=>{
            if (data.isLike){
                e.textContent='Unlike'
            }
            else{
                e.textContent = 'Like'
            }
        })
    });
    
}