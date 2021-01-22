class ApplicationControl{
    constructor(control_url, play_url,getData){
        this.state = "stopped" // started, stopped, paused
        this.control_url = control_url
        this.play_url = play_url
        this.getData = getData
        this.$click_start_button_handler()
        this.$click_stop_button_handler()
        this.$click_pause_button_handler()
    }
    $change_state(){
        switch (this.state){
            case "started":
                $(".application-control").find(".btn").removeClass().addClass("btn btn-success")
            break;
            case "stopped":
                $(".application-control").find(".btn").removeClass().addClass("btn btn-info")
            break;
            case "paused":
                $(".application-control").find(".btn").removeClass().addClass("btn btn-warning")
            break;
        }
    }

    $click_start_button_handler(){
        let application_control = this
        $("#start_bttn").on("click",function(){
            (application_control.state == "paused" ? application_control.$resume() : application_control.$start());
        })
    }

    $click_stop_button_handler(){
        application_control = this
        $("#stop_bttn").on("click",function(){
            application_control.$stop()
        })
    }

    $click_pause_button_handler(){
        application_control = this
        $("#pause_bttn").on("click",function(){
            if(application_control.state == "started") application_control.$pause();
        })
    }

    $resume(){
        $.post(application_control.control_url,{RESUME:''}).done(function(){
            application_control.state = "started"
            application_control.$change_state()
            $("#start_bttn").text("Start")
            }
        )
    }

    $start(){
        $.post(application_control.play_url,application_control.getData()).done(function(){
                    application_control.state = "started"
                    application_control.$change_state()
                    $(this).text("Start")
                    }
        )
    }

    $stop(){
        $.post(application_control.control_url,{STOP:''}).done(function(){
                application_control.state = "stopped"
                $("#start_bttn").text("Start")
                application_control.$change_state()
                }
        )
    }

    $pause(){
        $("#start_bttn").text("Resume")
        $.post(application_control.control_url,{PAUSE:''}).done(function(){
            application_control.state = "paused"
            application_control.$change_state()
        })
    }
}
