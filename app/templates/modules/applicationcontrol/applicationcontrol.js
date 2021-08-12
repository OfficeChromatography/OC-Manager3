class ApplicationControl{
    constructor(startEvent, stopEvent, pauseEvent, resumeEvent){
        this.state = "stopped" // started, stopped, paused

        this.startEvent = startEvent
        this.stopEvent = stopEvent
        this.pauseEvent = pauseEvent
        this.resumeEvent = resumeEvent

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
        let application_control = this
        $("#stop_bttn").on("click",function(){
            application_control.$stop()
        })
    }

    $click_pause_button_handler(){
        let application_control = this
        $("#pause_bttn").on("click",function(){
            if(application_control.state == "started") application_control.$pause();
        })
    }

    async $resume(){
        let res = await this.resumeEvent()
        if (res.ok){
            this.state = "started"
            this.$change_state()
            $("#start_bttn").text("Start")
        }
    }

    async $start(){
        let res = await this.startEvent()
        if (res.ok){
            this.state = "started"
            this.$change_state()
            $("#start_bttn").text("Start")
        }
    }

    async $stop(){
        let res = await this.stopEvent()
        if (res.ok){
            this.state = "stopped"
            $("#start_bttn").text("Start")
            this.$change_state()
        }
    }

    async $pause(){
        let res = await this.pauseEvent()
        if (res.ok){
            this.state = "paused"
            $("#start_bttn").text("Resume")
            this.$change_state()
        }
    }
}
