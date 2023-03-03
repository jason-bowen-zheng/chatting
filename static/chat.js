$(() => {
    sendMsg = () => {
        let user_input = $(".input-area input").val()
        if (user_input.length > 0) {
            if (user_input == "/clear") {
                $.ajax({
                    url: "/api/clear_history",
                    success: () => {
                        $(".chat-area").html("")
                        $(".input-area input").val("")
                    }
                })
                return
            }
            $(".chat-area").append(`<div class="mine"><img class="avatar" src="/static/mine.png"><div class="msg">${user_input}</div></div>`)
            $(".chat-area").append(`<div class="ai loading"><img class="avatar" src="/static/ai.png"><div class="msg">Loading...</div></div>`)
            $(".input-area input").val("")
            $(".input-area input").attr("disabled", "disabled")
            $.ajax({
                url: "/api/new_msg",
                method: "post",
                contentType: "application/json",
                data: JSON.stringify({
                    msg: user_input
                })
            })
            listenResponse()
        }
    }
    listenResponse = () => {
        $.ajax({
            url: "/api/get_response",
            success: (data) => {
                if (data.responsed == -1) {
                    setTimeout(listenResponse, 2000)
                } else {
                    $(".input-area input").removeAttr("disabled")
                    $(".chat-area .ai:last .msg").text(data.msg.trim())
                    $(".chat-area .ai.loading").removeClass("loading")
                }
            }
        })
    }
    $.ajax({
        async: true,
        url: "/api/get_history",
        success: (data) => {
            for (let i = 0; i < data.length; ++i) {
                who = ["mine", "ai"][i % 2]
                $(".chat-area").append(`<div class="${who}"><img class="avatar" src="/static/${who}.png"><div class="msg">${data[i].trim()}</div></div>`)
            }
			if (data.length % 2 != 0) {
            	$(".input-area input").attr("disabled", "disabled")
            	$(".chat-area").append(`<div class="ai loading"><img class="avatar" src="/static/ai.png"><div class="msg">Loading...</div></div>`)
				listenResponse()
			}
        }
    })
    $(".input-area input").keypress((event) => {
        if (event.which == 13) {
            sendMsg();
        }
    })
    $(".input-area .send-btn").click(sendMsg)
})
