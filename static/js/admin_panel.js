function uploadImage(){
    let imageInput=document.getElementById('customFile')
    let imagenName=document.getElementById('imageName')
    if (imageInput.value=="" || imageName.value==""){
        alert("Please Fill Require Data...")
    }
}

//ADD NEW POST
let addNewPostBTN=document.getElementById('addNewPostBTN');
addNewPostBTN.addEventListener('click',function (e) {
    e.preventDefault()
    postTitle=document.getElementById('post-title');
    postSlug=document.getElementById('post-slug');
    postStitle=document.getElementById('post-stitle');
    postAuthor=document.getElementById('post-author');
    postImage=document.getElementById('post-image');
    postBody=document.getElementById('post-body');
    if (postTitle.value === ""||postSlug.value === ""||postStitle.value === ""||postAuthor.value === ""||postImage.value === ""||postBody.value === ""){
        alert("Please Enter Valid Input")
    }else {
        let xhr=new XMLHttpRequest();
        xhr.open('POST',`http://127.0.0.1:5000/addnewpost`,true);
        xhr.setRequestHeader('Content-Type','application/x-www-form-urlencoded')
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
        let allData=`post-title=${postTitle.value}&post-slug=${postSlug.value}&post-stitle=${postStitle.value}&post-author=${postAuthor.value}&post-image=${postImage.value}&post-body=${postBody.value}`
        xhr.send(allData)
        }
    

    });

function deletePost(pid){
    console.log("Dleete")
    let xhr=new XMLHttpRequest();
    xhr.open('POST',`http://127.0.0.1:5000/deletePost`,true);
    xhr.setRequestHeader('Content-Type','application/x-www-form-urlencoded')
    xhr.onload=function () {
        // if(this.status===200){
        //     alert("postDeleted SuccessFully")
        // }else {
        //     alert("Delete Failed")
        // }
        document.getElementById("tr"+pid).style.display='none'
        
        
    }
    let data=`post-id=${pid}`
    xhr.send(data)



}




