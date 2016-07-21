/**
 * Created by dengyun on 2015/3/10.
 */
/**
 * zhaojun delete
 * @param url
 */
function delcfm(url) {
        $('#url').val(url);//给会话中的隐藏属性URL赋值
        $('#delcfmModel').modal();
    }
function isuselcfm(url) {
        $('#url').val(url);//给会话中的隐藏属性URL赋值
        $('#isusecfmModel').modal();
    }
function urlSubmit(){
        var url=$.trim($("#url").val());//获取会话中的隐藏属性URL
        window.location.href=url;

    }




function disp_confirm(var1, url) {
    var r = confirm(var1)
    if (r == true) {
        window.location.href = url
        //document.write("You pressed OK!")
    }
    else {
        return false
        //document.write("You pressed Cancel!")
    }
}

/**
 * 提交表单
 * @param form_name
 */
function submit_form(form_name) {
    //openDialog();
    document.getElementById(form_name).submit();
}

/**
 * 删除数据
 * @param url
 */
function data_del(url) {
    var r = confirm(var1)
    if (r == true) {
        //
    }
    else {
        alert("You pressed Cancel!");
        //document.write("You pressed Cancel!")
    }
}

/**
 * 重置Redis
 * @param msg
 * @param url
 * @param ip
 * @param cmd
 */
function shell_scripts_control(msg, url, ip, cmd) {
    var r = confirm(msg)
    if (r == true) {
        var aj = $.ajax({
            url: url,
            data: {
                ip: ip,
                cmd: cmd
            },
            type: 'post',
            cache: false,
            dataType: 'json',
            success: function (data) {
                if (data.code == 0) {
                    alert('success');
                } else {
                    alert('fail');
                }
            },
            error: function () {
                alert("异常！");
            }
        });
    }
    else {
        alert("你已经放弃!");
    }

}

/**
 * 弹出进度条
 * @param sHTML
 * @param sTitle
 * @param bCancel
 * @constructor
 */
function NeatDialog(sHTML, sTitle, bCancel) {
    window.neatDialog = null;
    this.elt = null;
    if (document.createElement && document.getElementById) {
        var dg = document.createElement("div");
        dg.className = "neat-dialog";
        if (sTitle)
            sHTML = '<div class="neat-dialog-title">' + sTitle +
            ((bCancel) ?
                '<img src="x.gif" alt="Cancel" class="nd-cancel" />' : '') +
            '</div>\n' + sHTML;
        dg.innerHTML = sHTML;

        var dbg = document.createElement("div");
        dbg.id = "nd-bdg";
        dbg.className = "neat-dialog-bg";

        var dgc = document.createElement("div");
        dgc.className = "neat-dialog-cont";
        dgc.appendChild(dbg);
        dgc.appendChild(dg);

        //adjust positioning if body has a margin
        if (document.body.offsetLeft > 0)
            dgc.style.marginLeft = document.body.offsetLeft + "px";

        document.body.appendChild(dgc);
        if (bCancel) document.getElementById("nd-cancel").onclick = function () {
            window.neatDialog.close();
        };
        this.elt = dgc;
        window.neatDialog = this;
    }
}
NeatDialog.prototype.close = function () {
    if (this.elt) {
        this.elt.style.display = "none";
        this.elt.parentNode.removeChild(this.elt);
    }
    window.neatDialog = null;
}
