<%inherit file="root.mako"/>

<%!
  def setupEntityIdList(spList):
      optionList = ""
      for entityId in spList:
        optionList += "<option value='" + entityId + "'>" + entityId + "</option>"
      return optionList
%>



    <p class="description">
        Click on the entity id for the service provider you wish to configure.
    </p>
    <form action="${action}" method="post">
        <p><label for="sp">Service Provider</label><br />
        <select name='sp' size=30>")
            ${setupEntityIdList(splist)}
        </select>
        </p>
        <input class="submit" type="submit" name="form.submitted" value="Next >"/>
    </form>
