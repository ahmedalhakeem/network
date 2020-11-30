document.addEventListener('DOMContentLoaded', function(){
    
    document.addEventListener('click', event =>{
        const element = event.target;
        if(element.className === 'edit-post'){
            const parents =  element.parentElement;
            console.log(parents.children);
            parents.children[5].style.display = 'none';
            parents.children[4].style.display = 'block';
            parents.children[0].style.display = 'none';
            parents.children[1].style.display = 'block';

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