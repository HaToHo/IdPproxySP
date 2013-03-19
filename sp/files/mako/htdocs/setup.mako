<%inherit file="root.mako"/>

<%!
  def setupEntityIdList(spList):
      optionList = ""
      for entityId in spList:
        optionList += "<option value='" + entityId + "'>" + entityId + "</option>"
      return optionList
%>

<%!
    def setupJavaScriptEntityIdArray(spList):
      first = True
      entityIdArray = "["
      for entityId in spList:
        if not first:
            entityIdArray += ","
        entityIdArray += "{'value' : '" + entityId + "','text' : '" + entityId + "'}"
        first = False
      entityIdArray += "];"
      return entityIdArray
%>

    <script language="JavaScript">
        function filterOptions(str)
        {
            var dataArr = ${setupJavaScriptEntityIdArray(splist)}
            //alert(dataArr[0]['text']);
            //alert('.*'+str+'.*');
            //alert(dataArr[0]['text'].match('.*'+str+'.*'));
            $("#sp option").remove();
            $.each(dataArr,
                    function(i) {
                             if (dataArr[i]['text'].match('.*'+str+'.*') != null) {
                                 $("#sp").append($("<option></option>")
                                         .attr("value",dataArr[i]['value'])
                                         .text(dataArr[i]['text']));
                             }
                    }
            )
        }

    </script>

    <p class="description">
        Click on the entity id for the service provider you wish to configure.
    </p>
    <form action="${action}" method="post">
        <p>
            <label for='filter'>Filter SP's</label><br />
            <input type='text' class='inputValue' onkeyup="filterOptions(this.value)" name='filter' id='filter' value=''/>
            <br />
            <label for="sp">Service Provider</label><br />
            <select name='sp' id="sp" size=30>")
                ${setupEntityIdList(splist)}
            </select>
        </p>
        <input class="submit" type="submit" name="form.submitted" value="Next >"/>
    </form>
