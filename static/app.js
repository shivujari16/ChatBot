let sendButton = document.querySelector(".send__button");
//let data = [
//    {
//        //fee
//        "0": "college fee",
//        "1": "exam fee",
//        "2": "fees in wrong category",
//        "3": "paid less fees",
//        "4": "entered incorrect info",
//        "5": "fee online process"
//    },
//    {
//        //marksheet
//        "0":"Name correction",
//    }
//]

let data = {
    "fee": [
        //fee
        "fee",
        "College Fee",
        "Exam Fee",
        "Paid Less Fee",
        "Entered incorrect info",
        "Online process for paying fees",
        "Paid fees in wrong category"
    ],
    "marksheet": [
        "marksheet",
        "Name correction",
        "duplicate marksheet"
    ],
    "scholarship": [
        "scholarship",
        "Scholarship type",
        "Contact details"
    ],
    "library":[
        "library",
        "Issue a book",
        "Facility",
        "Library timing"
    ],
    "hostel":[
        "hostel",
        "Boys hostel details",
        "Girls hostel detail",
        "Apply for hostel",
        "Mess facility"
    ]
}

class Chatbox
{

  constructor()
  {
    this.args =
    {
      openButton: document.querySelector(".chatbox__button"),
      chatBox: document.querySelector(".chatbox__support"),
      sendButton: document.querySelector(".send__button"),
    };
    this.state = false;
    this.messages = [];
  }



  display()
  {
    const { openButton, chatBox, sendButton } = this.args;
    openButton.addEventListener("click", () => this.toggleState(chatBox));
    sendButton.addEventListener("click", () => this.onSendButton(chatBox));

    const node = chatBox.querySelector("input"); //ithr input liye
    node.addEventListener("keyup", ({ key }) => { //keyboard se enter krne ke liye
      if (key === "Enter") {
        this.onSendButton(chatBox);
      }
    });
  }
  toggleState(chatbox) {
    this.state = !this.state;
    if (this.state)
    {
      chatbox.classList.add("chatbox--active");
    }
    else
    {
      chatbox.classList.remove("chatbox--active");
    }
  }
  onSendButton(chatbox)
  {
    let textField = chatbox.querySelector("input");
    let text1 = textField.value; //input ki value li
    if (text1 === "") //agar kuch ni dala toh
    {
      return;
    }
    let msg1 = { name: "User", message: text1 }; //jab user message type krke send krega
    this.messages.push(msg1); //tab woh text messages m push kr denge
    textField.value = "";
    sendButton.style.display = "none";


    fetch($SCRIPT_ROOT + "/predict", { //ye wala JSON ka part h, jisme hum database comb krte
      method: "POST",
      body: JSON.stringify({ message: text1 }),
      mode: "cors",
      headers: { "Content-Type": "application/json" },
    })
      .then((r) => r.json())
      .then((r) => {
        let msg2 = { name: "SDF", message: r.answer }; //response ke liye
        this.messages.push(msg2); //ye response ko add kiye messages mein
        this.updateChatText(chatbox);
        textField.value = ""; //wapis textfield wala space clear kr denge


      })
      .catch((error) => { //error ke liye
        console.error("Error: ", error);
        this.updateChatText(chatbox);
        textField.value = "";
      });
  }



  updateChatText(chatbox)
  {

    let html = "";

    this.messages.slice().reverse().forEach(function (item)
      {
        if (item.name === "SDF")
        {

          if(Array.isArray(item.message)) {
              let allOptions = item.message;

            html += '<div class="click_btn_boxes">';
            html += '<div class="messages__item messages__item--visitor">' +
                'Choose appropriate option' +
            "</div>";
            for(let i=1;i<allOptions.length;i++) {
                html += '<button class="click_btn" onclick=chatbox.clickBtnHandleMessage(chatbox,"' +  allOptions[0]  + '",' + i + ') ><span class="click_btn_text">' + allOptions[i] + '</span></button>'
            }
            html += '</div>';

          }
          else {
              html +=
                '<div class="messages__item messages__item--visitor">' +
                item.message +
                "</div>";
          }

        }

        else
        {
          html +=
            '<div class="messages__item messages__item--operator">' +
            item.message +
            "</div>";
        }

      });


        //text response
        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;

  }

  clickBtnHandleMessage(chatbox,key,index) {
       let msg = data[key][index];
       let msg2 = { name: "SDF", message: msg }; //response ke liye
       this.messages.push(msg2); //ye response ko add kiye messages mein
       this.updateChatText(chatbox.args.chatBox);
  }


  refundFeesResponse(chatbox)
  {
        //button
        var button = document.createElement("button");
        button.innerHTML = "Do Something";var body = chatbox.querySelector(".chatbox__messages");body.appendChild(button);button.addEventListener ("click", function() {alert("did something");});

  }
}


const chatbox = new Chatbox();
chatbox.display();

sendButton.style.display = "none";

function handleInputChangeField() {
    let inputValue = document.querySelector("input");
    if(inputValue.value.length === 0) {
        sendButton.style.display = "none";
    }
    else {
        sendButton.style.display = "flex";
    }
}