<%inherit file="root.mako"/>

<%!
  def setupEntityIdList(spList):
      """
      Creates option tags for a select tag.
      The option tags contains entityID for SP's-
      :param spList: A list of string with entityId's-
      :return: A string with multiple option tags.
      """
      optionList = ""
      for entityId in spList:
        optionList += "<option value='" + entityId + "'>" + entityId + "</option>"
      return optionList
%>

<%!
    def setupJavaScriptEntityIdArray(spList):
      """
      Creates a JSON list with a dictionary with the keys value and text.
      [{'value' : 'value1','text' : 'text1'},{'value' : 'valuen','text' : 'textn'}]
      The JSON list is created from a list of strings containing entityId's for sp's.
      :param spList: A list of string with entityId's-
      :return: A JSON list.
      """
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
        //Will empty all options from the select with id sp.
        //Then fill it again with all options that have a text that matches the string str.
        //The data array is constructed in python and represents a JSON list
        // [{'value' : 'value1','text' : 'text1'},{'value' : 'valuen','text' : 'textn'}]
        function filterOptions(str)
        {
            var dataArr = ${setupJavaScriptEntityIdArray(splist)}
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
