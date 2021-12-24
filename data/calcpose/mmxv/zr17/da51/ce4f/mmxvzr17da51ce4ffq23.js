var me = this; 
var ME = $('#'+me.UUID)[0];

me.ready = function(api){
  componentHandler.upgradeAllRegistered();
  me.updateSnapshot();
  
  $(ME).find('.maximizebutton').click(function(){ me.maximize(me.updateSnapshot); });
  $(ME).find('.resetcambutton').click(function(){ me.resetCamera(me.updateSnapshot); });
  $(ME).find('.modvalslider').change(function(){ 
    $(ME).find('.modvalfield').val($(this).val()/100); 
    me.setModifier(me.updateSnapshot); 
  });
  $(ME).find('.modvalfield').change(function(){ 
    $(ME).find('.modvalslider').val($(this).val()*100); 
    me.setModifier(me.updateSnapshot); 
  });
  
  $(ME).find('.targetbygroup').click(function(){ 
    var group = $(ME).find('.modgroupselect').find('select').val();
    modifiers = [];
    for (var i in me.modifiers[group]){
      modifiers.push(group+"/"+me.modifiers[group][i]);
    }
    console.log(modifiers);
    step = Number($(ME).find('.approachstepfield').val());
    $(ME).find('.hideonapproach').css('display', 'none')
    $(ME).find('.showonapproach').html('<i>Beginning approach...</i>');
    var gennum = 1;
    function nextGen(){
      var stepnum = 1;
      function nextStep(){
        send_approach_target(modifiers, step, function(result){
          var data = JSON.parse(result.msg);
          console.log(data);
          var newhtml = 'Generation: '
            + gennum
            + '<br>Step: '
            + stepnum++
            + '<br>Step size: '
            + step
            + '<br>Loss function: '
            + Math.round(data.loss)
            + '<br>Number of changes: '
            + data.count;
          $(ME).find('.showonapproach').html(newhtml);
          me.addThumb();
          if (data.count == 0) {
            step *= Number($(ME).find('.shrinkagefield').val());
            if (step>=Number($(ME).find('.minstepfield').val())) {
              gennum++;
              me.updateSnapshot(nextGen);
            }
            else {
              $(ME).find('.hideonapproach').css('display', 'block');
              me.updateSnapshot(me.addThumb);
            }
          }
          else me.updateSnapshot(nextStep);
        });
      }
      nextStep();
    }
    nextGen();
  });

  $(ME).find('.clearthumbsbutton').click(function(){ 
    $(ME).find('.thumbs').empty();
  });
  
  $(ME).find('.playthumbsbutton').click(function(){ 
    var imgs = $(ME).find('.thumbs').find('img');
    var list = []
    var i = imgs.length;
    while (i-->0) {
      list.push($(imgs[i]));
      console.log(typeof imgs[i]);
    }
    function showNext(){
      if (list.length>0){
        $(ME).find('.humandisplay').prop('src', list.pop().prop('src'));
        setTimeout(showNext, 100);
      }
    }
    showNext();
  });
  
  $(ME).find('.addthumbbutton').click(function(){ 
    me.addThumb();
  });
  
  $(ME).find('.refreshhumanbutton').click(function(){ 
    me.updateSnapshot();
  });

  $(ME).find('.fixzrotbutton').click(function(){ 
    $(ME).find('.targetzrot').text('--');
    send_optimize_rotation(function(result){
      url = result.data.data;
      var el = $('#targetimage');
      el.attr('src', url);
      $(ME).find('.targetzrot').text(result.data.rotation);
    });
  });
  
  $(ME).find('.targetuploadfile').change(function(){ 
    var file = this.files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = function (e) {
          var el = $('#targetimage');
          var url = e.target.result;
          send_set_target(url, function(result){
            if (result.status != 'ok') {
              alert(result.msg);
              $(ME).find('.showontarget').css('display', 'none');
            }
            else {
              url = result.msg;
              el.attr('src', url);
              $(ME).find('.showontarget').css('display', 'block');
            }
          });
        }
        reader.onerror = function (evt) {
            alert("error reading file");
        }
        reader.readAsDataURL(file);
    }
  });
  
  send_list_modifiers(function(result){
    var d = {};
    var n = [];
    for (var i in result.data){
      rdi = result.data[i];
      var j = rdi.indexOf("/");
      var group = rdi.substring(0,j);
      var modifier = rdi.substring(j+1);
      if (!d[group]) {
        d[group] = [];
        n.push(group);
      }
      d[group].push(modifier);
    }
    //d.all = n;
    me.modifiers = d;
    d = {
      "label": "Group",
      "list": n,
      "ready": function(api){
        me.groupapi = api;
        me.selectGroup(api.value());
      },
      "cb": me.selectGroup
    };
    installControl($(ME).find('.modgroupselect')[0], "metabot", "select", function(api){}, d);
  });
};

me.setModifier = function(cb){
  var group = $(ME).find('.modgroupselect').find('select').val();
  var modifier = $(ME).find('.modifierselect').find('select').val();
  var val = $(ME).find('.modvalfield').val();
  send_modify(group+'/'+modifier, val, function(result){ 
    console.log(result); 
    if (cb) cb();
  });
};

me.selectGroup = function(group){
  d = {
    "label": "Modifier",
    "list": me.modifiers[group],
    "ready": function(api){
      me.selectModifier(group, api.value());
    },
    "cb": function(val){
      me.selectModifier(group, val);
    }
  };
  installControl($(ME).find('.modifierselect')[0], "metabot", "select", function(api){}, d);
};

me.selectModifier = function(group, modifier){
  var mod = group+'/'+modifier;
  send_get_modifier_value(mod, function(result){
    console.log(result);
    var val = result.data ? result.data[mod] : 0.0;
    $(ME).find('.modvalfield').val(val);
    $(ME).find('.modvalslider').val(100*val);
  });
};

me.addThumb = function(){
  var img = $('<img width="60"/>');
  img.prop('src', $(ME).find('.humandisplay').prop('src'));
  img.click(function(e){
    $(ME).find('.humandisplay').prop('src', $(this).prop('src'));
  });
  $(ME).find('.thumbs').append(img);
};

me.updateSnapshot = function(cb){
  send_snapshot(function(result){
    if (result.status != "ok") alert(result.msg);
    else {
      $(ME).find('.humandisplay').prop('src', result.msg);
      if (cb) cb();
    }
  });
};

me.resetCamera = function(cb){
  send_reset_camera(function(result){
    if (result.status != "ok") alert(result.msg);
    else if (cb) cb();
  });
};

me.maximize = function(cb){
  send_maximize(function(result){
    if (result.status != "ok") alert(result.msg);
    else if ((typeof cb) == 'function') cb();
  });
};