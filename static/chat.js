$(() => {
    sendMsg = () => {
        let user_input = $(".input-area input").val()
        if (user_input.length == 0) return
		if (user_input[0] == "/") {
			if (user_input.substring(1) == "clear") {
				$.ajax({
					url: "/api/clear_history",
					success: () => {
						$(".chat-area").html("")
						$(".input-area input").val("")
					}
				})
			} else {
				msg = `No command "${user_input}" found.\n`
				msg+= "The following commands are supported:\n"
				msg+= "/clear: clear conversations"
				alert(msg)
				$(".input-area input").val("")
			}
			return
		}
		$.ajax({
			url: "/api/new_msg",
			method: "post",
			contentType: "application/json",
			data: JSON.stringify({
				msg: user_input
			})
		})
		$(".chat-area").append(`<div class="mine">${user_input}</div>`)
		$(".chat-area").append(`<div class="ai loading">Loading...</div>`)
		$(".input-area input").val("")
		$(".input-area input").attr("disabled", "disabled")
		$(".input-area input").attr("placeholder", "Waiting for response...")
		$(".chat-area *:last")[0].scrollIntoView({
			behavior: "smooth",
			block: "start"
		})
		listenResponse()
    }
    listenResponse = () => {
        $.ajax({
            url: "/api/get_response",
            success: (data) => {
                if (data.responsed == -1) {
                    setTimeout(listenResponse, 2000)
                } else {
                    $(".input-area input").removeAttr("disabled")
                    $(".input-area input").attr("placeholder", "Chatting...")
                    $(".chat-area .ai:last").text(data.msg.trim())
                    $(".chat-area .ai.loading").removeClass("loading")
                    $(".chat-area *:last")[0].scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    })
                }
            }
        })
    }
    $.ajax({
        async: true,
        url: "/api/get_history",
        success: (data) => {
            for (let i = 0; i < data.length; ++i) {
                who = ["mine", "ai"][data[i].who % 2]
                $(".chat-area").append(`<div class="${who}">${data[i].msg.trim()}</div>`)
            }
            if ((data.length > 0) && (data[data.length - 1].who == 0)) {
                $(".input-area input").attr("disabled", "disabled")
                $(".chat-area").append(`<div class="ai loading">Loading</div>`)
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
