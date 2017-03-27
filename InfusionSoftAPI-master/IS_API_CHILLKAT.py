from infusionsoft.library import InfusionsoftOAuth
import webbrowser
import chilkat
import sys

#---- ckCHECK ----#
glob = chilkat.CkGlobal()
success = glob.UnlockBundle("CHILKAT KEY GOES HERE")

#--------------------------------REQUEST TOKEN FROM InfusionSoft--------------------------------------#
oauth2 = chilkat.CkOAuth2()
oauth2.put_ListenPort(8080)

oauth2.put_AuthorizationEndpoint('https://signin.infusionsoft.com/app/oauth/authorize')
oauth2.put_TokenEndpoint('https://api.infusionsoft.com/token')

oauth2.put_ClientId('CLIENT ID GOES HERE')
oauth2.put_ClientSecret('CLIENT SECRET GOES HERE')

oauth2.put_CodeChallenge(True)
oauth2.put_CodeChallengeMethod("S256")

       #----User authorization - Opens URL with Params requesting access
new = 2
url = oauth2.startAuth()
if (oauth2.get_LastMethodSuccess() != True):
    print(oauth2.lastErrorText())
    sys.exit()
webbrowser.open(url, new=new)

#  If there was no response from the browser within 30 seconds, then
#  the AuthFlowState will be equal to 1 or 2.
#  1: Waiting for Redirect. The OAuth2 background thread is waiting to receive the redirect HTTP request from the browser.
#  2: Waiting for Final Response. The OAuth2 background thread is waiting for the final access token response.
#  In that case, cancel the background task started in the call to StartAuth.

numMsWaited = 0
while (numMsWaited < 40000) and (oauth2.get_AuthFlowState() < 3) :
    oauth2.SleepMs(100)
    numMsWaited = numMsWaited + 100

#  Check the AuthFlowState to see if authorization was granted, denied, or if some error occurred
#  The possible AuthFlowState values are:
#  3: Completed with Success. The OAuth2 flow has completed, the background thread exited, and the successful JSON response is available in AccessTokenResponse property.
#  4: Completed with Access Denied. The OAuth2 flow has completed, the background thread exited, and the error JSON is available in AccessTokenResponse property.
#  5: Failed Prior to Completion. The OAuth2 flow failed to complete, the background thread exited, and the error information is available in the FailureInfo property.

if (oauth2.get_AuthFlowState() == 5):
    print("OAuth2 failed to complete.")
    print(oauth2.failureInfo())
    sys.exit()

if (oauth2.get_AuthFlowState() == 4):
    print("OAuth2 authorization was denied.")
    print(oauth2.accessTokenResponse())
    sys.exit()

if (oauth2.get_AuthFlowState() != 3):
    print("Unexpected AuthFlowState:" + str(oauth2.get_AuthFlowState()))
    sys.exit()
#-----------------------End Token Request-------------------------------#


#---- Use this line to test with Oauth ----#
infusionsoft = InfusionsoftOAuth(oauth2.accessToken())

#---- Use this line to test with direct accessToken. If using this line, comment out the Token Request section and Oauth line above---- #
#infusionsoft = InfusionsoftOAuth('aysra77rcjbz9nchh27y3eg9')

#Dictionary to store contact information we will need
contact_Info = {'FirstName':'','LastName':'','Email':'','FeaturePack':''}

def get_Customer_Id():
    '''Retrieves customer information. updates contact_Info with relevant information. Returns customer['Id] to be used in Order search'''
    first_Name = input("Enter First Name: ")
    last_Name = input("Enter Last Name: ")
    cust_Email = input("Enter your Email: ")
    table = 'Contact'
    page = 0
    returnFields = ['Id', 'FirstName', 'LastName','Email']
    query = {'FirstName' : first_Name, 'LastName':last_Name, 'Email':cust_Email}
    limit = 1
    results = infusionsoft.DataService('query', table, limit,page, query, returnFields)
    for customer in results:
        contact_Info['FirstName'] = customer['FirstName']
        contact_Info['LastName'] = customer['LastName']
        contact_Info['Email'] = customer['Email']
        return customer['Id']

def find_by_Id(cust_Id = get_Customer_Id()):
    '''Uses cust_Id to search through Jobs(orders). If order has a Feature Pack, the value is added to a list
    the list is then assigned to contact_Info['FeaturePack']'''
    table = 'Job'
    page = 0
    returnFields = ['ContactId', '_SoftwareFeaturePack','_ShipDate']
    limit = 10
    fieldName = 'ContactId'
    fieldValue = cust_Id
    results = infusionsoft.DataService('findByField', table, limit, page, fieldName, fieldValue, returnFields)
    FeaturePackOrders = []
    for order in results:
        if '_SoftwareFeaturePack' in order:
            FeaturePackOrders.append(order['_SoftwareFeaturePack'])
    contact_Info['FeaturePack'] = FeaturePackOrders

    

def main():
    find_by_Id()
    print(contact_Info)
if __name__ == '__main__':
    main()
