<%inherit file="root.mako"/>

<%!
  def setupServiceList(serviceList):
      htmlOutput = ""
      for service in serviceList:
        serviceName = service.keys()[0]
        settingsExists = service[serviceName]
        htmlOutput += "<p><span class='service'>" + serviceName + "</span><br />"
        hiddenKey = ""
        if settingsExists:
            hiddenKey = "********************"
        htmlOutput += "<input type='hidden' id='service' name='service' value='" + serviceName + "' />"
        htmlOutput += "<label for='secret'>Secret</label><br /><input type='text' class='inputValue' name='secret' id='secret' value='" + hiddenKey + "'/><br />"
        htmlOutput += "<label for='key'>Key</label><br /><input type='text' class='inputValue' name='key' id='key' value='" + hiddenKey + "'/><br />"
        htmlOutput += "</p>"
      return htmlOutput
%>


    <script>
        function setupInputFields() {
            //$(":text:not([value])").val(" ");
            $('form').find("input[type=text]").each(function(ev) {
                if($(this).val()=='') { $(this).val(' '); }
            });


        }
    </script>

    <p class="description">
        Follow the guid at <a href="https://portal.nordu.net/display/SWAMID/Social2SAML">>SWAMID</a> to retrive secret and key for the social service you which to configure.<br> />
        <br/>
        Clear key and secret for a service if you wish to remove it from the IdPproxy.<br />
        <br />
        If a field contains ******************** it is already configured. Leave it if you do not wish to change it.
    </p>
    <form action="${action}" method="post">
        ${setupServiceList(sociallist)}
        <input type="hidden" id="sp" name="sp" value="${sp}" />
        <input class="back" type="button" onclick="window.location.href = '${back}'" name="form.submitted" value="< Back"/>
        <input class="submit" type="submit" onclick="setupInputFields();" name="form.submitted" value="Save changes >"/>
    </form>
