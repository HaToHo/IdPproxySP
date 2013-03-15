<%inherit file="root.mako"/>

<%!
  def setupEntityIdList(spList):
      optionList = ""
      for entityId in spList:
        optionList += "<option value='" + entityId + "'>" + entityId + "</option>"
      return optionList
%>



    <p class="description">
        Follow the guid at SWAMID to retrive secret and key for the social service you which to configure.
    </p>
    <form action="${action}" method="post">
        <p><label for="sp">Service Provider</label><br />
        <select name='sp' size=30>")
            ${setupEntityIdList(splist)}
        </select>
        </p>
        <input class="submit" type="submit" name="form.submitted" value="Next >"/>
    </form>
