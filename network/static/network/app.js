// get csrf token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');


function hide(id) {
  let element = document.getElementById(id);
  element.style.display = "None";
  return false;
}


function display_posts() {

  // clear posts view
  document.getElementById("posts").innerHTML = "";

  // get all posts
  fetch("/api/posts/all/", {
    method: "POST",
    headers: {'X-CSRFToken': csrftoken},

  }).then(response => response.json()).then(response => {
    let show_post = document.getElementById("posts");
    show_post.classList.add("container");

    if (response.posts.length === 0){
      // display message
      let message = document.createElement("h3");
      message.innerHTML = "No Posts Yet";
      show_post.append(message);
    }

    else {
      response.posts.forEach(element => {
        let row = document.createElement("li");
        row.classList.add("row")
        row.classList.add("post-info")
        row.innerHTML = `
        <div class="col-12">
          <div class="row"><div class="col-12" style="color: grey">${element.sender}</div></div>
          <div class="row"><div class="col-12">${element.content}</div></div>
        </div>
        `;
        show_post.append(row);
      });
    }

  });
}


// main
document.addEventListener("DOMContentLoaded", () => {
  // show post view if logged in
  let add_post = document.getElementById("add_post");
  if (is_authenticated) {
    add_post.style.display = "block";
    
    // submit post
    document.getElementById("new_post_form").onsubmit = () => {
      content = document.getElementById("new_post_content");

      if (content.value === "") {
        alert("content cannot be blank");
        return false;
      }

      fetch("/api/posts/new/", {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({
          content: content.value,
        })

      }).then(response => response.json()).then(response => {
        if (response.status === "success") {
          document.getElementById("add_post_success").style.display = "block";
          document.getElementById("add_post_failure").style.display = "none";
          document.getElementById("new_post_content").value = "";
          display_posts();
        } else {
          document.getElementById("add_post_failure").style.display = "block";
          document.getElementById("add_post_success").style.display = "none";
        }

      }).catch(err => {
        alert("Error! you need to log in!")
      })
      return false;
    };
  }

  // display all posts
  if (is_authenticated){
    display_posts()
  }
});