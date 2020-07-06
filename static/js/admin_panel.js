/*function uploadImage(){
    let imageInput=document.getElementById('customFile')
    let imagenName=document.getElementById('imageName')
    if (imageInput.value=="" || imageName.value==""){
        alert("Please Fill Require Data...")
    }
}

let addNewPostBTN=document.getElementById('addNewPostBTN');
addNewPostBTN.addEventListener('click',function (e) {
    e.preventDefault()
    postTitle=document.getElementById('post-title');
    postSlug=document.getElementById('post-slug');
    postStitle=document.getElementById('post-stitle');
    postAuthor=document.getElementById('post-author');
    postImage=document.getElementById('post-image');
    postBody=document.getElementById('post-body');
    let xhr=new XMLHttpRequest();
    xhr.open('POST',`http://127.0.0.1:5000/addnewpost`,true);
    xhr.setRequestHeader('Content-Type','application/json')
    xhr.onload = function (){
            postTitle.value = "";
            postSlug.value = "";
            postStitle.value = "";
            postAuthor.value = "";
            postImage.value = "";
            postBody.value = "";
        if(this.status===200){
            
            alert("Data Added Succesfully");
        }else {
            alert("Internal System Error...")
        }
    }
    allData={
    'post-title':postTitle.value,
    'post-slug':postSlug.value,
    'post-stitle':postStitle.value,
    'post-author':postAuthor.value,
    'post-image':postImage.value,
    'post-body':postBody.value
    }
    allData=JSON.stringify(allData)
    xhr.send(allData)

   
    console.log(allData)

    })

*/
