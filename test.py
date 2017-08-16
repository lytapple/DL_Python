%%javascript

function set_label(label){
    var kernel = IPython.notebook.kernel;
    kernel.execute("labels.append(" + label + ")");
    load_next_tweet();
}

function load_next_tweet(){
   var code_input = "get_tweet()";
   var kernel = IPython.notebook.kernel;
   var callbacks = { 'iopub' : {'output' : handle_output}};
   kernel.execute(code_input, callbacks, {silent:false});
}

function handle_output(out){
   console.log(out);
   var res = out.content.data["text/plain"];
   $("div#tweet_text").html(res);
}
